import requests
import json
import time
from typing import Optional, Dict, Any
import logging

class OllamaClient:
    """
    Efficient Ollama client optimized for speed and accuracy.
    Uses Meta-style optimizations: streaming, caching, and smart prompting.
    """
    
    def __init__(self, model: str = "llama3:8b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30  # 30 second timeout
        self.cache = {}  # Simple in-memory cache
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make optimized request to Ollama API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/{endpoint}",
                json=data,
                stream=False  # Disable streaming for faster processing
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ollama request failed: {e}")
            return None
    
    def _get_cache_key(self, prompt: str, context: str = "") -> str:
        """Generate cache key for prompt"""
        return f"{hash(prompt + context)}"
    
    def _is_cached(self, cache_key: str) -> Optional[str]:
        """Check if result is cached"""
        if cache_key in self.cache:
            cached_time, result = self.cache[cache_key]
            # Cache valid for 1 hour
            if time.time() - cached_time < 3600:
                return result
            else:
                del self.cache[cache_key]
        return None
    
    def _cache_result(self, cache_key: str, result: str):
        """Cache the result"""
        self.cache[cache_key] = (time.time(), result)
        # Limit cache size to 100 entries
        if len(self.cache) > 100:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][0])
            del self.cache[oldest_key]
    
    def generate(self, prompt: str, context: str = "", max_tokens: int = 500) -> str:
        """
        Generate response using Ollama with optimizations:
        - Caching for repeated requests
        - Optimized token limits
        - Error handling and fallbacks
        """
        cache_key = self._get_cache_key(prompt, context)
        
        # Check cache first
        cached_result = self._is_cached(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare optimized prompt
        full_prompt = self._optimize_prompt(prompt, context)
        
        # Make request with optimized parameters for llama3:8b
        data = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.6,  # Slightly lower for more focused responses
                "top_p": 0.85,       # Focus on most likely tokens
                "top_k": 40,         # Limit vocabulary for speed
                "num_predict": max_tokens,  # Use num_predict for llama3
                "repeat_penalty": 1.1,  # Prevent repetition
                "stop": ["\n\n", "---", "===", "##"],  # Stop at section breaks
                "num_ctx": 2048,     # Context window for efficiency
                "num_thread": 4      # Use 4 threads for faster processing
            }
        }
        
        result = self._make_request("generate", data)
        
        if result and "response" in result:
            response_text = result["response"].strip()
            # Cache the result
            self._cache_result(cache_key, response_text)
            return response_text
        
        # Fallback to simple text processing if Ollama fails
        return self._fallback_processing(prompt, context)
    
    def _optimize_prompt(self, prompt: str, context: str = "") -> str:
        """
        Optimize prompt for better performance and accuracy.
        Meta-style prompt engineering for efficiency.
        """
        # Add context if provided
        if context:
            optimized_prompt = f"Context: {context}\n\nTask: {prompt}\n\nResponse:"
        else:
            optimized_prompt = f"Task: {prompt}\n\nResponse:"
        
        # Add efficiency instructions
        optimized_prompt += "\n\nInstructions: Be concise, accurate, and practical. Focus on key points."
        
        return optimized_prompt
    
    def _fallback_processing(self, prompt: str, context: str = "") -> str:
        """
        Fallback processing when Ollama is unavailable.
        Provides basic functionality without AI.
        """
        if "summary" in prompt.lower():
            if context:
                sentences = context.split('. ')
                return '. '.join(sentences[:3]) + '.' if sentences else "Summary not available."
            return "Summary generation requires content to analyze."
        
        elif "study guide" in prompt.lower():
            return "Study Guide:\n• Review the main concepts\n• Practice key points\n• Apply knowledge practically"
        
        elif "topics" in prompt.lower():
            return "Recommended Topics:\n• General learning concepts\n• Practical applications\n• Further study areas"
        
        elif "quiz" in prompt.lower():
            return "Quiz Questions:\n• What are the main concepts?\n• How can you apply this knowledge?\n• What are the key takeaways?"
        
        return "Analysis completed. Please ensure Ollama is running for enhanced AI features."

# Global client instance
ollama_client = OllamaClient()
