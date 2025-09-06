from ai.ollama_client import ollama_client

class Summarizer:
    def __init__(self):
        self.client = ollama_client
    
    def summarize(self, transcript):
        """
        Generate intelligent summary using Ollama with Meta-style optimizations.
        Focuses on key insights and main points for maximum value.
        """
        if not transcript or len(transcript.strip()) < 50:
            return "Transcript too short for meaningful summary."
        
        # Optimized prompt for fast, accurate summarization
        prompt = """Create a concise, informative summary of this video transcript. 
        Focus on:
        - Main topic and key message
        - 3-5 most important points
        - Practical takeaways
        
        Keep it under 150 words and make it actionable."""
        
        try:
            summary = self.client.generate(prompt, transcript, max_tokens=200)
            return summary if summary else self._fallback_summary(transcript)
        except Exception as e:
            print(f"AI summarization failed: {e}")
            return self._fallback_summary(transcript)
    
    def _fallback_summary(self, transcript):
        """Fallback summary when AI is unavailable"""
        sentences = transcript.split('. ')
        if len(sentences) > 3:
            return '. '.join(sentences[:3]) + '.'
        return transcript[:200] + "..." if len(transcript) > 200 else transcript

    def extract_key_points(self, transcript):
        """Extract key points using AI analysis"""
        if not transcript:
            return []
        
        prompt = """Extract 5 key points from this transcript. 
        Format as a simple list, one point per line.
        Focus on actionable insights and main concepts."""
        
        try:
            result = self.client.generate(prompt, transcript, max_tokens=300)
            if result:
                # Parse the AI response into a list
                points = [line.strip() for line in result.split('\n') if line.strip()]
                return points[:5]  # Limit to 5 points
        except Exception:
            pass
        
        # Fallback to simple extraction
        sentences = transcript.split('. ')
        return sentences[:3] if sentences else []