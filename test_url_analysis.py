#!/usr/bin/env python3
"""
Standalone URL analysis test script
Tests the URL analysis functionality without the web server
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.video_downloader import video_downloader
from analyzer.summarizer import Summarizer
from analyzer.study_guide import StudyGuide
from analyzer.topic_recommender import TopicRecommender
from analyzer.quiz_generator import QuizGenerator
from offline.processor import VideoProcessor

def analyze_url_standalone(url):
    """Analyze a video URL standalone"""
    print(f"🎬 Analyzing URL: {url}")
    print("=" * 60)
    
    try:
        # Validate URL
        if not video_downloader.is_valid_url(url):
            print("❌ Error: Invalid or unsupported video URL")
            return
        
        # Get video info
        print("📺 Getting video information...")
        video_info = video_downloader.get_video_info(url)
        if not video_info:
            print("❌ Error: Could not retrieve video information")
            return
        
        print(f"✅ Title: {video_info['title']}")
        print(f"✅ Uploader: {video_info['uploader']}")
        print(f"✅ Duration: {video_info['duration']} seconds")
        print()
        
        # Download audio for faster processing
        print("📥 Downloading audio...")
        audio_path = video_downloader.download_audio_only(url)
        if not audio_path:
            print("❌ Error: Failed to download video audio")
            return
        
        print(f"✅ Audio downloaded: {os.path.basename(audio_path)}")
        print()
        
        try:
            # Initialize analysis components
            print("🤖 Initializing AI components...")
            processor = VideoProcessor(audio_path)
            summarizer = Summarizer()
            study_guide = StudyGuide()
            topic_recommender = TopicRecommender()
            quiz_generator = QuizGenerator()
            
            # Process the audio
            print("🎤 Transcribing audio...")
            transcript = processor.transcribe_audio()
            
            if not transcript or len(transcript.strip()) < 20:
                print("❌ Error: Could not transcribe audio from the video")
                return
            
            print(f"✅ Transcription completed ({len(transcript)} characters)")
            print()
            
            # Generate analysis results
            print("🧠 Generating AI analysis...")
            summary = summarizer.summarize(transcript)
            guide = study_guide.create_guide(summary)
            topics = topic_recommender.recommend_topics(transcript)
            quizzes = quiz_generator.generate_quizzes(guide)
            
            # Display results
            print("🎯 ANALYSIS RESULTS")
            print("=" * 60)
            print()
            
            print("📺 VIDEO INFORMATION:")
            print(f"Title: {video_info['title']}")
            print(f"Uploader: {video_info['uploader']}")
            print(f"Duration: {video_info['duration']} seconds")
            print(f"URL: {url}")
            print()
            
            print("📝 TRANSCRIPT:")
            print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
            print()
            
            print("📊 SUMMARY:")
            print(summary)
            print()
            
            print("📚 STUDY GUIDE:")
            print(guide[:300] + "..." if len(guide) > 300 else guide)
            print()
            
            print("🎯 RECOMMENDED TOPICS:")
            print(topics[:300] + "..." if len(topics) > 300 else topics)
            print()
            
            print("❓ QUIZZES:")
            print(quizzes[:300] + "..." if len(quizzes) > 300 else quizzes)
            print()
            
            print("✅ Analysis completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
        finally:
            # Clean up downloaded file
            video_downloader.cleanup_file(audio_path)
        
    except Exception as e:
        print(f"❌ Error analyzing URL: {e}")

def main():
    """Main function"""
    print("🎬 Video AI Analyzer - URL Analysis Test")
    print("=" * 60)
    print()
    
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll - short and well-known
        "https://youtu.be/dQw4w9WgXcQ",  # Short YouTube URL
    ]
    
    print("Available test URLs:")
    for i, url in enumerate(test_urls, 1):
        print(f"{i}. {url}")
    print()
    
    # Get user input
    while True:
        try:
            choice = input("Enter URL number (1-2) or paste your own URL: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(test_urls):
                url = test_urls[int(choice) - 1]
                break
            elif choice.startswith('http'):
                url = choice
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
    
    print()
    analyze_url_standalone(url)

if __name__ == "__main__":
    main()
