import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel
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

# class TEMPFlagMultiple():
#     # flags: list[str]
#     # meaning: str
#     def __init__(self, flags=["letters/Alfa.svg"], meaning=""):
#         self.flags = flags
#         self.meaning = meaning
# ...TEMP FLAG CLASS

class Flashcards(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the flashcards screen

        To draw the flashcard, call show_flashcard_front or show_flashcard_back AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing flashcards frame")

        self.flag_list = Alphabet.get_all_flags()
        # self.flag_list = random.sample(list(Alphabet._characters.values()), 3) # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]

        self.exit_button = ctk.CTkButton(self, text="Wyjdź", width=40, command=self.exit)
        self.exit_button.pack(side="top", anchor="nw", ipadx=10, ipady=10, padx=10, pady=10)

        self.flag_index = 0
        self.create_flashcard(self.flag_list[self.flag_index])

    def start(self): self.show_flashcard_front()
    
    def create_flashcard(self, flag: Flag | FlagMultiple):
        """Creates a flashcard with the FLAG
        """
        self.flag = flag
        if (isinstance(flag, Flag)):
            self.flags = [flag]
        else:
            self.flags = flag.flags
    
    def show_flashcard_base(self):
        try:
            self.flashcard.destroy()
        except AttributeError: pass
        
        self.flashcard = ctk.CTkFrame(self, cursor="hand2")
        self.flashcard.place(relx=0.5, rely=0.5, anchor="center", relheight=0.5, relwidth=0.5)

        # next button
        try:
            self.next_button.destroy()
        except AttributeError: pass
        if (self.flag_index < len(self.flag_list)-1):
            self.next_button = ctk.CTkButton(self, text="〉", font=ctk.CTkFont(size=30), width=40, command=self.increment_flag_index)
            self.next_button.place(relx=0.98, rely=0.5, anchor="e", relheight=0.2, relwidth=0.1)
        
        # back button
        try:
            self.back_button.destroy()
        except AttributeError: pass
        if (self.flag_index > 0):
            self.back_button = ctk.CTkButton(self, text="〈", font=ctk.CTkFont(size=30), width=40, command=lambda: self.increment_flag_index(number=-1))
            self.back_button.place(relx=0.02, rely=0.5, anchor="w", relheight=0.2, relwidth=0.1)

        self.update_idletasks()

    def show_flashcard_front(self, event=None):
        """Make sure to first make the main Flashcards frame visible with the place/pack/grid functions
        """
        self.show_flashcard_base()
        
        self.flashcard.bind("<Button-1>", self.show_flashcard_back)
        self.flashcard.grid_rowconfigure(0, weight=1)
        self.images = []
        for i, flag in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1)
            if (self.flashcard.winfo_height() < self.flashcard.winfo_width() * len(self.flags)):
                print("height smaller than width")
                img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletoheight=int(self.flashcard.winfo_height()*0.9/len(self.flags)))
            else:
                print("height bigger than width")
                img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletowidth=int(self.flashcard.winfo_width()*0.9/len(self.flags)))
            label = ctk.CTkLabel(self.flashcard, text='', image=img)
            label.grid(row=0, column=i, sticky="nsew")
            label.bind("<Button-1>", self.show_flashcard_back)

            self.images.append(label)
        print(f"Front flashcard height={self.flashcard.winfo_height()} width={self.flashcard.winfo_width()}")
    
    def show_flashcard_back(self, event=None):
        """Make sure to first make the main Flashcards frame visible with the place/pack/grid functions
        """
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>", self.show_flashcard_front)

        self.flashcard.rowconfigure(0, weight=1)
        self.flashcard.rowconfigure(1, weight=3)
        self.flashcard.rowconfigure(2, weight=1)
        self.flashcard.columnconfigure(0, weight=1)
        print(f"Back flashcard height={self.flashcard.winfo_height()} width={self.flashcard.winfo_width()}")

        self.flashcard.meaning = ctk.CTkLabel(self.flashcard, text=self.flag.meaning, wraplength=int(self.flashcard.winfo_width()*0.75), justify="left")
        self.flashcard.meaning.grid(row=1, column=0, sticky='w', padx=10)
        self.flashcard.meaning.bind("<Button-1>", self.show_flashcard_front)

        isSingleFlag = isinstance(self.flag, Flag)
        text = self.flag.letter if isSingleFlag else " ".join([x.letter for x in self.flag.flags])
        self.flashcard.letter = ctk.CTkLabel(self.flashcard, text=text)
        self.flashcard.letter.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.flashcard.letter.bind("<Button-1>", self.show_flashcard_front)
        if (not isSingleFlag): return

        self.flashcard.morse_code = ctk.CTkLabel(self.flashcard, text=self.flag.morse_code)
        self.flashcard.morse_code.grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.flashcard.morse_code.bind("<Button-1>", self.show_flashcard_front)
        if (text == ""): return

        infoicon = tksvg.SvgImage(file="graphics/icons/info-icon.svg", scaletoheight=int(self.flashcard.letter.cget("height")))
        self.flashcard.info_mnemonic = ctk.CTkLabel(self.flashcard, text='', image=infoicon)
        self.flashcard.info_mnemonic.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        CustomTooltipLabel(self.flashcard.info_mnemonic, text=self.flag.mnemonics, font=ctk.CTkFont(size=16), hover_delay=200, anchor="e")
        self.flashcard.info_mnemonic.bind("<Button-1>", self.show_flashcard_front)

    def change_flag_index(self, index: int = 0):
        if (index not in range(0, len(self.flag_list))):
            raise IndexError("Index out of range")
        self.flag_index = index
        self.create_flashcard(self.flag_list[self.flag_index])
        self.show_flashcard_front()

    def increment_flag_index(self, number: int = 1):
        """Adjust the flag index by the given number
        """
        self.change_flag_index(index=self.flag_index + number)
    
    def exit(self):
        self.master.main_menu()
        self.destroy()