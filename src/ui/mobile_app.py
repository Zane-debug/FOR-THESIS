from flask import Flask, render_template, request
from analyzer.summarizer import Summarizer
from analyzer.study_guide import StudyGuide
from analyzer.topic_recommender import TopicRecommender
from analyzer.quiz_generator import QuizGenerator
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_file = request.files['video']
    if video_file:
        video_path = os.path.join('uploads', video_file.filename)
        video_file.save(video_path)

        # Here you would call the offline processor to extract audio and transcribe
        # For example:
        # transcript = process_video(video_path)

        # Assuming we have a transcript for demonstration
        transcript = "This is a sample transcript of the video content."

        summarizer = Summarizer()
        summary = summarizer.summarize(transcript)

        study_guide = StudyGuide()
        guide = study_guide.create_guide(summary)

        recommender = TopicRecommender()
        topics = recommender.recommend_topics(transcript)

        quiz_generator = QuizGenerator()
        quiz = quiz_generator.generate_quiz(guide)

        return render_template('results.html', summary=summary, guide=guide, topics=topics, quiz=quiz)

    return "No video file uploaded", 400

class MobileApp:
    def __init__(self):
        self.app = app  # Reference to the Flask app

    def run(self):
        self.app.run(debug=True)

