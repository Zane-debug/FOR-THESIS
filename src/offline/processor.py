import os
import subprocess
import sys

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.audio_path = "output_audio.mp3"

    def check_ffmpeg(self):
        """Check if ffmpeg is available in the system PATH"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def extract_audio(self):
        import moviepy.editor as mp
        print("🎬 Extracting audio...")
        clip = mp.VideoFileClip(self.video_path)
        clip.audio.write_audiofile(self.audio_path)
        print("✅ Audio extracted:", self.audio_path)

    def transcribe_audio(self):
        import whisper
        print("\n📝 Transcribing audio with Whisper...")
        
        # Check if ffmpeg is available
        if not self.check_ffmpeg():
            print("⚠️  FFmpeg not found. Attempting to use alternative method...")
            # Try to use whisper with a different approach
            try:
                # Load the audio file directly with whisper
                model = whisper.load_model("small")
                result = model.transcribe(self.audio_path)
                transcript = result["text"]
                return transcript
            except Exception as e:
                print(f"❌ Error with alternative method: {e}")
                print("💡 Please install ffmpeg to resolve this issue:")
                print("   Option 1: Download from https://ffmpeg.org/download.html")
                print("   Option 2: Use chocolatey: choco install ffmpeg")
                print("   Option 3: Use winget: winget install ffmpeg")
                raise Exception("FFmpeg is required for audio processing. Please install it and restart your application.")
        
        # If ffmpeg is available, proceed normally
        model = whisper.load_model("small")
        result = model.transcribe(self.audio_path)
        transcript = result["text"]
        return transcript

    def process_video(self):
        self.extract_audio()
        transcript = self.transcribe_audio()
        return transcript

class Processor(VideoProcessor):
    pass