class VideoAIAnalyzerTypes:
    """This class defines various types and interfaces used throughout the application."""
    
    class Transcript:
        def __init__(self, text: str):
            self.text = text

    class Summary:
        def __init__(self, content: str):
            self.content = content

    class StudyGuide:
        def __init__(self, topics: list, summary: Summary):
            self.topics = topics
            self.summary = summary

    class QuizQuestion:
        def __init__(self, question: str, answer: str):
            self.question = question
            self.answer = answer

    class Quiz:
        def __init__(self, questions: list):
            self.questions = questions

    class TopicRecommendation:
        def __init__(self, topics: list):
            self.topics = topics