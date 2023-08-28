class ScoreTracker:
    def __init__(self):
        self.score = 0

    def correct_answer(self):
        self.score += 1

    def incorrect_answer(self):
        self.score -= 0

    def get_score(self):
        return self.score