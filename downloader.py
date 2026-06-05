import os
from yt_dlp import YoutubeDL

class YTDownloader:
    """
    Core logic for downloading YouTube content using yt-dlp.
    Supports MP3 (audio), MP4 (video), and MKV (high-quality video).
    """

    def __init__(self, download_dir="downloads", progress_hook=None):
        self.download_dir = download_dir
        self.progress_hook = progress_hook
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_options(self, format_type):
        """Returns the yt-dlp options based on the requested format."""
        
        # Base options
        options = {
            'progress_hooks': [self.progress_hook] if self.progress_hook else [],
            'outtmpl': f'{self.download_dir}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        if format_type == 'mp3':
            options.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_type == 'mp4':
            # Ensures compatibility by forcing mp4 container
            options.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            })
        elif format_type == 'mkv':
            # Best quality available, often results in MKV
            options.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mkv',
            })
        
        return options

    def download(self, url, format_type='mp4'):
        """
        Downloads a video from a URL.
        :param url: The YouTube URL.
        :param format_type: 'mp3', 'mp4', or 'mkv'.
        :return: Dict containing info about the download or an error.
        """
        try:
            ydl_opts = self.get_options(format_type)
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    "status": "success",
                    "title": info.get('title', 'Unknown Title'),
                    "file": ydl.prepare_filename(info)
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
