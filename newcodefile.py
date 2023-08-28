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
question_tracker = QuestionTracker.QuestionTracker()
user_id = "5"

def load_knowledge_base():
    try:
        with open('output.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_knowledge_base(knowledge_base):
    with open('output.json', 'w') as f:
        json.dump(knowledge_base, f, indent=4)

def get_user_data(user_id):
    with open('Users.json', 'r') as f:
        users_data = json.load(f)
        for user in users_data['users']:
            if user['UserID'] == user_id:
                return user
        return None # or an appropriate default value if the user is not found
def update_user_data(user_id, updated_data):
    with open('Users.json', 'r') as f:
        users_data = json.load(f)

    for user in users_data['users']:
        if user['UserID'] == user_id:
            user.update(updated_data)
            break

    with open('users.json', 'w') as f:
        json.dump(users_data, f)
def get_user_level(user_id, subject_name):
    # Load the JSON data
    with open('Users.json.json', 'r') as file:
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

def home():
    subjects = ["HTML", "Python", "Machine Learning", "Artificial Intelligence"]
    return render_template('new.html', subjects=subjects)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    data = request.get_json()
    subject = data['subject']
    #username = session['username']  # Assuming you have username in the session

    knowledge_base = load_knowledge_base()

    try:
        with open(f'{username}.json', 'r') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}
        # Initialize the session data
    session['username'] = username
    session['incorrect_questions'] = user_data.get('incorrect_questions', [])

    # if existing_user:
