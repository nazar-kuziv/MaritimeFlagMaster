import tksvg


class Flag:
    def __init__(self, letter: str, img: tksvg.SvgImage, meaning: str, mnemonics: str, morse_code: str):
        self.letter = letter
        self.img = img
        self.meaning = meaning
        self.mnemonics = mnemonics
        self.morse_code = morse_code


class FlagMultiple:
    def __init__(self, img: tksvg.SvgImage, meaning: str):
        self.img = img
        self.meaning = meaning
