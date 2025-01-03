import customtkinter as ctk
import tksvg
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
import gui.util_functions as Util
from gui.countdown import add_countdown_timer_to_top_menu
from logic.modes.meanings_session import MeaningsSession

class Meanings(Util.AppQuizPage, Util.ISkippablePage):
    def __init__(self, master, questions_number: int = 0, time_minutes: int = 0, **kwargs):
        """Class for initializing the meanings screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.questions_number = questions_number
        self.time_minutes = time_minutes
        print(f"Questions number: {questions_number}, time: {time_minutes}")
        self.session = MeaningsSession(questions_number) if questions_number > 0 else MeaningsSession()

        # self.flag_list = [Alphabet._characters['C'], Alphabet._characters['B'], Alphabet._characters['A']] # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['6']]
        # self.flag_list = [Alphabet._allFlags[7]]
        self.meaning_frame = None

        self.alphabet = Alphabet.get_single_flags_shuffled()
        self.flag_images = []
        self.selected_flags = []
        self.images = []
    
    def draw(self):
        super().draw()

        if (self.time_minutes > 0):
            self.countdown = add_countdown_timer_to_top_menu(self, self.time_minutes)

        self.top_menu = ctk.CTkFrame(self)
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.grid_columnconfigure(0, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(1, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(2, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(3, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(4, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(5, weight=1, uniform="yes")
        self.top_menu.grid_columnconfigure(6, weight=1, uniform="yes")
        self.top_menu.dict = {}
        
        self.next_question()
    
    def show_question(self):
        """Make sure to first make the main Meanings frame visible with the place/pack/grid functions
        """
        loading_label = Util.loading_widget(self.winfo_toplevel())

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

        check_button = ctk.CTkButton(self.top_menu, text="Sprawdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.check_answer)
        check_button.grid(row=0, column=3, ipadx=10, ipady=10)
        self.top_menu.dict["check_button"] = check_button
        
        answer = ctk.CTkLabel(self.top_menu, text='', font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), fg_color='transparent')
        answer.grid(row=0, column=5, sticky="e", padx=10)
        self.top_menu.dict["answer"] = answer

        clear_button = ctk.CTkButton(self.top_menu, text="Wyczyść", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.clear_checked_flags)
        clear_button.grid(row=0, column=0, sticky="w", ipadx=10, ipady=10)
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

        self.top_menu.dict["skip"] = self.add_skip_button(self.skip_command)

        self.update_idletasks()
        try:
            self.countdown.startCountdown()
        except AttributeError: pass
        loading_label.destroy()

    def skip_command(self):
        self.top_menu.dict["skip"].configure(command=None)
        self.clear_checked_flags()
        correct_flags = [self.session.get_correct_answer()]
        if (isinstance(correct_flags[0], FlagMultiple)):
            correct_flags = correct_flags[0].flags
        for flag in correct_flags:
            flag_index = -1
            for i, x in enumerate(self.alphabet):
                if (x.code_word == flag.code_word):
                    flag_index = i
                    break
            
            label = self.flag_images[flag_index].flag
            label.children['!ctkcanvas'].event_generate("<Button-1>")
        
        print("Skipped.")
        self.top_menu.dict["answer"].configure(text='Pominięto.')
        self.show_next_button()

    def place_input_flags(self):
        alphabet_index = 0
        for i in range(self.input_rows):
            for j in range(self.input_columns):
                flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                flag_container.grid_rowconfigure(0, weight=1)
                flag_container.grid_columnconfigure(0, weight=1)
                flag_container.grid(row=i, column=j, sticky="nsew")
                flag_container.flag = ctk.CTkLabel(flag_container, text='', 
                                          font=ctk.CTkFont(size=int(self.master.scale_size*0.033), weight='bold'), image=self.images[alphabet_index], cursor="hand2")
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
        print(self.alphabet[index].code_word)
        if (index not in self.selected_flags):
            if (len(self.selected_flags) >= 3):
                print("longer than 3")
                return
            self.selected_flags.append(index)
            event.widget.master.configure(fg_color=f"green{1 + len(self.selected_flags)}", text=len(self.selected_flags), text_color=f"green{1 + len(self.selected_flags)}")
        else:
            print("removing selection")
            self.selected_flags.remove(index)
            event.widget.master.configure(fg_color="transparent", text="")
            for i, indx in enumerate(self.selected_flags):
                self.flag_images[indx].flag.configure(fg_color=f"green{i}", text=(i+1), text_color=f"green{i}")
        # if (len(self.selected_flags) > 0):
        #     self.top_menu.dict["clear_button"].configure(command=self.clear_checked_flags)
        #     self.update()
        #     self.top_menu.dict["check_button"].configure(command=self.check_answer)
        # else: 
        #     [ x.configure(command=None) for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
        self.top_menu.dict["answer"].configure(text='')

    def clear_checked_flags(self):
        if (len(self.selected_flags) <= 0): return
        for index in self.selected_flags:
            print("removing selection")
            self.flag_images[index].flag.configure(fg_color="transparent", text="")
        self.selected_flags.clear()
        [ x.configure(command=None) for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
        self.top_menu.dict["answer"].configure(text='')

    def check_answer(self):
        if (len(self.selected_flags) == 0): return
        print(f"Checking, {self.flag}, {len(self.selected_flags)}")
        print(f"Selected list is {self.selected_flags}")

        if (len(self.selected_flags) > 3):
            self.show_answer(False)
            return
        elif (len(self.selected_flags) == 1):
            self.show_answer(self.session.check_answer(self.alphabet[self.selected_flags[0]]))
        else:
            self.show_answer(self.session.check_answer([self.alphabet[i] for i in self.selected_flags]))
    
    def show_answer(self, isCorrect: bool):
        # try:
        #     self.top_menu.dict["answer"].destroy()
        # except (AttributeError, KeyError) as e: pass
        answer_text = "Poprawnie!" if isCorrect else "Źle"
        self.top_menu.dict["answer"].configure(text=answer_text)
        print(answer_text)
        
        if (not isCorrect): return
        
        self.skip_button.configure(command=None)
        self.show_next_button()

    def show_next_button(self):
        [ x.configure(command=None) for x in list(map(self.top_menu.dict.get, ["check_button", "clear_button"]))]
        for f in self.flag_images:
            f.flag.unbind("<Button-1>")
            f.flag.configure(cursor='')
        
        next_exists = self.session.next_question()
        next_command = self.next_question if next_exists else self.finish
        next_text = "Następny" if next_exists else "Wyniki"
        if (not next_exists):
            try:
                self.countdown.pause()
            except AttributeError: pass

        next_button = ctk.CTkButton(self.top_menu, text=next_text, font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), command=next_command)
        next_button.grid(row=0, column=6, sticky="nse", ipadx=10)
        self.top_menu.dict["next_button"] = next_button

    def next_question(self):
        self.selected_flags = []
        self.flag = self.session.get_question()
        self.show_question()
