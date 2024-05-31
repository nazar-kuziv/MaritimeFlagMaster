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
        self.master = master

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
        print(self.master.winfo_width())
        #self.flashcard = ctk.CTkFrame(self, width=self.master.winfo_width()*0.5, height=self.master.winfo_height()*0.5, cursor="hand2")
        self.flashcard = ctk.CTkFrame(self, cursor="hand2")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2, minsize=int(self.master.winfo_height()*0.5))
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2, minsize=int(self.master.winfo_width()*0.5))
        self.grid_columnconfigure(2, weight=1)
        self.flashcard.grid(row=1, column=1, sticky='nsew')

    def show_flashcard_front(self, event=None):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>", self.show_flashcard_back)
        self.flashcard.grid_rowconfigure(0, weight=0)
        self.flashcard.images = []
        for i, flag in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1)
            # img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletowidth=500)
            if (self.flashcard.cget("height") > self.flashcard.cget("width")):
                img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletoheight=int(self.flashcard.cget("height")))
            else:
                img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletowidth=int(self.flashcard.cget("width")))
            label = ctk.CTkLabel(self.flashcard, text='', image=img)
            label.grid(row=0, column=i, padx=2, pady=20)
            label.bind("<Button-1>", self.show_flashcard_back)

            self.flashcard.images.append(label)
        print(f"Flashcard height={self.flashcard.cget("height")} width={self.flashcard.cget("width")}")
    
    def show_flashcard_back(self, event=None):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>", self.show_flashcard_front)

        self.flashcard.rowconfigure(0, weight=1)
        self.flashcard.rowconfigure(1, weight=3)
        self.flashcard.rowconfigure(2, weight=1)
        self.flashcard.columnconfigure(0, weight=1)

        self.flashcard.letter = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].letter)
        self.flashcard.letter.grid(row=0, column=0, sticky='w')
        self.flashcard.letter.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.meaning = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].meaning, wraplength=int(self.master.winfo_width()*0.5), justify="left")
        self.flashcard.meaning.grid(row=1, column=0, sticky='w')
        self.flashcard.meaning.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.morse_code = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].morse_code)
        self.flashcard.morse_code.grid(row=2, column=0, sticky='e')
        self.flashcard.morse_code.bind("<Button-1>", self.show_flashcard_front)

        infoicon = tksvg.SvgImage(file="graphics/icons/info-icon.svg", scaletoheight=int(self.flashcard.letter.cget("height")))
        self.flashcard.info_mnemonic = ctk.CTkLabel(self.flashcard, text='', image=infoicon)
        self.flashcard.info_mnemonic.grid(row=0, column=0, sticky='e')
        self.flashcard.info_mnemonic.bind("<Button-1>", self.show_flashcard_front)
        print(f"Flashcard height={self.flashcard.cget("height")} width={self.flashcard.cget("width")}")

    # def flashcard_front_callback(self):
    #     self.flashcard_callback("front")
    
    # def flaschard_back_callback(self):
    #     self.flashcard_callback("back")