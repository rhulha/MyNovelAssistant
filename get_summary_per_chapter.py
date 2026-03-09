import os
import re
from MyNovelAssistant import MyNovelAssistant

folder = "./The_Chapters"

pattern = "chapter(\d+).*\.txt"
files = {int(re.search(pattern, f).group(1)): f for f in os.listdir(folder) if re.match(pattern, f)}


for chapter_number in sorted(files.keys()):
    assistant = MyNovelAssistant()

    print(f"Reading chapter {chapter_number}...", files[chapter_number])
    assistant.addFile(folder + "/" + files[chapter_number], f"Here is chapter {chapter_number} of my book RoboCop.")

    assistant.setTask("Please write a two or three sentence summary of the chapter.")
    response = assistant.runWithClaude()

    output_file = f"./chapter_{chapter_number}_summary.txt"

    with open(output_file, "w", encoding="utf-8") as _:
        _.write(response)

    print(f"Saved to {output_file}.")
