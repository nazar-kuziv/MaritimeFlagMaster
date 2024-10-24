import customtkinter as ctk
import tksvg
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from logic.constants import *
from gui.util_functions import *

class SenFlag(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the Sentence-Flags screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.top_menu = ctk.CTkFrame(self)
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.exit_button = ctk.CTkButton(self.top_menu, text="Wyjdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="orange red", command=self.exit)
        self.top_menu.exit_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list = {}

        self.alphabet = Alphabet.get_characters_flags_shuffled()
        self.flag_index = 0
        self.images = []
    
    def start(self): self.show_choice()

    def show_choice(self):
        self.choice_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.choice_menu.pack(side="bottom", fill="y", expand=True)
        self.top_menu.list["choice_menu"] = self.choice_menu

        self.default_mode_button = ctk.CTkButton(self.choice_menu, text='Wbudowane', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), 
                                                  command=lambda: self.get_file_sentence(Alphabet.load_default_sentences, Alphabet.get_default_sentence))
        self.default_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)

        self.internet_mode_button = ctk.CTkButton(self.choice_menu, text='Z internetu', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), 
                                                  command=lambda: self.flag_sentence_mode_method(Alphabet.get_flag_sentence_from_api))
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
            self.flag_sentence_mode_method(lambda: "Didn't load")
        else:
            self.flag_sentence_mode_method(next_method)

    def flag_sentence_mode_method(self, method):
        self.get_flag_sentence_method = method
        message = self.get_new_sentence()
        if (message is not None):
            error_message = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=int(self.master.scale_size*0.05)), fg_color='white')
            error_message.grid(row=0, column=1, rowspan=2)
            return
        self.show_question()

    def get_new_sentence(self):
        error_text = None
        self.sentence = self.get_flag_sentence_method()
        # self.sentence = NO_INTERNET_CONNECTION

        if (isinstance(self.sentence, str) or self.sentence is None):
            print("Didn't get new sentence, ", self.sentence)
            if (self.sentence == REQUEST_LIMIT_EXCEEDED):
                error_text = "Limit zapytań cytatów został osiągnięty, prosimy chwilę poczekać."
            elif (self.sentence == NO_INTERNET_CONNECTION):
                error_text = "Brak połączenia z internetem."
            else:
                error_text = "Błąd czytania z pliku."
            return error_text

        print(self.sentence.cleaned_sentence)
    
    def show_question(self):
        """Make sure to first make the main SenFlags frame visible with the place/pack/grid functions
        """
        loading_label = loading_widget(self.master)
        self.flag_images = []
        self.answer_flags = []
        self.input_flags = []
        for widget in self.flag_images:
            widget.destroy()
        print(self.top_menu.list.keys())
        for widget in self.top_menu.list.values():
            widget.destroy()
        self.top_menu.list = {}
        try:
            self.input_frame.destroy()
        except AttributeError: print("Couldn't destroy input_frame")
        try:
            self.input_parent.destroy()
        except AttributeError: print("Couldn't destroy flag_input_box")
        self.update()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        meaning_label = ctk.CTkLabel(self.top_menu, text=self.sentence.cleaned_sentence, width=int(self.master.winfo_width()*0.3), font=ctk.CTkFont(size=int(self.master.winfo_width()*0.011)), 
                                     fg_color='transparent', wraplength=int(self.master.winfo_width()*0.28))
        meaning_label.pack(side="left", padx=10)
        self.top_menu.list["meaning_label"] = meaning_label

        check_button = ctk.CTkButton(self.top_menu, text="Sprawdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.check_answer, state="disabled")
        check_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list["check_button"] = check_button

        self.input_parent = ctk.CTkFrame(self, height=int(self.master.scale_size*0.05), fg_color="transparent")
        self.input_parent.pack(side="top", fill="x", padx=10)
        self.text_length = ctk.CTkLabel(self.input_parent, text=f"0/{len(self.sentence.cleaned_sentence)}", font=ctk.CTkFont(size=int(self.winfo_width()*0.013)), justify="right", 
                                                       height=int(self.master.scale_size*0.055), fg_color='transparent')
        self.text_length.pack(side="left", padx=(0, 5))
        self.flag_input_box = ctk.CTkScrollableFrame(self.input_parent, height=int(self.master.scale_size*0.05), orientation="horizontal")
        self.master.bind("<BackSpace>", self.delete_input_flag)
        self.flag_input_box.pack(side="left", fill="x", expand=True)

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(side="top", fill="both", expand=True)

        self.input_rows = 5
        self.input_columns = 9
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
        
        self.place_input_flags()
        self.update_idletasks()
        loading_label.destroy()

    def place_input_flags(self):
        alphabet_index = 0
        for i in range(self.input_rows):
            for j in range(self.input_columns):
                if (alphabet_index == len(self.alphabet)):
                    flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                    flag_container.grid_rowconfigure(0, weight=1)
                    flag_container.grid_columnconfigure(0, weight=1)
                    flag_container.grid(row=i, column=j, columnspan=self.input_columns, sticky="nsew")
                    flag_container.flag = ctk.CTkLabel(flag_container, text='SPACJA', text_color="blue", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), cursor="hand2")
                    flag_container.flag.bind("<Button-1>", command=lambda event, i='SPACJA': self.flag_input_handler(event, index=i))
                    flag_container.flag.grid(ipadx=10, ipady=10)
                    self.flag_images.append(flag_container)
                    return
                
                flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                flag_container.grid_rowconfigure(0, weight=1)
                flag_container.grid_columnconfigure(0, weight=1)
                flag_container.grid(row=i, column=j, sticky="nsew")
                flag_container.flag = ctk.CTkLabel(flag_container, text='', image=self.images[alphabet_index], cursor="hand2")
                flag_container.flag.bind("<Button-1>", command=lambda event, i=alphabet_index: self.flag_input_handler(event, index=i))
                flag_container.flag.grid(ipadx=10, ipady=10)
                self.flag_images.append(flag_container)
                
                alphabet_index += 1

    def flag_input_handler(self, event=None, index: int | str = -1):
        """Handler function for clicking on flags.
        """
        if (len(self.input_flags) >= len(self.sentence.cleaned_sentence)):
            return
        print(f"New flag {index}")
        if ((isinstance(index, str) and index != "SPACJA") or (isinstance(index, int) and index < 0)):
            return

        if (index == "SPACJA"):
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='␣', font=ctk.CTkFont(size=int(self.master.scale_size*0.05), weight='bold'), text_color="blue", fg_color='transparent')
            new_input_flag.pack(side="left", padx=1)
            self.input_flags.append(new_input_flag)
            self.answer_flags.append(None)
        else:
            input_image = tksvg.SvgImage(file=Environment.resource_path(self.alphabet[index].img_path), scaletoheight=int(self.master.scale_size*0.04))
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='', image=input_image)
            new_input_flag.pack(side="left", padx=1)
            self.input_flags.append(new_input_flag)
            self.answer_flags.append(self.alphabet[index])
        
        self.text_length.configure(text=f"{len(self.input_flags)}/{len(self.sentence.cleaned_sentence)}")
        self.top_menu.list["check_button"].configure(state="enabled", cursor="hand2")
        try:
            self.answer_response.destroy()
        except AttributeError: pass

    
    def delete_input_flag(self, event = None):
        print("Backspace fired")
        if (len(self.input_flags) > 0):
            flag = self.input_flags.pop()
            flag.destroy()
            self.answer_flags.pop()
            self.text_length.configure(text=f"{len(self.input_flags)}/{len(self.sentence.cleaned_sentence)}")
            if (len(self.input_flags) <= 0):
                self.top_menu.list["check_button"].configure(state="disabled", cursor='')
            if (self.answer_response is not None):
                self.answer_response.destroy()

    def check_answer(self):
        try:
            self.answer_response.destroy()
        except AttributeError: pass
        # correct_answer = self.flag.letter[0].upper()
        
        if (not self.sentence.check_flags(self.answer_flags)):
            print("Wrong answer.")
            self.answer_response = ctk.CTkLabel(self.top_menu, text="Źle", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
            self.answer_response.pack(side="left", padx=10)
            self.top_menu.list["answer_response"] = self.answer_response
        else:
            print("Correct answer!")
            self.answer_response = ctk.CTkLabel(self.top_menu, text="Poprawnie!", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
            self.answer_response.pack(side="left", padx=10)
            self.top_menu.list["answer_response"] = self.answer_response

            self.top_menu.list["check_button"].configure(state="disabled", cursor='')
            for f in self.flag_images:
                f.flag.unbind("<Button-1>")
                f.flag.configure(cursor='')

            def save_image():
                if (Alphabet.saveFlagSentencePNG(self.sentence.flags)):
                    label = ctk.CTkLabel(self.input_parent, text='Zapisano.', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
                    label.pack(side="right", padx=10)
                    label.after(4000, lambda: label.destroy())
        
            self.save_image = ctk.CTkButton(self.input_parent, text='Zapisz jako zdjęcie...', width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=save_image)
            self.save_image.pack(side="right", ipadx=10, ipady=10, padx=10, pady=5)

            message = self.get_new_sentence()
            if (message == "Błąd czytania z pliku."):
                return
            elif (message is not None):
                error_message = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=int(self.master.scale_size*0.05)), fg_color='white')
                error_message.grid(row=0, column=1, rowspan=2)
                return
            
            # next button
            self.next_button = ctk.CTkButton(self.top_menu, text="Nowe zdanie", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.show_question)
            self.next_button.pack(side="right", fill='y')
            self.top_menu.list["new_sentence"] = self.next_button
    
    def exit(self):
        self.master.unbind("<BackSpace>")
        self.master.main_menu()
        self.destroy()