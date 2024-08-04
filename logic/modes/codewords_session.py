from logic.alphabet import Alphabet
from logic.flags import Flag


class CodewordsSession:
    def __init__(self, number_of_flags: int = 36):
        self.number_of_flags = number_of_flags
        if number_of_flags < 1 or number_of_flags > 36:
            self.number_of_flags = 36
        self.flags = Alphabet.get_characters_flags_shuffled(number_of_flags)
        self.flag_index = 0
        self.number_of_correct_answers = 0

    def get_flag(self) -> Flag:
        """Returns the current flag"""
        return self.flags[self.flag_index]

    def check_answer(self, answer: str) -> bool:
        """Checks if the answer is correct and updates the number of correct answers if it is"""
        if self.get_flag().check_code_word(answer):
            self.number_of_correct_answers += 1
            return True
        return False

    def next_flag(self):
        """Moves to the next flag"""
        self.flag_index += 1
        if self.flag_index >= self.number_of_flags:
            return False
        return True

    def get_correct_answer(self) -> str:
        """Returns the correct answer for the current flag"""
        return self.get_flag().code_word