from docx import Document
import json

def extract_data(doc):
    data = {"Lessons": {}}
    current_level = None
    current_question = None
    section = "lessons"

    for paragraph in doc.paragraphs:
        line = paragraph.text.strip()

        if line == "Lessons":
            section = "lessons"
        elif line == "Short Answer Explanations":
            section = "short"
        elif line == "Long Answer Explanation":
            section = "long"
        elif line.startswith("Alternative Answer"):
            section = "alternate"

        if section == "lessons":
            if line.startswith("Level"):
                current_level = line
                data["Lessons"][current_level] = []
            elif line.startswith("Question"):
                current_question = {"question": line[9:].split("?")[0], "options": []}
                data["Lessons"][current_level].append(current_question)
            elif line.startswith(("a)", "b)", "c)", "d)")):
                option_text = line[2:].strip()
                current_question["options"].append(option_text)
                if "[Correct]" in option_text:
                    current_question["correctAnswer"] = len(current_question["options"]) - 1
        else:
            if line.startswith("Level"):
                current_level = line
            elif line.startswith("Question"):
                question_number = int(line.split(" ")[1].split(":")[0]) - 1
                explanation_key = "shortExplanation" if section == "short" else "longExplanation" if section == "long" else "alternateExplanation"
                explanation = line.split(": ")[1].strip()
                current_question = data["Lessons"][current_level][question_number]
                current_question[explanation_key] = explanation

    return data

if __name__ == "__main__":
    doc = Document("Lessons.docx")  # Replace with your Word document's filename
    extracted_data = extract_data(doc)

    with open("output.json", "w") as json_file:
        json_file.write(json.dumps(extracted_data, indent=4))

    print("Data extracted and saved to output.json")
