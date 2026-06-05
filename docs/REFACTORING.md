# Project Refactoring Documentation

## Architectural Shift
The project is transitioning from a **CustomTkinter** desktop application to a **Streamlit** web application.

### Reasons for Transition
1.  **Dockerization**: Web apps are significantly easier to containerize and deploy on various platforms (NAS, local servers, cloud).
2.  **Stability**: Moving away from a local GUI toolkit avoids common threading issues (like GUI freezing) that often plague Python desktop apps.
3.  **Portability**: Users can access the downloader from any device on their network without installing Python or binaries locally.

## Format Decisions
We have narrowed down the supported formats to the three most relevant "Industry Standards" to keep the UI clean and the experience reliable:

### Audio
- **MP3**: The universal standard for audio. High compatibility with all devices and legacy systems.

### Video
- **MP4**: The web standard. Plays in every browser and on every mobile device without extra codecs.
- **MKV**: The "Power User" format. Ideal for media servers (like Plex or Jellyfin) as it supports higher quality, multiple audio tracks, and subtitles.

### Why not others? (e.g., WAV, FLAC, AVI, MOV)
While `yt-dlp` can handle many formats, providing too many options leads to:
1.  **Confusion**: Most users don't know the technical difference between `.webm` and `.mp4`.
2.  **Incompatibility**: Some formats (like `.flac`) aren't supported by all mobile players or web browsers.
3.  **Redundancy**: MP4/MKV and MP3 cover 99% of use cases efficiently.

## Core Component: `downloader.py`
The core logic has been decoupled into `downloader.py`. This class-based approach allows for:
- Independent testing.
- Easy integration with any UI (CLI, Web, or the legacy GUI).
- Centralized management of `yt-dlp` options and FFmpeg processing.
