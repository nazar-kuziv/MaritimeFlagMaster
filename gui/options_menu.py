import customtkinter as ctk
import gui.util_functions as Util
from typing import Type

class OptionsMenu(Util.AppPage):

    def __init__(self, master, next_page: Type[Util.AppPage], select_source: bool = False, questions_amount_choices: list[int] = [5, 10, 20], questions_amount_def_ind: int = 1, time_minutes_choices: list[int] = [5, 10, -1], time_minutes_def_ind: int = 0):
        """Frame for selecting various options for the picked mode

        :param forward_function: function used by the start button/source selection buttons
        :type forward_function: Callable
        :param select_source: if True shows 3 source select buttons instead of a simple Start button, defaults to False
        :type select_source: bool, optional
        """
        super().__init__(master, fg_color="transparent")
        self.next_page = next_page
        self.select_source = select_source
        self.questions_amount_choices = questions_amount_choices
        self.questions_amount_def_ind = questions_amount_def_ind
        self.time_minutes_choices = time_minutes_choices
        self.time_minutes_def_ind = time_minutes_def_ind
    
    def draw(self):
        super().draw()
        menu = ctk.CTkFrame(self, fg_color="transparent")
        menu.pack(fill="both", expand=True)
        menu.grid_columnconfigure(0, weight=1)
        menu.grid_columnconfigure(1, weight=1)
        menu.grid_rowconfigure(0, weight=1)
        menu.grid_rowconfigure(1, weight=0)
        menu.grid_rowconfigure(2, weight=1)

        menu.questions_amount = self.questions_amount_choices[self.questions_amount_def_ind]
        menu.time_minutes = self.time_minutes_choices[self.time_minutes_def_ind]

        def numbers_to_labels(nums: list):
            labels = []
            for n in nums:
                if (n <= 0):
                    labels.append("Bez limitu")
                else:
                    labels.append(str(n))
            return labels

        amounts = numbers_to_labels(self.questions_amount_choices)
        amount_label = ctk.CTkLabel(menu, text='Liczba pytań', fg_color='transparent')
        amount_label.grid(column=0, row=0, padx=5, pady=5, sticky="se")
        amount_var = ctk.StringVar(value=amounts[self.questions_amount_def_ind])
        def optionmenu_callback(choice):
            nonlocal menu
            print('optionmenu dropdown clicked:', choice)
            menu.questions_amount = int(choice)
        amount_options = ctk.CTkOptionMenu(menu, values=amounts,
                                            command=optionmenu_callback,
                                            variable=amount_var)
        amount_options.grid(column=1, row=0, padx=5, pady=5, sticky="sw")

        times = numbers_to_labels(self.time_minutes_choices)
        time_label = ctk.CTkLabel(menu, text='Limit czasu (minuty)', width=40, height=28, fg_color='transparent')
        time_label.grid(column=0, row=1, padx=5, pady=5, sticky="ne")
        time_var = ctk.StringVar(value=times[self.time_minutes_def_ind])
        def optionmenu_callback(choice):
            nonlocal menu
            print('optionmenu dropdown clicked:', choice)
            menu.time_minutes = int(choice)
        time_options = ctk.CTkOptionMenu(menu, values=times,
                                                command=optionmenu_callback,
                                                variable=time_var)
        time_options.grid(column=1, row=1, padx=5, pady=5, sticky="nw")

        if (not self.select_source):
            start_button = ctk.CTkButton(menu, text='Start', font=ctk.CTkFont(size=int(self.winfo_width()*0.015)), command=self.create_next_page)
            start_button.grid(column=0, row=2, columnspan=2, pady=5, sticky="n")
            return

        source_select_frame = ctk.CTkFrame(menu, fg_color="transparent")
        source_select_frame.grid(column=0, row=2, columnspan=2, pady=5, sticky="n")
        default_mode_button = ctk.CTkButton(source_select_frame, text='Wbudowane', font=ctk.CTkFont(size=int(self.winfo_width()*0.015)), 
                                                    command=lambda: self.create_next_page(source="default"))
        default_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)

        internet_mode_button = ctk.CTkButton(source_select_frame, text='Z internetu', font=ctk.CTkFont(size=int(self.winfo_width()*0.015)), 
                                                    command=lambda: self.create_next_page(source="internet"))
        internet_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)
        
        file_mode_button = ctk.CTkButton(source_select_frame, text='Z pliku...', font=ctk.CTkFont(size=int(self.winfo_width()*0.015)), 
                                                command=lambda: self.create_next_page(source="file"))
        file_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)

    def create_next_page(self, **kwargs):
        page = self.next_page(self.master, fg_color="transparent", **kwargs)
        Util.change_page(page)
        # Util.current_page = page
        # page.place(relwidth=1, relheight=1)
        # Util.double_buffer_frame(page, self, page.draw)
        # page.draw()
        # self.destroy()