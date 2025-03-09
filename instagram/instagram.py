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
        'Referer': 'https://www.instagram.com/',
    }

Config.TEMP_DIR.mkdir(exist_ok=True)

class InstagramDownloader:
    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        yt_dlp.utils.std_headers['User-Agent'] = Config.HEADERS['User-Agent']

    async def download_reel(self, url: str) -> Optional[dict]:
        self.temp_dir.mkdir(exist_ok=True)
        ydl_opts = {
            'format': 'best',
            'outtmpl': str(self.temp_dir / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'no_color': True,
            'simulate': False,
            'nooverwrites': True,
            'noprogress': True,
            'concurrent_fragment_downloads': 10,
        }

        try:
            loop = asyncio.get_event_loop()
            reel_info = await loop.run_in_executor(None, self._download_reel, ydl_opts, url)
            return reel_info
        except Exception as e:
            logger.error(f"Instagram Reels download error: {e}")
            return None

    def _download_reel(self, ydl_opts, url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            if os.path.exists(filename):
                return {
                    'title': info_dict.get('title', 'Unknown Title'),
                    'filename': filename,
                    'webpage_url': info_dict.get('webpage_url', url)
                }
            else:
                return None

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
        logger.error(f"Error updating progress: {e}")

def setup_in_handlers(app: Client):
    ig_downloader = InstagramDownloader(Config.TEMP_DIR)

    @app.on_message(filters.regex(r"^[/.]in(\s+https?://\S+)?$") & (filters.private | filters.group))
    async def ig_handler(client: Client, message: Message):
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Please provide an Instagram Reels link ❌**",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        url = command_parts[1]
        downloading_message = await client.send_message(
            chat_id=message.chat.id,
            text="**Searching The Reel**",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            reel_info = await ig_downloader.download_reel(url)
            if reel_info:
                await downloading_message.edit_text("**Found ☑️ Downloading...**", parse_mode=ParseMode.MARKDOWN)
                
                title = reel_info['title']
                filename = reel_info['filename']
                webpage_url = reel_info['webpage_url']
                
                if message.from_user:
                    user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
                    user_info = f"[{user_full_name}](tg://user?id={message.from_user.id})"
                else:
                    group_name = message.chat.title or "this group"
                    group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "this group"
                    user_info = f"[{group_name}]({group_url})"

                caption = (
                    f"🎥 **Title**: **{title}**\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 **Url**: [Watch On Instagram]({webpage_url})\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"**Downloaded By**: {user_info}"
                )
                
                async with aiofiles.open(filename, 'rb') as video_file:
                    start_time = time.time()
                    last_update_time = [start_time]
                    await client.send_video(
                        chat_id=message.chat.id,
                        video=filename,
                        supports_streaming=True,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        progress=progress_bar,
                        progress_args=(downloading_message, start_time, last_update_time)
                    )
                
                await downloading_message.delete()
                os.remove(filename)
            else:
                await downloading_message.edit_text("Download Error ❌")
        except Exception as e:
            logger.error(f"Error downloading Instagram Reel: {e}")
            await downloading_message.edit_text("An error occurred❌")
