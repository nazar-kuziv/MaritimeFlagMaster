import customtkinter as ctk
import tksvg
import random
from logic.flags import *
from logic.alphabet import Alphabet

# TEMP FLAG CLASS...
# class TEMPFlag():
#     # img: str
#     # code: str
#     # meaning: str
#     # mnemonic: str
#     # morse: str
#     def __init__(self, img="letters/Alfa.svg", code="", meaning="", mnemonic="", morse=""):
#         self.img = img
#         self.code = code
#         self.meaning = meaning
#         self.mnemonic = mnemonic
#         self.morse = morse

testFlag = Alphabet._characters['A']

# class TEMPFlagMultiple():
#     # flags: list[str]
#     # meaning: str
#     def __init__(self, flags=["letters/Alfa.svg"], meaning=""):
#         self.flags = flags
#         self.meaning = meaning
# ...TEMP FLAG CLASS

class Flashcards(ctk.CTkFrame):
    """Class for initializing flashcards
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing flaschards frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.flag_list = [random.choice(list(Alphabet._characters.values()))] # randomly choose a flag, change later

        self.create_flashcard(self.flag_list[0])
    
    def create_flashcard(self, flag: Flag | FlagMultiple):
        """Creates a flashcard widget with the FLAG
        """
        print(flag)
        if (isinstance(flag, Flag)):
            self.flags = [flag]
        else:
            self.flags = flag.flags
        self.show_flashcard_front()
    
    def show_flashcard_base(self):
        try:
            self.flashcard.destroy()
        except AttributeError: pass
        self.flashcard = ctk.CTkFrame(self, width=180, height=140, cursor="hand2")
        self.flashcard.grid()
        self.flashcard.grid_rowconfigure(0, weight=1)
    
    def show_flashcard_front(self, event=None):
        self.show_flashcard_base()
        #self.flashcard.bind("<Button-1>", lambda event: self.flashcard_callback(side="front"))
        self.flashcard.bind("<Button-1>", self.show_flashcard_back)
        self.flashcard.images = []
        for i, flag in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1)
            img = tksvg.SvgImage(file=f"graphics/{flag.img_path}")
            label = ctk.CTkLabel(self.flashcard, image=img, text="")
            label.grid(row=0, column=i, padx=2, pady=20)
            label.bind("<Button-1>", self.show_flashcard_back)

            self.flashcard.images.append(label)
    
    def show_flashcard_back(self, event=None):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>", self.show_flashcard_front)

        self.flashcard.columnconfigure(0, weight=1)
        self.flashcard.columnconfigure(1, weight=1)
        self.flashcard.rowconfigure(0, weight=1)
        self.flashcard.rowconfigure(1, weight=3)
        self.flashcard.rowconfigure(2, weight=1)

        self.flashcard.letter = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].letter, width=40, height=28, fg_color='transparent')
        self.flashcard.letter.grid(row=0, column=0, sticky='w')
        self.flashcard.letter.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.meaning = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].meaning, width=40, height=28, fg_color='transparent')
        self.flashcard.meaning.grid(row=1, column=0, sticky='w')
        self.flashcard.meaning.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.morse_code = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].morse_code, width=40, height=28, fg_color='transparent')
        self.flashcard.morse_code.grid(row=2, column=0, sticky='e')
        self.flashcard.morse_code.bind("<Button-1>", self.show_flashcard_front)

    # def flashcard_front_callback(self):
    #     self.flashcard_callback("front")
    
    # def flaschard_back_callback(self):
    #     self.flashcard_callback("back")