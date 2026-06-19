# YouTube Downloader (PySide6 & yt-dlp)

A lightweight desktop application for downloading YouTube videos in maximum quality without using any browser cookies or logging into Google accounts.

## 🛠 Installation & Setup Guide

Follow these simple steps to get the downloader working on your machine:

### 1. Install Python Dependencies
Open your terminal/command prompt and run the following command to install the required GUI and scraping libraries:
```bash
pip install -r requirements.txt
```

### 2. Download Required Binaries
For the app to bypass YouTube's protections and merge high-quality formats, you need three external files placed strictly in the root directory alongside your `main.py`:

- **Node.js**: Download the portable binary [Node.exe (v22+ LTS)](https://nodejs.org). Rename it to exactly `node.exe`.
- **FFmpeg & FFprobe**: Download the ready-to-use archive from [gyan.dev](https://gyan.dev). Open the archive, go into the `bin/` folder, and extract only two files: `ffmpeg.exe` and `ffprobe.exe`.

### 3. Check Directory Structure
Before launching, make sure your project folder looks exactly like this (without any extra unzipped folders):
```text
your_project_directory/
├── main.py            # The main Python script (or downloader.py)
├── node.exe           # Extracted Node.js binary
├── ffmpeg.exe         # Extracted FFmpeg binary
├── ffprobe.exe        # Extracted FFprobe binary
├── requirements.txt   # File with dependency names
└── README.md          # This documentation file
```

## 🚀 How to Run & Use

1. Open your terminal in the project directory and launch the script:
   ```bash
   python main.py
   ```
2. Click the **"Select Root Folder"** button in the GUI window to choose where you want your downloaded videos to be saved.
3. Paste any valid YouTube video or playlist link into the text input field.
4. Click **"Download"** and wait for the progress bar to finish.

*Note: FullHD, 2K, and 4K video clips will be downloaded as individual video and audio streams, and then automatically merged into a single crisp `.mp4` or `.webm` file by FFmpeg in the background.*
