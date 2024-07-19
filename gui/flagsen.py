import customtkinter as ctk
import tksvg
import math
from logic.constants import *
from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from gui.util_functions import *

class FlagSen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the Flags-sentence screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing codewords frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        
        self.question_widgets = []
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=0)

        self.exit_button = ctk.CTkButton(self, text="Wyjdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="orange red", command=self.exit)
        self.exit_button.grid(row=0, column=0, sticky="nw", ipadx=10, ipady=10, padx=10, pady=10)
    
    def start(self): self.show_choice()

    def show_choice(self):
        self.choice_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.choice_menu.grid(row=1, column=0, columnspan=2)
        self.question_widgets.append(self.choice_menu)

        self.default_mode_button = ctk.CTkButton(self.choice_menu, text='Wbudowane', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), 
                                                  command=lambda: self.get_file_sentence(Alphabet.load_default_sentences, Alphabet.get_default_sentence))
        self.default_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)
        self.question_widgets.append(self.choice_menu)

        self.internet_mode_button = ctk.CTkButton(self.choice_menu, text='Z internetu', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), 
                                                  command=lambda: self.flag_sentence_method(Alphabet.get_flag_sentence_from_api))
        self.internet_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)
        
        self.file_mode_button = ctk.CTkButton(self.choice_menu, text='Z pliku...', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), 
                                              command=lambda: self.get_file_sentence(Alphabet.load_sentences_from_user_file, Alphabet.get_sentence_from_user_file))
        self.file_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)
    
    def get_file_sentence(self, method, next_method):
        print("loading file sentence...")
        isLoaded = method()
        if (isLoaded is None):
            pass
        elif (not isLoaded):
            self.flag_sentence_method(lambda: "Didn't load")
        else:
            self.flag_sentence_method(next_method)

    def flag_sentence_method(self, method):
        self.get_flag_sentence_method = method
        self.show_question()

    def show_question(self):
        """Make sure to first make the main FlagSen frame visible with the place/pack/grid functions
        """
        loading_label = loading_widget(self.master)
        for widget in self.question_widgets:
            widget.destroy()
        self.update()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.is_answered = False

        def save_image():
            if (Alphabet.saveFlagSentencePNG(self.sentence.flags, suggest_file_name=self.is_answered)):
                label = ctk.CTkLabel(self, text='Zapisano.', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
                label.grid(column=1, row=0, sticky="e", pady=10)
                label.after(4000, lambda: label.destroy())
        
        self.save_image = ctk.CTkButton(self, text='Zapisz obecne jako zdjęcie...', width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=save_image)
        self.save_image.grid(column=2, row=0, sticky="ne", ipadx=10, ipady=10, padx=10, pady=10)
        
        self.sentence = self.get_flag_sentence_method()
        # self.sentence = NO_INTERNET_CONNECTION

        if (isinstance(self.sentence, str) or self.sentence is None):
            print("Didn't get request, ", self.sentence)
            if (self.sentence == REQUEST_LIMIT_EXCEEDED):
                error_text = "Limit zapytań cytatów został osiągnięty, prosimy chwilę poczekać."
            elif (self.sentence == NO_INTERNET_CONNECTION):
                error_text = "Brak połączenia z internetem."
            else:
                error_text = "Błąd czytania z pliku."
            error_message = ctk.CTkLabel(self, text=error_text, font=ctk.CTkFont(size=int(self.master.scale_size*0.05)), fg_color='white')
            error_message.grid(row=0, column=1, rowspan=2)
            loading_label.destroy()
            return

        print(self.sentence.cleaned_sentence)

        self.flag_sentence = ctk.CTkFrame(self, fg_color=None)
        self.flag_sentence.grid(row=1, column=0, columnspan=3)
        self.flag_sentence.flags = []

        flag_columns = 12
        flag_rows = math.floor(len(self.sentence.flags)/flag_columns)
        for i in range(flag_rows):
            self.flag_sentence.grid_rowconfigure(i, weight=1)
        for i in range(flag_columns):
            self.flag_sentence.grid_columnconfigure(i, weight=1, uniform="yes")

        for i, flag in enumerate(self.sentence.flags):
            img = None
            if (self.master.winfo_height() < self.master.winfo_width()):
                img = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{flag.img_path}"), scaletoheight=int(self.master.scale_size*0.1)) if (flag is not None) else None
            else:
                img = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{flag.img_path}"), scaletowidth=int(self.master.scale_size*0.05)) if (flag is not None) else None
            image = ctk.CTkLabel(self.flag_sentence, text='', image=img, fg_color="transparent")
            image.grid(row=math.floor(i/(flag_columns+1)), column=(i%(flag_columns+1)), padx=2, pady=10)
            self.flag_sentence.flags.append(image)
        
        self.question_widgets.append(self.flag_sentence)

        self.answer_cell = ctk.CTkFrame(self, fg_color="transparent")
        self.answer_cell.grid(row=2, column=0, columnspan=3, pady=10)
        self.question_widgets.append(self.answer_cell)

        validate_command = self.register(self.validate_answer)
        self.answer_cell.entry = ctk.CTkEntry(self.answer_cell, width=int(self.master.scale_size*0.6), font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), 
                                              validate="key", validatecommand=(validate_command,'%P'))
        self.answer_cell.entry.bind("<Return>", self.enter_answer)

        self.text_length = ctk.CTkLabel(self.answer_cell, text=f"0/{len(self.sentence.cleaned_sentence)}", fg_color='transparent')
        self.text_length.pack(side="left", padx=10)
        self.answer_cell.entry.pack(side="left")
        self.answer_cell.entry.focus()
        
        self.answer_cell.submit_button = ctk.CTkButton(self.answer_cell, text='Sprawdź', width=0, font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), command=self.enter_answer)
        self.answer_cell.submit_button.pack(side="left", padx=5)
        self.update_idletasks()
        loading_label.destroy()

    def validate_answer(self, new_text):
        if (len(new_text) > len(self.sentence.cleaned_sentence)): return False
        self.text_length.configure(text=f"{len(new_text)}/{len(self.sentence.cleaned_sentence)}")
        return True

    def enter_answer(self, event=None):
        try:
            self.answer_response.destroy()
        except AttributeError: pass
        # correct_answer = self.flag.letter[0].upper()
        
        if (not self.sentence.check_sentence(self.answer_cell.entry.get())):
            print("Wrong answer.")
            self.answer_response = ctk.CTkLabel(self, text='Źle', font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), fg_color='transparent')
            self.answer_response.grid(row=0, column=1)
            self.question_widgets.append(self.answer_response)
        else:
            print("Correct answer!")
            self.is_answered = True
            self.answer_response = ctk.CTkLabel(self, text='Poprawnie!', font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), fg_color='transparent')
            self.answer_response.grid(row=0, column=1)
            self.question_widgets.append(self.answer_response)

            self.answer_cell.entry.configure(state="disabled")
            self.answer_cell.submit_button.configure(state="disabled")
            self.answer_cell.entry.unbind("<Return>")

            # next button
            self.next_button = ctk.CTkButton(self, text="Nowe zdanie", font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), height=40, command=self.show_question)
            self.next_button.grid(row=2, column=2)
            self.question_widgets.append(self.next_button)
    
    def exit(self):
        self.master.main_menu()
        self.destroy()