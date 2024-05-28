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

        # self.button_flashcard = ctk.CTkLabel(self, text='Flashcard', width=180, height=140, cursor="hand2")
        # self.button_flashcard.grid()
    
    def create_flashcard(self, flag: Flag | FlagMultiple):
        """Creates a flashcard widget with the FLAG
        """
        print(flag)
        if (isinstance(flag, Flag)):
            self.flags = [flag]
        else:
            self.flags = flag.flags
        self.show_flashcard_front()
        # self.flashcard.bind("<Button-1>")
        # self.flashcard.images = []
        # for i, flag in enumerate(self.flags):
        #     self.flashcard.grid_columnconfigure(i, weight=1)
        #     img = tksvg.SvgImage(file=flag.img_path)
        #     label = ctk.CTkLabel(self.flashcard, image=img)
        #     label.grid(row=0, column=i, padx=2, pady=20)

        #     self.flashcard.images.append(label)
        # self.button_flashcard = ctk.CTkButton(self, image=flag.img, width=180, height=140, command=self.button_callback)
    
    def show_flashcard_base(self):
        self.flashcard = ctk.CTkFrame(self, width=180, height=140, cursor="hand2")
        self.flashcard.grid()
        self.flashcard.grid_rowconfigure(0, weight=1)
    
    def show_flashcard_front(self):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>", lambda event: self.flashcard_callback(side="front"))
        self.flashcard.images = []
        for i, flag in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1)
            img = tksvg.SvgImage(file=f"graphics/{flag.img_path}")
            label = ctk.CTkLabel(self.flashcard, image=img)
            label.grid(row=0, column=i, padx=2, pady=20)

            self.flashcard.images.append(label)
    
    def show_flashcard_back(self):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>", lambda event: self.flashcard_callback(side="back"))
    
    def flashcard_callback(self, side: str):
        """Callback function for clicking on the flashcard

        :param side: values - "front", "back"
        :type side: str
        """
        print("button pressed")

    # def flashcard_front_callback(self):
    #     self.flashcard_callback("front")
    
    # def flaschard_back_callback(self):
    #     self.flashcard_callback("back")