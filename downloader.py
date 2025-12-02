import os
import streamlit as st
from yt_dlp import YoutubeDL
from pathlib import Path

# -----------------------------
# STREAMLIT CONFIG
# -----------------------------
st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("📥 YouTube Downloader with FFmpeg Support")
st.write("Download **Video or Audio**, choose quality, progress bar, save folder, and custom FFmpeg folder.")

# -----------------------------
# USER INPUT FIELDS
# -----------------------------
url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

download_type = st.radio("Select Download Type:", ["Video", "Audio"])

# Quality Options
if download_type == "Video":
    quality = st.selectbox("Video Quality", ["best", "1080p", "720p", "480p", "360p"])
else:
    quality = st.selectbox("Audio Quality (kbps)", ["best", "320", "192", "128"])

# Save Folder
default_folder = os.path.join(os.getcwd(), "downloads")
save_folder = st.text_input("Save Folder Path", default_folder)
Path(save_folder).mkdir(parents=True, exist_ok=True)

# FFmpeg Folder
ffmpeg_folder = st.text_input(
    "FFmpeg Folder Path",
    help="Provide folder containing ffmpeg & ffprobe. Example: C:/ffmpeg/bin"
)

# Download Button
start = st.button("Start Download")

# Progress Display
status_box = st.empty()
progress_bar = st.empty()


# -----------------------------
# PROGRESS HOOK FUNCTION
# -----------------------------
def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get("total_bytes", 0)
        downloaded = d.get("downloaded_bytes", 0)

        if total != 0:
            percent = int(downloaded / total * 100)
        else:
            percent = 0

        progress_bar.progress(percent)
        status_box.info(f"Downloading... {percent}%")

    elif d['status'] == 'finished':
        progress_bar.progress(100)
        status_box.success("Download finished! Processing file...")


# -----------------------------
# BUILD YDL OPTIONS
# -----------------------------
def build_options():
    if download_type == "Video":
        if quality == "best":
            format_selector = "bestvideo+bestaudio"
        else:
            height = quality.replace("p", "")
            format_selector = f"bestvideo[height<={height}]+bestaudio/best"
    else:
        format_selector = "bestaudio/best"

    opts = {
        "format": format_selector,
        "outtmpl": os.path.join(save_folder, "%(title)s.%(ext)s"),
        "ffmpeg_location": ffmpeg_folder if ffmpeg_folder else None,
        "progress_hooks": [progress_hook],
        "noplaylist": True,
    }

    # convert audio to MP3
    if download_type == "Audio":
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality if quality.isdigit() else "320"
        }]

    return opts


# -----------------------------
# DOWNLOAD PROCESS
# -----------------------------
if start:
    if not url:
        st.error("Please enter a YouTube URL.")
    else:
        try:
            status_box.info("Starting download...")
            with YoutubeDL(build_options()) as ydl:
                ydl.download([url])
            status_box.success("Download completed successfully! File saved.")
        except Exception as e:
            st.error(f"Error: {e}")
