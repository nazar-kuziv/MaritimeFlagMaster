from tkinter import Event

import customtkinter as ctk
import tksvg
import difflib

import gui.util_functions as Util
from logic.alphabet import Alphabet
from logic.environment import Environment


class MakeImage(Util.AppPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.alphabet = dict(Alphabet._characters, **Alphabet._additionalFlags)
        self.flag_index = 0
        self.images = []
        self.is_transparent = "grey"
        self.flag_images = []
        self.answer_flags = []
        self.input_image_labels = []
    
    def draw(self):
        super().draw()
        self.show_question()
    
    def show_question(self):
        loading_label = Util.loading_widget(self.master)
        # for widget in self.flag_images:
        #     widget.destroy()
        # print(self.top_menu.list.keys())
        # for widget in self.top_menu.list.values():
        #     widget.destroy()
        # self.top_menu.list = {}
        # try:
        #     self.input_frame.destroy()
        # except AttributeError: print("Couldn't destroy input_frame")
        # try:
        #     self.input_parent.destroy()
        # except AttributeError: print("Couldn't destroy flag_input_box")
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        def input_callback(event: Event):
            if (event.state & 4 and event.keysym in "vV"):
                Util.text_paste(event, self.top_menu.input_text)
            new_text = self.top_menu.input_text.get("1.0", "end - 1c")
            if (new_text == self.text): return
            
            print(f"New text: {new_text}")
            seq_mat = difflib.SequenceMatcher(None, self.text, new_text)
            for tag, i1, i2, j1, j2 in seq_mat.get_opcodes():
                print(f"Opcode: {tag}, {i1}, {i2}, {j1}, {j2}")

                if (tag in ["delete", "replace"]):
                    for i in reversed(range(i1, i2)):
                        self.input_image_labels[i].destroy()
                        del self.input_image_labels[i]
                        del self.answer_flags[i]
                
                if (tag in ["insert", "replace"]):
                    for j in range(j1, j2):
                        inputChar = "SPACJA" if new_text[j] == " " else new_text[j].upper()
                        self.flag_input_handler(None, inputChar, i1)
                        i1 += 1

            self.text = self.top_menu.input_text.get("1.0", "end - 1c")
            # length = len(self.top_menu.input_text.get("1.0", "end - 1c"))
            # if (self.top_menu.input_text.edit_modified()):
            #     print("Textbox callback ", length)
            #     if (length < self.text_length):
            #         for i in reversed(range(length, self.text_length)):
            #             self.input_images[i].destroy()
            #             del self.input_images[i]
            #             del self.answer_flags[i]

            #     for i in reversed(range(length)):
            #         char = self.top_menu.input_text.get(f"1.0+{i}c").upper()
            #         if (i < len(self.answer_flags)):
            #             flagChar = " " if self.answer_flags[i] is None else self.answer_flags[i].code_word[0].upper()
            #             if (char != flagChar):
            #                 self.input_images[i].destroy()
            #                 del self.input_images[i]
            #                 del self.answer_flags[i]
            #             else: continue
            #         inputChar = "SPACJA" if char == " " else ord(char) - 65
            #         self.flag_input_handler(None, inputChar, i)
            #     self.top_menu.input_text.edit_modified(False)
            # self.text_length = length

        self.top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)
        
        self.top_menu.input_text = ctk.CTkTextbox(self.top_menu, width=400, height=0)
        self.top_menu.input_text.pack(side="left", fill="y", padx=10)
        self.top_menu.input_text.focus()

        self.text = self.top_menu.input_text.get("1.0", "end - 1c")
        self.master.bind("<KeyPress>", input_callback)
        self.master.bind("<Control-Key-a>", lambda event: Util.text_select_all(event, self.top_menu.input_text))
        self.master.bind("<Control-Key-A>", lambda event: Util.text_select_all(event, self.top_menu.input_text))

        self.top_menu.check_button = ctk.CTkButton(self.top_menu, text="Zapisz...", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)))
        self.top_menu.check_button.pack(side="right", ipadx=10, ipady=10)

        def checkbox_event():
            print('checkbox toggled, current value:', check_var.get())
            self.is_transparent = 'transparent' if check_var.get() == 'on' else 'grey'
        
        check_var = ctk.StringVar(value='off')
        self.top_menu.checkbox = ctk.CTkCheckBox(self.top_menu, text='Transparentne tło', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.01)), command=checkbox_event, 
                                                 variable=check_var, onvalue='on', offvalue='off')
        self.top_menu.checkbox.pack(side="right", padx=10)

        self.input_parent = ctk.CTkFrame(self, height=int(self.winfo_width()*0.1), fg_color="transparent")
        self.input_parent.pack(side="top", fill="x", padx=10)
        self.flag_input_box = ctk.CTkScrollableFrame(self.input_parent, height=int(self.master.scale_size*0.05), orientation="horizontal")
        # self.master.bind("<BackSpace>", self.delete_input_flag)
        self.flag_input_box.pack(side="top", fill="x")

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(side="top", fill="both", expand=True)

        self.input_rows = 5
        self.input_columns = 9
        for i in range(self.input_rows):
            self.input_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.input_columns):
            self.input_frame.grid_columnconfigure(j, weight=1)

        for f in self.alphabet.values():
            if (self.master.winfo_height() < self.master.winfo_width()):
                self.images.append(tksvg.SvgImage(file=Environment.resource_path(f.img_path), scaletoheight=int(self.master.scale_size*0.8/self.input_columns)))
            else:
                self.images.append(tksvg.SvgImage(file=Environment.resource_path(f.img_path), scaletowidth=int(self.master.scale_size*0.8/self.input_columns)))
            
        
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

                if (not tuple):
                    flag_container.grid(row=i, column=j, columnspan=self.input_columns, sticky="nsew")
                    flag_container.flag = ctk.CTkLabel(flag_container, text='SPACJA', text_color="blue", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), cursor="hand2")
                    flag_container.flag.bind("<Button-1>", command=lambda event, i='SPACJA': self.flag_input_handler(event, char=i))
                else:
                    flag_container.grid(row=i, column=j, sticky="nsew")
                    flag_container.flag = ctk.CTkLabel(flag_container, text='', image=self.images[tuple[0]], cursor="hand2")
                    flag_container.flag.bind("<Button-1>", command=lambda event, i=tuple[1]: self.flag_input_handler(event, char=i))
                flag_container.flag.grid(ipadx=10, ipady=10)
                self.flag_images.append(flag_container)

                if (not tuple): return

    def flag_input_handler(self, event=None, char: str = "", pos: int = -1):
        """Handler function for clicking on flags.
        """
        if (char == ""):
            return
        
        print(f"New flag {char}")
        if (pos == -1): pos = len(self.answer_flags)
        if (char in ["SPACJA", "\n"]):
            txt = '  ' if char == "\n" else "␣"
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text=txt, font=ctk.CTkFont(size=int(self.master.scale_size*0.05), weight='bold'), text_color="blue", fg_color='transparent')
            new_input_flag.pack(side="left", padx=1)
            self.input_image_labels.insert(pos, new_input_flag)
            self.answer_flags.insert(pos, None)
            if (event is not None):
                self.top_menu.input_text.insert('end', ' ')
        else:
            try:
                input_image = tksvg.SvgImage(file=Environment.resource_path(self.alphabet[char].img_path), scaletoheight=int(self.master.scale_size*0.04))
                new_input_flag = ctk.CTkLabel(self.flag_input_box, text='', image=input_image)
                before = {"before": self.input_image_labels[pos]} if (pos < len(self.answer_flags)) else {}
                new_input_flag.pack(side="left", padx=1, **before)

                self.input_image_labels.insert(pos, new_input_flag)
                self.answer_flags.insert(pos, self.alphabet[char])
                if (event is not None):
                    self.top_menu.input_text.insert('end', self.alphabet[char].code_word[0])
            except KeyError:
                print("Invalid character")
                self.top_menu.input_text.delete(f"1.{pos}")
            
        self.text = self.top_menu.input_text.get("1.0", "end - 1c")

    def save_image(self):
        if (not self.text): return
        if Alphabet.saveFlagSentencePNG(self.answer_flags, background=self.is_transparent):
            label = ctk.CTkLabel(self.top_menu, text='Zapisano.', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
            label.pack(side="right", padx=10)
            label.after(4000, lambda: label.destroy())
    
    def unbind(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<Control-Key-a>")
        self.master.unbind("<Control-Key-A>")
        super().unbind()