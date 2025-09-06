# filepath: video-ai-analyzer/src/main.py
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import modules
from analyzer.summarizer import Summarizer
from analyzer.study_guide import StudyGuide
from analyzer.topic_recommender import TopicRecommender
from analyzer.quiz_generator import QuizGenerator
from offline.processor import Processor, VideoProcessor
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from utils.video_downloader import video_downloader
import shutil
import os
import sys

app = FastAPI()

# Mount static files and templates
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "ui", "static")
templates_dir = os.path.join(current_dir, "ui", "templates")

# Create directories if they don't exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

def main():
    # Initialize components
    summarizer = Summarizer()
    study_guide = StudyGuide()
    topic_recommender = TopicRecommender()
    quiz_generator = QuizGenerator()

    # Check for command line arguments to determine mode (offline/online)
    if len(sys.argv) > 1 and sys.argv[1] == 'offline':
        # Process video file offline
        video_file = sys.argv[2] if len(sys.argv) > 2 else None
        if video_file:
            processor = Processor(video_file)
            transcript = processor.process_video()
            summary = summarizer.summarize(transcript)
            guide = study_guide.create_guide(summary)
            topics = topic_recommender.recommend_topics(transcript)
            quizzes = quiz_generator.generate_quizzes(guide)
            # Display results
            print("Summary:", summary)
            print("Study Guide:", guide)
            print("Recommended Topics:", topics)
            print("Quizzes:", quizzes)
        else:
            print("Please provide a video file for offline processing.")
    else:
        # Start the FastAPI server
        import uvicorn
        print("🚀 Starting Video AI Analyzer server...")
        print("📡 Server will be available at: http://localhost:8002")
        print("📖 API documentation at: http://localhost:8002/docs")
        print("\n🤖 AI Features:")
        print("   • Smart summarization with Ollama")
        print("   • Intelligent study guide generation")
        print("   • Context-aware topic recommendations")
        print("   • Dynamic quiz question creation")
        print("\n💡 To enable AI features, run: python setup_ollama.py")
        uvicorn.run(app, host="0.0.0.0", port=8002)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

# @app.post("/analyze-url", response_class=PlainTextResponse)
# async def analyze_url(url: str = Form(...)):
#     """Analyze video from URL - Temporarily disabled"""
#     return "URL analysis is temporarily disabled. Please use file upload instead."

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
    main()