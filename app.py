from flask import Flask, render_template, request
import json
import openai  # Import the OpenAI Python library and set your API key here

app = Flask(__name__)

# Load quiz data
with open('knowledge_base.json', 'r') as quiz_file:
    quiz_data = json.load(quiz_file)

# Load user data
try:
    with open('user_data.json', 'r') as user_file:
        user_data = json.load(user_file)
except FileNotFoundError:
    user_data = {}

# Set your OpenAI API key
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz/<topic>', methods=['GET', 'POST'])
def select_level(topic):
    if topic == "Generative AI":
        levels = quiz_data.get(topic, {}).get('modules', {}).keys()
        return render_template('select_level.html', topic=topic, levels=levels)
    elif topic == "GPT-4":
        levels = quiz_data.get(topic, {}).get('modules', {}).keys()
        return render_template('select_level.html', topic=topic, levels=levels)
    elif topic =="HTML":
        levels = quiz_data.get(topic, {}).get('modules', {}).keys()
        return render_template('select_level.html', topic=topic, levels=levels)
    elif topic == "Machine Learning and Artifiical Intelligence":
        levels = quiz_data.get(topic, {}).get('modules', {}).keys()
        return render_template('select_level.html', topic=topic, levels=levels)
    else:
        return "Invalid topic selection"


@app.route('/quiz/<topic>/<level>/<int:question_index>', methods=['GET', 'POST'])
def quiz(topic, level, question_index):
    questions = quiz_data.get(topic, {}).get('modules', {}).get(level, {}).get('questions', [])
    question = questions[question_index]
    number_of_questions = len(questions)
    questions = quiz_data.get(topic, {}).get('modules', {}).get(level, {}).get('questions', [])
    level_data = quiz_data.get(topic, {}).get('modules', {}).get(level, {})
    questions = level_data.get('questions', [])

    if not (0 <= question_index < len(questions)):
        return render_template('quiz_completed.html')  # Redirect to a "Quiz Completed" page or handle as needed

    question = questions[question_index]
    number_of_questions = len(questions)

    if request.method == 'POST':
        user_answer = int(request.form['answer'])
        correct_answer_index = question['correctAnswer']
        is_correct = user_answer == correct_answer_index
        update_user_score(is_correct)
        return render_template('result.html', is_correct=is_correct, explanation_buttons=True, question=question,
                               question_index=question_index, number_of_questions=number_of_questions)

    return render_template('question_page.html', question=question, question_index=question_index)


def update_user_score(is_correct):
    user_id = "user123"  # Replace with actual user identification
    if user_id in user_data:
        user_data[user_id].setdefault('score', 0)
        if is_correct:
            user_data[user_id]['score'] += 1
        save_user_data()


def calculate_score(user_answers, questions):
    # Calculate the score based on user answers
    total_questions = len(questions)
    correct_answers = 0

    for question_index, question in enumerate(questions):
        correct_answer_index = question['correctAnswer']

        user_answer_key = str(question_index)
        if user_answer_key in user_answers:
            user_answer_index = int(user_answers[user_answer_key])
            if user_answer_index == correct_answer_index:
                correct_answers += 1

    return (correct_answers / total_questions) * 100


def save_user_data():
    with open('user_data.json', 'w') as user_file:
        json.dump(user_data, user_file, indent=4)


if __name__ == '__main__':
    app.run(debug=True)
