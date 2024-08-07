import customtkinter as ctk
import tksvg
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from gui.util_functions import *

class Meanings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the meanings screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.flag_list = Alphabet.get_all_flags_with_meaning()
        # self.flag_list = [Alphabet._characters['C'], Alphabet._characters['B'], Alphabet._characters['A']] # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]

        self.top_menu = ctk.CTkFrame(self)
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.grid_columnconfigure(0, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(1, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(2, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(3, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(4, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(5, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(6, weight=1, uniform="yes")

        self.top_menu.exit_button = ctk.CTkButton(self.top_menu, text="Wyjdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="orange red", command=self.exit)
        self.top_menu.exit_button.grid(row=0, column=0, sticky="w", ipadx=10, ipady=10)
        self.top_menu.dict = {}
        self.meaning_frame = None

        self.alphabet = Alphabet.get_single_flags_shuffled()
        self.flag_images = []
        self.selected_flags = []
        self.flag_index = 0
        self.flag = self.flag_list[0]
        self.images = []
    
    def start(self): self.show_question()
    
    def show_question(self):
        """Make sure to first make the main Meanings frame visible with the place/pack/grid functions
        """
        loading_label = loading_widget(self.master)
        for widget in self.flag_images:
            widget.destroy()
        self.flag_images = []
        for widget in self.top_menu.dict.values():
            widget.destroy()
        self.top_menu.dict = {}
        if (self.meaning_frame is not None):
            self.meaning_frame.destroy()
        try:
            self.input_frame.destroy()
        except AttributeError: pass
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.meaning_frame = ctk.CTkFrame(self)
        self.meaning_frame.pack()

        meaning_label = ctk.CTkLabel(self.meaning_frame, text=self.flag.meaning, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.017)), wraplength=int(self.master.winfo_width()*0.8))
        meaning_label.pack(padx=5, pady=5)
        self.top_menu.dict["meaning_label"] = meaning_label

        check_button = ctk.CTkButton(self.top_menu, text="Sprawdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.check_answer, state="disabled")
        check_button.grid(row=0, column=3, ipadx=10, ipady=10)
        self.top_menu.dict["check_button"] = check_button

        clear_button = ctk.CTkButton(self.top_menu, text="Wyczyść", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.clear_checked_flags, state="disabled")
        clear_button.grid(row=0, column=4, ipadx=10, ipady=10)
        self.top_menu.dict["clear_button"] = clear_button

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
                if (self.master.winfo_height() < self.master.winfo_width()):
                    self.images.append(tksvg.SvgImage(file=Environment.resource_path(f.img_path), scaletoheight=int(self.master.scale_size*0.8/self.input_columns)))
                else:
                    self.images.append(tksvg.SvgImage(file=Environment.resource_path(f.img_path), scaletowidth=int(self.master.scale_size*0.8/self.input_columns)))
        else:
            temp = list(zip(self.images, self.alphabet))
            random.shuffle(temp)
            self.images, self.alphabet = zip(*temp)
        
        for f in self.images:
            kwargs = { "scaletoheight":int(self.master.scale_size*0.8/self.input_columns) } if (self.master.winfo_height() < self.master.winfo_width()) else { "scaletowidth":int(self.master.scale_size*0.8/self.input_columns) }
            f.configure(**kwargs)
        self.place_input_flags()
        self.update_idletasks()
        loading_label.destroy()

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
        print(event.widget)
        if (index not in self.selected_flags):
            if (len(self.selected_flags) >= 3):
                print("longer than 3")
                return
            self.selected_flags.append(index)
            event.widget.master.configure(fg_color=f"green{5 - len(self.selected_flags)}", text=len(self.selected_flags), 
                                          font=ctk.CTkFont(size=int(self.master.scale_size*0.03), weight='bold'), text_color=f"green{5 - len(self.selected_flags)}")
        else:
            print("removing selection")
            self.selected_flags.remove(index)
            event.widget.master.configure(fg_color="transparent", text="")
            for i, indx in enumerate(self.selected_flags):
                self.flag_images[indx].flag.configure(fg_color=f"green{4 - i}", text=(i+1), text_color=f"green{4 - i}")
        if (len(self.selected_flags) > 0):
            [ x.configure(state="normal") for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
        else: 
            [ x.configure(state="disabled") for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
        try:
            self.top_menu.dict["answer"].destroy()
        except (AttributeError, KeyError) as e: pass

    def clear_checked_flags(self):
        for index in self.selected_flags:
            print("removing selection")
            self.flag_images[index].flag.configure(fg_color="transparent", text="")
        self.selected_flags.clear()
        [ x.configure(state="disabled") for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
        try:
            self.top_menu.dict["answer"].destroy()
        except (AttributeError, KeyError) as e: pass

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
            self.top_menu.dict["answer"].destroy()
        except (AttributeError, KeyError) as e: pass
        answer_text = "Poprawnie!" if isCorrect else "Źle"
        print(answer_text)
        answer = ctk.CTkLabel(self.top_menu, text=answer_text, font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), fg_color='transparent')
        answer.grid(row=0, column=5, sticky="e", padx=10)
        self.top_menu.dict["answer"] = answer
        
        if (isCorrect):
            [ x.configure(state="disabled") for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
            for f in self.flag_images:
                f.flag.unbind("<Button-1>")
                f.flag.configure(cursor='')
            
            self.selected_flags = []
            next_button = ctk.CTkButton(self.top_menu, text='Następny', font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), command=self.increment_question)
            next_button.grid(row=0, column=6, sticky="nse", ipadx=10)
            self.top_menu.dict["next_button"] = next_button

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