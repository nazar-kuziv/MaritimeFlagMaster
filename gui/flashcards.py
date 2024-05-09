import customtkinter as ctk
import tksvg

# TEMP FLAG CLASS...
class TEMPFlag():
    # img: str
    # code: str
    # meaning: str
    # mnemonic: str
    # morse: str
    def __init__(self, img="letters/Alfa.svg", code="", meaning="", mnemonic="", morse=""):
        self.img = img
        self.code = code
        self.meaning = meaning
        self.mnemonic = mnemonic
        self.morse = morse

testFlag = TEMPFlag()
# ...TEMP FLAG CLASS

class Flashcards(ctk.CTkFrame):
    """Class for initializing flashcards
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing flaschards frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button_flashcard = ctk.CTkButton(self, text='Flashcard', width=180, height=140, command=self.button_callback)
        self.button_flashcard.grid()
    
    def create_flashcard(self, flag: TEMPFlag):
        self.button_flashcard = ctk.CTkButton(self, image=flag.img, width=180, height=140, command=self.button_callback)
        self.button_flashcard.grid()
        
    def button_callback(self):
        print("button pressed")