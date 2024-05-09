from typing import List


class Flag:
    def __init__(self, letter: str, img_path: str, meaning: str, mnemonics: str, morse_code: str):
        self.letter = letter
        self.img_path = img_path
        self.meaning = meaning
        self.mnemonics = mnemonics
        self.morse_code = morse_code


class FlagMultiple:
    def __init__(self, flags: List[Flag], meaning: str):
        self.flags = flags
        self.meaning = meaning
