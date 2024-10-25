import customtkinter as ctk
import tksvg

from logic.environment import Environment
import gui.util_functions as Util
from gui.countdown import add_countdown_timer_to_top_menu
from logic.modes.codewords_session import CodewordsSession

class Codewords(Util.AppQuizPage):
    def __init__(self, master, questions_number: int = 0, time_minutes: int = 0, **kwargs):
        """Class for initializing the codewords screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing codewords frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.questions_number = questions_number
        self.time_minutes = time_minutes
        print(f"Questions number: {questions_number}, time: {time_minutes}")

        # self.flag_list = random.sample(list(Alphabet._characters.values()), 3) # randomly choose a flag, change later
        # self.flag_list = [Alphabet._characters['A'], Alphabet._characters['B'], Alphabet._characters['C']] # randomly choose a flag, change later
        self.codewords_session = CodewordsSession(questions_number) if questions_number > 0 else CodewordsSession()

        self.flag_index = 0
    
    def draw(self):
        super().draw()

        if (self.time_minutes > 0):
            self.countdown = add_countdown_timer_to_top_menu(self)

        self.question_widgets = []
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.pack(fill="both", expand=True)
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_rowconfigure(1, weight=3)
        self.container_frame.grid_rowconfigure(2, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1, uniform="side")
        self.container_frame.grid_columnconfigure(1, weight=3)
        self.container_frame.grid_columnconfigure(2, weight=1, uniform="side")

        self.next_question()

    def show_question(self):
        """Make sure to first make the main Codewords frame visible with the place/pack/grid functions
        """
        for widget in self.question_widgets:
            widget.destroy()
        self.update_idletasks()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()

        self.answer_response = ctk.CTkLabel(self.container_frame, text='', font=ctk.CTkFont(size=int(self.master.scale_size*0.04)), fg_color='transparent')
        self.answer_response.grid(row=0, column=1)
        self.question_widgets.append(self.answer_response)
        
        img = tksvg.SvgImage(file=Environment.resource_path(self.flag.img_path), scaletoheight=int(self.master.scale_size*0.5))
        self.image = ctk.CTkLabel(self.container_frame, text='', image=img)
        self.image.grid(row=1, column=0, columnspan=3, sticky="n")
        self.question_widgets.append(self.image)

        self.answer_cell = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.answer_cell.grid(row=2, column=1, pady=10)
        self.question_widgets.append(self.answer_cell)

        print(self.flag.code_word)
        self.answer_cell.entry = ctk.CTkEntry(self.answer_cell, font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), width=int(self.master.scale_size*0.3), validate="key")
        self.answer_cell.entry.bind("<Return>", lambda x: self.enter_answer())
        self.answer_cell.entry.pack(side="left")
        self.answer_cell.entry.focus()
        
        self.answer_cell.submit_button = ctk.CTkButton(self.answer_cell, text='Sprawdź', font=ctk.CTkFont(size=int(self.master.scale_size*0.025)), width=0, command=self.enter_answer)
        self.answer_cell.submit_button.pack(side="left", padx=5, fill='y')

        def skip_command():
            next_exists = self.codewords_session.next_flag()
            self.next_question() if next_exists else self.finish()

        self.question_widgets.append(self.add_skip_button(skip_command))

        try:
            self.countdown.startCountdown()
        except AttributeError: pass


    def enter_answer(self):
        if (not self.codewords_session.check_answer(self.answer_cell.entry.get())):
            print("Wrong answer.")
            self.answer_response.configure(text='Źle')
        else:
            print("Correct answer!")
            self.answer_response.configure(text='Poprawnie!')

            self.answer_cell.entry.configure(state="disabled")
            self.answer_cell.submit_button.configure(state="disabled")

            # next button
            next_exists = self.codewords_session.next_flag()
            next_command = self.next_question if next_exists else self.finish
            next_text = "Następny" if next_exists else "Wyniki"
            if (not next_exists):
                try:
                    self.countdown.pause()
                except AttributeError: pass

            self.master.bind("<Return>", lambda x: next_command())
            self.next_button = ctk.CTkButton(self.container_frame, text=next_text, font=ctk.CTkFont(size=int(self.master.scale_size*0.025)), 
                                                height=int(self.master.scale_size*0.18), width=int(self.master.scale_size*0.14), command=next_command)
            self.update()
            self.next_button.grid(row=1, column=2)
            self.question_widgets.append(self.next_button)
    
    def next_question(self):
        self.master.unbind("<Return>")
        self.flag = self.codewords_session.get_flag()
        self.show_question()