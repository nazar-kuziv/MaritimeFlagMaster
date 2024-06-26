import customtkinter as ctk
import tksvg
from custom_hovertip import CustomTooltipLabel
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from logic.constants import *

class SenFlag(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """Class for initializing the Sentence-Flags screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")

        self.top_menu = ctk.CTkFrame(self)
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.exit_button = ctk.CTkButton(self.top_menu, text="Wyjdź", width=40, command=self.exit, fg_color="orange red")
        self.top_menu.exit_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list = {}

        self.alphabet = list(Alphabet._characters.values())
        self.flag_index = 0
        self.images = []
    
    def start(self): self.show_question()
    
    def show_question(self):
        """Make sure to first make the main SenFlags frame visible with the place/pack/grid functions
        """
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
        self.update_idletasks()

        self.sentence = Alphabet.get_flag_sentence()
        # self.sentence = NO_INTERNET_CONNECTION

        if (isinstance(self.sentence, str)):
            print("Didn't get request, ", self.sentence)
            if (self.sentence == REQUEST_LIMIT_EXCEEDED):
                error_text = "The limit for quote requests have been reached, please wait before trying again."
            else:
                error_text = "No internet connection has been detected."
            error_message = ctk.CTkLabel(self, text=error_text, font=ctk.CTkFont(size=20), fg_color='white')
            error_message.grid(row=0, column=1, rowspan=3)
            return

        print(self.sentence.cleaned_sentence)

        meaning_label = ctk.CTkLabel(self.top_menu, text=self.sentence.cleaned_sentence, width=500, fg_color='transparent', wraplength=int(self.winfo_width()*0.5))
        meaning_label.pack(side="left", padx=10)
        self.top_menu.list["meaning_label"] = meaning_label

        check_button = ctk.CTkButton(self.top_menu, text="Sprawdź", width=30, command=self.check_answer, state="disabled")
        check_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list["check_button"] = check_button

        self.input_parent = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.input_parent.pack(side="top", fill="x", padx=10)
        self.flag_input_box = ctk.CTkScrollableFrame(self.input_parent, height=40, orientation="horizontal")
        self.master.bind("<BackSpace>", self.delete_input_flag)
        self.flag_input_box.pack(side="top", fill="x")
        self.flag_input_box.text_length = ctk.CTkLabel(self.flag_input_box, text=f"0/{len(self.sentence.cleaned_sentence)}", justify="right", height=50, width=40, fg_color='transparent')
        self.flag_input_box.text_length.pack(side="left", padx=10)

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
                if (alphabet_index == len(self.alphabet)):
                    flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                    flag_container.grid_rowconfigure(0, weight=1)
                    flag_container.grid_columnconfigure(0, weight=1)
                    flag_container.grid(row=i, column=j, columnspan=self.input_columns, sticky="nsew")
                    flag_container.flag = ctk.CTkLabel(flag_container, text='SPACJA', text_color="blue", cursor="hand2")
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
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='␣', font=ctk.CTkFont(size=20, weight='bold'), text_color="blue", fg_color='transparent')
            new_input_flag.pack(side="left", padx=1)
            self.input_flags.append(new_input_flag)
            self.answer_flags.append(None)
        else:
            input_image = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{self.alphabet[index].img_path}"), scaletoheight=int(self.winfo_height()*0.04))
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='', image=input_image)
            new_input_flag.pack(side="left", padx=1)
            self.input_flags.append(new_input_flag)
            self.answer_flags.append(self.alphabet[index])
        
        self.flag_input_box.text_length.configure(text=f"{len(self.input_flags)}/{len(self.sentence.cleaned_sentence)}")
        self.top_menu.list["check_button"].configure(state="enabled", cursor="hand2")

    
    def delete_input_flag(self, event = None):
        print("Backspace fired")
        if (len(self.input_flags) > 0):
            flag = self.input_flags.pop()
            flag.destroy()
            self.answer_flags.pop()
            self.flag_input_box.text_length.configure(text=f"{len(self.input_flags)}/{len(self.sentence.cleaned_sentence)}")
            if (len(self.input_flags) <= 0):
                self.top_menu.list["check_button"].configure(state="disabled", cursor='')

    def check_answer(self):
        try:
            self.answer_response.destroy()
        except AttributeError: pass
        # correct_answer = self.flag.letter[0].upper()
        
        if (not self.sentence.check_flags(self.answer_flags)):
            print("Wrong answer.")
            self.answer_response = ctk.CTkLabel(self.top_menu, text="Wrong", fg_color='transparent')
            self.answer_response.pack(side="left", padx=10)
            self.top_menu.list["answer_response"] = self.answer_response
        else:
            print("Correct answer!")
            self.answer_response = ctk.CTkLabel(self.top_menu, text="Correct!", fg_color='transparent')
            self.answer_response.pack(side="left", padx=10)
            self.top_menu.list["answer_response"] = self.answer_response

            self.top_menu.list["check_button"].configure(state="disabled", cursor='')
            for f in self.flag_images:
                f.flag.unbind("<Button-1>")
                f.flag.configure(cursor='')

            # next button
            self.next_button = ctk.CTkButton(self.top_menu, text="Nowe zdanie", font=ctk.CTkFont(size=16), height=40, command=self.show_question)
            self.next_button.pack(side="right", padx=10)
            self.top_menu.list["new_sentence"] = self.next_button
    
    def exit(self):
        self.master.unbind("<BackSpace>")
        self.master.main_menu()
        self.destroy()