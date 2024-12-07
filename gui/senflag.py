import customtkinter as ctk
import tksvg
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from logic.exceptions import *
import gui.util_functions as Util
from gui.countdown import add_countdown_timer_to_top_menu
from logic.modes.senflag_session import SenflagSession

class SenFlag(Util.AppQuizPage, Util.ISkippablePage):
    def __init__(self, master, source: str = "default", questions_number: int = 0, time_minutes: int = 0, **kwargs):
        """Class for initializing the Sentence-Flags screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.source = source
        self.questions_number = questions_number
        self.time_minutes = time_minutes
        print(f"Questions number: {questions_number}, time: {time_minutes}")

        self.alphabet = Alphabet.get_characters_flags_shuffled()
        self.flag_index = 0
        self.images = []
    
    def draw(self):
        super().draw()

        if (self.time_minutes > 0):
            self.countdown = add_countdown_timer_to_top_menu(self, self.time_minutes)
        
        self.top_menu = ctk.CTkFrame(self, height=0)
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.dict = {}

        # self.show_options()
        self.establish_session(self.source)

    def establish_session(self, mode: str):
        error_text = ""
        try:
            self.session = SenflagSession(mode, self.questions_number)
        except NoInternetConnectionException:
            error_text = "Brak połączenia z internetem."
        except RequestLimitExceededException:
            error_text = "Limit zapytań cytatów został osiągnięty, prosimy chwilę poczekać."
        except SmthWrongWithFileException:
            error_text = "Błąd czytania z pliku."
        except Exception:
            error_text = "Wystąpił błąd."

        if (error_text != ""):
            error_message = ctk.CTkLabel(self.container_menu, text=error_text, font=ctk.CTkFont(size=int(self.master.scale_size*0.05)), fg_color='white')
            error_message.grid(row=0, column=1, rowspan=2)
            return
        
        Util.double_buffer_frame(self, Util.loading_widget(self.winfo_toplevel(), True), self.next_question)
    
    def show_question(self):
        """Make sure to first make the main SenFlags frame visible with the place/pack/grid functions
        """
        self.flag_images = []
        self.input_flag_objects = []
        self.input_flag_labels = []
        for widget in self.flag_images:
            widget.destroy()
        print(self.top_menu.dict.keys())
        for widget in self.top_menu.dict.values():
            widget.destroy()
        self.top_menu.dict = {}
        try:
            self.input_frame.destroy()
        except AttributeError: print("Couldn't destroy input_frame")
        try:
            self.input_parent.destroy()
        except AttributeError: print("Couldn't destroy flag_input_box")
        self.update()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.sentence = self.session.get_question()
        print(self.sentence.cleaned_sentence)

        print(self.question.cleaned_sentence)
        meaning_label = ctk.CTkLabel(self.top_menu, text=self.question.cleaned_sentence, width=int(self.master.winfo_width()*0.3), font=ctk.CTkFont(size=int(self.master.winfo_width()*0.011)), 
                                     fg_color='transparent', wraplength=int(self.master.winfo_width()*0.28))
        meaning_label.pack(side="left", padx=10)
        self.top_menu.dict["meaning_label"] = meaning_label

        check_button = ctk.CTkButton(self.top_menu, text="Sprawdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.check_answer)
        check_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.dict["check_button"] = check_button
        
        self.answer_response = ctk.CTkLabel(self.top_menu, text="", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
        self.answer_response.pack(side="left", padx=10)
        self.top_menu.dict["answer_response"] = self.answer_response

        self.input_parent = ctk.CTkFrame(self, height=int(self.master.scale_size*0.05), fg_color="transparent")
        self.input_parent.pack(side="top", fill="x", padx=10)
        self.text_length = ctk.CTkLabel(self.input_parent, text=f"0/{len(self.question.cleaned_sentence)}", font=ctk.CTkFont(size=int(self.winfo_width()*0.013)), justify="right", 
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

        self.top_menu.dict["skip"] = self.add_skip_button(self.skip_command)

        try:
            self.countdown.startCountdown()
        except AttributeError: pass

    def skip_command(self):
        self.top_menu.dict["skip"].configure(command=None)
        correct_flags = self.session.get_correct_answer().flags
        for f in correct_flags:
            if (f is None):
                new_input_flag = ctk.CTkLabel(self.flag_input_box, text='␣', font=ctk.CTkFont(size=int(self.master.scale_size*0.05), weight='bold'), text_color="blue", fg_color='transparent')
                new_input_flag.pack(side="left", padx=1)
                self.update()
                self.input_flag_labels.append(new_input_flag)
                self.input_flag_objects.append(None)
            else:
                input_image = tksvg.SvgImage(file=Environment.resource_path(f.img_path), scaletoheight=int(self.master.scale_size*0.04))
                new_input_flag = ctk.CTkLabel(self.flag_input_box, text='', image=input_image)
                new_input_flag.pack(side="left", padx=1)
                self.input_flag_labels.append(new_input_flag)
                self.input_flag_objects.append(f)
        
        self.text_length.configure(text=f"{len(self.input_flag_labels)}/{len(self.question.cleaned_sentence)}")
        print("Skipped.")
        self.answer_response.configure(text='Pominięto.')
        self.show_next_button()

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
        if (len(self.input_flag_labels) >= len(self.question.cleaned_sentence)):
            return
        print(f"New flag {index}")
        if ((isinstance(index, str) and index != "SPACJA") or (isinstance(index, int) and index < 0)):
            return

        if (index == "SPACJA"):
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='␣', font=ctk.CTkFont(size=int(self.master.scale_size*0.05), weight='bold'), text_color="blue", fg_color='transparent')
            new_input_flag.pack(side="left", padx=1)
            self.update()
            self.input_flag_labels.append(new_input_flag)
            self.input_flag_objects.append(None)
        else:
            input_image = tksvg.SvgImage(file=Environment.resource_path(self.alphabet[index].img_path), scaletoheight=int(self.master.scale_size*0.04))
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='', image=input_image)
            new_input_flag.pack(side="left", padx=1)
            self.input_flag_labels.append(new_input_flag)
            self.input_flag_objects.append(self.alphabet[index])
        
        self.text_length.configure(text=f"{len(self.input_flag_labels)}/{len(self.question.cleaned_sentence)}")
        self.answer_response.configure(text='')

    
    def delete_input_flag(self, event = None):
        print("Backspace fired")
        if (len(self.input_flag_labels) > 0):
            flag = self.input_flag_labels.pop()
            flag.destroy()
            self.input_flag_objects.pop()
            self.text_length.configure(text=f"{len(self.input_flag_labels)}/{len(self.question.cleaned_sentence)}")
            self.answer_response.configure(text='')

    def check_answer(self):
        # correct_answer = self.flag.letter[0].upper()
        
        if (not self.session.check_answer(self.input_flag_objects)):
            print("Wrong answer.")
            self.answer_response.configure(text='Źle')
            return
        
        print("Correct answer!")
        self.answer_response.configure(text='Poprawnie')

        def save_image():
            if (Alphabet.saveFlagSentencePNG(self.question.flags)):
                label = ctk.CTkLabel(self.input_parent, text='Zapisano.', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
                label.pack(side="right", padx=10)
                label.after(4000, lambda: label.destroy())
    
        self.save_image = ctk.CTkButton(self.input_parent, text='Zapisz jako zdjęcie...', width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=save_image)
        self.save_image.pack(side="right", ipadx=10, ipady=10, padx=10, pady=5)

        # message = self.get_new_sentence()
        # if (message == "Błąd czytania z pliku."):
        #     return
        # elif (message is not None):
        #     error_message = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=int(self.master.scale_size*0.05)), fg_color='white')
        #     error_message.grid(row=0, column=1, rowspan=2)
        #     return
        
        self.update() # for internet delays, so that the user knows if it was right immediately
        self.show_next_button()

    def show_next_button(self):
        self.top_menu.dict["check_button"].configure(command=None)
        for f in self.flag_images:
            f.flag.unbind("<Button-1>")
            f.flag.configure(cursor='')

        next_exists = self.session.next_question()
        next_command = self.next_question if next_exists else self.finish
        next_text = "Nowe zdanie" if next_exists else "Wyniki"
        if (not next_exists):
            try:
                self.countdown.pause()
            except AttributeError: pass
        
        self.next_button = ctk.CTkButton(self.top_menu, text=next_text, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=next_command)
        self.next_button.pack(side="right", fill='y')
        self.top_menu.dict["new_sentence"] = self.next_button
    
    def next_question(self):
        self.flag = self.senflag_session.get_question()
        self.show_question()