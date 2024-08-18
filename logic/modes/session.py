class Session:
    def __init__(self, number_of_questions):
        self.number_of_questions = number_of_questions
        self.number_of_correct_answers = 0
        self.current_question = 0
