📥 YouTube Downloader (Streamlit + yt-dlp + FFmpeg)

A simple and powerful YouTube Video & Audio Downloader built using Streamlit and yt-dlp.
Supports:

✔ Video download
✔ Audio (MP3) download
✔ Quality selection
✔ Custom save folder
✔ FFmpeg folder selection
✔ Real-time progress bar
✔ Clean UI

This project is ideal for learning Streamlit, yt-dlp, and FFmpeg integration.

📁 Folder Structure
youtube_downloader/
│
├── app.py               # Main Streamlit app
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

✨ Features
🎬 Video & Audio Download

Download any YouTube video in 1080p, 720p, 480p, 360p, or best quality.

Extract audio as MP3 with custom bitrate (320/192/128/etc.)

📁 Custom Save Location

Choose any folder where downloaded files will be saved.

🛠 FFmpeg from Your Custom Folder

No need to install FFmpeg system-wide.
Just select the folder containing:

ffmpeg.exe
ffprobe.exe

📊 Live Progress Bar

Shows:

% completed

Downloading status

Processing status

💡 Easy to Run

Just one command:

streamlit run app.py

🚀 Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube_downloader.git
cd youtube_downloader

2. Install dependencies
pip install -r requirements.txt

3. Run the app
streamlit run app.py


or on Windows (works always):

python -m streamlit run app.py

⚙ Requirements

Python 3.9+

FFmpeg (portable folder supported)

yt-dlp

Streamlit

🖥 Usage

Enter a YouTube URL

Select Video or Audio

Choose download quality

Enter Save Folder Path

Enter FFmpeg Folder Path

Click Start Download

Your file will download with progress updates and be saved in your selected folder.

📸 Screenshots (Add your images here)
![App Screenshot](./images/screen1.png)
![Download Progress](./images/screen2.png)


Create a folder:

youtube_downloader/images/


And put your screenshots there.

🧰 Tech Stack

Python

Streamlit

yt-dlp

FFmpeg

🛠 Troubleshooting
❌ Streamlit not recognized?

Use:

python -m streamlit run app.py

❌ FFmpeg not found?

Make sure your FFmpeg folder contains:

ffmpeg.exe
ffprobe.exe

❌ Dependencies missing?
pip install streamlit yt-dlp blinker watchdog

🤝 Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests.

📜 License

This project is open-source under the MIT License.youtube--download
