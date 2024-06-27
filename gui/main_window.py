import customtkinter as ctk

from logic.alphabet import Alphabet
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
        self.state('zoomed')

        self.main_menu()
        self.scale_size = self.winfo_height() if (self.winfo_height() < self.winfo_width()) else self.winfo_width()

    def main_menu(self):
        # self.bind("<Configure>", change_scale_size)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.update()
        buttonNames = ["Fiszki", "Słowo kodowe", "Znaczenie", "Flagi → Zdanie", "Zdanie → Flagi", "Stwórz zdjęcie"]
        commands = [lambda: self.new_menu(Flashcards),
                    lambda: self.new_menu(Codewords), 
                    lambda: self.new_menu(Meanings), 
                    lambda: self.new_menu(FlagSen), 
                    lambda: self.new_menu(SenFlag),
                    lambda: self.new_menu(MakeImage)]
        self.button = [None] * len(buttonNames)
        for i in range(len(buttonNames)):
            self.button_frame.grid_columnconfigure(i, weight=1)
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], font=ctk.CTkFont(size=int(self.button_frame.winfo_width()*0.013)), command=commands[i])
            self.button[i].grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
            
    def new_menu(self, menu_callback):
        self.button_frame.destroy()
        self.new_frame = menu_callback(self, fg_color="transparent")
        self.new_frame.grid(sticky="nsew")
        self.new_frame.start()