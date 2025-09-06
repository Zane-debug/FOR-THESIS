import yt_dlp
import validators
import os
import tempfile
import uuid
from typing import Optional, Dict, Any
import logging

class VideoDownloader:
    """
    Video downloader for YouTube and other video platforms.
    Supports multiple formats and quality options.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_platforms = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'twitch.tv', 'facebook.com', 'instagram.com', 'tiktok.com'
        ]
    
    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is a valid video URL"""
        if not validators.url(url):
            return False
        
        # Check if it's from a supported platform
        url_lower = url.lower()
        return any(platform in url_lower for platform in self.supported_platforms)
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                    'thumbnail': info.get('thumbnail', ''),
                    'url': url
                }
        except Exception as e:
            self.logger.error(f"Failed to get video info: {e}")
            return None
    
    def download_video(self, url: str, max_duration: int = 3600) -> Optional[str]:
        """
        Download video from URL with optimized settings.
        Returns the path to the downloaded video file.
        """
        if not self.is_valid_url(url):
            raise ValueError("Invalid or unsupported video URL")
        
        # Create temporary file for the video
        temp_dir = tempfile.gettempdir()
        video_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(temp_dir, f"video_{video_id}.%(ext)s")
        
        # Optimized download options
        ydl_opts = {
            'format': 'best[height<=720]/best',  # Prefer 720p or lower for faster processing
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'max_duration': max_duration,  # Limit to 1 hour max
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'prefer_insecure': False,
        }
        
        try:
            print(f"📥 Downloading video from: {url}")
            print("⏳ This may take a few minutes depending on video length...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first to get the actual filename
                info = ydl.extract_info(url, download=False)
                ydl.download([url])
                
                # Find the downloaded file
                downloaded_files = []
                for file in os.listdir(temp_dir):
                    if file.startswith(f"video_{video_id}") and file.endswith(('.mp4', '.webm', '.mkv', '.avi')):
                        downloaded_files.append(os.path.join(temp_dir, file))
                
                if downloaded_files:
                    video_path = downloaded_files[0]
                    print(f"✅ Video downloaded successfully: {os.path.basename(video_path)}")
                    return video_path
                else:
                    print("❌ Video download failed - no file found")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Video download failed: {e}")
            print(f"❌ Download failed: {str(e)}")
            return None
    
    def download_audio_only(self, url: str, max_duration: int = 3600) -> Optional[str]:
        """
        Download only audio from video URL for faster processing.
        Returns the path to the downloaded audio file.
        """
        if not self.is_valid_url(url):
            raise ValueError("Invalid or unsupported video URL")
        
        # Create temporary file for the audio
        temp_dir = tempfile.gettempdir()
        audio_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(temp_dir, f"audio_{audio_id}.%(ext)s")
        
        # Audio-only download options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192K',
            'max_duration': max_duration,
            'ignoreerrors': True,
            'no_check_certificate': True,
        }
        
        try:
            print(f"🎵 Downloading audio from: {url}")
            print("⏳ Extracting audio for faster processing...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
                # Find the downloaded audio file
                downloaded_files = []
                for file in os.listdir(temp_dir):
                    if file.startswith(f"audio_{audio_id}") and file.endswith(('.mp3', '.m4a', '.webm')):
                        downloaded_files.append(os.path.join(temp_dir, file))
                
                if downloaded_files:
                    audio_path = downloaded_files[0]
                    print(f"✅ Audio extracted successfully: {os.path.basename(audio_path)}")
                    return audio_path
                else:
                    print("❌ Audio extraction failed - no file found")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Audio download failed: {e}")
            print(f"❌ Audio extraction failed: {str(e)}")
            return None
    
    def cleanup_file(self, file_path: str):
        """Clean up downloaded file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Cleaned up: {os.path.basename(file_path)}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup file {file_path}: {e}")

# Global downloader instance
video_downloader = VideoDownloader()
