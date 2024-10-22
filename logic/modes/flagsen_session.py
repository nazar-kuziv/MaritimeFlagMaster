from logic.alphabet import Alphabet
from logic.flags import FlagSentence
from logic.modes.session import Session


class FlagsenSession(Session):
    def __init__(self, mode: str, number_of_sentences: int = 50):
        """Initializes the FlagsenSession object

        :raise ValueError: If the mode is not 'default', 'internet' or 'file'
        :raise NoFileSelectedException: If the mode is 'file' and the user has not selected a file
        :raise SmthWrongWithFileException: If the mode is 'file' and there is something wrong with the file
        :raise CantLoadDefaultSentencesException: If the mode is 'default' and the default sentences can't be loaded
        :raise NoInternetConnectionException: If the mode is 'internet' and there is no internet connection
        :raise RequestLimitExceededException: If the mode is 'internet' and the request limit has been exceeded

        :param mode: The mode of the session
        :param number_of_sentences: The number of sentences to be used in the session
        """
        if (mode != 'default') and (mode != 'internet') and (mode != 'file'):
            raise ValueError('Invalid mode')

        match mode:
            case 'default':
                Alphabet.load_default_sentences()
                if number_of_sentences > Alphabet.get_number_of_default_sentences():
                    number_of_sentences = Alphabet.get_number_of_default_sentences()
            case 'file':
                Alphabet.load_sentences_from_user_file()
                if number_of_sentences > Alphabet.get_number_of_sentences_from_user_file():
                    number_of_sentences = Alphabet.get_number_of_sentences_from_user_file()

        super().__init__(number_of_sentences)
        self.mode = mode
        self.next_sentence()

    def get_sentence(self) -> FlagSentence:
        """Returns the current sentence"""
        return self.sentence

    def next_sentence(self):
        """Moves to the next sentence. If there are no more sentences, returns False, otherwise returns True.

        :raise NoInternetConnectionException: If the mode is 'internet' and there is no internet connection
        :raise RequestLimitExceededException: If the mode is 'internet' and the request limit has been exceeded
        """
        if self.current_question >= self.number_of_questions:
            return False
        match self.mode:
            case 'default':
                self.sentence = Alphabet.get_default_sentence()
            case 'internet':
                self.sentence = Alphabet.get_flag_sentence_from_api()
            case 'file':
                self.sentence = Alphabet.get_sentence_from_user_file()
        self.current_question += 1
        return True

    def check_answer(self, answer: str) -> bool:
        """Checks the answer and returns True if the answer is correct, otherwise returns False

        :param answer: The answer to be checked
        """
        if self.sentence.check_sentence(answer):
            self.number_of_correct_answers += 1
            return True
        return False

    def get_correct_answer(self) -> str:
        """Returns the correct answers"""
        return self.sentence.cleaned_sentence
