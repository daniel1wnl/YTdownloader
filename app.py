import streamlit as st
from downloader import YTDownloader
import os
import time

# Page configuration
st.set_page_config(
    page_title="YTdownloader Web",
    page_icon="📥",
    layout="centered"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main {
        max-width: 700px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF0000;
        color: white;
    }
    .stButton>button:hover {
        background-color: #CC0000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 YTdownloader")
st.subheader("High-Quality YouTube Downloader")

# Initialize Session State for progress
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'status_text' not in st.session_state:
    st.session_state.status_text = ""

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        try:
            st.session_state.progress = float(p) / 100
            st.session_state.status_text = f"Downloading: {d.get('_percent_str', '0%')} at {d.get('_speed_str', 'N/A')}"
        except:
            pass
    elif d['status'] == 'finished':
        st.session_state.progress = 1.0
        st.session_state.status_text = "Processing complete! Converting/Merging..."

# UI Elements
url = st.text_input("Paste YouTube Link here:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns([2, 1])
with col1:
    format_choice = st.selectbox(
        "Select Format:",
        options=["mp4 (Standard Video)", "mp3 (High Quality Audio)", "mkv (Best Quality Video)"],
        index=0
    )
    # Map selection to internal format keys
    format_map = {
        "mp4 (Standard Video)": "mp4",
        "mp3 (High Quality Audio)": "mp3",
        "mkv (Best Quality Video)": "mkv"
    }
    selected_format = format_map[format_choice]

with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    download_btn = st.button("Download")

# Progress Bar Area
progress_bar = st.progress(st.session_state.progress)
status_message = st.empty()
status_message.text(st.session_state.status_text)

if download_btn:
    if not url:
        st.error("Please enter a valid YouTube URL.")
    else:
        # Reset progress
        st.session_state.progress = 0
        st.session_state.status_text = "Initializing..."
        
        # Initialize downloader
        downloader = YTDownloader(
            download_dir="downloads",
            progress_hook=progress_hook
        )
        
        with st.spinner(f"Preparing {selected_format} download..."):
            result = downloader.download(url, format_type=selected_format)
            
            if result["status"] == "success":
                st.success(f"Successfully downloaded: **{result['title']}**")
                st.balloons()
                
                # Show file path (relative to the app)
                file_name = os.path.basename(result['file'])
                st.info(f"File saved in `downloads/` folder as: `{file_name}`")
            else:
                st.error(f"Download failed: {result['message']}")

st.divider()
st.caption("Built with Python, Streamlit, and yt-dlp. For personal use only.")
