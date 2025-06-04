# MyNovelAssistant

A flexible AI-powered library designed to help authors with various writing tasks, including chapter generation, summaries, and character analysis for novels.

## Overview

MyNovelAssistant is a Python library that leverages multiple AI models (Claude, ChatGPT, Mistral, and Gemini) to assist with novel writing. It allows you to load existing chapters and summaries, maintain context across your writing, and generate new content based on your existing work.

## Features

- **Multi-Model Support**: Choose between different AI models
  - Claude (Anthropic)
  - ChatGPT (OpenAI)
  - Mistral
  - Gemini (Google)
- **Chapter Management**: Load existing chapters and summaries
- **Context-Aware**: Each AI response takes into account your entire novel's context
- **Custom Instructions**: Set specific writing goals and style requirements

## Requirements

- Python 3.10+
- Required packages:
  - anthropic
  - openai
  - mistralai
  - google-generativeai
  - python-dotenv

## Installation

1. Clone this repository or download the files
2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:

```
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
MISTRAL_API_KEY=your_mistral_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Usage

### Basic Example

```python
from MyNovelAssistant import MyNovelAssistant

# Create an instance
assistant = MyNovelAssistant()

# Add existing files to provide context
assistant.addFile("./synopsis.txt", "Here is the synopsis of my book")
assistant.addFile("./characters.txt", "Here are the characters of my book")
assistant.addFile("./ch03_beats.txt", "Here are the beats for chapter 3")

# Set a task for the AI
assistant.setTask("Write chapter 3 with dynamic dialogue between the protagonist and antagonist")

# Generate content using your preferred AI model
response = assistant.runWithClaude()  # or runWithChatGPT(), runWithMistral(), runWithGemini()

# Save the output
with open("chapter3_draft.txt", "w", encoding="utf-8") as f:
    f.write(response)
```

### Loading Multiple Chapters

The library can handle multiple chapters following a naming convention:

```python
# Load all chapters from a directory
assistant.load_all_chapters("./novel_chapters")

# Load just chapter summaries
assistant.load_summaries("./chapter_summaries")
```

Expected file naming format:
- Chapters: `chapter1_the_beginning.txt`, `chapter2_the_conflict.txt`, etc.
- Summaries: `chapter1_summary.txt`, `chapter2_summary.txt`, etc.

## Example Script

The included `write_ch.py` demonstrates how to use the library to generate a new chapter:

```python
from MyNovelAssistant import MyNovelAssistant

assistant = MyNovelAssistant()

# Load existing content for context
assistant.addFile("./synopsis.txt", "Here is the synopsis")
assistant.addFile("./characters.txt", "Here are the characters")
assistant.addFile("./ch01_ai.txt", "Here is chapter 1")

# Define the task
assistant.setTask("Please write chapter 2. Use past tense. Write 3000 words.")

# Generate the chapter
response = assistant.runWithClaude()  # Choose your preferred AI model

# Save the result
with open("ch02_ai.txt", "w", encoding="utf-8") as output_file:
    output_file.write(response)
```

## Customization

You can set a system prompt to guide the AI's behavior:

```python
assistant.setSystemPrompt("You are an expert novelist specializing in mystery fiction. Your writing style should be concise and suspenseful.")
```

## License

[MIT License](LICENSE)
