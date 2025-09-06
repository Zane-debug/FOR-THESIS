from ai.ollama_client import ollama_client

class QuizGenerator:
    def __init__(self):
        self.client = ollama_client

    def generate_quizzes(self, study_guide):
        """
        Generate intelligent quiz questions using AI analysis.
        Creates varied question types that test different levels of understanding.
        """
        if not study_guide or len(study_guide.strip()) < 50:
            return self._fallback_quizzes()
        
        # Optimized prompt for quiz generation
        prompt = """Create 5-7 quiz questions based on this study guide. Include:
        
        1. Multiple choice questions (with 4 options each)
        2. Short answer questions
        3. Application-based questions
        
        For each question, provide:
        - Clear, specific question
        - Correct answer with explanation
        - Difficulty level (Easy/Medium/Hard)
        
        Focus on testing:
        - Key concepts understanding
        - Practical application
        - Critical thinking
        - Knowledge retention
        
        Format clearly with Q1, Q2, etc."""
        
        try:
            quizzes = self.client.generate(prompt, study_guide, max_tokens=600)
            if quizzes and len(quizzes.strip()) > 200:
                return f"❓ AI-GENERATED QUIZ QUESTIONS\n{'='*50}\n\n{quizzes}\n\n💡 TIP: Test yourself regularly to reinforce learning!"
        except Exception as e:
            print(f"AI quiz generation failed: {e}")
        
        return self._fallback_quizzes()
    
    def _fallback_quizzes(self):
        """Fallback quiz questions when AI is unavailable"""
        quiz_content = []
        quiz_content.append("❓ QUIZ QUESTIONS")
        quiz_content.append("=" * 50)
        quiz_content.append("")
        
        quiz_content.append("📝 SAMPLE QUESTIONS:")
        quiz_content.append("")
        quiz_content.append("Q1. What are the main concepts discussed in this content?")
        quiz_content.append("   Answer: Review the key points and main topics covered.")
        quiz_content.append("")
        quiz_content.append("Q2. How can you apply this knowledge practically?")
        quiz_content.append("   Answer: Consider real-world applications and scenarios.")
        quiz_content.append("")
        quiz_content.append("Q3. What are the key takeaways from this content?")
        quiz_content.append("   Answer: Focus on the most important points and insights.")
        quiz_content.append("")
        quiz_content.append("Q4. Which concepts would you like to explore further?")
        quiz_content.append("   Answer: Identify areas that need deeper understanding.")
        quiz_content.append("")
        quiz_content.append("Q5. How does this content relate to your existing knowledge?")
        quiz_content.append("   Answer: Connect new information to what you already know.")
        
        quiz_content.append("")
        quiz_content.append("💡 TIP: Use these questions to test your understanding!")
        
        return "\n".join(quiz_content)