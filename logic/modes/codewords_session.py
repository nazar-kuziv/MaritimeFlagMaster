from logic.alphabet import Alphabet
from logic.flags import Flag
from logic.modes.session import Session


class CodewordsSession(Session):
    def __init__(self, number_of_flags: int = 36):
        if number_of_flags < 1 or number_of_flags > 36:
            number_of_flags = 36
        super().__init__(number_of_flags)
        self.flags = Alphabet.get_characters_flags_shuffled(number_of_flags)

    def get_flag(self) -> Flag:
        """Returns the current flag"""
        return self.flags[self.current_question]

    def check_answer(self, answer: str) -> bool:
        """Checks if the answer is correct and updates the number of correct answers if it is"""
        if self.get_flag().check_code_word(answer):
            self.number_of_correct_answers += 1
            return True
        return False

    def next_flag(self):
        """Moves to the next flag"""
        self.current_question += 1
        if self.current_question >= self.number_of_questions:
            return False
        return True

    def get_correct_answer(self) -> str:
        """Returns the correct answer for the current flag"""
        return self.get_flag().code_word
