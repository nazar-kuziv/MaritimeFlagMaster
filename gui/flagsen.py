import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel
import random
import math
from logic.flags import *
from logic.alphabet import Alphabet

class FlagSen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the Flags-sentence screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing codewords frame")
        
        self.question_widgets = []
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="side")
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1, uniform="side")

        self.exit_button = ctk.CTkButton(self, text="Exit", width=40, height=20, command=self.exit)
        self.exit_button.grid(row=0, column=0, sticky="nw", ipadx=10, ipady=10, padx=10, pady=10)
    
    def start(self): self.show_question()
    
    def show_question(self):
        """Make sure to first make the main FlagSen frame visible with the place/pack/grid functions
        """
        for widget in self.question_widgets:
            widget.destroy()
        self.update_idletasks()


        # sentence = Alphabet.get_flag_sentence()
        # sentence = [Alphabet._characters['A'], Alphabet._characters['B'], Alphabet._characters['C']]
        sentence = list(Alphabet._characters.values())

        self.flag_sentence = ctk.CTkLabel(self, text='', fg_color="transparent")
        self.flag_sentence.grid(row=1, column=0, columnspan=3)
        self.flag_sentence.flags = []

        flag_columns = 12
        flag_rows = math.floor(len(sentence)/flag_columns)
        for i in range(flag_rows):
            self.flag_sentence.grid_rowconfigure(i, weight=1)
        for i in range(flag_columns):
            self.flag_sentence.grid_columnconfigure(i, weight=1, uniform="yes")

        for i, flag in enumerate(sentence):
            img = tksvg.SvgImage(file=f"graphics/{flag.img_path}", scaletoheight=int(self.winfo_height()*0.08))
            image = ctk.CTkLabel(self.flag_sentence, text='', image=img)
            image.grid(row=math.floor(i/(flag_columns+1)), column=(i%(flag_columns+1)), padx=1, pady=10)
            self.flag_sentence.flags.append(image)
        
        self.question_widgets.append(self.flag_sentence)

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
                self.next_button = ctk.CTkButton(self, text="Next", font=ctk.CTkFont(size=16), width=70, height=40, command=self.increment_question)
                self.next_button.grid(row=2, column=2)
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