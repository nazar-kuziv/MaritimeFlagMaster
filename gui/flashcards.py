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
    def __init__(self, master, **kwargs):
        """Class for initializing flashcards

        To draw the flashcard, call show_flashcard_front or show_flashcard_back AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing flashcards frame")
        self.master = master

        # self.flag_list = [random.choice(list(Alphabet._characters.values()))] # randomly choose a flag, change later
        self.flag_list = [Alphabet._characters['6']] # randomly choose a flag, change later

        self.create_flashcard(self.flag_list[0])
        # self.create_flashcard(self.flag_list)
    
    def create_flashcard(self, flag: Flag | FlagMultiple):
        """Creates a flashcard object with the FLAG
        """
        print(flag)
        if (isinstance(flag, Flag)):
            self.flags = [flag]
        else:
            self.flags = flag.flags
        # self.show_flashcard_front()
    
    def show_flashcard_base(self):
        self.unbind("<Button-1>")
        try:
            self.flashcard.destroy()
        except AttributeError: pass
        
        self.flashcard = ctk.CTkFrame(self, fg_color="transparent") # not the main frame but required for calculations
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.flashcard = ctk.CTkFrame(self, cursor="hand2")
        # self.flashcard.place(relx=0.5, rely=0.5, anchor="center")#, relheight=0.9, relwidth=0.9)
        self.flashcard.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        print(self.winfo_width())

    def show_flashcard_front(self, event=None):
        """Make sure to first make the main Flashcards frame visible with the place/pack/grid functions (and possibly update the main CTk window)
        """
        self.show_flashcard_base()
        
        self.bind("<Button-1>", self.show_flashcard_back)
        self.flashcard.bind("<Button-1>", self.show_flashcard_back)
        self.flashcard.grid_rowconfigure(0, weight=1, pad=0)
        self.images = []
        for i, flag in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1, pad=0)
            # img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletowidth=500)
            if (self.winfo_height() < self.winfo_width()):
                print("height smaller than width")
                img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletoheight=int(self.winfo_height()*0.9))
            else:
                print("height bigger than width")
                img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletowidth=int(self.winfo_width()*0.9))
            label = ctk.CTkLabel(self.flashcard, text='', image=img)
            label.grid(row=0, column=i, pady=20, sticky="nsew")
            # label.place(relx=0.5, rely=0.5, anchor="center")
            label.bind("<Button-1>", self.show_flashcard_back)

            self.images.append(label)
        print(f"Front flashcard height={self.winfo_height()} width={self.winfo_width()}")
    
    def show_flashcard_back(self, event=None):
        """Make sure to first make the main Flashcards frame visible with the place/pack/grid functions (and possibly update the main CTk window)
        """
        self.show_flashcard_base()
        self.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.bind("<Button-1>", self.show_flashcard_front)

        self.flashcard.rowconfigure(0, weight=1)
        self.flashcard.rowconfigure(1, weight=3)
        self.flashcard.rowconfigure(2, weight=1)
        self.flashcard.columnconfigure(0, weight=1)

        self.flashcard.letter = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].letter)
        self.flashcard.letter.grid(row=0, column=0, sticky='w')
        self.flashcard.letter.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.meaning = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].meaning, wraplength=int(self.master.winfo_width()*0.3), justify="left")
        self.flashcard.meaning.grid(row=1, column=0, sticky='w')
        self.flashcard.meaning.bind("<Button-1>", self.show_flashcard_front)
        self.flashcard.morse_code = ctk.CTkLabel(self.flashcard, text=self.flag_list[0].morse_code)
        self.flashcard.morse_code.grid(row=2, column=0, sticky='e')
        self.flashcard.morse_code.bind("<Button-1>", self.show_flashcard_front)

        infoicon = tksvg.SvgImage(file="graphics/icons/info-icon.svg", scaletoheight=int(self.flashcard.letter.cget("height")))
        self.flashcard.info_mnemonic = ctk.CTkLabel(self.flashcard, text='', image=infoicon)
        self.flashcard.info_mnemonic.grid(row=0, column=0, sticky='e')
        self.flashcard.info_mnemonic.bind("<Button-1>", self.show_flashcard_front)
        print(f"Back flashcard height={self.winfo_height()} width={self.winfo_width()}")

    # def flashcard_front_callback(self):
    #     self.flashcard_callback("front")
    
    # def flaschard_back_callback(self):
    #     self.flashcard_callback("back")