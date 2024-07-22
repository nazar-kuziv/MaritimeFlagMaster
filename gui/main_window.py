import customtkinter as ctk

from .about import AboutWindow
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
        # ctk.set_appearance_mode("Dark") # Dark, Light

        self.title("Maritime Flag Master")
        self.geometry("1000x600")
        self.minsize(800, 400)
        # self.state('zoomed')

        self.main_menu()
        self.scale_size = self.winfo_height() if (self.winfo_height() < self.winfo_width()) else self.winfo_width()

        self.about_window = None

        self.tests_submenu = {
            "buttonNames": ["Słowo kodowe\n\nDopasuj słowo kodowe MKS do flagi", 
            "Znaczenie\n\nDopasuj flagi do komunikatu", 
            "Flagi → Zdanie\n\nPrzetłumacz zestaw flag na tekst", 
            "Zdanie → Flagi\n\nZakoduj komunikat za pomocą flag"],
            "commands": [lambda: self.new_menu(Codewords), 
            lambda: self.new_menu(Meanings), 
            lambda: self.new_menu(FlagSen), 
            lambda: self.new_menu(SenFlag),]
        }
    
    def main_menu(self):
        # self.bind("<Configure>", change_scale_size)
        previous_widgets = self.winfo_children()
        self.update()

        self.breadcrumb = BreadcrumbTrail(self,
            page_names=["Start"],
            page_functions=[None]
        )
        self.breadcrumb.pack(anchor="nw")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.lower()
        self.main_frame.place(relwidth=1, relheight=1)

        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.title_frame.pack(pady=(20, 0))
        self.welcome_to = ctk.CTkLabel(self.title_frame, text='Witamy w ', 
                                       font=ctk.CTkFont(size=int(self.winfo_width()*0.017)), fg_color='transparent')
        self.welcome_to.pack(side="left")
        self.maritime_flag_master = ctk.CTkLabel(self.title_frame, text='Maritime Flag Master!', 
                                                 font = ctk.CTkFont(size=int(self.winfo_width()*0.017), weight='bold'), fg_color='transparent')
        self.maritime_flag_master.pack(side="left")

        def open_about_window():
            if self.about_window is None or not self.about_window.winfo_exists():
                self.about_window = AboutWindow(self)  # create window if its None or destroyed
                self.about_window.after(50, self.about_window.lift)
            else:
                self.about_window.focus()
        
        self.about = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.about.place(anchor="ne", rely=0, relx=1)
        self.about.button = ctk.CTkButton(self.about, text='O aplikacji', font = ctk.CTkFont(size=int(self.winfo_width()*0.013)), width=0, command=open_about_window)
        self.about.button.pack(padx=5)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10,)
        self.button_frame.grid_rowconfigure(0, weight=1)
        buttonNames = ["Nauka\n\nPoznaj flagi i co oznaczają",
                 "Testy\n\nSprawdź się!",
                 "Stwórz zdjęcie\n\nZłóż własny komunikat za pomocą flag"]
        commands = [lambda: self.new_menu(Flashcards),
                    lambda: self.submenu(**self.tests_submenu),
                    lambda: self.new_menu(MakeImage)]
        self.button = [None] * len(buttonNames)
        for i in range(len(buttonNames)):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform="yes")
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], 
                                           font=ctk.CTkFont(size=int(self.button_frame.winfo_width()*0.013)), command=commands[i])
            self.button[i]._text_label.configure(wraplength=int(self.winfo_width()*0.13))
            self.button[i].grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        self.update()
        for widget in previous_widgets:
            widget.destroy()

    def submenu(self, buttonNames: list[str], commands: list):

        self.sub_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sub_frame.lower(self.main_frame)
        self.sub_frame.place(relwidth=1, relheight=1)

        self.exit_button = ctk.CTkButton(self.sub_frame, text="Wróć", width=0, font=ctk.CTkFont(size=int(self.winfo_width()*0.015)), fg_color="orange red", command=self.main_menu)
        self.exit_button.pack(side="top", anchor="nw", ipadx=10, ipady=10, padx=10, pady=(10, 0))

        self.button_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, padx=10, pady=10,)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button = [None] * len(buttonNames)
        for i in range(len(buttonNames)):
            self.button_frame.grid_columnconfigure(i, weight=1, uniform="yes")
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], 
                                           font=ctk.CTkFont(size=int(self.button_frame.winfo_width()*0.013)), command=commands[i])
            self.button[i]._text_label.configure(wraplength=int(self.winfo_width()*0.13))
            self.button[i].grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        self.update()
        self.main_frame.destroy()

    def new_menu(self, menu_callback):
        previous_widgets = self.winfo_children()
        self.new_frame = menu_callback(self, fg_color="transparent")
        self.new_frame.lower()
        self.new_frame.pack(fill="both", expand=True)
        self.new_frame.start()
        self.update()
        for widget in previous_widgets:
            widget.destroy()