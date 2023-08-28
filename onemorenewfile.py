from flask import Flask, render_template_string, request, jsonify, session, url_for, redirect, render_template
import openai
import random
import json

import ScoreTracker
import QuestionTracker

app = Flask(__name__)
username = "Sunny"
app.secret_key = 'XYDHSKD889SKDHDJS'
openai.api_key = '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'
score_tracker = ScoreTracker.ScoreTracker()
consecutive_correct_answers = 0
question_tracker = QuestionTracker.QuestionTracker

# Load user data from JSON file
try:
    with open(f'{username}.json', 'r') as f:
        user_data = json.load(f)
except FileNotFoundError:
    user_data = {'incorrect_questions': [], 'asked_questions': []}


def load_knowledge_base():
    try:
        with open('output.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_knowledge_base(knowledge_base):
    with open('output.json', 'w') as f:
        json.dump(knowledge_base, f, indent=4)


def save_knowledge_base1(subject, question, explanation=None, example=None, elaborated_explanation=None):
    # Check if the question already exists in the knowledge base
    knowledge_base = load_knowledge_base()
    if question in knowledge_base:
        if explanation:
            knowledge_base[question]['explanation'] = explanation
        if example:
            knowledge_base[question]['example'] = example
        if elaborated_explanation:
            knowledge_base[question]['elaborated_explanation'] = elaborated_explanation
    else:
        # If the question doesn't exist, create a new entry
        knowledge_base[question] = {
            'subject': subject,
            'explanation': explanation,
            'example': example,
            'elaborated_explanation': elaborated_explanation,
        }

    # At this point, you might want to persist 'knowledge_base' into a database or a file,
    # because currently it's just an in-memory dictionary and will be lost when the program ends
def get_user_data(user_id):
    with open('users.json', 'r') as f:
        users_data = json.load(f)
        for user in users_data['users']:
            if user['UserID'] == user_id:
                return user
        return None # or an appropriate default value if the user is not found
def update_user_data(user_id, updated_data):
    with open('users.json', 'r') as f:
        users_data = json.load(f)

    for user in users_data['users']:
        if user['UserID'] == user_id:
            user.update(updated_data)
            break

    with open('users.json', 'w') as f:
        json.dump(users_data, f)
def get_user_level(user_id, subject_name):
    # Load the JSON data
    with open('user_data.json', 'r') as file:
        data = json.load(file)

    # Iterate through the users to find the matching user ID
    for user in data['users']:
        if user['UserID'] == str(user_id):
            # Iterate through the subjects to find the matching subject name
            for subject in user['Subjects']:
                if subject['Name'] == subject_name:
                    # Return the number of sub-modules completed in the selected subject
                    return len(subject['Modules'][0]['SubModules'])

    return None


@app.route('/')
def home():
    subjects = ["HTML", "Python", "Machine Learning", "Artificial Intelligence"]
    return render_template('myhtml.html', subjects=subjects)


@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    data = request.get_json()
    subject = data['subject']
    module = data['module']
    submodule = data['submodule']

    knowledge_base = load_knowledge_base()

    try:
        with open(f'{username}.json', 'r') as f:
            user_data = json.load(f)
            existing_user = True
    except FileNotFoundError:
        user_data = {}
        existing_user = False
        # Initialize the session data
    if existing_user:
        # Logic for existing users, e.g. load existing level, subject, module
        current_level = user_data['level']
        current_subject = user_data['subject']
        current_module = user_data['module']
        # Continue the quiz at the existing level
        # ...
    else:
        session['username'] = username
        session['incorrect_questions'] = user_data.get('incorrect_questions', [])

        print(module)
        print(submodule)
        print(len(knowledge_base[subject]["modules"][module][submodule]['questions']))
        if subject not in knowledge_base or module not in knowledge_base[subject]['modules'] or len(
                knowledge_base[subject]["modules"][module][submodule]['questions']) < 10:
            if subject in knowledge_base and module in knowledge_base[subject]['modules']:
                existing_questions_text = [q['question'] for q in
                                           knowledge_base[subject]['modules'][module][submodule]['questions']]
            else:
                existing_questions_text = []

            num_questions_to_generate = 10 - len(existing_questions_text)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",
                     "content": f"Generate 2 distinct multiple-choice questions and their answers about {subject} and {submodule}. " \
                                f"After that, provide an explanation and example for each answer in format Question:, Options:,Answer:,Explanation:,Example:. " \
                                f"Please end each set of question, options, answer, explanation, and example with the phrase '***End of Question***'. " \
                                f"Do not use image or code snippet questions."}
                ],
                max_tokens=1000,
                temperature=0.2

            )
            print(response)
            assistant_responses = [message['message'] for message in response['choices'] if 'message' in message]
            content = ""
            for assistant_response in assistant_responses:
                if 'content' in assistant_response:
                    content += assistant_response['content'] + "\n"

            # Split into separate question blocks
            question_blocks = content.split("***End of Question***")
            question_blocks = [block.strip() for block in question_blocks if block.strip() != ""]

            new_questions = []

            for block in question_blocks:

                # Split into question/options and answer
                question_and_options, rest_of_block = block.split("\nAnswer:")
                # Split the rest_of_block into answer, explanation and example
                answer, rest_of_block = rest_of_block.split("\nExplanation: ")
                explanation, example = rest_of_block.split("\nExample:")

                # Split the rest_of_block into answer, explanation and example

                # Split the answer block to get the answer text without the option letter
                answer_text = answer.strip().split(") ")[1]

                # Split into separate lines
                question_and_options = question_and_options.split("\n")

                # Extract the question (excluding the question number)
                question = question_and_options[0].strip()

                # Extract the options (excluding the option letters)
                options = []
                for option in question_and_options[1:]:
                    option_parts = option.strip().split(") ")
                    if len(option_parts) > 1:
                        options.append(option_parts[1])

                # Extract the explanation and example
                explanation = explanation.strip()
                example = example.strip()

                print("Question:", question)
                print("Options:", options)
                print("Answer:", answer_text)
                print("Explanation:", explanation)
                print("Example:", example)

                # Find the index of the correct answer in the options list
                correct_answer_index = options.index(answer_text.strip())
                # Add to new_questions list
                new_questions.append({
                    'question': question,
                    'options': options,
                    'correctAnswer': correct_answer_index,
                    'explanation': explanation,
                    'example': example
                })

                if subject in knowledge_base and module in knowledge_base[subject]['modules']:
                    for question_data in new_questions:
                        if question_data['question'] not in existing_questions_text:
                            knowledge_base[subject]['modules'][module][submodule]['questions'].append(question_data)
                else:
                    if subject not in knowledge_base:
                        knowledge_base[subject] = {'modules': {}}
                    knowledge_base[subject]['modules'][module][submodule] = {'questions': new_questions}

                save_knowledge_base(knowledge_base)

    return jsonify({"status": "Quiz started successfully"})


