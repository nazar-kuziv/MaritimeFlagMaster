import customtkinter as ctk
from typing import Dict, Callable

from .options_menu import OptionsMenu
from .about import AboutWindow
from .flashcards import Flashcards
from .codewords import Codewords
from .meanings import Meanings
from .flagsen import FlagSen
from .senflag import SenFlag
from .makeimage import MakeImage
import gui.util_functions as Util

class MainWindow(ctk.CTk):
    """Class for initializing the main window
    """

    def __init__(self):
        super().__init__()
        # ctk.set_appearance_mode("Dark") # Dark, Light

        self.title("Maritime Flag Master")
        self.geometry("1000x600")
        self.minsize(800, 400)
        # self.state('zoomed')

class MainMenu(Util.AppPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.window = self.winfo_toplevel()

        self.tests_submenu = {
            "buttonNames": ["Słowo kodowe\n\nDopasuj słowo kodowe MKS do flagi", 
            "Znaczenie\n\nDopasuj flagi do komunikatu", 
            "Flagi → Zdanie\n\nPrzetłumacz zestaw flag na tekst", 
            "Zdanie → Flagi\n\nZakoduj komunikat za pomocą flag"],
            "commands": [lambda: Util.new_page(OptionsMenu, "Słowo kodowe", master=self.window, next_page=Codewords), 
            lambda: Util.new_page(OptionsMenu, "Znaczenie", master=self.window, next_page=Meanings), 
            lambda: Util.new_page(OptionsMenu, "Flagi→Zdanie", master=self.window, next_page=FlagSen), 
            lambda: Util.new_page(SenFlag, "Zdanie → Flagi", master=self.window, fg_color="transparent"),]
        }

        self.about_window = None
    
    def draw(self):
        super().draw()
        self.main_menu()
    
    def main_menu(self):
        # self.bind("<Configure>", change_scale_size)
        # print(f"CURRENT WIDTH: {self.winfo_toplevel().winfo_width()}")

        self.title_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.title_frame.pack(pady=(10, 0))
        self.welcome_to = ctk.CTkLabel(self.title_frame, text='Witamy w ', 
                                       font=ctk.CTkFont(size=int(self.winfo_width()*0.022)), fg_color='transparent')
        self.welcome_to.pack(side="left")
        self.maritime_flag_master = ctk.CTkLabel(self.title_frame, text='Maritime Flag Master!', 
                                                 font = ctk.CTkFont(size=int(self.winfo_width()*0.022), weight='bold'), fg_color='transparent')
        self.maritime_flag_master.pack(side="left")

        def open_about_window():
            if self.about_window is None or not self.about_window.winfo_exists():
                self.about_window = AboutWindow(self)  # create window if its None or destroyed
                self.about_window.after(50, self.about_window.lift)
            else:
                self.about_window.focus()
        
        self.about = ctk.CTkButton(self._top_menu, text='O aplikacji', font = ctk.CTkFont(size=int(self.winfo_width()*0.013)), width=0, command=open_about_window)
        self.about.pack(side="right", padx=5)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10,)
        self.button_frame.grid_rowconfigure(0, weight=1)
        buttonNames = ["Nauka\n\nPoznaj flagi i co oznaczają",
                 "Testy\n\nSprawdź się!",
                 "Stwórz zdjęcie\n\nZłóż własny komunikat za pomocą flag"]
        commands = [lambda: Util.new_page(OptionsMenu, "Flashcards", master=self.window, next_page=Flashcards, time_minutes_choices=[-1, 5, 10],  time_minutes_def_ind=0),
                    lambda: Util.new_page(Submenu, "Testy", master=self.window, menu=self.tests_submenu, fg_color="transparent"),
                    lambda: Util.new_page(MakeImage, "Zdjęcie", master=self.window, fg_color="transparent")]
        self.button = [None] * len(buttonNames)
        for i in range(len(buttonNames)):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform="yes")
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], 
                                           font=ctk.CTkFont(size=int(self.winfo_width()*0.02)), command=commands[i])
            self.button[i].grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            self.button[i]._text_label.configure(wraplength=int(self.winfo_width()*0.81/len(buttonNames)))

    def new_page(self, menu_callback):
        # previous_widgets = self.winfo_children()
        self.new_frame = menu_callback(self, fg_color="transparent")
        self.new_frame.lower()
        # for widget in previous_widgets:
        #     widget.destroy()
        self.destroy()
        self.new_frame.pack(fill="both", expand=True)
        self.new_frame.draw()

class Submenu(Util.AppPage):
    def __init__(self, master, menu: Dict[list[str], list[Callable]], **kwargs):
        """
        :param menu: Dictionary with a list "buttonNames" and a list "commands"
        :type menu: Dict[list[str], list[Callable]]
        """
        super().__init__(master, **kwargs)
        self.menu = menu
    
    def draw(self):
        super().draw()
        self.submenu(self.menu["buttonNames"], self.menu["commands"])
    
    def submenu(self, buttonNames: list[str], commands: list):
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10,)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button = [None] * len(buttonNames)
        for i in range(len(buttonNames)):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform="yes")
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], 
                                           font=ctk.CTkFont(size=int(self.winfo_width()*0.02)), command=commands[i])
            self.button[i]._text_label.configure(wraplength=int(self.winfo_width()*0.81/len(buttonNames)))
            self.button[i].grid(row=0, column=i, padx=10, pady=10, sticky="nsew")