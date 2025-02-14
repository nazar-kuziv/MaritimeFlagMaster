import difflib
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
        self.is_transparent = "gray"
        self.flag_images = []
        self.answer_flags = [[]]
        self.input_image_labels = [[]]
    
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
        self.master.scale_size = self.master.winfo_height() if (
                    self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        def input_callback(event: Event):
            if (event.state & 4 and event.keysym in "vV"):
                Util.text_paste(event, self.top_menu.input_text)
            new_text: str = self.top_menu.input_text.get("1.0", "end - 1c")
            if (new_text == self.text): return

            print(f"New text: {new_text}")
            seq_mat = difflib.SequenceMatcher(None, self.text, new_text)
            for tag, i1, i2, j1, j2 in seq_mat.get_opcodes():
                print(f"Opcode: {tag}, {i1}, {i2}, {j1}, {j2}")

                def get_pos(i) -> list[int]:
                    pos = new_text[:i+1].splitlines(keepends=True)
                    return [len(pos)-1, len(pos[-1])-1]
                pos1, pos2, posj1, posj2 = list(map(get_pos, [i1, i2, j1, j2]))
                # pos1 = get_pos(i1)
                length = sum(len(x) for x in self.input_image_labels)

                if (tag in ["delete", "replace"]):
                    for i in reversed(range(i1, i2)):
                        if (i >= length): i = length - 1
                        pos = get_pos(i)
                        self.input_image_labels[pos[0]][pos[1]].destroy()
                        del self.input_image_labels[pos[0]][pos[1]]
                        del self.answer_flags[pos[0]][pos[1]]
                
                if (tag in ["insert", "replace"]):
                    for j in range(j1, j2):
                        self.flag_input_handler(None, new_text[j].upper(), tuple(pos1))
                        if (new_text[pos1[1]] == "\n"):
                            pos1[0] += 1
                            pos1[1] = -1
                        pos1[1] += 1

            self.text = self.top_menu.input_text.get("1.0", "end - 1c")

        self.top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.top_menu.pack(side="top", anchor="w", fill="x", padx=10, pady=10)

        self.top_menu.input_text = ctk.CTkTextbox(self.top_menu, width=400, height=0)
        self.top_menu.input_text.pack(side="left", fill="y", padx=10)
        self.top_menu.input_text.focus()

        self.text = self.top_menu.input_text.get("1.0", "end - 1c")
        self.master.bind("<KeyPress>", input_callback)
        self.master.bind("<Control-Key-a>", lambda event: Util.text_select_all(event, self.top_menu.input_text))
        self.master.bind("<Control-Key-A>", lambda event: Util.text_select_all(event, self.top_menu.input_text))

        self.top_menu.check_button = ctk.CTkButton(self.top_menu, text="Zapisz...", width=0,
                                                   font=ctk.CTkFont(size=int(self.master.winfo_width() * 0.015)),
                                                   command=self.save_image)
        self.top_menu.check_button.pack(side="right", ipadx=10, ipady=10)

        def checkbox_event():
            print("checkbox toggled, current value:", check_var.get())
            self.is_transparent = "transparent" if check_var.get() == "on" else "gray"
        
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

        self.input_parent = ctk.CTkFrame(self, fg_color="transparent")
        self.input_parent.pack(side="left", fill="both", expand=True, padx=10)
        self.flag_input_box = ctk.CTkScrollableFrame(self.input_parent, orientation="horizontal", label_anchor="center")
        self.flag_input_box.pack(side="left", fill="both", expand=True)
        
        
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

                flag_container.grid(row=i, column=j, sticky="nsew")
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

    def flag_input_handler(self, event=None, char: str = "", pos: tuple[int, int] = (-1, -1)):
        """Handler function for clicking on flags.
        """
        if (char == ""):
            return
        
        print(f"New flag {char} at position {pos[0]}.{pos[1]}")
        if (pos == (-1, -1)):
            pos = (len(self.input_image_labels)-1, len(self.input_image_labels[-1])-1)

        # if (char == "\n"):
        #     self.answer_flags.insert(pos[2], (None if char == "\n" else ""))
        if (char in " \n"):
            new_input_flag = ctk.CTkLabel(self.flag_input_box, text=("␣" if char == " " else "⏎"), font=ctk.CTkFont(size=int(self.master.scale_size*0.05), weight="bold"), text_color="blue", fg_color="transparent")
            self.answer_flags[pos[0]].insert(pos[1], (None if char == "\n" else ""))

            if (char == "\n" and pos[1] < len(self.input_image_labels[pos[0]])):      # If newline and there are characters after it
                for col in range(len(self.input_image_labels[pos[0]])-1 - pos[1]):    # Put the next characters in a new row
                    self.input_image_labels[pos[0]+1].insert(col, self.input_image_labels[pos[0]][pos[1]+col])
                    self.input_image_labels[pos[0]+1][col].grid(row=pos[0]+1, column=col, padx=1)
                    del self.input_image_labels[pos[0]][pos[1]]

                    self.answer_flags[pos[0]+1].insert(col, self.answer_flags[pos[0]][pos[1]+col])
                    del self.answer_flags[pos[0]][pos[1]]
            
            if (event is not None):
                self.top_menu.input_text.insert("end", char)
        else:
            try:
                input_image = tksvg.SvgImage(file=Environment.resource_path(self.alphabet[char].img_path), scaletoheight=int(self.master.scale_size*0.04))
                new_input_flag = ctk.CTkLabel(self.flag_input_box, text="", image=input_image)
                self.answer_flags[pos[0]].insert(pos[1], self.alphabet[char])
                if (event is not None):
                    self.top_menu.input_text.insert("end", self.alphabet[char].code_word[0])
            except KeyError:
                print("Invalid character")
                self.top_menu.input_text.delete(f"{pos[0]+1}.{pos[1]}")

        if (pos[1] < len(self.input_image_labels[pos[0]])):
            for i in range(pos[1], len(self.input_image_labels[pos[0]])):
                self.input_image_labels[pos[0]][i].grid(row=pos[0], column=i+1, padx=1)

        new_input_flag.grid(row=pos[0], column=pos[1], padx=1)
        self.input_image_labels[pos[0]].insert(pos[1], new_input_flag)

        self.text = self.top_menu.input_text.get("1.0", "end - 1c")
        print()

    def save_image(self):
        if (not self.text): return
        if Alphabet.saveFlagSentencePNG([x for xs in self.answer_flags for x in xs], background=self.is_transparent):
            label = ctk.CTkLabel(self.top_menu, text="Zapisano.", font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color="transparent")
            label.pack(side="right", padx=10)
            label.after(4000, lambda: label.destroy())

    def unbind(self):
        self.master.unbind("<KeyPress>")
        self.master.unbind("<Control-Key-a>")
        self.master.unbind("<Control-Key-A>")
        super().unbind()