@app.route('/generate_question', methods=['GET'])
def generate_question():
    subject = request.args.get('subject')
    module = request.args.get('modules')
    submodule = request.args.get('submodule')

    knowledge_base = load_knowledge_base()
    questions = knowledge_base[subject]['modules'][module][submodule]['questions']

    # Check if all questions have been asked
    if len(user_data['asked_questions']) == len(questions):
        # If all questions are asked, then check for incorrect questions
        if user_data['incorrect_questions']:
            selected_question = random.choice(user_data['incorrect_questions'])
        else:
            return redirect(url_for('end_of_quiz'))  # Redirect or handle end of quiz
    else:
        # Select an unasked question
        unasked_questions = [q for q in questions if q['question'] not in user_data['asked_questions']]
        selected_question = random.choice(unasked_questions)

    question = selected_question['question']
    options = selected_question['options']
    correct_answer = selected_question['correctAnswer']

    # Add the asked question to the user asked_questions in JSON
    user_data['asked_questions'].append(question)
    # Save user_data to JSON file
    with open(f'{username}.json', 'w') as f:
        json.dump(user_data, f)

    return jsonify({
        'question': question,
        'options': options,
        'correctAnswer': correct_answer
    })

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global consecutive_correct_answers
    data = request.get_json()
    user_choice = data.get('user_choice')
    subject = data.get('subject')
    question = data.get('question')
    module = data.get('modules')
    submodule = data.get('submodule')

    if user_choice is None or subject is None or question is None:
        return jsonify({'error': 'Invalid request payload'})

    knowledge_base = load_knowledge_base()

    if subject in knowledge_base:
        questions = knowledge_base[subject]["modules"][module][submodule]['questions']

        for q in questions:
            if q['question'] == question:
                correct_answer = q['correctAnswer']
                options = q['options']
                explanation = q['shortExplanation']
                longexplanation = q['longExplanation']
                alternateexplanation = q['alternateExplanation']
                print('correct',correct_answer)
                print('options',options)
                print('explanation',explanation)

                is_correct = user_choice == correct_answer

                if is_correct:
                    score_tracker.correct_answer()
                    # Remove the question from incorrect_questions if answered correctly
                    if question in user_data['incorrect_questions']:
                        user_data['incorrect_questions'].remove(question)
                    consecutive_correct_answers += 1
                    # Check for three consecutive correct answers
                    if consecutive_correct_answers == 3:
                        # Send message: "Three in a row! you are rolling."
                        response_message = "Three in a row! you are rolling."
                    elif consecutive_correct_answers == 5:
                        # Display GIF for "Five in a row."
                        response_gif_url = "/static/five_in_a_row.gif"
                else:
                    # Add the incorrect question if not already present
                    consecutive_correct_answers = 0
                    if question not in user_data['incorrect_questions']:
                        user_data['incorrect_questions'].append(question)
                        score_tracker.incorrect_answer()
                        print(session)
                if question_tracker.get_current_question() == 10:
                    if score_tracker.get_score() == 10:
                        # Display GIF for all correct answers
                        response_gif_url = "/static/all_correct.gif"
                    elif score_tracker.get_score() < 10:
                        # Display GIF for level 1 completed but with incorrect answers
                        response_gif_url = "/static/level1_completed_with_incorrect.gif"
                        # Your logic to re-ask incorrect questions ...

                return jsonify({
                    'is_correct': is_correct,
                    'correctAnswer': options[correct_answer],
                    'explanation': explanation,  # Return explanation, if any
                    'longexplanation': longexplanation,
                    'alternateExplanation': alternateexplanation,
                    "gif_url": response_gif_url
                })

        return jsonify({'error': 'Invalid question'})
    else:
        return jsonify({'error': 'Invalid subject'})

