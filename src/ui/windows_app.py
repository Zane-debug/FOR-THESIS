from tkinter import Tk, Label, Button, Text, Scrollbar, END, messagebox
from analyzer.summarizer import Summarizer
from analyzer.study_guide import StudyGuide
from analyzer.topic_recommender import TopicRecommender
from analyzer.quiz_generator import QuizGenerator
from offline.processor import Processor

class WindowsApp:
    def __init__(self, master):
        self.master = master
        master.title("Video AI Analyzer")

        self.label = Label(master, text="Video AI Analyzer")
        self.label.pack()

        self.transcript_text = Text(master, height=15, width=50)
        self.transcript_text.pack()

        self.analyze_button = Button(master, text="Analyze Video", command=self.analyze_video)
        self.analyze_button.pack()

        self.result_text = Text(master, height=15, width=50)
        self.result_text.pack()

        self.scrollbar = Scrollbar(master, command=self.result_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=self.scrollbar.set)

    def analyze_video(self):
        transcript = self.transcript_text.get("1.0", END).strip()
        if not transcript:
            messagebox.showwarning("Input Error", "Please enter a transcript.")
            return

        summarizer = Summarizer()
        summary = summarizer.summarize(transcript)

        study_guide = StudyGuide()
        guide = study_guide.create_guide(summary)

        topic_recommender = TopicRecommender()
        topics = topic_recommender.recommend_topics(transcript)

        quiz_generator = QuizGenerator()
        quiz = quiz_generator.generate_quiz(guide)

        result = f"Summary:\n{summary}\n\nStudy Guide:\n{guide}\n\nRecommended Topics:\n{', '.join(topics)}\n\nQuiz:\n{quiz}"
        self.result_text.delete("1.0", END)
        self.result_text.insert(END, result)

