from typing import List

import re


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

    def check_flag(self, user_flag: 'Flag') -> bool:
        """Checks if the flag provided by the user represents this flag

        :param user_flag: Flag from user.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        return user_flag.letter.strip().capitalize() == self._letter.strip().capitalize()


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

    def check_flags(self, user_flags: List[Flag]) -> bool:
        """Checks if the flags provided by the user represent this FlagMultiple.

        :param user_flags: List of flags from user.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        user_flags = [flag.meaning.strip().capitalize() for flag in user_flags]
        correct_flags = [flag.meaning.strip().capitalize() for flag in self._flags]
        return user_flags == correct_flags


class FlagSentence:
    def __init__(self, flags: List[Flag | None], original_sentence: str, cleaned_sentence: str):
        self._flags = flags
        self._original_sentence = original_sentence
        self._cleaned_sentence = cleaned_sentence

    @property
    def flags(self) -> List[Flag | None]:
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
        user_cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', user_sentence).upper().strip()
        return user_cleaned_sentence == self._cleaned_sentence

    def check_flags(self, user_flags: List[Flag | None]) -> bool:
        """Checks if the flags provided by the user represent this FlagSentence.

        :param user_flags: List of flags from user.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        user_flags_meanings = []
        for flag in user_flags:
            if flag is None:
                user_flags_meanings.append(None)
            else:
                user_flags_meanings.append(flag.meaning.strip().capitalize())
        correct_flags_meaning =[]
        for flag in self._flags:
            if flag is None:
                correct_flags_meaning.append(None)
            else:
                correct_flags_meaning.append(flag.meaning.strip().capitalize())
        return user_flags_meanings == correct_flags_meaning
