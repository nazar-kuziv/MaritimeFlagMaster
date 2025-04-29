import cProfile
from tkinter import Event

import customtkinter as ctk
import tksvg

import gui.util_functions as Util
from logic.alphabet import Alphabet
from logic.environment import Environment


class MakeImage(Util.AppPage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        print("Initializing meanings frame")
        self.master.scale_size = self.master.winfo_height() if (
                    self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.alphabet = dict(Alphabet._characters, **Alphabet._additionalFlags)
        self.flag_index = 0
        self.images = []
        self.bg_color = "grey"
        self.flag_images = []
        self.preview = None
    
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
        #     self.preview_frame.destroy()
        # except AttributeError: print("Couldn't destroy preview_label")
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (
                    self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        
        def show_preview():
            text = self.top_menu.input_text.get("1.0", "end - 1c")
            img_path, height, width = Alphabet.get_flag_sentence_svg(text, self.bg_color)

            scale_size = ({"scaletowidth": int(self.preview_frame.winfo_width()*0.9)}
                          if (width > height)
                          else {"scaletoheight": int(self.preview_frame.winfo_height()*0.9)})

            self.preview_img = tksvg.SvgImage(file=img_path, **scale_size)
            # self.preview_img = tksvg.SvgImage(file=r'C:\Users\firek\Desktop\repos\MaritimeFlagMaster\static\graphics\example.svg', **scale_size)
            self.preview_label.configure(image=self.preview_img, text="")

            print("Preview updated")

        def input_callback(event: Event):
            if (event.state & 4 and event.keysym in "vV"):
                Util.text_paste(event, self.top_menu.input_text)

            if (self.preview):
                self.after_cancel(self.preview)
            self.preview = self.after(750, show_preview)
            # new_text: str = self.top_menu.input_text.get("1.0", "end - 1c")
            # if (new_text == self.text): return
            
            # print(f"New text: {new_text}")
            # seq_mat = difflib.SequenceMatcher(None, self.text, new_text)
            # shift = 0   # opcodes indices don't take into account changes after insert and delete operations

            # def get_pos(i, text) -> list[int]: # starts from 0.0
            #     i += shift
            #     pos = text[:i+1].splitlines(keepends=True)
            #     return [len(pos)-1, len(pos[-1])-1]

            # for tag, i1, i2, j1, j2 in seq_mat.get_opcodes():
            #     print(f"Opcode: {tag}, {i1}, {i2}, {j1}, {j2}")
                
            #     if (tag in ["delete", "replace"]):
            #         self.flag_delete_handler(get_pos(i1, self.text), i2-i1, False)
            #         shift -= i2-i1
                
            #     if (tag in ["insert", "replace"]):
            #         pos1 = get_pos(i1, new_text)
            #         for j in range(j1, j2):
            #             self.flag_input_handler(None, new_text[j].upper(), tuple(pos1))
            #             if (new_text[pos1[1]] == "\n"):
            #                 pos1[0] += 1
            #                 pos1[1] = -1
            #             pos1[1] += 1
            #         shift += j2-j1

            # self.text = self.top_menu.input_text.get("1.0", "end - 1c")

        self.top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)

        self.top_menu.input_text = ctk.CTkTextbox(self.top_menu, width=400, height=0)
        self.top_menu.input_text.pack(side="left", fill="y", padx=10)
        self.top_menu.input_text.focus_set()

        self.top_menu.backspace_button = ctk.CTkButton(self.top_menu, text="Kasuj", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.flag_delete_handler)
        self.top_menu.backspace_button.pack(side="left", ipadx=10, ipady=10, padx=5)

        self.top_menu.clear_button = ctk.CTkButton(self.top_menu, text="Wyczyść", width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=self.flag_clear_handler)
        self.top_menu.clear_button.pack(side="left", ipadx=10, ipady=10, padx=5)

        # self.text = self.top_menu.input_text.get("1.0", "end - 1c")
        self.master.bind("<KeyPress>", input_callback)
        self.master.bind("<Control-Key-a>", lambda event: Util.text_select_all(event, self.top_menu.input_text))
        self.master.bind("<Control-Key-A>", lambda event: Util.text_select_all(event, self.top_menu.input_text))

        self.top_menu.check_button = ctk.CTkButton(self.top_menu, text="Zapisz...", width=0,
                                                   font=ctk.CTkFont(size=int(self.master.winfo_width() * 0.015)),
                                                   command=self.save_image)
        self.top_menu.check_button.pack(side="right", ipadx=10, ipady=10)

        def checkbox_event():
            print("checkbox toggled, current value:", check_var.get())
            self.bg_color = "transparent" if check_var.get() == "on" else "grey"
        
        check_var = ctk.StringVar(value="off")
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
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Zacznij pisać...")
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
                    flag_container.flag.bind("<Button-1>", command=lambda event, i=" ": self.flag_input_handler(event, char=i))
                else:
                    flag_container.flag = ctk.CTkLabel(flag_container, text="", image=self.images[tuple[0]], cursor="hand2")
                    flag_container.flag.bind("<Button-1>", command=lambda event, i=tuple[1]: self.flag_input_handler(event, char=i))
                flag_container.flag.grid(ipadx=8, ipady=10, sticky="nsew")
                self.flag_images.append(flag_container)

                if (not tuple):
                    flag_container2 = ctk.CTkFrame(self.input_frame, fg_color="transparent")
                    flag_container2.grid_rowconfigure(0, weight=1)
                    flag_container2.grid_columnconfigure(0, weight=1)
                    flag_container2.grid(row=i, column=j+1, sticky="nsew")
                    flag_container2.rtrn = ctk.CTkLabel(flag_container2, text="⏎", text_color="blue", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.025)), justify="center", cursor="hand2")
                    flag_container2.rtrn.bind("<Button-1>", command=lambda event, i="\n": self.flag_input_handler(event, char=i))
                    flag_container2.rtrn.grid(row=0, column=1, ipadx=8, ipady=10, sticky="nsew")
                    self.flag_images.append(flag_container2)
                    return

    # def flag_input_handler(self, event=None, char: str = "", pos: tuple[int, int] = (-1, -1)):
    #     """Handler function for clicking on flags.
    #     """
    #     if (char == ""):
    #         return
        
    #     if (pos == (-1, -1)):
    #         pos = (len(self.input_image_labels)-1, len(self.input_image_labels[-1]))
    #     print(f"New flag {char} at position {pos[0]}.{pos[1]}")

    #     # if (char == "\n"):
    #     #     self.answer_flags.insert(pos[2], (None if char == "\n" else ""))
    #     if (char in " \n"):
    #         new_input_flag = ctk.CTkLabel(self.preview_label, text=("␣" if char == " " else "⏎"), font=ctk.CTkFont(size=int(self.master.scale_size*0.03), weight="bold"), text_color="blue", fg_color="transparent")
    #         self.answer_flags[pos[0]].insert(pos[1], (None if char == "\n" else ""))
    #         if (char == "\n"):
    #             self.answer_flags.insert(pos[0]+1, [])
    #             self.input_image_labels.insert(pos[0]+1, [])
            
    #         # def move_row(img_list: list, char_list: list, pos1: int, pos2: int):
    #         #     move_number = 1
    #         #     col = 0
    #         #     for _ in range(len(img_list[pos1])-1 - pos2):    # Put the next characters in a new row
    #         #         img_list[pos1+move_number].insert(col, img_list[pos1][pos2+col])
    #         #         img_list[pos1+move_number][col].grid(row=pos1+move_number, column=col, padx=1)
    #         #         del img_list[pos1][pos2]

    #         #         char_list[pos1+move_number].insert(col, char_list[pos1][pos2+col])
    #         #         del char_list[pos1][pos2]

    #         #         col += 1
    #         #         if (char_list[pos1] is None):
    #         #             move_number += 1
    #         #             col = 0

    #         if (char == "\n" and pos[1] < len(self.input_image_labels[pos[0]])):      # If newline and there are characters after it
    #             print(f"newline inserted, {len(self.input_image_labels[pos[0]]) - pos[1]}")
    #             # for col in range(len(self.input_image_labels[pos[0]])-1 - pos[1]):    # Put the next characters in a new row
    #             #     self.input_image_labels[pos[0]+1].insert(col, self.input_image_labels[pos[0]][pos[1]+col])
    #             #     self.input_image_labels[pos[0]+1][col].grid(row=pos[0]+1, column=col, padx=1)
    #             #     del self.input_image_labels[pos[0]][pos[1]]

    #             #     self.answer_flags[pos[0]+1].insert(col, self.answer_flags[pos[0]][pos[1]+col])
    #             #     del self.answer_flags[pos[0]][pos[1]]
    #             move_number = 1
    #             col = 0
    #             for _ in range(len(self.input_image_labels[pos[0]]) - pos[1]):    # Put the next characters in a new row
    #                 # if (len(self.input_image_labels) <= pos[0]+move_number):
    #                 #     self.input_image_labels[pos[0]+move_number] = []
    #                 #     self.answer_flags[pos[0]+move_number] = []
    #                 self.input_image_labels[pos[0]+move_number].insert(col, self.input_image_labels[pos[0]].pop(pos[1]))
    #                 self.input_image_labels[pos[0]+move_number][col].grid(row=pos[0]+move_number, column=col, padx=1)
    #                 # del self.input_image_labels[pos[0]][pos[1]]

    #                 self.answer_flags[pos[0]+move_number].insert(col, self.answer_flags[pos[0]].pop(pos[1]))
    #                 # del self.answer_flags[pos[0]][pos[1]]

    #                 col += 1
    #                 if (self.answer_flags[pos[0]] is None):
    #                     move_number += 1
    #                     col = 0
            
    #         if (event is not None):
    #             self.top_menu.input_text.insert("end", char)
    #     else:
    #         try:
    #             input_image = tksvg.SvgImage(file=Environment.resource_path(self.alphabet[char].img_path), scaletoheight=int(self.master.scale_size*0.04))
    #             new_input_flag = ctk.CTkLabel(self.preview_label, text="", image=input_image)
    #             self.answer_flags[pos[0]].insert(pos[1], self.alphabet[char])
    #             if (event is not None):
    #                 self.top_menu.input_text.insert("end", self.alphabet[char].code_word[0])
    #         except KeyError:
    #             print("Invalid character")
    #             self.top_menu.input_text.delete(f"{pos[0]+1}.{pos[1]}")

    #     if (pos[1] < len(self.input_image_labels[pos[0]])):
    #         for i in range(pos[1], len(self.input_image_labels[pos[0]])):
    #             self.input_image_labels[pos[0]][i].grid(row=pos[0], column=i+1, padx=1)

    #     new_input_flag.grid(row=pos[0], column=pos[1], padx=1)
    #     self.input_image_labels[pos[0]].insert(pos[1], new_input_flag)

    #     self.text = self.top_menu.input_text.get("1.0", "end - 1c")
    #     print()

    def flag_delete_handler(self):
        # if (sum(len(x) for x in self.input_image_labels) <= num):
        #     self.flag_clear_handler()
        #     return

        # if (pos == (-1, -1)):
        #     pos1 = len(self.answer_flags)-1
        #     pos2 = len(self.answer_flags[-1])-1
        #     if (pos2 < 0):
        #         pos1 -= 1
        #         pos2 = len(self.answer_flags[-2])-1
        #     if (pos1 < 0): return
        #     pos = (pos1, pos2)
        # print(f"Deleting {num} characters from position {pos[0]}.{pos[1]}")

    #     for _ in range(num):
    #         self.input_image_labels[pos[0]][pos[1]].destroy()
    #         del self.input_image_labels[pos[0]][pos[1]]
    #         del self.answer_flags[pos[0]][pos[1]]
    #         if (pos[1] < len(self.answer_flags[pos[0]]) or 
    #             pos[0]+1 >= len(self.answer_flags) or len(self.answer_flags[pos[0]+1]) <= 0): continue
            
    #         if (pos[0]+1 >= len(self.answer_flags)): break
    #         self.answer_flags[pos[0]].extend(self.answer_flags.pop(pos[0]+1))
    #         self.input_image_labels[pos[0]].extend(self.input_image_labels.pop(pos[0]+1))

    #     start_col = pos[1]
    #     for row in range(pos[0], len(self.input_image_labels)):
    #         for col in range(start_col, len(self.input_image_labels[row])):
    #             self.input_image_labels[row][col].grid(row=row, column=col, padx=1)
    #         start_col = 0

        self.top_menu.input_text.delete("end - 2c")
        # self.text = self.top_menu.input_text.get("1.0", "end - 1c")

    def flag_clear_handler(self):
    #     print(f"Clearing input")
    #     for xs in self.input_image_labels:
    #         for x in xs:
    #             x.destroy()
        
    #     self.input_image_labels = [[]]
    #     self.answer_flags = [[]]
        self.top_menu.input_text.delete("1.0", "end")
    #     self.text = ""

    def save_image(self):
        if (not self.top_menu.input_text.get("1.0", "end - 1c")): return
        if Alphabet.saveFlagSentencePNG([x for xs in self.answer_flags for x in xs], background=self.bg_color):
            label = ctk.CTkLabel(self.top_menu, text="Zapisano.", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="transparent")
            label.pack(side="right", padx=10)
            label.after(4000, lambda: label.destroy())

    def unbind(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<Control-Key-a>")
        self.master.unbind("<Control-Key-A>")
        super().unbind()
