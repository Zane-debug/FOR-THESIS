#!/usr/bin/env python3
"""
Ollama Setup Script for Video AI Analyzer
Helps you download and test efficient models for AI-powered analysis.
"""

import subprocess
import sys
import time
import requests

def check_ollama_installed():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            return True
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
    except requests.exceptions.RequestException:
        print("❌ Ollama service is not running")
        return False

def start_ollama():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    try:
        # Start Ollama in background
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for service to start
        return check_ollama_running()
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return False

def download_model(model_name):
    """Download a specific Ollama model"""
    print(f"📥 Downloading {model_name}...")
    try:
        result = subprocess.run(['ollama', 'pull', model_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully downloaded {model_name}")
            return True
        else:
            print(f"❌ Failed to download {model_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error downloading {model_name}: {e}")
        return False

def test_model(model_name):
    """Test if a model is working"""
    print(f"🧪 Testing {model_name}...")
    try:
        test_prompt = "Hello, can you respond with just 'OK'?"
        result = subprocess.run([
            'ollama', 'run', model_name, test_prompt
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and 'OK' in result.stdout:
            print(f"✅ {model_name} is working correctly")
            return True
        else:
            print(f"❌ {model_name} test failed")
            return False
    except Exception as e:
        print(f"❌ Error testing {model_name}: {e}")
        return False

def main():
    """Main setup function"""
    print("🎬 Video AI Analyzer - Ollama Setup")
    print("=" * 50)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("\n📋 To install Ollama:")
        print("1. Visit: https://ollama.ai/download")
        print("2. Download and install Ollama for Windows")
        print("3. Run this script again")
        return
    
    # Check if Ollama service is running
    if not check_ollama_running():
        if not start_ollama():
            print("\n❌ Cannot start Ollama service. Please start it manually:")
            print("   ollama serve")
            return
    
    # Recommended models (from fastest to most capable)
    models = [
        ("tinyllama", "Fastest, smallest model (1.1GB)"),
        ("phi3:mini", "Microsoft's efficient model (2.3GB)"),
        ("llama3.2:3b", "Meta's balanced model (2GB)"),
        ("llama3.2:1b", "Ultra-lightweight model (1.3GB)")
    ]
    
    print("\n🤖 Recommended Models for Video AI Analyzer:")
    for i, (model, description) in enumerate(models, 1):
        print(f"{i}. {model} - {description}")
    
    print("\n💡 For best performance, we recommend starting with 'tinyllama' or 'phi3:mini'")
    
    # Ask user which model to download
    while True:
        try:
            choice = input("\nEnter model number (1-4) or model name: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(models):
                model_name = models[int(choice) - 1][0]
                break
            elif choice in [model[0] for model in models]:
                model_name = choice
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n👋 Setup cancelled")
            return
    
    # Download and test the model
    if download_model(model_name):
        if test_model(model_name):
            print(f"\n🎉 Setup complete! {model_name} is ready to use.")
            print("\n🚀 You can now run your Video AI Analyzer with AI-powered analysis!")
            print("   python src/main.py")
        else:
            print(f"\n⚠️  {model_name} downloaded but not working properly.")
            print("   Try a different model or check Ollama documentation.")
    else:
        print(f"\n❌ Failed to download {model_name}")
        print("   Check your internet connection and try again.")

if __name__ == "__main__":
    main()
