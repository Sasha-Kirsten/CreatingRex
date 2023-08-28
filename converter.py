import re
from docx import Document
import json

def extract_data(doc):
    data = {}
    current_level = None
    current_question = None
    current_section = None

    for paragraph in doc.paragraphs:
        line = paragraph.text.strip()

        if line == "Lessons":
            current_section = "Lessons"
        elif line == "Short Answer Explanations":
            current_section = "Short Answer Explanations"
        elif line == "Long Answer Explanation":
            current_section = "Long Answer Explanation"
        elif line == "Alternative Answer Explanation (with example)":
            current_section = "Alternative Answer Explanation"
        elif current_section == "Lessons":
            if line.startswith("Level"):
                current_level = line
                data[current_level] = []
            elif line.startswith("Question"):
                current_question = {"question": line.split(": ")[1], "options": []}
                data[current_level].append(current_question)
            elif line.startswith(("a)", "b)", "c)", "d)")):
                option_text = line[2:].strip()
                current_question["options"].append(option_text)
                if "[Correct]" in option_text:
                    current_question["correctAnswer"] = len(current_question["options"]) - 1
        elif current_section in ["Short Answer Explanations", "Long Answer Explanation", "Alternative Answer Explanation"]:
            match = re.match(r'(Level \d+: .+?)\n?Question (\d+): (.+)', line)
            if match:
                current_level, question_number, explanation = match.groups()
                question_number = int(question_number) - 1
                if current_section == "Short Answer Explanations":
                    data[current_level][question_number]["shortexplanation"] = explanation
                elif current_section == "Long Answer Explanation":
                    data[current_level][question_number]["longexplanation"] = explanation
                elif current_section == "Alternative Answer Explanation":
                    data[current_level][question_number]["alternateexplanation"] = explanation

    return data

if __name__ == "__main__":
    doc = Document("Lessons.docx")  # Replace with your Word document's filename

    extracted_data = extract_data(doc)

    with open("output.json", "w") as json_file:
        json_file.write(json.dumps(extracted_data, indent=4))

    print("Data extracted and saved to output.json")
