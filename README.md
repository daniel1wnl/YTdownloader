# YTdownloader: Web-Based YouTube Downloader

A modern, cross-platform web application designed for seamless downloading of YouTube content. Built with **Python** and **Streamlit**, this tool allows users to easily save their favorite videos as high-quality `.mp3`, `.mp4`, or `.mkv` files via a clean web interface.

## 🚀 Key Features

- **Web-Based Interface**: A responsive UI built with `Streamlit`, accessible from any device on your network.
- **High-Quality Extraction**: 
  - **Audio (MP3)**: Extracts high-quality audio at 192kbps.
  - **Standard Video (MP4)**: Best for universal compatibility.
  - **Best Quality Video (MKV)**: Ideal for media servers (Plex, Jellyfin, Navidrome).
- **Decoupled Core**: Powerful download logic powered by `yt-dlp` and `FFmpeg`.
- **Docker Ready**: "Just works" deployment with all dependencies (including FFmpeg) pre-configured.
- **Minimalist Aesthetic**: Clean, monospace design focused on utility.
- **Dark Mode**: Integrated toggle for comfortable low-light usage.

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Web Framework**: [Streamlit](https://streamlit.io/)
- **Processing Engine**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Multimedia Framework**: [FFmpeg](https://ffmpeg.org/)

## 📋 Prerequisites

- **Option A (Docker)**: Only [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- **Option B (Local)**: Python 3.9+ and **FFmpeg** installed and added to your system's PATH.

## ⚙️ How to Run

### 🐳 Method 1: Docker (Recommended)
This is the easiest way. It handles all dependencies for you.
1. Clone the repository and navigate to the folder.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Open your browser to: `http://localhost:8501`

### 🐍 Method 2: Local Python
1. **Clone the repository:**
   ```bash
   git clone https://github.com/daniel1wnl/YTdownloader.git
   cd YTdownloader
   ```
2. **Setup Virtual Environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # Unix/macOS
   # .\env\Scripts\activate # Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📖 How to Use

1. **Open the Web UI**: Navigate to `http://localhost:8501` (or your server's IP) in your browser.
2. **Select Theme**: Use the **"Mode"** button in the top right to toggle between Light and Dark themes.
3. **Enter Link**: Paste a YouTube video URL into the input field.
4. **Select Format**:
   - **mp4**: For standard video compatible with all devices.
   - **mp3**: For high-quality audio extraction.
   - **mkv**: For best quality video (best for media servers like Plex/Jellyfin).
5. **Prepare Download**: Click the **"Prepare Download"** button. The server will fetch the content and process it.
6. **Save to Computer**: Once the green **"Save to your Computer"** button appears, click it. Your browser will then prompt you to save the file to your preferred location.

## 🏠 Self-Hosting (NAS / Ubuntu Server)

Since this app is containerized, you can host it just like **Jellyfin**, **Immich**, or **Plex**:

1. **Copy the files**: Move the project folder to your server.
2. **Run Docker**: Execute `docker-compose up -d` (the `-d` runs it in the background).
3. **Access via Network**: Instead of `localhost`, your family/friends can use the server's IP address: `http://192.168.x.x:8501`.
4. **Storage**: All temporary processing happens in the container, and final downloads are sent directly to the user's browser.

## 🐳 Docker Tips

When running `docker-compose up`, you might see some hints in your terminal:
- **`w Enable Watch`**: This is for developers; it tells Docker to watch for code changes and restart automatically.
- **`d Detach`**: Press `d` to run the container in the background, freeing up your terminal window. You can stop it later with `docker-compose stop`.

## 📁 Project Structure

- `app.py`: The Streamlit web interface.
- `downloader.py`: Core logic for `yt-dlp` processing.
- `Dockerfile` & `docker-compose.yml`: For containerized deployment.
- `docs/REFACTORING.md`: Technical details on the architecture.

## 👤 Author

**Daniel Gregorio-Torres**
- [GitHub](https://github.com/daniel1wnl)
- [LinkedIn](https://www.linkedin.com/in/danielgregoriotorres/)
