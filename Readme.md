
---

# AI Tutor Bot

## Description

AI Tutor Bot is an interactive web application designed to provide personalized quiz sessions and elaborate explanations in various subjects such as HTML, Python, Machine Learning, and Artificial Intelligence. It utilizes OpenAI's GPT-3 to generate questions and explanations, providing an engaging and adaptive learning experience.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Endpoints](#endpoints)
4. [Score Tracking](#score-tracking)
5. [Question Tracking](#question-tracking)
6. [License](#license)

## Installation

Before running the application, you need to install the required dependencies. You can install them using the following command:

```bash
pip install flask openai
```

Make sure to replace the OpenAI API key in the code with your own.

## Usage

Run the application by executing:

```bash
python app.py
```

Access the application through your web browser at:

```
http://localhost:5000
```

## Layout and Styling

The application consists of three main sections:

- **Chatbot Interface:** Allows users to interact with quizzes.
- **Code Editor Section:** A space for writing code.
- **Result Viewer Section:** Displays code results.

The styling is defined in CSS, providing a visually appealing and user-friendly interface.

### JavaScript Interactions

The JavaScript code is an essential part of the AI Tutor Bot, providing dynamic interactions and managing the user experience throughout the quiz. Below are some key functionalities:

#### Starting the Quiz
- **Selecting Subjects, Modules, and Submodules:** Users can choose their desired subject, module, and submodule to begin the quiz. The selections trigger API calls to fetch the corresponding data.
- **User Status Handling:** Depending on whether the user is new or returning, the quiz starts from the appropriate level.

#### Question Generation
- **Fetching Questions:** Based on the selected subject, module, and submodule, questions are dynamically generated and presented to the user.
- **Displaying Options:** Multiple-choice options are displayed, and users can click on their chosen answer.

#### Answer Submission
- **User Choice Handling:** The chosen answer is sent to the server for validation.
- **Correct/Incorrect Feedback:** Users receive immediate feedback on whether their answer is correct or incorrect, along with optional explanations.
- **Achievement Tracking:** Achievements such as correct streaks are tracked and visualized using GIFs.

#### User Input Handling
- **Interactive Learning:** Users can type custom questions or requests for further explanation, which the bot responds to interactively.
- **Speech Integration:** Utilizes the browser's speech synthesis capabilities to audibly read out text.

#### Explanation and Assistance
- **Elaborate Explanations:** For incorrect answers, users can request more detailed explanations or examples.
- **Typewriter Effect:** A typewriter animation is used to make the text appear more interactively.
- **Adaptive Learning:** The bot may ask if the user needs further explanation, providing more detailed responses based on user feedback.

#### Animations and Speech
- **Visual Effects:** Animations and visual cues make the user experience more engaging.
- **Voice Feedback:** Utilizes speech synthesis to provide audible feedback and assistance, enhancing the learning experience.

Together, these JavaScript interactions create a seamless and interactive learning environment, allowing users to engage with quizzes, seek explanations, and learn at their own pace.

## Endpoints

### Home
- **URL:** `/`
- **Method:** `GET`
- **Description:** Renders the homepage, displaying available subjects for the quiz.
- **Response:** HTML page.

### Start Quiz
- **URL:** `/start_quiz`
- **Method:** `POST`
- **Description:** Initiates the quiz session for the selected subject, module, and submodule.
- **Request Parameters:** JSON object containing `subject`, `module`, `submodule`.
- **Response:** JSON object with status.

### Generate Question
- **URL:** `/generate_question`
- **Method:** `GET`
- **Description:** Randomly selects and sends a new question for the quiz.
- **Query Parameters:** `subject`, `modules`, `submodule`.
- **Response:** JSON object containing `question`, `options`, `correctAnswer`.

### Check Answer
- **URL:** `/check_answer`
- **Method:** `POST`
- **Description:** Validates the user's selected answer for a given question.
- **Request Parameters:** JSON object containing `user_choice`, `subject`, `question`, `modules`, `submodule`.
- **Response:** JSON object containing validation result and explanations.

### Get Modules
- **URL:** `/get_modules`
- **Method:** `GET`
- **Description:** Retrieves the modules for the selected subject.
- **Query Parameters:** `subject`.
- **Response:** JSON object containing list of modules.

### Get Submodules
- **URL:** `/get_submodules`
- **Method:** `GET`
- **Description:** Retrieves the submodules for the selected subject and module.
- **Query Parameters:** `subject`, `module`.
- **Response:** JSON object containing list of submodules.

### End Session
- **URL:** `/end_session`
- **Method:** `POST`
- **Description:** Ends the current quiz session and saves the session data.
- **Response:** JSON object with status.

### Get Explanation
- **URL:** `/get_explanation`
- **Method:** `POST`
- **Description:** Provides an explanation for a specific question and answer.
- **Request Parameters:** JSON object containing `subject`, `question`, `correctAnswer`.
- **Response:** JSON object containing the explanation.

### User Input
- **URL:** `/user_input`
- **Method:** `POST`
- **Description:** Processes custom user input for an interactive learning experience.
- **Request Parameters:** JSON object containing `subject`, `userInput`.
- **Response:** JSON object containing the bot's response.

### Get More Examples
- **URL:** `/get_more_examples`
- **Method:** `POST`
- **Description:** Provides additional examples related to a specific concept.
- **Request Parameters:** JSON object containing `subject`, `question`, `answer`.
- **Response:** JSON object containing examples.

### Elaborate Explanation
- **URL:** `/elaborate_explanation`
- **Method:** `POST`
- **Description:** Offers a more detailed and easier-to-understand explanation of a concept.
- **Request Parameters:** JSON object containing `subject`, `question`, `answer`.
- **Response:** JSON object containing the elaborated explanation.


## Score Tracking

The application uses `ScoreTracker` to keep track of the user's score throughout the quiz.

## Question Tracking

`QuestionTracker` is used to manage the questions that have been asked and the incorrect questions to re-ask.

## License

Please refer to the project's license for information on usage rights.

---
