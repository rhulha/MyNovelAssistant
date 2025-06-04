from MyNovelAssistant import MyNovelAssistant

assistant = MyNovelAssistant()

assistant.addFile("./synopsis.txt", "Here is the synopsis of my new book Ex Machina 2.")

assistant.addFile("./characters.txt", "Here are the characters and locations of my new book Ex Machina 2.")

assistant.addFile("./ch01_ai.txt", "Here is chapter 1.")

assistant.addFile("./ch03_ai.txt", "Here is chapter 3.")

assistant.addFile("./ch05_ai.txt", "Here is chapter 5.")

assistant.addFile("./ch10_beats.txt", "Here are the beats of chapter 10.")

#assistant.setTask("Write a short, succinct overview of the characters and settings so far. Don't use asterisks.")

#assistant.setTask("Please write chapter 3. Go into great detail. Try to miminize the number of adverbs. Use strong verbs. Use Show don't tell. Use past tense. Write 3000 words.")

assistant.setTask("Please write chapter 10. Go into great detail. Try to miminize the number of adverbs. Use strong verbs. Use Show don't tell. Use past tense. Write 3000 words.")

response = assistant.runWithGemini() # runWithClaude()  # Or use `runWithChatGPT()` if preferred

output_file = "ch10_ai.txt"

with open(output_file, "w", encoding="utf-8") as brainstorm_file:
    brainstorm_file.write(response)

print(f"Saved to {output_file}.")