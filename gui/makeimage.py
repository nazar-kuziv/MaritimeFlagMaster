import customtkinter as ctk
import tksvg
import random

from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from logic.constants import *
from gui.util_functions import *

class MakeImage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        self.top_menu.exit_button = ctk.CTkButton(self.top_menu, text="Wyjdź", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="orange red", command=self.exit)
        self.top_menu.exit_button.pack(side="left", ipadx=10, ipady=10)
        self.top_menu.list = {}

        self.alphabet = Alphabet.get_single_flags()
        self.flag_index = 0
        self.images = []
    
    def start(self): self.show_question()
    
    def show_question(self):
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
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        check_button = ctk.CTkButton(self.top_menu, text="Zapisz...", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.check_answer, state="disabled")
        check_button.pack(side="right", ipadx=10, ipady=10)
        self.top_menu.list["check_button"] = check_button

        self.input_parent = ctk.CTkFrame(self, height=int(self.winfo_width()*0.1), fg_color="transparent")
        self.input_parent.pack(side="top", fill="x", padx=10)
        self.flag_input_box = ctk.CTkScrollableFrame(self.input_parent, height=int(self.master.scale_size*0.05), orientation="horizontal")
        self.master.bind("<BackSpace>", self.delete_input_flag)
        self.flag_input_box.pack(side="top", fill="x")

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
                    self.images.append(tksvg.SvgImage(file=Environment.resource_path(f"graphics/{f.img_path}"), scaletoheight=int(self.master.scale_size*0.8/self.input_columns)))
                else:
                    self.images.append(tksvg.SvgImage(file=Environment.resource_path(f"graphics/{f.img_path}"), scaletowidth=int(self.master.scale_size*0.8/self.input_columns)))
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
        print(f"New flag {index}")
        if ((isinstance(index, str) and index != "SPACJA") or (isinstance(index, int) and index < 0)):
            return

        if (index == "SPACJA"):
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='␣', font=ctk.CTkFont(size=int(self.master.scale_size*0.05), weight='bold'), text_color="blue", fg_color='transparent')
            new_input_flag.pack(side="left", padx=1)
            self.input_flags.append(new_input_flag)
            self.answer_flags.append(None)
        else:
            input_image = tksvg.SvgImage(file=Environment.resource_path(f"graphics/{self.alphabet[index].img_path}"), scaletoheight=int(self.master.scale_size*0.04))
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text='', image=input_image)
            new_input_flag.pack(side="left", padx=1)
            self.input_flags.append(new_input_flag)
            self.answer_flags.append(self.alphabet[index])
        
        self.top_menu.list["check_button"].configure(state="enabled", cursor="hand2")

    
    def delete_input_flag(self, event = None):
        print("Backspace fired")
        if (len(self.input_flags) > 0):
            flag = self.input_flags.pop()
            flag.destroy()
            self.answer_flags.pop()
            if (len(self.input_flags) <= 0):
                self.top_menu.list["check_button"].configure(state="disabled", cursor='')

    def check_answer(self):
        if Alphabet.saveFlagSentencePNG(self.answer_flags, background="transparent"):
            label = ctk.CTkLabel(self.top_menu, text='Zapisano.', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
            label.pack(side="right", padx=10)
            label.after(2000, lambda: label.destroy())
    
    def exit(self):
        self.master.unbind("<BackSpace>")
        self.master.main_menu()
        self.destroy()