import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet

class Flashcards(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the flashcards screen

        To draw the flashcard, call show_flashcard_front or show_flashcard_back AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing flashcards frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.flag_list = Alphabet.get_all_flags()
        # self.flag_list = random.sample(list(Alphabet._characters.values()), 3) # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]

        self.exit_button = ctk.CTkButton(self, text="Wyjdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="orange red", command=self.exit)
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
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        
        self.flashcard = ctk.CTkFrame(self, cursor="hand2")
        self.flashcard.place(relx=0.5, rely=0.5, anchor="center", relheight=0.5, relwidth=0.5)

        # next button
        try:
            self.next_button.destroy()
        except AttributeError: pass
        if (self.flag_index < len(self.flag_list)-1):
            self.next_button = ctk.CTkButton(self, text="〉", font=ctk.CTkFont(size=int(self.master.scale_size*0.08), weight="bold"), width=40, command=self.increment_flag_index)
            self.next_button.place(relx=0.98, rely=0.5, anchor="e", relheight=0.2, relwidth=0.1)
        
        # back button
        try:
            self.back_button.destroy()
        except AttributeError: pass
        if (self.flag_index > 0):
            self.back_button = ctk.CTkButton(self, text="〈", font=ctk.CTkFont(size=int(self.master.scale_size*0.08), weight="bold"), width=40, command=lambda: self.increment_flag_index(number=-1))
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
                img = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{flag.img_path}"), scaletoheight=int(self.flashcard.winfo_height()*0.9/len(self.flags)))
            else:
                print("height bigger than width")
                img = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{flag.img_path}"), scaletowidth=int(self.flashcard.winfo_width()*0.9/len(self.flags)))
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

        self.flashcard.rowconfigure(0, weight=1, uniform="yes")
        self.flashcard.rowconfigure(1, weight=3)
        self.flashcard.rowconfigure(2, weight=1, uniform="yes")
        self.flashcard.columnconfigure(0, weight=1)
        print(f"Back flashcard height={self.flashcard.winfo_height()} width={self.flashcard.winfo_width()}")

        self.flashcard.meaning = ctk.CTkLabel(self.flashcard, text=self.flag.meaning, font=ctk.CTkFont(size=int(self.master.scale_size*0.04)), wraplength=int(self.flashcard.winfo_width()*0.75), justify="left")
        self.flashcard.meaning.grid(row=1, column=0, sticky='w', padx=10)
        self.flashcard.meaning.bind("<Button-1>", self.show_flashcard_front)

        isSingleFlag = isinstance(self.flag, Flag)
        if (any(i in self.flag.letter for i in '@<>?')): text = ""
        else: text = self.flag.letter if isSingleFlag else " ".join([x.letter for x in self.flag.flags])
        self.flashcard.letter = ctk.CTkLabel(self.flashcard, text=text, font=ctk.CTkFont(size=int(self.master.scale_size*0.035)))
        self.flashcard.letter.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.flashcard.letter.bind("<Button-1>", self.show_flashcard_front)
        if (not isSingleFlag): return

        self.flashcard.morse_code = ctk.CTkLabel(self.flashcard, text=self.flag.morse_code, font=ctk.CTkFont(size=int(self.master.scale_size*0.035)))
        self.flashcard.morse_code.grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.flashcard.morse_code.bind("<Button-1>", self.show_flashcard_front)
        if (text == ""): return

        infoicon = tksvg.SvgImage(file=Environment.resource_path("graphics/icons/info-icon.svg"), scaletoheight=int(self.master.scale_size*0.05))
        self.flashcard.info_mnemonic = ctk.CTkLabel(self.flashcard, text='', image=infoicon)
        self.flashcard.info_mnemonic.grid(row=0, column=0, sticky='ne', padx=10, pady=10)
        CustomTooltipLabel(self.flashcard.info_mnemonic, text=f"Mnemotechnika:\n{self.flag.mnemonics}", font=ctk.CTkFont(size=20), hover_delay=200, anchor="e")
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

