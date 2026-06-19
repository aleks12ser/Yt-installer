import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget,
    QFileDialog, QMessageBox, QProgressBar
)
import yt_dlp


# ==================================================
# DIRECTORY UTILS & ENVIRONMENT SETUP
# ==================================================
def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# Base directory where the script, node.exe, and ffmpeg.exe are located
BASE_DIR = get_app_dir()

# Add the script folder to the system PATH so yt-dlp can easily find ffmpeg
if BASE_DIR not in os.environ["PATH"]:
    os.environ["PATH"] = BASE_DIR + os.pathsep + os.environ["PATH"]

ROOT_POINTER = os.path.join(BASE_DIR, "root_path.txt")


def load_root_folder():
    if os.path.exists(ROOT_POINTER):
        with open(ROOT_POINTER, "r", encoding="utf-8") as f:
            path = f.read().strip()
            if path and os.path.exists(path):
                return path
    return None


ROOT_FOLDER = load_root_folder()


def build_paths(root):
    app_folder = os.path.join(root, "ProgramFiles")
    download_folder = os.path.join(root, "youtube_library")
    config_file = os.path.join(app_folder, "config.txt")
    return app_folder, download_folder, config_file


if ROOT_FOLDER:
    APP_FOLDER, DOWNLOAD_FOLDER, CONFIG_FILE = build_paths(ROOT_FOLDER)
else:
    APP_FOLDER = DOWNLOAD_FOLDER = CONFIG_FILE = None


def ensure_folders():
    if not ROOT_FOLDER:
        return
    os.makedirs(APP_FOLDER, exist_ok=True)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


ensure_folders()


# ==================================================
# YT-DLP LOGIC (NO COOKIES, USES NODE.JS & FFMPEG)
# ==================================================
def get_ydl_opts(progress_hook):
    node_exe_path = os.path.join(BASE_DIR, 'node.exe')

    return {
        # Download video + audio in max quality (FullHD / 4K)
        "format": "bestvideo+bestaudio/best",
        # Save files to the selected library folder
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),

        # Completely disable browser cookies
        "no_cookies": True,

        # Explicitly pass absolute paths to ffmpeg and node.exe
        "ffmpeg_location": BASE_DIR,
        "js_runtimes": ['node', f'node:{node_exe_path}'],

        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [progress_hook],
    }


# ==================================================
# GUI CLASS
# ==================================================
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader (Max Quality)")
        self.resize(650, 450)

        layout = QVBoxLayout()
        path_layout = QHBoxLayout()

        self.path_label = QLabel(f"📁 Root: {ROOT_FOLDER if ROOT_FOLDER else 'Not selected'}")
        btn_change = QPushButton("Select Root Folder")
        btn_change.clicked.connect(self.select_root_folder)

        path_layout.addWidget(self.path_label)
        path_layout.addWidget(btn_change)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube link here...")

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        self.btn_download = QPushButton("Download")
        self.btn_download.clicked.connect(self.download_video)

        self.status = QLabel("")
        self.video_list = QListWidget()
        self.video_list.itemDoubleClicked.connect(self.open_video)

        layout.addLayout(path_layout)
        layout.addWidget(self.url_input)
        layout.addWidget(self.btn_download)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status)
        layout.addWidget(self.video_list)

        self.setLayout(layout)
        self.refresh_list()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                val = int(float(p))
                self.progress_bar.setValue(val)
                self.status.setText(f"⏬ Downloading: {val}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)
            self.status.setText("📦 Merging video and audio formats...")
        QApplication.processEvents()

    def select_root_folder(self):
        global ROOT_FOLDER, APP_FOLDER, DOWNLOAD_FOLDER, CONFIG_FILE
        root = QFileDialog.getExistingDirectory(self, "Select root folder")
        if not root: return
        ROOT_FOLDER = root
        APP_FOLDER, DOWNLOAD_FOLDER, CONFIG_FILE = build_paths(ROOT_FOLDER)
        ensure_folders()
        with open(ROOT_POINTER, "w", encoding="utf-8") as f:
            f.write(ROOT_FOLDER)
        self.path_label.setText(f"📁 Root: {ROOT_FOLDER}")
        self.refresh_list()

    def download_video(self):
        if not ROOT_FOLDER:
            QMessageBox.warning(self, "Error", "Select folder first")
            return
        url = self.url_input.text().strip()
        if not url: return

        # Disable the button during downloading
        self.btn_download.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.status.setText("⏬ Analyzing and bypassing checks...")

        try:
            # Run yt-dlp download process
            with yt_dlp.YoutubeDL(get_ydl_opts(self.progress_hook)) as ydl:
                ydl.download([url])
            self.status.setText("✅ Done")
            self.url_input.clear()
            self.refresh_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status.setText("❌ Error occurred")
        finally:
            self.progress_bar.hide()
            self.btn_download.setEnabled(True)

    def refresh_list(self):
        self.video_list.clear()
        if not DOWNLOAD_FOLDER or not os.path.exists(DOWNLOAD_FOLDER): return
        for f in os.listdir(DOWNLOAD_FOLDER):
            # Now properly identifies and displays mp4, mkv, and webm files
            if f.lower().endswith((".mp4", ".mkv", ".webm")):
                self.video_list.addItem(f)

    def open_video(self, item):
        os.startfile(os.path.join(DOWNLOAD_FOLDER, item.text()))


# ==================================================
# ENTRY POINT
# ==================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
