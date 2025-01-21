import customtkinter as ctk
import tksvg
import math
from logic.environment import Environment
from logic.flags import *
from logic.alphabet import Alphabet
from logic.exceptions import *
import gui.util_functions as Util
from gui.countdown import add_countdown_timer_to_top_menu
from logic.modes.flagsen_session import FlagsenSession

class FlagSen(Util.AppQuizPage, Util.ISkippablePage):
    def __init__(self, master, source: str = "default", questions_number: int = 0, time_minutes: int = 0, **kwargs):
        """Class for initializing the Flags-sentence screen

        To draw the question, call show_question AFTER making this frame visible with the place/pack/grid functions
        """
        super().__init__(master, **kwargs)
        print("Initializing codewords frame")
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.source = source
        self.questions_number = questions_number
        self.time_minutes = time_minutes
        print(f"Questions number: {questions_number}, time: {time_minutes}")
        
        self.question_widgets = []
    
    def draw(self):
        super().draw()

        if (self.time_minutes > 0):
            self.countdown = add_countdown_timer_to_top_menu(self, self.time_minutes)

        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.pack(fill="both", expand=True)
        self.container_frame.grid_rowconfigure(0, weight=0)
        self.container_frame.grid_rowconfigure(1, weight=3)
        self.container_frame.grid_rowconfigure(2, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(1, weight=3)
        self.container_frame.grid_columnconfigure(2, weight=0)

        def save_image():
            if (Alphabet.saveFlagSentencePNG(self.question.flags, suggest_file_name=self.is_answered)):
                label = ctk.CTkLabel(self.container_frame, text='Zapisano.', font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), fg_color='transparent')
                label.grid(column=1, row=0, sticky="e", pady=10)
                label.after(4000, lambda: label.destroy())
        
        self.save_image = ctk.CTkButton(self.container_frame, text='Zapisz obecne jako zdjęcie...', width=0, font=ctk.CTkFont(size=int(self.master.winfo_width()*0.015)), command=save_image)
        self.save_image.grid(column=2, row=0, sticky="ne", ipadx=10, ipady=10, padx=10, pady=10)

        # self.options = Util.options_menu(self, self.establish_session)
        self.establish_session(self.source)

    def establish_session(self, source: str):
        error_text = ""
        try:
            self.session = FlagsenSession(source, self.questions_number)
        except NoInternetConnectionException:
            error_text = "Brak połączenia z internetem."
        except RequestLimitExceededException:
            error_text = "Limit zapytań cytatów został osiągnięty, prosimy chwilę poczekać."
        except SmthWrongWithFileException:
            error_text = "Błąd czytania z pliku."
        except Exception:
            error_text = "Wystąpił błąd."

        if (error_text != ""):
            error_message = ctk.CTkLabel(self, text=error_text, font=ctk.CTkFont(size=int(self.master.scale_size*0.05)), fg_color='white')
            error_message.place(relx=0.5, rely=0.5)
            return
        
        self.next_question()

    def show_question(self):
        """Make sure to first make the main FlagSen frame visible with the place/pack/grid functions
        """
        loading_label = Util.loading_widget(self.winfo_toplevel())
        for widget in self.question_widgets:
            widget.destroy()
        self.update()
        self.master.scale_size = self.master.winfo_height() if (self.master.winfo_height() < self.master.winfo_width()) else self.master.winfo_width()
        self.is_answered = False

        print(self.question.original_sentence)
        self.flag_sentence = ctk.CTkFrame(self.container_frame, fg_color=None)
        self.flag_sentence.grid(row=1, column=0, columnspan=3)
        self.flag_sentence.flags = []

        self.answer_response = ctk.CTkLabel(self.container_frame, text='', font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), fg_color='transparent')
        self.answer_response.grid(row=0, column=0, columnspan=3)
        self.question_widgets.append(self.answer_response)

        flag_columns = 12
        flag_rows = math.floor(len(self.question.flags)/flag_columns)
        for i in range(flag_rows):
            self.flag_sentence.grid_rowconfigure(i, weight=1)
        for i in range(flag_columns):
            self.flag_sentence.grid_columnconfigure(i, weight=1, uniform="yes")

        for i, flag in enumerate(self.question.flags):
            img = None
            if (self.master.winfo_height() < self.master.winfo_width()):
                img = tksvg.SvgImage(file=Environment.resource_path(flag.img_path), scaletoheight=int(self.master.scale_size*0.1)) if (flag is not None) else None
            else:
                img = tksvg.SvgImage(file=Environment.resource_path(flag.img_path), scaletowidth=int(self.master.scale_size*0.05)) if (flag is not None) else None
            image = ctk.CTkLabel(self.flag_sentence, text='', image=img, fg_color="transparent")
            image.grid(row=math.floor(i/(flag_columns+1)), column=(i%(flag_columns+1)), padx=2, pady=10)
            self.flag_sentence.flags.append(image)
        
        self.question_widgets.append(self.flag_sentence)

        self.answer_cell = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.answer_cell.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        self.question_widgets.append(self.answer_cell)
        self.answer_cell.grid_columnconfigure(0, weight=1, minsize=int(self.master.scale_size*0.05))
        self.answer_cell.grid_columnconfigure(1, weight=0)
        self.answer_cell.grid_columnconfigure(2, weight=1, minsize=int(self.master.scale_size*0.1))

        self.entry_font = ctk.CTkFont(size=int(self.master.scale_size*0.03))
        validate_command = self.register(self.validate_answer)

        self.answer_cell.entry = ctk.CTkEntry(self.answer_cell, width=int(self.master.scale_size*0.6), font=self.entry_font,
                                              validate="key", validatecommand=(validate_command,'%P'))
        self.answer_cell.entry.bind("<Return>", self.enter_answer)
        self.answer_cell.entry.grid(row=0, column=1, sticky="ew")
        self.answer_cell.entry.focus()

        self.text_length = ctk.CTkLabel(self.answer_cell, text=f"0/{len(self.question.cleaned_sentence)}", width=int(self.master.scale_size*0.05), fg_color='transparent')
        self.text_length.grid(row=0, column=0, sticky="e", padx=10)
        
        self.answer_cell.submit_button = ctk.CTkButton(self.answer_cell, text='Sprawdź', font=ctk.CTkFont(size=int(self.master.scale_size*0.03)), command=self.enter_answer)
        self.answer_cell.submit_button.grid(row=0, column=2, sticky="e", padx=5)

        self.skip_button = self.add_skip_button(self.skip_command)
        self.question_widgets.append(self.skip_button)

        self.update_idletasks()
        try:
            self.countdown.startCountdown()
        except AttributeError: pass
        loading_label.destroy()

    def skip_command(self):
        print("Skipped.")
        self.answer_response.configure(text='Pominięto.')
        self.answer_cell.entry.delete(0, 'end')
        self.answer_cell.entry.insert(0, self.session.get_correct_answer())
        self.answer_cell.entry.configure(state="disabled")
        self.answer_cell.submit_button.configure(command=None)
        self.answer_cell.entry.unbind("<Return>")
        self.skip_button.configure(command=None)
        self.show_next_button()

    def validate_answer(self, new_text):
        if (len(new_text) > len(self.question.cleaned_sentence)): return False
        self.text_length.configure(text=f"{len(new_text)}/{len(self.question.cleaned_sentence)}")

        text_pixel_length = self.entry_font.measure(new_text)
        if (text_pixel_length > int(self.master.scale_size*0.55)):
            self.answer_cell.entry.configure(width=text_pixel_length + 35)
        return True

    def enter_answer(self, event=None):
        # try:
        #     self.answer_response.destroy()
        # except AttributeError: pass
        # correct_answer = self.flag.letter[0].upper()
        
        if (not self.session.check_answer(self.answer_cell.entry.get())):
            print("Wrong answer.")
            self.answer_response.configure(text='Źle')
            return
        
        print("Correct answer!")
        self.is_answered = True
        self.answer_response.configure(text='Poprawnie')

        self.answer_cell.entry.configure(state="disabled")
        self.answer_cell.entry.unbind("<Return>")
        self.skip_button.configure(command=None)
        
        self.update() # for internet delays, so that the user knows if it was right immediately
        self.show_next_button()

    def show_next_button(self):
        next_exists = self.session.next_question()
        next_command = self.next_question if next_exists else self.finish
        next_text = "Nowe zdanie" if next_exists else "Wyniki"
        if (not next_exists):
            try:
                self.countdown.pause()
            except AttributeError: pass
        
        self.answer_cell.submit_button.configure(text=next_text, command=next_command)

    def next_question(self):
        self.question = self.session.get_question()
        self.show_question()
