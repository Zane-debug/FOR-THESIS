#!/usr/bin/env python3
"""
Simple working server with URL support
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

# Import analyzer components
from analyzer.summarizer import Summarizer
from analyzer.study_guide import StudyGuide
from analyzer.topic_recommender import TopicRecommender
from analyzer.quiz_generator import QuizGenerator
from offline.processor import VideoProcessor

# Import video downloader
from utils.video_downloader import video_downloader

app = FastAPI()

# Setup templates and static files
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "src", "ui", "static")
templates_dir = os.path.join(current_dir, "src", "ui", "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

@app.post("/analyze-url", response_class=PlainTextResponse)
async def analyze_url(url: str = Form(...)):
    """Analyze video from URL"""
    try:
        # Validate URL
        if not video_downloader.is_valid_url(url):
            return "Error: Invalid or unsupported video URL. Please provide a valid YouTube, Vimeo, or other supported video URL."
        
        # Get video info
        video_info = video_downloader.get_video_info(url)
        if not video_info:
            return "Error: Could not retrieve video information. Please check the URL and try again."
        
        print(f"📺 Analyzing video: {video_info['title']}")
        print(f"👤 Uploader: {video_info['uploader']}")
        print(f"⏱️ Duration: {video_info['duration']} seconds")
        
        # Download audio for faster processing
        audio_path = video_downloader.download_audio_only(url)
        if not audio_path:
            return "Error: Failed to download video audio. Please try again or check your internet connection."
        
        try:
            # Initialize analysis components
            processor = VideoProcessor(audio_path)
            summarizer = Summarizer()
            study_guide = StudyGuide()
            topic_recommender = TopicRecommender()
            quiz_generator = QuizGenerator()
            
            # Process the audio
            print("🎬 Processing audio...")
            transcript = processor.transcribe_audio()
            
            if not transcript or len(transcript.strip()) < 20:
                return "Error: Could not transcribe audio from the video. The video might not have clear speech or audio."
            
            print("✅ Transcription completed!")
            
            # Generate analysis results
            print("📊 Generating AI analysis...")
            summary = summarizer.summarize(transcript)
            guide = study_guide.create_guide(summary)
            topics = topic_recommender.recommend_topics(transcript)
            quizzes = quiz_generator.generate_quizzes(guide)
            
            # Format the results with video info
            results = f"""
🎯 VIDEO ANALYSIS RESULTS
========================

📺 VIDEO INFORMATION:
Title: {video_info['title']}
Uploader: {video_info['uploader']}
Duration: {video_info['duration']} seconds
URL: {url}

📝 TRANSCRIPT:
{transcript}

📊 SUMMARY:
{summary}

📚 STUDY GUIDE:
{guide}

🎯 RECOMMENDED TOPICS:
{topics}

❓ QUIZZES:
{quizzes}

========================
Analysis completed successfully!
"""
            
            print("✅ Analysis completed!")
            return results
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return f"Error processing video: {str(e)}"
        finally:
            # Clean up downloaded file
            video_downloader.cleanup_file(audio_path)
        
    except Exception as e:
        print(f"❌ Error analyzing URL: {e}")
        return f"Error analyzing video URL: {str(e)}"

@app.post("/analyze-video", response_class=PlainTextResponse)
async def analyze_video(video: UploadFile = File(...)):
    temp_video_path = f"temp_{video.filename}"
    with open(temp_video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    try:
        # Initialize analysis components
        processor = VideoProcessor(temp_video_path)
        summarizer = Summarizer()
        study_guide = StudyGuide()
        topic_recommender = TopicRecommender()
        quiz_generator = QuizGenerator()
        
        # Process the video
        print("🎬 Processing video...")
        transcript = processor.process_video()
        print("✅ Transcription completed!")
        
        # Generate analysis results
        print("📊 Generating analysis...")
        summary = summarizer.summarize(transcript)
        guide = study_guide.create_guide(summary)
        topics = topic_recommender.recommend_topics(transcript)
        quizzes = quiz_generator.generate_quizzes(guide)
        
        # Format the results
        results = f"""
🎯 VIDEO ANALYSIS RESULTS
========================

📝 TRANSCRIPT:
{transcript}

📊 SUMMARY:
{summary}

📚 STUDY GUIDE:
{guide}

🎯 RECOMMENDED TOPICS:
{topics}

❓ QUIZZES:
{quizzes}

========================
Analysis completed successfully!
"""
        
        print("✅ Analysis completed!")
        return results
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return f"Error processing video: {str(e)}"
    finally:
        # Clean up temporary file
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Video AI Analyzer server...")
    print("📡 Server will be available at: http://localhost:8003")
    print("📖 API documentation at: http://localhost:8003/docs")
    print("\n🤖 AI Features:")
    print("   • Smart summarization with Ollama")
    print("   • Intelligent study guide generation")
    print("   • Context-aware topic recommendations")
    print("   • Dynamic quiz question creation")
    print("   • URL analysis for YouTube, Vimeo, and more!")
    uvicorn.run(app, host="127.0.0.1", port=8003)
