from typing import List

import re


class Flag:
    def __init__(self, code_word: str, img_path: str, meaning: str, flag_mnemonics: str, morse_code: str,
                 morse_mnemonics: str):
        self._code_word = code_word
        self._img_path = img_path
        self._png_img_path = img_path.replace('.svg', '.png')
        self._meaning = meaning
        self._flag_mnemonics = flag_mnemonics
        self._morse_code = morse_code
        self._morse_mnemonics = morse_mnemonics

    @property
    def code_word(self) -> str:
        return self._code_word

    @property
    def img_path(self) -> str:
        return self._img_path

    @property
    def png_img_path(self) -> str:
        return self._png_img_path

    @property
    def meaning(self) -> str:
        return self._meaning

    @property
    def flag_mnemonics(self) -> str:
        return self._flag_mnemonics

    @property
    def morse_code(self) -> str:
        return self._morse_code

    @property
    def morse_mnemonics(self) -> str:
        return self._morse_mnemonics

    def check_code_word(self, user_code_word: str) -> bool:
        """Checks if the code word provided by the user represents this flag

        :param user_code_word: Code word from user.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        user_code_word = user_code_word.strip().upper()
        return user_code_word == self._code_word.strip().upper()

    def check_flag(self, user_flag: 'Flag') -> bool:
        """Checks if the flag provided by the user represents this flag

        :param user_flag: Flag from user.
        :rtype: bool
        :return: True if the answer is correct, False otherwise.
        """
        return user_flag.code_word.strip().capitalize() == self.code_word.strip().capitalize()

    def get_flag_character(self) -> str:
        if self.code_word == 'Nadazero':
            return '0'
        elif self.code_word == 'Unaone':
            return '1'
        elif self.code_word == 'Bissotwo':
            return '2'
        elif self.code_word == 'Terrathree':
            return  '3'
        elif self.code_word == 'Kartefour':
            return '4'
        elif self.code_word == 'Pantafive':
            return '5'
        elif self.code_word == 'Soxisix':
            return '6'
        elif self.code_word == 'Setteseven':
            return '7'
        elif self.code_word == 'Oktoeight':
            return '8'
        elif self.code_word == 'Novenine':
            return '9'
        else :
            return self.code_word[0].upper()


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
        correct_flags_meaning = []
        for flag in self._flags:
            if flag is None:
                correct_flags_meaning.append(None)
            else:
                correct_flags_meaning.append(flag.meaning.strip().capitalize())
        return user_flags_meanings == correct_flags_meaning
