class QuestionTracker:
    def __init__(self):
        self.current_question = 0
        self.total_questions = 0

    def set_total_questions(self, total_questions):
        self.total_questions = total_questions

    def increment_question(self):
        self.current_question += 1

    def get_current_question(self):
        return self.current_question

    def get_remaining_questions(self):
        return self.total_questions - self.current_question

    def is_last_question(self):
        return self.current_question == self.total_questions

    def reset(self):
        self.current_question = 0
