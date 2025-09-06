from ai.ollama_client import ollama_client

class TopicRecommender:
    def __init__(self):
        self.client = ollama_client
    
    def recommend_topics(self, transcript):
        """
        Generate intelligent topic recommendations using AI analysis.
        Provides context-aware suggestions for deeper learning.
        """
        if not transcript or len(transcript.strip()) < 50:
            return self._fallback_topics()
        
        # Optimized prompt for topic recommendation
        prompt = """Analyze this transcript and recommend 5-7 related topics for further study. 
        For each topic, provide:
        - Topic name
        - Why it's relevant (1 sentence)
        - Learning level (Beginner/Intermediate/Advanced)
        
        Focus on:
        - Directly related concepts
        - Practical applications
        - Prerequisites for deeper understanding
        - Emerging trends in the field
        
        Format as a numbered list with clear explanations."""
        
        try:
            recommendations = self.client.generate(prompt, transcript, max_tokens=500)
            if recommendations and len(recommendations.strip()) > 100:
                return f"🎯 AI-RECOMMENDED TOPICS FOR FURTHER STUDY\n{'='*60}\n\n{recommendations}\n\n💡 TIP: Start with topics that match your current skill level!"
        except Exception as e:
            print(f"AI topic recommendation failed: {e}")
        
        return self._fallback_topics()
    
    def _fallback_topics(self):
        """Fallback topic recommendations when AI is unavailable"""
        result = "🎯 RECOMMENDED TOPICS FOR FURTHER STUDY:\n"
        result += "=" * 50 + "\n\n"
        
        fallback_topics = [
            "General Learning: Review the main concepts discussed",
            "Practical Application: Consider real-world uses of the content", 
            "Further Study: Explore related topics and resources",
            "Skill Development: Practice the techniques mentioned",
            "Research: Look into recent developments in this field"
        ]
        
        for i, topic in enumerate(fallback_topics, 1):
            result += f"{i}. {topic}\n"
        
        result += "\n💡 TIP: Focus on topics that interest you most for deeper learning!"
        
        return result