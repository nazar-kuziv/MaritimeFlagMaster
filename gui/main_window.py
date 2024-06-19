import customtkinter as ctk
from .flashcards import *

class MainWindow(ctk.CTk):
    """Class for initializing the main window
    """
    def __init__(self):
        super().__init__()

        self.title("Maritime Flag Master")
        self.geometry("800x300")

        self.main_menu()

    def main_menu(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.button_frame.grid_rowconfigure(0, weight=1)
        buttonNames = ["Fiszki", "Słowo kodowe", "Znaczenie", "Zdanie"]
        commands = [self.button_flashcards, None, None, None]
        self.button = [None] * 4
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], command=commands[i])
            self.button[i].grid(row=0, column=i, padx=20, pady=20, sticky="ns")
            
    def button_flashcards(self):
        self.button_frame.destroy()
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        self.flashcards_frame = Flashcards(self, fg_color="transparent")
        self.flashcards_frame.grid(sticky="nsew")
        self.flashcards_frame.show_flashcard_front()