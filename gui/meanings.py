import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet

class Meanings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the meanings screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")

        self.flag_list = Alphabet.get_all_flags()
        # self.flag_list = [Alphabet._characters['C'], Alphabet._characters['B'], Alphabet._characters['A']] # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]

        self.top_menu = ctk.CTkFrame(self)
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.exit_button = ctk.CTkButton(self.top_menu, text="Wyjdź", width=40, command=self.exit, fg_color="orange red")
        self.top_menu.exit_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list = {}

        self.alphabet = Alphabet.get_single_flags_shuffled()[:-10]
        self.flag_images = []
        self.selected_flags = []
        self.flag_index = 0
        self.flag = self.flag_list[0]
        self.images = []
    
    def start(self): self.show_question()
    
    def show_question(self):
        """Make sure to first make the main Meanings frame visible with the place/pack/grid functions
        """
        for widget in self.flag_images:
            widget.destroy()
        self.flag_images = []
        for widget in self.top_menu.list.values():
            widget.destroy()
        self.top_menu.list = {}
        try:
            self.input_frame.destroy()
        except AttributeError: pass
        self.update_idletasks()

        meaning_label = ctk.CTkLabel(self.top_menu, text=self.flag.meaning, width=500, fg_color='transparent', wraplength=int(self.winfo_width()*0.5))
        meaning_label.pack(side="left", padx=10)
        self.top_menu.list["meaning_label"] = meaning_label

        check_button = ctk.CTkButton(self.top_menu, text="Sprawdź", width=30, command=self.check_answer, state="disabled")
        check_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list["check_button"] = check_button

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(side="bottom", fill="both", expand=True)

        self.input_rows = 5
        self.input_columns = 8
        for i in range(self.input_rows):
            self.input_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.input_columns):
            self.input_frame.grid_columnconfigure(j, weight=1)

        # create svgs of flags the first time, after that shuffle both images and alphabet list
        if (len(self.images) == 0):
            for f in self.alphabet:
                self.images.append(tksvg.SvgImage(file=Environment.resource_path(f"graphics/{f.img_path}"), scaletoheight=int(self.winfo_height()*0.8/self.input_columns)))
        else:
            temp = list(zip(self.images, self.alphabet))
            random.shuffle(temp)
            self.images, self.alphabet = zip(*temp)
        
        self.place_input_flags()

    def place_input_flags(self):
        alphabet_index = 0
        for i in range(self.input_rows):
            for j in range(self.input_columns):
                flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                flag_container.grid_rowconfigure(0, weight=1)
                flag_container.grid_columnconfigure(0, weight=1)
                flag_container.grid(row=i, column=j, sticky="nsew")
                flag_container.flag = ctk.CTkLabel(flag_container, text='', image=self.images[alphabet_index], cursor="hand2")
                flag_container.flag.bind("<Button-1>", command=lambda event, i=alphabet_index: self.flag_input_handler(event, index=i))
                flag_container.flag.grid(ipadx=10, ipady=10)
                self.flag_images.append(flag_container)
                
                alphabet_index += 1
                if (alphabet_index == len(self.alphabet)): return

    def flag_input_handler(self, event=None, index: int = -1):
        """Handler function for clicking on flags, 3 max at once. Indices of the selected flags are added to self.selected_flags
        """
        if (index < 0): return
        print(f"{len(self.selected_flags)}, {index}")
        if (index not in self.selected_flags):
            if (len(self.selected_flags) >= 3):
                print("longer than 3")
                return
            self.selected_flags.append(index)
            event.widget.master.configure(fg_color=f"green{5 - len(self.selected_flags)}", text=len(self.selected_flags), font=ctk.CTkFont(size=20, weight='bold'), text_color=f"green{5 - len(self.selected_flags)}")
        else:
            print("removing selection")
            self.selected_flags.remove(index)
            event.widget.master.configure(fg_color="transparent", text="")
            for i, indx in enumerate(self.selected_flags):
                self.flag_images[indx].flag.configure(fg_color=f"green{4 - i}", text=(i+1), text_color=f"green{4 - i}")
        if (len(self.selected_flags) > 0): self.top_menu.list["check_button"].configure(state="normal")
        else: self.top_menu.list["check_button"].configure(state="disabled")

    def check_answer(self):
        print(f"Checking, {self.flag}, {len(self.selected_flags)}")
        print(f"Selected list is {self.selected_flags}")
        if (len(self.selected_flags) == 1):
            print("Flag")
            if (not isinstance(self.flag, Flag)):
                print("Incorrect Flag")
                self.show_answer(False)
                return
            print(self.alphabet[self.selected_flags[0]].meaning)
            if (self.flag.check_flag(self.alphabet[self.selected_flags[0]])):
                print("Correct Flag")
                self.show_answer(True)
            else:
                print("Incorrect Flag")
                self.show_answer(False)
        else:
            print("FlagMultiple")
            if (not isinstance(self.flag, FlagMultiple)):
                print("Incorrect FlagMultiple")
                self.show_answer(False)
                return
            if (self.flag.check_flags([self.alphabet[i] for i in self.selected_flags])):
                print("Correct FlagMultiple")
                self.show_answer(True)
            else:
                print("Incorrect FlagMultiple")
                self.show_answer(False)
    
    def show_answer(self, isCorrect: bool):
        try:
            self.top_menu.list["answer"].destroy()
        except (AttributeError, KeyError) as e: pass
        answer_text = "Correct!" if isCorrect else "Wrong"
        print(answer_text)
        answer = ctk.CTkLabel(self.top_menu, text=answer_text, fg_color='transparent')
        answer.pack(side="left", padx=10)
        self.top_menu.list["answer"] = answer
        
        if (isCorrect):
            self.top_menu.list["check_button"].configure(state="disabled")
            for f in self.flag_images:
                f.flag.unbind("<Button-1>")
                f.flag.configure(cursor='')
            
            self.selected_flags = []
            next_button = ctk.CTkButton(self.top_menu, text='Następny', width=40, command=self.increment_question)
            next_button.pack(side="right", ipadx=10, ipady=10)
            self.top_menu.list["next_button"] = next_button

    def change_question(self, event=None, index: int = 0):
        if (index not in range(0, len(self.flag_list))):
            raise IndexError("Index out of range")
        self.flag_index = index
        self.flag = self.flag_list[index]
        self.show_question()

    def increment_question(self, event=None, number: int = 1):
        """Adjust the flag index by the given number
        """
        self.change_question(index=self.flag_index + number)
    
    def exit(self):
        self.master.main_menu()
        self.destroy()