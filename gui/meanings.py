import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel
import random
from logic.flags import *
from logic.alphabet import Alphabet

class Meanings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the meanings screen

        To draw the flashcard, call show_flashcard_front or show_flashcard_back AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")

        self.flag_list = [Alphabet._characters['C'], Alphabet._characters['B'], Alphabet._characters['A']] # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]

        self.top_menu = ctk.CTkFrame(self)
        self.top_menu.pack(side="top", anchor="w", padx=10, pady=10)
        self.top_menu.exit_button = ctk.CTkButton(self.top_menu, text="Exit", width=40, command=self.exit)
        self.top_menu.exit_button.pack(side="left", ipadx=10, ipady=10)

        self.flag_images = []
        self.selected_flags = []
        self.flag_index = 0
        self.flag = self.flag_list[0]
    
    def show_question(self):
        """Make sure to first make the main Meanings frame visible with the place/pack/grid functions
        """
        for widget in self.flag_images:
            widget.destroy()
        self.update_idletasks()

        self.top_menu.meaning_label = ctk.CTkLabel(self.top_menu, text=self.flag.meaning, fg_color='transparent', wraplength=int(self.winfo_width()*0.5))
        self.top_menu.meaning_label.pack(side="left", padx=10)

        self.top_menu.check_button = ctk.CTkButton(self.top_menu, text="Check", width=30, command=self.check_answer, state="disabled")
        self.top_menu.check_button.pack(side="left", ipadx=10, ipady=10)

        self.alphabet = list(Alphabet._characters.values())
        random.shuffle(self.alphabet)
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(side="bottom", fill="both", expand=True)

        self.input_rows = 4
        self.input_columns = 7
        for i in range(self.input_rows):
            self.input_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.input_columns):
            self.input_frame.grid_columnconfigure(j, weight=1)
        
        self.place_input_flags()

    def place_input_flags(self):
        alphabet_index = 0
        for i in range(self.input_rows):
            for j in range(self.input_columns):
                flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                flag_container.grid_rowconfigure(0, weight=1)
                flag_container.grid_columnconfigure(0, weight=1)
                flag_container.grid(row=i, column=j, sticky="nsew")
                img = tksvg.SvgImage(file=f"graphics/{self.alphabet[alphabet_index].img_path}", scaletoheight=int(self.winfo_height()*0.8/self.input_columns))
                flag_container.flag = ctk.CTkLabel(flag_container, text='', image=img, cursor="hand2")
                flag_container.flag.bind("<Button-1>", command=lambda event, i=alphabet_index: self.flag_input_handler(event, index=i))
                flag_container.flag.grid(ipadx=10, ipady=10)
                self.flag_images.append(flag_container)
                
                alphabet_index += 1
                if (alphabet_index == 26): return

    def flag_input_handler(self, event=None, index: int = -1):
        if (index < 0): return
        print(f"{len(self.selected_flags)}, {index}")
        if (index not in self.selected_flags):
            if (len(self.selected_flags) >= 3):
                print("longer than 3")
                return
            self.selected_flags.append(index)
            event.widget.master.configure(fg_color="green")
        else:
            print("removing selection")
            self.selected_flags.remove(index)
            event.widget.master.configure(fg_color="transparent")
        if (len(self.selected_flags) > 0): self.top_menu.check_button.configure(state="normal")
        else: self.top_menu.check_button.configure(state="disabled")

    def check_answer(self):
        print("Checking")

    def change_question(self, event=None, index: int = 0):
        if (index not in range(0, len(self.flag_list))):
            raise IndexError("Index out of range")
        self.flag_index = index
        self.show_question()

    def increment_question(self, event=None, number: int = 1):
        """Adjust the flag index by the given number
        """
        self.change_flag_index(index=self.flag_index + number)
    
    def exit(self):
        self.master.main_menu()
        self.destroy()