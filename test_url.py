#!/usr/bin/env python3
"""
Test script for URL analysis functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.video_downloader import video_downloader

def test_url_validation():
    """Test URL validation"""
    print("🧪 Testing URL Validation...")
    
    test_urls = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://youtu.be/dQw4w9WgXcQ", True),
        ("https://vimeo.com/123456789", True),
        ("https://www.facebook.com/watch/?v=123456789", True),
        ("https://www.instagram.com/p/ABC123/", True),
        ("https://www.tiktok.com/@user/video/123456789", True),
        ("https://www.google.com", False),
        ("invalid-url", False),
        ("", False)
    ]
    
    for url, expected in test_urls:
        result = video_downloader.is_valid_url(url)
        status = "✅" if result == expected else "❌"
        print(f"{status} {url[:50]}... -> {result}")
    
    print()

def test_video_info():
    """Test video info extraction"""
    print("🧪 Testing Video Info Extraction...")
    
    # Test with a short, public YouTube video
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - short and well-known
    
    if video_downloader.is_valid_url(test_url):
        print(f"📺 Testing with: {test_url}")
        info = video_downloader.get_video_info(test_url)
        
        if info:
            print("✅ Video info extracted successfully!")
            print(f"   Title: {info['title']}")
            print(f"   Uploader: {info['uploader']}")
            print(f"   Duration: {info['duration']} seconds")
        else:
            print("❌ Failed to extract video info")
    else:
        print("❌ Invalid test URL")
    
    print()

def main():
    """Main test function"""
    print("🎬 Video AI Analyzer - URL Analysis Test")
    print("=" * 50)
    
    test_url_validation()
    test_video_info()
    
    print("🎉 URL functionality tests completed!")
    print("\n🚀 Your Video AI Analyzer now supports:")
    print("   • YouTube videos")
    print("   • Vimeo videos") 
    print("   • Facebook videos")
    print("   • Instagram videos")
    print("   • TikTok videos")
    print("   • And many more platforms!")
    print("\n📡 Start the server: python src/main.py")
    print("🌐 Open: http://localhost:8002")

if __name__ == "__main__":
    main()
