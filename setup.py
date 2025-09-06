from setuptools import setup, find_packages

setup(
    name="video-ai-analyzer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Video AI Analyzer application that summarizes video content, creates study guides, recommends related topics, and generates practice quizzes.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "moviepy",
        "whisper",
        "requests",
        "flask",  # if using Flask for the online API
        "tkinter",  # if using Tkinter for the Windows UI
        # Add other dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "video-ai-analyzer=main:main",  # Adjust the entry point as necessary
        ],
    },
)