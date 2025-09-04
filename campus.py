import json
import requests
import threading
import time
import re
from colorama import Fore, Style, init

# Initialize colorama (for Windows support too)
init(autoreset=True)

# Load dataset
with open("students.json", "r") as f:
    data = json.load(f)

# Simple loading spinner
def spinner(stop_event):
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        print(f"\r⏳ Loading {symbols[i % len(symbols)]}", end="", flush=True)
        i += 1
        time.sleep(0.1)
    print("\r", end="")  # clear line when done

# Function to clean unwanted code fences or tags
def clean_output(text: str) -> str:
    text = re.sub(r"```[a-zA-Z]*", "", text)  # remove ``` and language tags
    text = text.replace("```", "")
    return text

# Apply formatting to make headings/bullets colorful
def format_output(text: str) -> str:
    lines = text.splitlines()
    formatted = []
    for line in lines:
        if line.startswith("### "):
            # Big section heading
            formatted.append(Fore.CYAN + Style.BRIGHT + line[4:].upper() + Style.RESET_ALL)
        elif line.startswith("## "):
            formatted.append(Fore.CYAN + Style.BRIGHT + line[3:].upper() + Style.RESET_ALL)
        elif line.startswith("- "):
            formatted.append(Fore.GREEN + "• " + Style.RESET_ALL + line[2:])
        else:
            formatted.append(line)
    return "\n".join(formatted)

# Function to call Ollama API (phi model) with streaming
def ollama_phi(prompt: str):
    url = "http://localhost:11435/api/generate" #localhost:11434/api/generate
    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": True
    }

    stop_event = threading.Event()
    spin_thread = threading.Thread(target=spinner, args=(stop_event,))
    spin_thread.start()

    buffer = ""  # collect all text before formatting
    with requests.post(url, json=payload, stream=True) as resp:
        first_chunk = True
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    text = clean_output(data["response"])
                    if not text.strip():
                        continue
                    if first_chunk:
                        stop_event.set()
                        spin_thread.join()
                        print("\n")  # newline after spinner
                        first_chunk = False
                    buffer += text
                if data.get("done"):
                    break

    # Format and print the full response
    print(format_output(buffer))
    print("\n✅ Done")

# Select student by ID
student_id = int(input("Enter student ID: "))
student = next((s for s in data if s["id"] == student_id), None)

if not student:
    print("❌ Student ID not found.")
else:
    # Structured prompt
    prompt = f"""
You are given the following student's record in JSON format:
{json.dumps(student, indent=2)}

Perform the following analysis and format the response clearly as plain text with section headings.
⚠️ Do not return code, JSON, or JavaScript. Only use descriptive text.

### Student Overview
- Name: ...
- Course: ...
- Quiz Score: ... / ...
- Exam Score: ... / ...
- Awards: ...
- Proficiency: ...

### Performance Analysis
(Explain their quiz vs exam results)

### Awards Analysis
(Interpret the significance of their awards, or lack of them)

### Proficiency Context
(Explain what their proficiency level means and how it relates to performance)

### Descriptive Summary
(A paragraph summarizing strengths, weaknesses, and areas for improvement)
"""
    ollama_phi(prompt)
