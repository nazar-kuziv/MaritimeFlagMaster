import customtkinter as ctk
from .flashcards import Flashcards
from .codewords import Codewords
from .meanings import Meanings

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
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.button_frame.grid_rowconfigure(0, weight=1)
        buttonNames = ["Fiszki", "Słowo kodowe", "Znaczenie", "Zdanie"]
        commands = [self.flashcards, self.codewords, self.meanings, None]
        self.button = [None] * 4
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
            self.button[i] = ctk.CTkButton(self.button_frame, text=buttonNames[i], command=commands[i])
            self.button[i].grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
            
    def flashcards(self):
        self.button_frame.destroy()
        self.flashcards_frame = Flashcards(self, fg_color="transparent")
        self.flashcards_frame.grid(sticky="nsew")
        self.flashcards_frame.show_flashcard_front()

    def codewords(self):
        self.button_frame.destroy()
        self.codewords_frame = Codewords(self, fg_color="transparent")
        self.codewords_frame.grid(sticky="nsew")
        self.codewords_frame.show_question()

    def meanings(self):
        self.button_frame.destroy()
        self.meanings_frame = Meanings(self, fg_color="transparent")
        self.meanings_frame.grid(sticky="nsew")
        self.meanings_frame.show_question()