<h1 align="center">SmartDlBot Telegram Bot 🌌</h1>

<p align="center">
  <em>SmartDlBot: The ultimate toolkit on Telegram, offering Facebook,YouTube,Pinterest,Spotify Downloader. Simplify your tasks with ease!</em>
</p>

<p align="center">
  <a href="https://github.com/abirxdhack/SmartDlBot/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/abirxdhack/SmartDlBot"></a>
  <a href="https://github.com/abirxdhack/SmartDlBot/network/members"><img alt="GitHub forks" src="https://img.shields.io/github/forks/abirxdhack/SmartDlBot"></a>
  <a href="https://github.com/abirxdhack/SmartDlBot/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/abirxdhack/SmartDlBot"></a>
  <a href="https://github.com/abirxdhack/SmartDlBot/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/abirxdhack/SmartDlBot"></a>
  <a href="https://github.com/abirxdhack/SmartDlBot/pulls"><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/abirxdhack/SmartDlBot"></a>
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pyrogram">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/abirxdhack/SmartDlBot">
</p>

<hr>

## 🌟 Features

- **Facebook Video Downloader**: Download videos from Facebook.
- **YouTube Video Downloader**: Download videos from YouTube.
- **Pinterest Video Downloader**: Download videos from Pinterest.
- **Spotify Track Downloader**: Download tracks from Spotify.

## Requirements

Before you begin, ensure you have met the following requirements:

- 🐍 Python 3.9 or higher.
- 📦 `pyrogram` , `yt-dlp` , `spotipy` , `requests` , `pillow` , `asyncio` , `aiofiles` , `aiohttp`  library.
- 🤖 A Telegram bot token (you can get one from [@BotFather](https://t.me/BotFather) on Telegram).
- 🔑 API ID and Hash: You can get these by creating an application on [my.telegram.org](https://my.telegram.org).
- 🎸 SPOTIFY_CLIENT_ID from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- 🎸 SPOTIFY_CLIENT_SECRET from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Installation

To install `pyrogram` , `yt-dlp` , `spotipy` , `requests` , `pillow` , `asyncio` , `aiofiles` , `aiohttp`  run the following command:

```bash
pip install -r requirements.txt
```

**Note: If you previously installed `pyrofork`, uninstall it before installing `pyrogram`.**

## Handling YouTube Download Errors with Cookies

To avoid errors related to YouTube sign-in requirements, using a cookie file is effective. Here's how to set it up:

### Steps to Export and Use Cookies:

1. **Create a Dedicated Chrome Profile:**
   - It's recommended to create a new Chrome profile for managing your bot's cookies.

2. **Install a Cookie Management Extension:**
   - Use "Cookie Editor" or similar extensions to manage your cookies.

3. **Export Cookies from YouTube:**
   - Log into YouTube in your new browser profile and export cookies in Netscape format via the cookie extension.

4. **Save the Cookies File:**
   - Update your `cookies.txt` in the `SmartDlBot/cookies` directory of your project.

### Managing Cookies:

- **Cookie Expiry:**
  - Refresh your cookies by exporting new ones if you encounter download issues.

- **Cookie Depletion:**
  - Avoid frequent bot restarts and excessive YouTube requests to prevent early cookie expiry.

This setup should help manage YouTube content access efficiently without encountering sign-in or bot protection errors.

## Configuration

1. Open the `config.py` file in your favorite text editor.
2. Replace the placeholders for `API_ID`, `API_HASH`,  `BOT_TOKEN`, `SPOTIFY_CLIENT_ID`, and `SPOTIFY_CLIENT_SECRET` with your actual values:
   - **`API_ID`**: Your API ID from [my.telegram.org](https://my.telegram.org).
   - **`API_HASH`**: Your API Hash from [my.telegram.org](https://my.telegram.org).
   - **`BOT_TOKEN`**: The token you obtained from [@BotFather](https://t.me/BotFather).
   - **`SPOTIFY_CLIENT_ID`**: SPOTIFY_CLIENT_ID from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - **`SPOTIFY_CLIENT_SECRET`**: SPOTIFY_CLIENT_SECRET from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Deploy the Bot

```sh
git clone https://github.com/abirxdhack/SmartDlBot
cd SmartDlBot
python main.py
```

## Usage 🛠️

The bot supports the following commands:

Download videos and tracks from popular platforms using these commands:

➢ **`/fb [Video URL]`** - Download a Facebook video.
   - Example: **/fb https://www.facebook.com/share/v/18VH1yNXoq/** **`Downloads the specified Facebook video`**
   - Note: Private Facebook videos cannot be downloaded.

➢ **`/pin [Video URL]`** - Download a Pinterest video.
   - Example: **/pin https://pin.it/6GoDMRwmE** **`Downloads the specified Pinterest video`**


➢ **`/sp [Track URL]`** - Download a Spotify track.
   - Example: **/sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta** **`Downloads the specified Spotify track**`

➢ **`/yt [Video URL]`** - Download a YouTube video.
   - Example: **/yt https://youtu.be/In8bfGnXavw** **`Downloads the specified YouTube video`**

➢ **`/song [Video URL]`** - Download a YouTube video as an MP3 file.
   - Example: **/song https://youtu.be/In8bfGnXavw** **`Converts and downloads the video as MP3`**

**Or You Can Use Below Commands **

➢ **`.fb [Video URL]`** - Download a Facebook video.
   - Example: **.fb https://www.facebook.com/share/v/18VH1yNXoq/** **`Downloads the specified Facebook video`**
   - Note: Private Facebook videos cannot be downloaded.

➢ **`.pin [Video URL]`** - Download a Pinterest video.
   - Example: **.pin https://pin.it/6GoDMRwmE** **`Downloads the specified Pinterest video`**
   - Note: 18+ Instagram Reels cannot be downloaded.

➢ **`.sp [Track URL]`** - Download a Spotify track.
   - Example: **.sp https://open.spotify.com/track/7ouBSPZKQpm7zQz2leJXta** **`Downloads the specified Spotify track`**

➢ **`.yt [Video URL]`** - Download a YouTube video.
   - Example: **.yt https://youtu.be/In8bfGnXavw** **`Downloads the specified YouTube video`**

➢ **`.song [Video URL]`** - Download a YouTube video as an MP3 file.
   - Example: **.song https://youtu.be/In8bfGnXavw** **`Converts and downloads the video as MP3`**

## NOTE
**Provide a valid public URL for each platform to download successfully**
For inquiries or feedback, please feel free to reach out via Telegram.

## Ethical Notice 🔔
> **Ethics Reminder:** Simply modifying a few lines of code does not constitute original authorship. When forking a project, always fork responsibly and give proper credit to the original creators.

# Project Contributors

## Author 📝

- Name: Abir Arafat Chawdhury
- Telegram: [@abirxdhackz](https://t.me/abirxdhackz)
