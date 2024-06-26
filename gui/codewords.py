import customtkinter as ctk
import tksvg
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet

class Codewords(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the codewords screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing codewords frame")

        # self.flag_list = random.sample(list(Alphabet._characters.values()), 3) # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['A'], Alphabet._characters['B'], Alphabet._characters['C']] # randomly choose a flag, change later
        self.flag_list = Alphabet.get_characters_flags_shuffled()
        
        self.question_widgets = []
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="side")
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1, uniform="side")

        self.exit_button = ctk.CTkButton(self, text="Wyjdź", width=40, height=20, command=self.exit)
        self.exit_button.grid(row=0, column=0, sticky="nw", ipadx=10, ipady=10, padx=10, pady=10)

        self.flag_index = 0
        self.flag = self.flag_list[0]
    
    def start(self): self.show_question()

    def show_question(self):
        """Make sure to first make the main Codewords frame visible with the place/pack/grid functions
        """
        for widget in self.question_widgets:
            widget.destroy()
        self.update_idletasks()
        
        img = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{self.flag.img_path}"), scaletoheight=int(self.winfo_height()*0.5))
        self.image = ctk.CTkLabel(self, text='', image=img)
        self.image.grid(row=1, column=0, columnspan=3, sticky="n")
        self.question_widgets.append(self.image)

        self.answer_cell = ctk.CTkFrame(self, fg_color="transparent")
        self.answer_cell.grid(row=2, column=1, pady=10)
        self.question_widgets.append(self.answer_cell)

        validate_command = self.register(self.validate_answer)
        self.answer_cell.entry = ctk.CTkEntry(self.answer_cell, justify="center", validate="key", validatecommand=(validate_command, '%d', '%P', '%S'))
        self.answer_cell.entry.bind("<Return>", self.enter_answer)
        self.answer_cell.entry.pack(side="left")
        self.answer_cell.entry.focus()
        
        self.answer_cell.submit_button = ctk.CTkButton(self.answer_cell, text='Enter', width=0, command=self.enter_answer)
        self.answer_cell.submit_button.pack(side="left", padx=5)

    def validate_answer(self, action, new_text, new_character):
        # print(f'Validating answer, {new_character} for {new_text} with action {action}.')
        # if (len(new_text) > 1):
        #     return False
        # elif (action == '1'):
        #     # print("changing answer")
        #     self.answer_cell.entry.delete(0, 'end')
        #     self.answer_cell.entry.insert(0, new_text.upper())
        #     # after changing text of the Entry widget during validation, the validate function changes to None so you have to change it back to 'key' through this function
        #     self.after_idle(lambda: self.answer_cell.entry.configure(validate="key"))
        return True

    def enter_answer(self, event=None):
        try:
            self.answer_response.destroy()
        except AttributeError: pass
        # correct_answer = self.flag.letter[0].upper()
        
        if (not self.flag.check_letter(self.answer_cell.entry.get())):
            print("Wrong answer.")
            self.answer_response = ctk.CTkLabel(self, text='Wrong', font=ctk.CTkFont(size=20), fg_color='transparent')
            self.answer_response.grid(row=0, column=1)
            self.question_widgets.append(self.answer_response)
        else:
            print("Correct answer!")
            self.answer_response = ctk.CTkLabel(self, text='Correct!', font=ctk.CTkFont(size=20), fg_color='transparent')
            self.answer_response.grid(row=0, column=1)
            self.question_widgets.append(self.answer_response)

            self.answer_cell.entry.configure(state="disabled")
            self.answer_cell.submit_button.configure(state="disabled")

            # next button
            if (self.flag_index < len(self.flag_list)-1):
                self.next_button = ctk.CTkButton(self, text="Następny", font=ctk.CTkFont(size=16), width=70, height=80, command=self.increment_question)
                self.next_button.grid(row=1, column=2)
                self.question_widgets.append(self.next_button)
    
    def change_question(self, index):
        self.flag_index = index
        self.flag = self.flag_list[self.flag_index]
        self.show_question()

    def increment_question(self, number: int = 1):
        self.change_question(self.flag_index + number)
    
    def exit(self):
        self.master.main_menu()
        self.destroy()