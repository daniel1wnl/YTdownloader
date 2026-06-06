import streamlit as st
from downloader import YTDownloader
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="YTdownloader",
    layout="centered"
)

# Monospace Minimalist CSS
st.markdown("""
    <style>
    /* Global Monospace Font */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, div, input, button, select {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Clean Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 2px;
        border: 1px solid #333;
        background-color: transparent;
        color: #333;
        height: 3em;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #333;
        color: #fff;
        border: 1px solid #333;
    }

    /* Green Download Button */
    .stDownloadButton>button {
        width: 100%;
        border-radius: 2px;
        border: 1px solid #28a745;
        background-color: transparent;
        color: #28a745;
        height: 3em;
    }
    .stDownloadButton>button:hover {
        background-color: #28a745;
        color: #fff;
    }

    /* Input Styling */
    .stTextInput>div>div>input {
        border-radius: 2px;
        border: 1px solid #ccc;
    }

    /* Footer Branding */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 20px;
        font-size: 12px;
        color: #888;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("YTdownloader")
st.text("Minimalist YouTube Content Extractor")
st.write("---")

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
            status_message.text(f"Progress: {d.get('_percent_str', '0%')} | Speed: {d.get('_speed_str', 'N/A')}")
        except:
            pass
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_message.text("Status: Processing complete.")

# UI Elements
url = st.text_input("URL", placeholder="Enter YouTube link...")

col1, col2 = st.columns([2, 1])
with col1:
    format_choice = st.selectbox(
        "Format",
        options=["mp4", "mp3", "mkv"],
        index=0
    )
    selected_format = format_choice

with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    process_btn = st.button("Prepare")

# Progress Area
progress_bar = st.progress(0)
status_message = st.empty()

if process_btn:
    if not url:
        st.error("Error: URL required.")
    else:
        temp_dir = tempfile.gettempdir()
        downloader = YTDownloader(
            download_dir=temp_dir,
            progress_hook=progress_hook
        )
        
        with st.spinner("Processing..."):
            result = downloader.download(url, format_type=selected_format)
            
            if result["status"] == "success":
                st.session_state.download_ready = True
                st.session_state.file_path = result['file']
                st.session_state.file_name = os.path.basename(result['file'])
            else:
                st.error(f"Error: {result['message']}")

# Download Trigger
if st.session_state.download_ready and st.session_state.file_path:
    if os.path.exists(st.session_state.file_path):
        st.write("---")
        st.text(f"Ready: {st.session_state.file_name}")
        
        with open(st.session_state.file_path, "rb") as f:
            st.download_button(
                label="Download to Local",
                data=f,
                file_name=st.session_state.file_name,
                mime="application/octet-stream"
            )
    else:
        st.error("Error: File resolution failed. Please retry.")
        st.session_state.download_ready = False

# Footer Branding
st.markdown("""
    <div class="footer">
        daniel1wnl / github
    </div>
    """, unsafe_allow_html=True)
