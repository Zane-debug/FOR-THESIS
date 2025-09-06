#!/usr/bin/env python3
"""
Test script for AI-powered Video Analyzer
Tests the Ollama integration with your installed models.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai.ollama_client import ollama_client
from analyzer.summarizer import Summarizer
from analyzer.study_guide import StudyGuide
from analyzer.topic_recommender import TopicRecommender
from analyzer.quiz_generator import QuizGenerator

def test_ollama_connection():
    """Test if Ollama is working"""
    print("🧪 Testing Ollama Connection...")
    try:
        result = ollama_client.generate("Say 'Hello, AI is working!'", max_tokens=50)
        if result and "working" in result.lower():
            print("✅ Ollama connection successful!")
            print(f"   Response: {result}")
            return True
        else:
            print("❌ Ollama connection failed - unexpected response")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def test_ai_components():
    """Test all AI components"""
    print("\n🤖 Testing AI Components...")
    
    # Sample transcript for testing
    sample_transcript = """
    Welcome to this tutorial on machine learning and artificial intelligence. 
    Today we'll cover the basics of neural networks, how they work, and their applications in real-world scenarios. 
    We'll start with the fundamentals of deep learning, including backpropagation and gradient descent. 
    Then we'll explore practical applications like image recognition, natural language processing, and recommendation systems. 
    By the end of this video, you'll understand how AI is transforming industries and what skills you need to get started in this field.
    """
    
    try:
        # Test Summarizer
        print("\n📊 Testing Summarizer...")
        summarizer = Summarizer()
        summary = summarizer.summarize(sample_transcript)
        print(f"✅ Summary generated: {summary[:100]}...")
        
        # Test Study Guide
        print("\n📚 Testing Study Guide...")
        study_guide = StudyGuide()
        guide = study_guide.create_guide(summary)
        print(f"✅ Study guide generated: {len(guide)} characters")
        
        # Test Topic Recommender
        print("\n🎯 Testing Topic Recommender...")
        topic_recommender = TopicRecommender()
        topics = topic_recommender.recommend_topics(sample_transcript)
        print(f"✅ Topics generated: {len(topics)} characters")
        
        # Test Quiz Generator
        print("\n❓ Testing Quiz Generator...")
        quiz_generator = QuizGenerator()
        quizzes = quiz_generator.generate_quizzes(guide)
        print(f"✅ Quizzes generated: {len(quizzes)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ AI component test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🎬 Video AI Analyzer - AI Integration Test")
    print("=" * 50)
    
    # Test Ollama connection
    if not test_ollama_connection():
        print("\n❌ Cannot proceed without Ollama connection.")
        print("   Make sure Ollama is running: ollama serve")
        return
    
    # Test AI components
    if test_ai_components():
        print("\n🎉 All AI components are working correctly!")
        print("\n🚀 Your Video AI Analyzer is ready with full AI capabilities!")
        print("   • Smart summarization with llama3:8b")
        print("   • Intelligent study guide generation")
        print("   • Context-aware topic recommendations")
        print("   • Dynamic quiz question creation")
        print("\n📡 Start the server: python src/main.py")
        print("🌐 Open: http://localhost:8002")
    else:
        print("\n❌ Some AI components failed. Check the error messages above.")

if __name__ == "__main__":
    main()
