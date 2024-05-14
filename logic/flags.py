from typing import List


class Flag:
    def __init__(self, letter: str, img_path: str, meaning: str, mnemonics: str, morse_code: str):
        self._letter = letter
        self._img_path = img_path
        self._meaning = meaning
        self._mnemonics = mnemonics
        self._morse_code = morse_code

    @property
    def letter(self) -> str:
        return self._letter

    @property
    def img_path(self) -> str:
        return self._img_path

    @property
    def meaning(self) -> str:
        return self._meaning

    @property
    def mnemonics(self) -> str:
        return self._mnemonics

    @property
    def morse_code(self) -> str:
        return self._morse_code

    def check_letter(self, user_letter: str) -> bool:
        """Checks if the letter provided by the user represents this flag

        :param user_letter: Letter from user.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        user_letter = user_letter.strip().upper()
        return user_letter == self._letter.strip().upper()


class FlagMultiple:
    def __init__(self, flags: List[Flag], meaning: str):
        self._flags = flags
        self._meaning = meaning

    @property
    def flags(self) -> List[Flag]:
        return self._flags

    @property
    def meaning(self) -> str:
        return self._meaning


class FlagSentence:
    def __init__(self, flags: List[Flag], original_sentence: str, cleaned_sentence: str):
        self._flags = flags
        self._original_sentence = original_sentence
        self._cleaned_sentence = cleaned_sentence

    @property
    def flags(self) -> List[Flag]:
        return self._flags

    @property
    def original_sentence(self) -> str:
        return self._original_sentence

    @property
    def cleaned_sentence(self) -> str:
        return self._cleaned_sentence

    def check_sentence(self, user_sentence: str) -> bool:
        """Checks if the sentence provided by the user represents this FlagSentence.

        :param user_sentence: Answer to check.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        user_sentence = user_sentence.strip().upper()
        return user_sentence == self._cleaned_sentence