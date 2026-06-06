import streamlit as st
from downloader import YTDownloader
import os
import tempfile

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
    /* Style for the browser download button */
    .stDownloadButton>button {
        width: 100%;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 YTdownloader")
st.subheader("High-Quality YouTube Downloader")

# Initialize Session State
if 'download_ready' not in st.session_state:
    st.session_state.download_ready = False
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        try:
            progress_bar.progress(float(p) / 100)
            status_message.text(f"Downloading: {d.get('_percent_str', '0%')} at {d.get('_speed_str', 'N/A')}")
        except:
            pass
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_message.text("Processing complete! Preparing for your browser...")

# UI Elements
url = st.text_input("Paste YouTube Link here:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns([2, 1])
with col1:
    format_choice = st.selectbox(
        "Select Format:",
        options=["mp4 (Standard Video)", "mp3 (High Quality Audio)", "mkv (Best Quality Video)"],
        index=0
    )
    format_map = {
        "mp4 (Standard Video)": "mp4",
        "mp3 (High Quality Audio)": "mp3",
        "mkv (Best Quality Video)": "mkv"
    }
    selected_format = format_map[format_choice]

with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    process_btn = st.button("Prepare Download")

# Progress Area (persistent placeholders)
progress_bar = st.progress(0)
status_message = st.empty()

if process_btn:
    if not url:
        st.error("Please enter a valid YouTube URL.")
    else:
        # We use a temp directory so we don't clutter the server/container disk
        temp_dir = tempfile.gettempdir()
        downloader = YTDownloader(
            download_dir=temp_dir,
            progress_hook=progress_hook
        )
        
        with st.spinner(f"Fetching {selected_format} from YouTube..."):
            result = downloader.download(url, format_type=selected_format)
            
            if result["status"] == "success":
                st.session_state.download_ready = True
                st.session_state.file_path = result['file']
                st.session_state.file_name = os.path.basename(result['file'])
            else:
                st.error(f"Error: {result['message']}")

# If the file is ready on the server, show the button to send it to the browser
if st.session_state.download_ready and st.session_state.file_path:
    if os.path.exists(st.session_state.file_path):
        st.success(f"Ready! **{st.session_state.file_name}** is processed.")
        
        with open(st.session_state.file_path, "rb") as f:
            btn = st.download_button(
                label="💾 Save to your Computer",
                data=f,
                file_name=st.session_state.file_name,
                mime="application/octet-stream"
            )
            
        st.info("Click the green button above to choose your save location via your browser.")
    else:
        st.error(f"Internal Error: The file was downloaded but we can't find it at `{st.session_state.file_path}`. Please try again.")
        st.session_state.download_ready = False

st.divider()
st.caption("Built with Python, Streamlit, and yt-dlp. Downloads are handled by your browser's default settings.")
