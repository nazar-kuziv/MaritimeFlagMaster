import customtkinter as ctk
import tksvg

# TEMP FLAG CLASS...
class TEMPFlag():
    # img: str
    # code: str
    # meaning: str
    # mnemonic: str
    # morse: str
    def __init__(self, img="letters/Alfa.svg", code="", meaning="", mnemonic="", morse=""):
        self.img = img
        self.code = code
        self.meaning = meaning
        self.mnemonic = mnemonic
        self.morse = morse

testFlag = TEMPFlag()

class TEMPFlagMultiple():
    # flags: list[str]
    # meaning: str
    def __init__(self, flags=["letters/Alfa.svg"], meaning=""):
        self.flags = flags
        self.meaning = meaning
# ...TEMP FLAG CLASS

class Flashcards(ctk.CTkFrame):
    """Class for initializing flashcards
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing flaschards frame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button_flashcard = ctk.CTkLabel(self, text='Flashcard', width=180, height=140, cursor="hand2")
        self.button_flashcard.grid()
    
    def create_flashcard(self, flag: TEMPFlag | TEMPFlagMultiple):
        """Creates a flashcard widget with the FLAG
        """
        if (isinstance(flag, TEMPFlag)):
            self.flags = [flag.img]
        else:
            self.flags = flag.flags
        self.flashcard.bind("<Button-1>")
        self.flashcard.images = []
        for flag, i in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1)
            img = tksvg.SvgImage(file=flag)
            label = ctk.CTkLabel(self.flashcard, image=img)
            label.grid(row=0, column=i, padx=2, pady=20)

            self.flashcard.images.append(label)
        # self.button_flashcard = ctk.CTkButton(self, image=flag.img, width=180, height=140, command=self.button_callback)
    
    def show_flashcard_base(self):
        self.flashcard = ctk.CTkFrame(self, width=180, height=140, cursor="hand2")
        self.flashcard.grid()
        self.flashcard.grid_rowconfigure(0, weight=1)
    
    def show_flashcard_front(self):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>")
        self.flashcard.images = []
        for flag, i in enumerate(self.flags):
            self.flashcard.grid_columnconfigure(i, weight=1)
            img = tksvg.SvgImage(file=flag)
            label = ctk.CTkLabel(self.flashcard, image=img)
            label.grid(row=0, column=i, padx=2, pady=20)

            self.flashcard.images.append(label)
    
    def show_flashcard_back(self):
        self.show_flashcard_base()
        self.flashcard.bind("<Button-1>")

    def button_callback(self):
        print("button pressed")