#!/usr/bin/env python3
"""
Simple test server to verify the URL endpoint works
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from utils.video_downloader import video_downloader

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test server is running"}

@app.post("/analyze-url", response_class=PlainTextResponse)
async def analyze_url(url: str = Form(...)):
    """Test URL analysis endpoint"""
    try:
        if not video_downloader.is_valid_url(url):
            return "Error: Invalid URL"
        
        video_info = video_downloader.get_video_info(url)
        if not video_info:
            return "Error: Could not get video info"
        
        return f"Success! Video: {video_info['title']}"
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    print("🧪 Starting test server...")
    print("📡 Server will be available at: http://localhost:8003")
    uvicorn.run(app, host="0.0.0.0", port=8003)
