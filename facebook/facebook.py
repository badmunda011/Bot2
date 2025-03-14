import os
import logging
import time
from pathlib import Path
from typing import Optional
import yt_dlp
import asyncio
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from moviepy import VideoFileClip

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    TEMP_DIR = Path("temp")
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.facebook.com/',
    }

Config.TEMP_DIR.mkdir(exist_ok=True)

class FacebookDownloader:
    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        yt_dlp.utils.std_headers['User-Agent'] = Config.HEADERS['User-Agent']

    async def download_video(self, url: str) -> Optional[dict]:
        self.temp_dir.mkdir(exist_ok=True)
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'no_color': True,
            'simulate': False,
            'nooverwrites': True,
            'noprogress': True,
            'concurrent_fragment_downloads': 10,  # Increase concurrency
            'merge_output_format': 'mp4',  # Ensure proper merging of video and audio
        }

        try:
            loop = asyncio.get_event_loop()
            video_info = await loop.run_in_executor(None, self._download_video, ydl_opts, url)
            return video_info
        except Exception as e:
            logger.error(f"Facebook download error: {e}")
            return None

    def _download_video(self, ydl_opts, url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            if os.path.exists(filename):
                duration = self.get_video_duration_moviepy(filename)
                return {
                    'title': info_dict.get('title', 'Unknown Title'),
                    'filename': filename,
                    'resolution': f"{info_dict.get('height', 'Unknown')}p",
                    'views': info_dict.get('view_count', 'Unknown'),
                    'duration': duration,
                    'webpage_url': info_dict.get('webpage_url', url)
                }
            else:
                return None

    def get_video_duration_moviepy(self, video_path: str) -> float:
        """
        Get video duration using MoviePy.
        Returns duration in seconds.
        """
        try:
            with VideoFileClip(video_path) as clip:
                return clip.duration
        except Exception as e:
            print(f"Error getting video duration: {e}")
            return 0.0

async def fix_metadata(video_path: str) -> str:
    new_path = video_path.replace(".mp4", "_fixed.mp4")
    command = f'ffmpeg -i "{video_path}" -c copy "{new_path}" -y'
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.communicate()
    return new_path if os.path.exists(new_path) else video_path

def setup_dl_handlers(app: Client):
    fb_downloader = FacebookDownloader(Config.TEMP_DIR)

    @app.on_message(filters.regex(r"^[/.]fb(\s+https?://\S+)?$") & (filters.private | filters.group))
    async def fb_handler(client: Client, message: Message):
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Please provide a Facebook link ❌**",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        url = command_parts[1]
        downloading_message = await client.send_message(
            chat_id=message.chat.id,
            text="**Searching The Video**",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            video_info = await fb_downloader.download_video(url)
            if video_info:
                await downloading_message.edit_text("**Found ☑️ Downloading...**", parse_mode=ParseMode.MARKDOWN)
                
                title = video_info['title']
                filename = video_info['filename']
                resolution = video_info['resolution']
                views = video_info['views']
                duration = video_info['duration']
                webpage_url = video_info['webpage_url']
                
                if message.from_user:
                    user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
                    user_info = f"[{user_full_name}](tg://user?id={message.from_user.id})"
                else:
                    group_name = message.chat.title or "this group"
                    group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
                    user_info = f"[{group_name}]({group_url})"

                # Convert duration to minutes and seconds
                duration_minutes = int(duration // 60)
                duration_seconds = int(duration % 60)
                
                caption = (
                    f"🎵 **Title**: **{title}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👁️‍🗨️ **Views**: **{views} views**\n"
                    f"🔗 **Url**: [Watch On Facebook]({webpage_url})\n"
                    f"⏱️ **Duration**: **{duration_minutes}:{duration_seconds:02d}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Downloaded By**: {user_info}"
                )

                fixed_filename = await fix_metadata(filename)
                
                async with aiofiles.open(fixed_filename, 'rb') as video_file:
                    start_time = time.time()
                    last_update_time = [start_time]
                    await client.send_video(
                        chat_id=message.chat.id,
                        video=fixed_filename,
                        supports_streaming=True,
                        caption=caption,
                        height=720,
                        width=1280,
                        duration=int(duration),
                        parse_mode=ParseMode.MARKDOWN,
                        progress=progress_bar,
                        progress_args=(downloading_message, start_time, last_update_time)
                    )
                
                await downloading_message.delete()
                os.remove(fixed_filename)
            else:
                await downloading_message.edit_text("Download Error ❌")
        except Exception as e:
            logger.error(f"Error downloading Facebook video: {e}")
            await downloading_message.edit_text("An error occurred❌")

async def progress_bar(current, total, status_message, start_time, last_update_time):
    """
    Display a progress bar for uploads.
    """
    elapsed_time = time.time() - start_time
    percentage = (current / total) * 100
    progress = "▓" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
    speed = current / elapsed_time / 1024 / 1024  # Speed in MB/s
    uploaded = current / 1024 / 1024  # Uploaded size in MB
    total_size = total / 1024 / 1024  # Total size in MB

    # Throttle updates: Only update if at least 1 second has passed since the last update
    if time.time() - last_update_time[0] < 1:
        return
    last_update_time[0] = time.time()  # Update the last update time

    text = (
        f"📥 Upload Progress 📥\n\n"
        f"{progress}\n\n"
        f"🚧 Percentage: {percentage:.2f}%\n"
        f"⚡️ Speed: {speed:.2f} MB/s\n"
        f"📶 Uploaded: {uploaded:.2f} MB of {total_size:.2f} MB"
    )
    try:
        await status_message.edit(text)
    except Exception as e:
        print(f"Error updating progress: {e}")
