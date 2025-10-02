import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

# --- CONFIG ---
# Portable ffmpeg (place ffmpeg.exe in "ffmpeg" folder inside project)
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")

# --- GLOBALS ---
current_progress = 0
downloading = False

# --- Progress Hook ---
def progress_hook(d):
    global current_progress
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0.0%').strip().replace('%', '')
        try:
            current_progress = float(percent)
        except:
            current_progress = 0
    elif d['status'] == 'finished':
        current_progress = 100

# --- Progress UI Update Loop ---
def update_progress():
    progress_var.set(current_progress)
    if downloading:
        root.after(200, update_progress)

# --- Download Functions ---
def download_video(url, output_folder, quality):
    if quality == "Best":
        fmt = "bestvideo+bestaudio/best"
    elif quality == "Medium":
        fmt = "bestvideo[height<=720]+bestaudio/best"
    else:
        fmt = "bestvideo[height<=360]+bestaudio/best"

    ydl_opts = {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "format": fmt,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "ffmpeg_location": FFMPEG_PATH,   # portable ffmpeg
        "progress_hooks": [progress_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio(url, output_folder, quality):
    if quality == "Best":
        fmt = "bestaudio/best"
        bitrate = "192"
    elif quality == "Medium":
        fmt = "bestaudio[abr<=128]/bestaudio"
        bitrate = "128"
    else:
        fmt = "bestaudio[abr<=64]/bestaudio"
        bitrate = "64"

    ydl_opts = {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "format": fmt,
        "noplaylist": True,
        "ffmpeg_location": FFMPEG_PATH,   # portable ffmpeg
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# --- Threaded Download ---
def threaded_download():
    global downloading
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        download_btn.config(state=tk.NORMAL)
        return

    output_folder = folder_entry.get().strip()
    if not output_folder:
        output_folder = "downloads"

    os.makedirs(output_folder, exist_ok=True)
    quality = quality_var.get()

    try:
        progress_var.set(0)
        downloading = True
        root.after(200, update_progress)

        if choice_var.get() == "mp4":
            download_video(url, output_folder, quality)
            messagebox.showinfo("Success", f"Video ({quality}) downloaded successfully!")
        else:
            download_audio(url, output_folder, quality)
            messagebox.showinfo("Success", f"Audio ({quality}) downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Download Failed", f"Reason: {str(e)}")
    finally:
        downloading = False
        download_btn.config(state=tk.NORMAL)

def start_download():
    download_btn.config(state=tk.DISABLED)
    t = threading.Thread(target=threaded_download)
    t.start()

# --- GUI Setup ---
root = tk.Tk()
root.title("YouTube Downloader (yt-dlp + portable ffmpeg)")
root.geometry("500x350")
root.resizable(False, False)

# URL input
tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Folder selection
tk.Label(root, text="Save to Folder:").pack(pady=5)
folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)
folder_entry = tk.Entry(folder_frame, width=45)
folder_entry.pack(side=tk.LEFT, padx=5)

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, path)

browse_btn = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_btn.pack(side=tk.LEFT)

# Choice MP4/MP3
choice_var = tk.StringVar(value="mp4")
tk.Radiobutton(root, text="Download as MP4 (Video)", variable=choice_var, value="mp4").pack()
tk.Radiobutton(root, text="Download as MP3 (Audio)", variable=choice_var, value="mp3").pack()

# Quality Dropdown
tk.Label(root, text="Select Quality:").pack(pady=5)
quality_var = tk.StringVar(value="Best")
quality_menu = ttk.Combobox(root, textvariable=quality_var,
                            values=["Best", "Medium", "Low"], state="readonly", width=15)
quality_menu.pack()

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, maximum=100, length=400, variable=progress_var)
progress_bar.pack(pady=15)

# Download button
download_btn = tk.Button(root, text="Download", command=start_download,
                        bg="green", fg="white", width=20)
download_btn.pack(pady=10)

root.mainloop()
