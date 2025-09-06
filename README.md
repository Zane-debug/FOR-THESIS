# Video AI Analyzer

## Overview
The Video AI Analyzer is an application designed to summarize video content, create study guides, recommend related topics, and generate practice quizzes. It supports both offline and online functionality, making it accessible on Windows and smartphones.

## Features
- **Video Summarization**: Extracts key information from video transcripts to provide concise summaries.
- **Study Guide Creation**: Organizes summarized content into structured study guides for effective learning.
- **Topic Recommendations**: Suggests related topics based on keywords found in the video transcript.
- **Quiz Generation**: Creates practice quizzes to reinforce learning and assess understanding.
- **Offline Functionality**: Allows users to process videos without an internet connection.
- **Online Integration**: Connects to external APIs for enhanced processing capabilities.

## Project Structure
```
video-ai-analyzer
├── src
│   ├── main.py
│   ├── analyzer
│   │   ├── summarizer.py
│   │   ├── study_guide.py
│   │   ├── topic_recommender.py
│   │   └── quiz_generator.py
│   ├── offline
│   │   └── processor.py
│   ├── online
│   │   └── api_client.py
│   ├── ui
│   │   ├── windows_app.py
│   │   └── mobile_app.py
│   └── types
│       └── index.py
├── requirements.txt
├── README.md
└── setup.py
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd video-ai-analyzer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
- To run the application, execute the following command:
  ```
  python src/main.py
  ```
- Follow the prompts in the user interface to analyze videos, generate study guides, and create quizzes.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.