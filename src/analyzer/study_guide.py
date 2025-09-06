from ai.ollama_client import ollama_client

class StudyGuide:
    def __init__(self):
        self.client = ollama_client

    def create_guide(self, summary):
        """
        Create intelligent study guide using AI analysis.
        Generates personalized learning materials based on content.
        """
        if not summary or len(summary.strip()) < 20:
            return self._fallback_guide(summary)
        
        # Optimized prompt for study guide generation
        prompt = """Create a comprehensive study guide from this summary. Include:
        
        1. KEY CONCEPTS (3-5 main ideas)
        2. LEARNING OBJECTIVES (what to achieve)
        3. STUDY STRATEGIES (how to learn effectively)
        4. PRACTICAL APPLICATIONS (real-world uses)
        5. FURTHER READING SUGGESTIONS (related topics)
        
        Format clearly with emojis and bullet points. Make it actionable and engaging."""
        
        try:
            guide = self.client.generate(prompt, summary, max_tokens=400)
            if guide and len(guide.strip()) > 50:
                return f"📚 AI-GENERATED STUDY GUIDE\n{'='*50}\n\n{guide}"
        except Exception as e:
            print(f"AI study guide generation failed: {e}")
        
        return self._fallback_guide(summary)
    
    def _fallback_guide(self, summary):
        """Fallback study guide when AI is unavailable"""
        guide_content = []
        guide_content.append("📚 STUDY GUIDE")
        guide_content.append("=" * 50)
        guide_content.append("")
        
        # Extract key points from summary
        sentences = summary.split('. ')
        key_points = sentences[:5] if len(sentences) > 5 else sentences
        
        guide_content.append("🔑 KEY POINTS:")
        for i, point in enumerate(key_points, 1):
            if point.strip():
                guide_content.append(f"{i}. {point.strip()}")
        
        guide_content.append("")
        guide_content.append("📖 LEARNING OBJECTIVES:")
        guide_content.append("• Understand the main concepts discussed")
        guide_content.append("• Identify key takeaways from the content")
        guide_content.append("• Apply knowledge to practical scenarios")
        
        guide_content.append("")
        guide_content.append("💡 STUDY TIPS:")
        guide_content.append("• Review the key points regularly")
        guide_content.append("• Practice explaining concepts in your own words")
        guide_content.append("• Connect new information to existing knowledge")
        
        return "\n".join(guide_content)