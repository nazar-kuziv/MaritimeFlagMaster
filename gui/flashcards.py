import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
import gui.util_functions as Util

class Flashcards(ctk.CTkFrame, Util.AppPage):
    def __init__(self, master, **kwargs):
        """Class for initializing the flashcards screen

        To draw the flashcard, call show_flashcard_front or show_flashcard_back AFTER making this frame visible with the place/pack/grid functions
        """
        ctk.CTkFrame.__init__(self, master, **kwargs)
        Util.AppPage.__init__(self, "Flashcards")
        print("Initializing flashcards frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.flag_list = Alphabet.get_all_flags()
        # self.flag_list = random.sample(list(Alphabet._characters.values()), 3) # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]

        # self.exit_button = ctk.CTkButton(self, text="Wyjdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="orange red", command=self.exit)
        # self.exit_button.pack(side="top", anchor="nw", ipadx=10, ipady=10, padx=10, pady=10)

        # self.breadcrumb = Util.BreadcrumbTrail(self)
        # self.breadcrumb.pack(side="top", anchor="nw")

        self.flag_index = 0
        self.create_flashcard(self.flag_list[self.flag_index])

    def start(self):
        self.show_flashcard_front()
        Util.AppPage.start(self)
    
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
                img = tksvg.SvgImage(file=Environment.resource_path(flag.img_path), scaletoheight=int(self.flashcard.winfo_height()*0.9/len(self.flags)))
            else:
                print("height bigger than width")
                img = tksvg.SvgImage(file=Environment.resource_path(flag.img_path), scaletowidth=int(self.flashcard.winfo_width()*0.9/len(self.flags)))
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
        if (isSingleFlag):
            if (any(i in self.flag.code_word for i in
                    ''.join(x for x in Alphabet._additionalFlags.keys())
                    )): text = ""
            else: text = self.flag.code_word
        else:
            text = " ".join([x.code_word for x in self.flag.flags])
        self.flashcard.letter = ctk.CTkLabel(self.flashcard, text=text, font=ctk.CTkFont(size=int(self.master.scale_size*0.035)))
        self.flashcard.letter.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.flashcard.letter.bind("<Button-1>", self.show_flashcard_front)
        if (not isSingleFlag): return

        self.flashcard.morse = ctk.CTkFrame(self.flashcard, fg_color="transparent")
        self.flashcard.morse.grid(column=0, row=2, sticky="w")

        self.flashcard.morse.morse_code = ctk.CTkLabel(self.flashcard.morse, text=self.flag.morse_code, font=ctk.CTkFont(size=int(self.master.scale_size*0.035)))
        self.flashcard.morse.morse_code.pack(side="left", padx=10, pady=10)
        self.flashcard.morse.morse_code.bind("<Button-1>", self.show_flashcard_front)
        if (text == ""): return

        infoicon = tksvg.SvgImage(file=Environment.resource_path("static/graphics/icons/info-icon.svg"), scaletoheight=int(self.master.scale_size*0.05))
        self.flashcard.flag_mnemonic = ctk.CTkLabel(self.flashcard, text='', image=infoicon)
        self.flashcard.flag_mnemonic.grid(row=0, column=0, sticky='ne', padx=10, pady=10)
        CustomTooltipLabel(self.flashcard.flag_mnemonic, text=f"Skojarzenie mnemotechniczne:\n{self.flag.flag_mnemonics}", font=ctk.CTkFont(size=20), hover_delay=200, anchor="e")
        self.flashcard.flag_mnemonic.bind("<Button-1>", self.show_flashcard_front)

        self.flashcard.morse.morse_mnemonic = ctk.CTkLabel(self.flashcard.morse, text='', image=infoicon)
        self.flashcard.morse.morse_mnemonic.pack(side="left")
        CustomTooltipLabel(self.flashcard.morse.morse_mnemonic, text=f"Skojarzenie mnemotechniczne:\n{self.flag.morse_mnemonics}", font=ctk.CTkFont(size=20), hover_delay=200, anchor="e")
        self.flashcard.morse.morse_mnemonic.bind("<Button-1>", self.show_flashcard_front)

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
    
    def exit(self, to_class: Util.AppPage):
        print("exiting flashcards page...")
        new_page = to_class(self.winfo_toplevel(), fg_color="transparent")
        self.destroy()

