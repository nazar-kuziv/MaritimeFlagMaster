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
        return self.flags[self.flag_index]

    def check_answer(self, answer: str) -> bool:
        if self.get_flag().check_code_word(answer):
            self.number_of_correct_answers += 1
            print(f"Correct: {self.number_of_correct_answers}")
            print(f"Questions: {self.number_of_flags}")
            return True
        print(f"Correct: {self.number_of_correct_answers}")
        print(f"Questieightons: {self.number_of_flags}")
        return False

    def next_flag(self):
        self.flag_index += 1
        if self.flag_index >= self.number_of_flags:
            return False
        return True
