# YouTube Downloader (PySide6 & yt-dlp)

A lightweight desktop application for downloading YouTube videos in maximum quality without using any browser cookies or logging into Google accounts.

## Features
- **No Cookies Required**: Completely bypasses YouTube's restrictions without sharing your browser data.
- **Maximum Quality**: Downloads full audio and separate high-definition video streams (1080p, 2K, 4K) and merges them seamlessly.
- **Modern JavaScript Bypass**: Locally utilizes an isolated Node.js binary to solve YouTube's internal player challenges and throttle-protection on the fly.
- **Customizable Storage**: Choose a custom root folder where your library and internal configuration structures will be generated automatically.
- **Wide Format Support**: Correctly lists and handles modern `.mp4`, `.mkv`, and `.webm` media formats.

## Project Structure
For the downloader to work correctly at max speed, keep the following portable executable structure inside your main directory:
```text
your_project_directory/
├── downloader.py      # The main Python script
├── node.exe           # Node.js binary (v22+) for decryption challenges
├── ffmpeg.exe         # FFmpeg binary for audio/video muxing
└── ffprobe.exe        # FFprobe binary for stream analysis
```

## Prerequisites
Install the required packages before launching the application:
```bash
pip install PySide6 yt-dlp
```

## Usage
1. Place `node.exe`, `ffmpeg.exe`, and `ffprobe.exe` alongside the `downloader.py` file.
2. Run the application: `python downloader.py`
3. Click **Select Root Folder** to set your library destination.
4. Paste any valid YouTube link and click **Download**.
EOF