import os
import re
from pathlib import Path
import anthropic
import openai
from mistralai import Mistral
import google.generativeai as genai
from dotenv import load_dotenv

class MyNovelAssistant:

    def __init__(self):
        self.files = {}
        self.system_prompt = ""
        self.task = ""
        self.messages = []
        load_dotenv()

    def setSystemPrompt(self, system_prompt):
        self.system_prompt = system_prompt

    def setTask(self, task):
        self.task = task

    def get_chapter_files(self, directory, pattern=r"chapter(\d+)_the_[_a-z]+\.txt"):
        return {
            int(re.search(pattern, f).group(1)): f
            for f in os.listdir(directory)
            if re.match(pattern, f)
        }

    def load_all_chapters(self, directory, custom_lambda=None):
        files = self.get_chapter_files(directory)

        if custom_lambda:
            files = custom_lambda(files)

        # this changes the contents of the files dictionary
        for chapter_number, filename in files.items():
            print(f"Reading chapter {chapter_number}...", files[chapter_number])
            with open(os.path.join(directory, files[chapter_number]), "r", encoding="utf-8") as f:
                files[chapter_number] = f.read()

        for chapter_number in sorted(files.keys()):
            print(f"Adding chapter {chapter_number}...")
            self.messages.extend([
                {"role": "user", "content": f"Here is chapter {chapter_number}:\n\n{files[chapter_number]}"},
                {"role": "assistant", "content": f"I have chapter {chapter_number}."}
            ])

    def load_summaries(self, directory, custom_lambda=None):
        files = {
            int(re.search(r"chapter(\d+)_summary.txt", f).group(1)): f
            for f in os.listdir(directory)
            if re.match(r"chapter\d+_summary.txt", f)
        }

        if custom_lambda:
            files = custom_lambda(files)

        # this changes the contents of the files dictionary
        for chapter_number, filename in files.items():
            print(f"Reading chapter {chapter_number}...", files[chapter_number])
            with open(os.path.join(directory, files[chapter_number]), "r", encoding="utf-8") as f:
                files[chapter_number] = f.read()

        for chapter_number in sorted(files.keys()):
            self.messages.extend([
                {"role": "user", "content": f"Here is a summary for chapter {chapter_number}:\n\n{files[chapter_number]}"},
                {"role": "assistant", "content": f"I have the summary for chapter {chapter_number}."}
            ])

    def runWithClaude(self):
        # Create a local copy of messages
        messages = self.messages + [{"role": "user", "content": self.task}]

        response = anthropic.Anthropic().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=5300,
            temperature=0.7,
            system=self.system_prompt,
            messages=messages
        )
        return response.content[0].text

    def runWithChatGPT(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Create a local copy of messages
        messages = [{"role": "system", "content": self.system_prompt}] + self.messages
        messages.append({"role": "user", "content": self.task})

        response = openai.Client().chat.completions.create(
            model="chatgpt-4o-latest",
            messages=messages,
            max_tokens=5300,
            temperature=0.7
        )
        return response.choices[0].message.content

    def runWithMistral(self):
        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

        messages = [{"role": "system", "content": self.system_prompt}] + self.messages
        messages.append({"role": "user", "content": self.task})

        response = client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            max_tokens=5300,
            temperature=0.7
        )
        return response.choices[0].message.content

    def runWithGemini(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        prompt = f"{self.system_prompt}\n\n"
        for message in self.messages:
            prompt += f"{message['role']}: {message['content']}\n"
        prompt += f"user: {self.task}"
        
        response = genai.GenerativeModel('gemini-2.5-pro-preview-03-25').generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 5300,
                "temperature": 0.7
            }
        )
        return response.text

    def debugMessages(self):
        for message in self.messages:
            print(message)

    def addFile(self, filename, message):
        with open(filename, "r", encoding="utf-8") as f:
            contents = f.read()

        self.messages.extend([
            {"role": "user", "content": message+"\n\n"+contents},
            {"role": "assistant", "content": "Okay, got it."}
        ])

    def text_to_speech(self, text, output_path, voice="onyx", max_chars=2000):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        chunk = ''
        for sentence in sentences:
            if len(chunk) + len(sentence) > max_chars:
                chunks.append(chunk)
                chunk = sentence
            else:
                chunk = (chunk + ' ' + sentence).strip()
        if chunk:
            chunks.append(chunk)

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        output_path = Path(output_path)

        part_files = []
        for i, chunk in enumerate(chunks, start=1):
            response = client.audio.speech.create(
                model='gpt-4o-mini-tts',
                voice=voice,
                input=chunk,
            )
            part_path = output_path.parent / f"{output_path.stem}_part{i}.mp3"
            part_path.write_bytes(response.content)
            part_files.append(part_path)
            print(f"Saved {part_path.name}")

        return part_files
