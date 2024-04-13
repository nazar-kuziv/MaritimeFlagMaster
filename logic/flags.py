from PIL import Image


class Flag:
    def __init__(self, letter: str, img: Image, meaning: str, mnemonics: str, morse_code: Image):
        self.letter = letter
        self.img = img
        self.meaning = meaning
        self.mnemonics = mnemonics
        self.morse_code = morse_code


class FlagMultiple:
    def __init__(self, img: Image, meaning: str):
        self.img = img
        self.meaning = meaning
