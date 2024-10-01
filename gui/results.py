import customtkinter as ctk
import gui.util_functions as Util

class Results(Util.AppPage):
    def __init__(self, master: ctk.CTkBaseClass, message: str = "Brawo! Oto twój wynik:", **kwargs):
        super().__init__(master, **kwargs)
        self.message = message

    def draw(self):
        super().draw()

        self.message = ctk.CTkLabel(self, text=self.message, fg_color='transparent')
        self.message.pack(side="top")