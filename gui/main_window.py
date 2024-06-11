import customtkinter as ctk
from .flashcards import *

class MainWindow(ctk.CTk):
    """Class for initializing the main window
    """
    def __init__(self):
        super().__init__()

        self.title("Maritime Flag Master")
        self.geometry("800x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.button_frame.grid_rowconfigure(0, weight=1)

        buttonNames = ["Fiszki", "Słowo kodowe", "Znaczenie", "Zdanie"]
        self.button = [None] * 4
        for x in range(4):
            self.button_frame.grid_columnconfigure(x, weight=1)
            self.button[x] = ctk.CTkButton(self.button_frame, text=buttonNames[x], command=self.button_flashcards)
            self.button[x].grid(row=0, column=x, padx=20, pady=20, sticky="ns")
        
    def button_callback(self):
        print("button pressed")

    def button_flashcards(self):
        self.button_frame.destroy()
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        self.flashcards_frame = Flashcards(self, cursor="hand2")
        self.flashcards_frame.place(relx=0.5, rely=0.5, anchor="center", relheight=0.5, relwidth=0.5)
        self.update()
        self.flashcards_frame.show_flashcard_front()