import cProfile
import re
from tkinter import Event

import customtkinter as ctk
import tksvg

import gui.util_functions as Util
from logic import exceptions
from logic.alphabet import Alphabet
from logic.environment import Environment
from logic.loading import check_thread_active_status

input_text_allowed_chars = r" a-zA-Z0-9?!@\"#£\u0016\u0008"

class MakeImage(Util.AppPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (
                    self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.alphabet = dict(Alphabet._characters, **Alphabet._additionalFlags)
        self.flag_index = 0
        self.images = []
        self.bg_color = "transparent"
        self.flag_images = []
        self.preview = None
    
    def draw(self):
        super().draw()
        self.show_question()

    def show_question(self):
        loading_label = Util.loading_widget(self.master)
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (
                    self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        def delete_illegal_chars():
            text = self.top_menu.input_text.get("1.0", "end - 1 chars")
            text = re.sub(f"[^{input_text_allowed_chars}]", "", text)
            print(f"New text: {text}")
            self.top_menu.input_text.delete("1.0", "end")
            self.top_menu.input_text.insert("1.0", text)

        def input_callback(event: Event):
            if (event.state & 4 and event.keysym in "vV"):
                Util.text_paste(event, self.top_menu.input_text)
                delete_illegal_chars()

            if (event.char and not re.match(f"[{input_text_allowed_chars}]", event.char)):
                print(f"Illegal character {event.char}, {ord(event.char)}")
                delete_illegal_chars()
                return

            if (self.preview):
                self.after_cancel(self.preview)

            if (self.top_menu.input_text.get("1.0", "end - 1 chars") == ""):
                self.preview_label.configure(text="Zacznij pisać", image='')
                return
            
            if (not event.char):
                return

            self.preview = self.after(750, self.show_preview)

        self.top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)

        self.top_menu.input_text = ctk.CTkTextbox(self.top_menu, width=400, height=0)
        self.top_menu.input_text.pack(side="left", fill="y", padx=10)
        self.top_menu.input_text.focus_set()

        self.top_menu.backspace_button = ctk.CTkButton(self.top_menu, text="Kasuj", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.flag_delete_handler)
        self.top_menu.backspace_button.pack(side="left", ipadx=10, ipady=10, padx=5)

        self.top_menu.clear_button = ctk.CTkButton(self.top_menu, text="Wyczyść", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.flag_clear_handler)
        self.top_menu.clear_button.pack(side="left", ipadx=10, ipady=10, padx=5)

        self.master.bind("<KeyPress>", input_callback)
        self.master.bind("<Control-Key-a>", lambda event: Util.text_select_all(event, self.top_menu.input_text))
        self.master.bind("<Control-Key-A>", lambda event: Util.text_select_all(event, self.top_menu.input_text))

        self.top_menu.check_button = ctk.CTkButton(self.top_menu, text="Zapisz...", width=0,
                                                   font=ctk.CTkFont(size=int(self.master.winfo_width() * 0.015)),
                                                   command=self.save_image)
        self.top_menu.check_button.pack(side="right", ipadx=10, ipady=10)

        def checkbox_event():
            print("checkbox toggled, current value:", check_var.get())
            self.bg_color = "transparent" if check_var.get() == "on" else "gray"
        
        check_var = ctk.StringVar(value="on")
        self.top_menu.checkbox = ctk.CTkCheckBox(self.top_menu, text="Transparentne tło", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.01)), command=checkbox_event, 
                                                 variable=check_var, onvalue="on", offvalue="off")
        self.top_menu.checkbox.pack(side="right", padx=10)

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent", width=400)
        self.input_frame.pack(side="left", fill="both", padx=15)

        self.input_rows = 7
        self.input_columns = 7
        for i in range(self.input_rows):
            self.input_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.input_columns):
            self.input_frame.grid_columnconfigure(j, weight=1)

        for f in self.alphabet.values():
            self.images.append(tksvg.SvgImage(file=Environment.resource_path(f.img_path), scaletowidth=int(self.master.scale_size/self.input_columns)*0.5))

        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Zacznij pisać")
        self.preview_label.pack(side="left", fill="both", expand=True)
        
        
        self.place_input_flags()
        self.update_idletasks()
        loading_label.destroy()

    def place_input_flags(self):
        alphabet_iter = enumerate(self.alphabet.keys())
        for i in range(self.input_rows):
            for j in range(self.input_columns):
                tuple = next(alphabet_iter, None)

                flag_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                flag_container.grid_rowconfigure(0, weight=1)
                flag_container.grid_columnconfigure(0, weight=1)

                flag_container.grid(row=i, column=j)
                if (not tuple):
                    flag_container.flag = ctk.CTkLabel(flag_container, text="␣", text_color="blue", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.025)), justify="center", cursor="hand2")
                    flag_container.flag.bind("<Button-1>", command=lambda event, i=" ": self.flag_input_handler(char=i))
                else:
                    flag_container.flag = ctk.CTkLabel(flag_container, text="", image=self.images[tuple[0]], cursor="hand2")
                    flag_container.flag.bind("<Button-1>", command=lambda event, i=tuple[1]: self.flag_input_handler(char=i))
                flag_container.flag.grid(ipadx=8, ipady=10, sticky="nsew")
                self.flag_images.append(flag_container)

                if (not tuple):
                    flag_container2 = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                    flag_container2.grid_rowconfigure(0, weight=1)
                    flag_container2.grid_columnconfigure(0, weight=1)
                    flag_container2.grid(row=i, column=j+1, sticky="nsew")
                    flag_container2.rtrn = ctk.CTkLabel(flag_container2, text="⏎", text_color="blue", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.025)), justify="center", cursor="hand2")
                    flag_container2.rtrn.bind("<Button-1>", command=lambda event, i="\n": self.flag_input_handler(char=i))
                    flag_container2.rtrn.grid(row=0, column=1, ipadx=8, ipady=10, sticky="nsew")
                    self.flag_images.append(flag_container2)
                    return
        
    def show_preview(self):
        self.preview_label.configure(text="Ładowanie obrazu...", image='')
        self.update_idletasks()
        while (check_thread_active_status()):
            self.after(100)
        text = self.top_menu.input_text.get("1.0", "end - 1c")
        img_path, height, width = Alphabet.get_flag_sentence_svg(text, self.bg_color)

        scale_size = ({"scaletowidth": int(self.preview_frame.winfo_width()*0.9)}
                        if (width > height)
                        else {"scaletoheight": int(self.preview_frame.winfo_height()*0.9)})

        self.preview_img = tksvg.SvgImage(file=img_path, **scale_size)
        self.preview_label.configure(image=self.preview_img, text="")

        print("Preview updated")

    def flag_input_handler(self, char):
        self.top_menu.input_text.insert('insert', char)

        if (self.preview):
            self.after_cancel(self.preview)
        self.preview = self.after(750, self.show_preview)

    def flag_delete_handler(self):
        self.top_menu.input_text.delete("end - 2c")

    def flag_clear_handler(self):
        self.top_menu.input_text.delete("1.0", "end")

    def save_image(self):
        text = self.top_menu.input_text.get("1.0", "end - 1c")
        if not text:
            return

        flags = []
        for char in text:
            if char == ' ':
                flags.append(None)
            else:
                try:
                    flag = Alphabet.get_flag_using_character(char)
                    flags.append(flag)
                except exceptions.InputCharacterException:
                    flags.append(None)

        if Alphabet.save_flag_sentence_png(flags, background=self.bg_color):
            label = ctk.CTkLabel(self.top_menu, text="Zapisano.",
                                 font=ctk.CTkFont(size=int(self.master.winfo_width() * 0.015)),
                                 fg_color="transparent")
            label.pack(side="right", padx=10)
            label.after(4000, lambda: label.destroy())

    def unbind(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<Control-Key-a>")
        self.master.unbind("<Control-Key-A>")
        super().unbind()