def end_of_quiz():
    # Code to handle the end of quiz, including displaying the "level completed" GIF
    user_response = input("Are you ready for the next level? (yes/no): ")
    if user_response.lower() == "yes":

        # Code to start next level
    else:
        question_response = input("Do you have any questions? (yes/no): ")
        if question_response.lower() == "no":
            comeback_response = input("Do you want to come back later? (yes/no): ")
            # Handle user's response



@app.route('/get_modules', methods=['GET'])
def get_modules():
    subject = request.args.get('subject')

    knowledge_base = load_knowledge_base()

    if subject in knowledge_base:
        modules = list(knowledge_base[subject]['modules'].keys())
        return jsonify({"modules": modules})
    else:
        return jsonify({"error": "Invalid subject"})


@app.route('/get_submodules', methods=['GET'])
def get_submodules():
    subject = request.args.get('subject')
    module = request.args.get('module')
    knowledge_base = load_knowledge_base()
    if subject not in knowledge_base or module not in knowledge_base[subject]['modules']:
        return jsonify({"error": "Subject or module not found"}), 404

    submodules = list(knowledge_base[subject]['modules'][module].keys())

    return jsonify({"submodules": submodules})


@app.route('/level_test', methods=['GET'])
def level_test():
    subject = request.args.get('subject')

    # Load the incorrect questions from the session data
    incorrect_questions = session.get('incorrect_questions', [])

    # Filter the incorrect questions based on the subject
    incorrect_questions = [q for q in incorrect_questions if q.get('subject') == subject]

    # Select up to 10 incorrect questions
    selected_questions = incorrect_questions[:10]

    return jsonify({"status": "Level test started successfully", "questions": selected_questions})


