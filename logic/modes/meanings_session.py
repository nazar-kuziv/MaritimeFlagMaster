from logic.alphabet import Alphabet
from logic.flags import Flag, FlagMultiple
from logic.modes.session import Session


class MeaningsSession(Session):
    def __init__(self, number_of_flags: int = 65):
        if number_of_flags < 1 or number_of_flags > 65:
            number_of_flags = 65
        super().__init__(number_of_flags)
        self.flags = Alphabet.get_all_flags_with_meaning(number_of_flags)

    def get_flag(self) -> Flag | FlagMultiple:
        """Returns the current flag"""
        return self.flags[self.current_question]

    def check_answer(self, answer: Flag | list[Flag]) -> bool:
        """Checks if the answer is correct and updates the number of correct answers if it is"""
        correct_answer = self.get_flag()
        if isinstance(correct_answer, Flag):
            if isinstance(answer, Flag):
                if correct_answer.check_flag(answer):
                    self.number_of_correct_answers += 1
                    return True
            return False
        elif isinstance(correct_answer, FlagMultiple):
            if isinstance(answer, list):
                if correct_answer.check_flags(answer):
                    self.number_of_correct_answers += 1
                    return True
            return False
        return False

    def next_flag(self):
        """Moves to the next flag"""
        self.current_question += 1
        if self.current_question >= self.number_of_questions:
            return False
        return True

    def get_correct_answer(self) -> Flag | FlagMultiple:
        """Returns the correct answer"""
        return self.get_flag()
