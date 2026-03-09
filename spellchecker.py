from MyNovelAssistant import MyNovelAssistant
import os
import re

assistant = MyNovelAssistant()

assistant.setSystemPrompt("You are a helpful AI that checks spelling errors in text and lists them clearly.")

directory = "./the_chapters"  # Adjust if necessary

files = assistant.get_chapter_files(directory)

for chapter_number in sorted(files.keys()):
    chapter_file = files[chapter_number]
    with open(os.path.join(directory, chapter_file), "r", encoding="utf-8") as f:
        chapter_text = f.read()

    assistant.setTask(f"Check the following chapter for spelling errors, punctuation issues, and capitalization considerations. List all issues clearly:\n\n{chapter_text}")

    response = assistant.runWithChatGPT()  # Or use `runWithClaude()` if preferred

    output_file = f"./spelling_issues_chapter_{chapter_number}.txt"
    
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(response)

    print(f"Spelling issues for Chapter {chapter_number} saved to {output_file}.")