@app.route('/end_session', methods=['POST'])
def end_session():
    # Save the session data to the username.json file
    with open(f'{session["username"]}.json', 'w') as f:
        json.dump({'incorrect_questions': session['incorrect_questions']}, f)

    # Clear the session data
    session.clear()

    return jsonify({"status": "Session ended successfully"})


@app.route('/get_explanation', methods=['POST'])
def get_explanation():
    data = request.get_json()
    subject = data.get('subject')
    question = data.get('question')
    correctAnswer = data.get('correctAnswer')
    knowledge_base = load_knowledge_base()

    if subject is None or question is None or correctAnswer is None:
        return jsonify({'error': 'Invalid request payload'})
    if question in knowledge_base and 'explanation' in knowledge_base[question]:
        explanation = knowledge_base[question]['explanation']
    else:
        messages = [
            {"role": "system", "content": f"We're discussing {subject}."},
            {"role": "user", "content": f"Explain more the answer to the question '{question}' '{correctAnswer}'?"},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or another engine you have access to
            messages=messages,
            temperature=0.7,  # Adjust temperature and max tokens as per your requirements
            max_tokens=200
        )

        explanation = response['choices'][0]['message']['content'].strip()
        save_knowledge_base1(subject, question, explanation)

        print(explanation)
    return jsonify({
        'explanation': explanation
    })


@app.route('/user_input', methods=['POST'])
def user_input():
    data = request.get_json()
    subject = data.get('subject')
    userInput = data.get('userInput')

    if subject is None or userInput is None:
        return jsonify({'error': 'Invalid request payload'})

    messages = [
        {"role": "system", "content": f"We're discussing {subject}."},
        {"role": "user", "content": userInput},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )

    botResponse = response['choices'][0]['message']['content'].strip()
    print(botResponse)
    return jsonify({
        'botResponse': botResponse
    })


@app.route('/get_more_examples', methods=['POST'])
def get_more_examples():
    data = request.get_json()
    subject = data['subject']
    question = data['question']
    answer = data['answer']
    knowledge_base = load_knowledge_base()
    if question in knowledge_base and 'example' in knowledge_base[question]:
        examples = knowledge_base[question]['example']
    else:
        messages = [
            {"role": "system", "content": f"We're discussing {subject}."},
            {"role": "user",
             "content": f"The question is: {question}. The answer is: {answer}. Can you provide some more examples related to this concept?"},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )

        examples = response['choices'][0]['message']['content'].strip()
        save_knowledge_base1(subject, question, examples)

    return jsonify({'examples': examples})


@app.route('/elaborate_explanation', methods=['POST'])
def elaborate_explanation():
    data = request.get_json()
    subject = data['subject']
    question = data['question']
    answer = data['answer']
    knowledge_base = load_knowledge_base()
    if question in knowledge_base and 'elaborated_explanation' in knowledge_base[question]:
        elaborated_explanation = knowledge_base[question]['elaborated_explanation']
    else:
        messages = [
            {"role": "system", "content": f"We're discussing {subject}."},
            {"role": "user",
             "content": f"The question is: {question}. The answer is: {answer}. Can you explain this concept in a more detailed and easier-to-understand way?"},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )

        elaborated_explanation = response['choices'][0]['message']['content'].strip()
        save_knowledge_base1(subject, question, elaborated_explanation)
        print(elaborated_explanation)
    return jsonify({'elaboration': elaborated_explanation})


if __name__ == '__main__':
    app.run(debug=True)
