import customtkinter as ctk

from .flashcards import Flashcards
from .codewords import Codewords
from .meanings import Meanings
from .flagsen import FlagSen
from .senflag import SenFlag
from .makeimage import MakeImage
from .util_functions import *

class MainWindow(ctk.CTk):
    """Class for initializing the main window
    """
    def __init__(self):
        super().__init__()

        self.title("Maritime Flag Master")
        self.geometry("1000x500")
        self.minsize(800, 400)
        # self.state('zoomed')

        self.main_menu()
        self.scale_size = self.winfo_height() if (self.winfo_height() < self.winfo_width()) else self.winfo_width()

    def main_menu(self):
        # self.bind("<Configure>", change_scale_size)
        self.update()

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=5)
        # self.grid_columnconfigure(0, weight=1)

        self.title_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.title_frame.pack(pady=(20, 0))
        self.welcome_to = ctk.CTkLabel(self.title_frame, text='Witamy w ', 
                                       font=ctk.CTkFont(size=int(self.winfo_width()*0.017)), fg_color='transparent')
        self.welcome_to.pack(side="left")
        self.maritime_flag_master = ctk.CTkLabel(self.title_frame, text='Maritime Flag Master!', 
                                                 font = ctk.CTkFont(size=int(self.winfo_width()*0.017), weight='bold'), fg_color='transparent')
        self.maritime_flag_master.pack(side="left")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10,)
        self.button_frame.grid_rowconfigure(0, weight=1)
        buttonNames = ["Fiszki\n\nPoznaj flagi i co oznaczają", 
                       "Słowo kodowe\n\nDopasuj słowo kodowe MKS do flagi", 
                       "Znaczenie\n\nDopasuj flagi do komunikatu", 
                       "Flagi → Zdanie\n\nPrzetłumacz zestaw flag na tekst", 
                       "Zdanie → Flagi\n\nZakoduj komunikat za pomocą flag", 
                       "Stwórz zdjęcie\n\nZłóż własny komunikat za pomocą flag"]
        commands = [lambda: self.new_menu(Flashcards),
                    lambda: self.new_menu(Codewords), 
                    lambda: self.new_menu(Meanings), 
                    lambda: self.new_menu(FlagSen), 
                    lambda: self.new_menu(SenFlag),
                    lambda: self.new_menu(MakeImage)]
        self.button = [None] * len(buttonNames)
        for i in range(len(buttonNames)):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform="yes")
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], 
                                           font=ctk.CTkFont(size=int(self.button_frame.winfo_width()*0.013)), command=commands[i])
            self.button[i]._text_label.configure(wraplength=int(self.winfo_width()*0.13))
            self.button[i].grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
    def new_menu(self, menu_callback):
        self.title_frame.destroy()
        self.button_frame.destroy()
        self.new_frame = menu_callback(self, fg_color="transparent")
        self.new_frame.pack(fill="both", expand=True)
        self.new_frame.start()