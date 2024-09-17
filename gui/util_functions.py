import customtkinter as ctk
from abc import ABC, abstractmethod
from typing import Any, Type, Callable

def get_scale_size(widget: ctk.CTkBaseClass) -> int:
    """Calculates and returns the scaling size to which to adjust element sizes

    :param widget: Any ctk widget
    :type widget: ctk.CTkBaseClass
    :return: Scale size
    :rtype: int
    """
    root = widget.winfo_toplevel()
    return root.winfo_height() if (root.winfo_height() < root.winfo_width()) else root.winfo_width()

class AppPage(ABC, ctk.CTkFrame):
    """Abstract class of every CTkFrame that acts as a new application page (e.g. for breadcrumbs)
    """
    @abstractmethod
    def __init__(self, master: ctk.CTkBaseClass, **kwargs):
        super().__init__(master, **kwargs)

    def draw(self):
        """Draws GUI elements

        Automatically adds a _top_menu_ frame with a _BreadcrumbTrail_
        """
        self._top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self._top_menu.pack(fill="x")
        self.update_idletasks()
        self.breadcrumb = BreadcrumbTrailWidget(self._top_menu)
        self.breadcrumb.pack(side="left")

def loading_widget(master, isFill: bool = False):
    """Shows some loading text in the middle of the screen

    :param isFill: should this widget cover up the whole window
    :type isFill: bool
    :return: the placed label with the text
    :rtype: CTkLabel
    """
    size = int(master.winfo_width()*0.03)
    if (isFill):
        master = ctk.CTkFrame(master, fg_color="transparent")
        master.place(relwidth=1, relheight=1)
    loading = ctk.CTkLabel(master, text='Ładowanie...', font=ctk.CTkFont(size=size), fg_color='transparent')
    loading.place(relx=0.5, rely=0.5, anchor="center")
    return master if isFill else loading

_page_names: list[str] = []
_page_class: list[Type[AppPage]] = []
_page_kwargs: list[dict[str, Any] | None] = []

def add_breadcrumb(name: str, to_class: Type[AppPage], **kwargs):
    """Add a page (frame) breadcrumb for the breadcrumb trail widget

    :param name: the name of the button visible in the GUI
    :type name: str
    :param function: the page that should be shown when clicking on the button;
    :type function: Type[AppPage]
    """
    # print(f"Adding breadcrumb {name} of class {to_class}")
    _page_names.append(name)
    _page_class.append(to_class)
    _page_kwargs.append(kwargs)

def delete_breadcrumb():
    """Delete the last breadcrumb from the breadcrumb trail widget
    """
    if (len (_page_names) <= 0): return
    _page_names.pop()
    _page_class.pop()

class BreadcrumbTrailWidget(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass, **kwargs):
        """A frame containing a clickable breadcrumb trail of previous pages (frames)

        """
        master.update_idletasks()
        # print(f"BREADCRUMB WIDTH: {master.winfo_toplevel().winfo_width()}")
        super().__init__(master, **kwargs, fg_color="transparent")
        # print(f"Creating breadcrumb trail of {len(_page_names)}, master {master}")

        for i, page in enumerate(_page_names):
            button = ctk.CTkButton(self, text=page, font=ctk.CTkFont(size=int(master.winfo_toplevel().winfo_width()*0.013)), text_color=("gray10", "#DCE4EE"), fg_color="transparent", width=0, command=lambda index = i: previous_page(index), **kwargs)
            if (_page_class[i] is None or i >= len(_page_class) - 1):
                button.configure(state="disabled")
            button.pack(side="left", padx=5)

            if (i < len(_page_names) - 1):
                arrow = ctk.CTkLabel(self, text='〉', font=ctk.CTkFont(size=int(master.winfo_toplevel().winfo_width()*0.018), weight='bold'), fg_color='transparent')
                arrow.pack(side="left")

_current_page: ctk.CTkBaseClass = None

def change_page(page: AppPage) -> ctk.CTkBaseClass:
    """Shows an app page with double buffering

    :return: the page object
    :rtype: ctk.CTkBaseClass
    """
    global _current_page
    def page_function():
        page.place(relwidth=1, relheight=1)
        page.draw()
    
    double_buffer_frame(page, _current_page, page_function)

    if (_current_page is not None):
        _current_page.destroy()
    _current_page = page
    return _current_page

def new_page(page: Type[AppPage], breadcrumb_name: str, **kwargs) -> ctk.CTkBaseClass:
    """Creates and shows a new app page not clicked from a breadcrumb
    
    :return: the new page object
    :rtype: ctk.CTkBaseClass
    """
    # print(f"Adding new page {page.__class__} to breadcrumb trail")
    page = page(**kwargs)
    add_breadcrumb(breadcrumb_name, page.__class__, **kwargs)
    return change_page(page)

def previous_page(index: int) -> ctk.CTkBaseClass:
    for i in range(index + 1, len(_page_class)):
            delete_breadcrumb()
    return change_page(_page_class[index](**_page_kwargs[index]))

def double_buffer_frame(frame: ctk.CTkBaseClass, buffer_frame: ctk.CTkBaseClass | None, draw_function: Callable):
    """Double-buffers the provided frame

    :param buffer_frame: frame to mask the new one with, normally should be the previous frame, None creates a blank one
    :type buffer_frame: ctk.CTkBaseClass
    :param draw_function: called between raising and destroying the double-buffer frame
    :type draw_function: Callable
    """
    if (buffer_frame is None):
        buffer_frame = ctk.CTkFrame(frame.master, fg_color="transparent")
        buffer_frame.place(relwidth=1, relheight=1)
    frame.lower(buffer_frame)
    draw_function()
    
    frame.update_idletasks()
    buffer_frame.destroy()

def options_menu(master: ctk.CTkBaseClass, forward_function: Callable, select_source: bool = False, questions_amount_choices: list[int] = [5, 10], questions_amount_def_ind: int = 1, time_minutes_choices: list[int] = [5, 10], time_minutes_def_ind: int = 0):
    """Frame for selecting various options for the picked mode

    :param forward_function: function used by the start button/source selection buttons
    :type forward_function: Callable
    :param select_source: if True shows 3 source select buttons instead of a simple Start button, defaults to False
    :type select_source: bool, optional
    """
    menu = ctk.CTkFrame(master, fg_color="transparent")
    menu.place(relwidth=1, relheight=1)
    menu.grid_columnconfigure(0, weight=1)
    menu.grid_columnconfigure(1, weight=1)
    menu.grid_rowconfigure(0, weight=1)
    menu.grid_rowconfigure(1, weight=0)
    menu.grid_rowconfigure(2, weight=1)

    menu.questions_amount = questions_amount_choices[questions_amount_def_ind]
    menu.time_minutes = time_minutes_choices[time_minutes_def_ind]

    def numbers_to_labels(nums: list):
        labels = []
        for n in nums:
            if (n <= -1):
                labels.append("Bez limitu")
            else:
                labels.append(str(n))
        return labels

    amounts = numbers_to_labels(questions_amount_choices)
    amount_label = ctk.CTkLabel(menu, text='Liczba pytań', fg_color='transparent')
    amount_label.grid(column=0, row=0, padx=5, pady=5, sticky="se")
    amount_var = ctk.StringVar(value=amounts[questions_amount_def_ind])
    def optionmenu_callback(choice):
        nonlocal menu
        print('optionmenu dropdown clicked:', choice)
        menu.questions_amount = int(choice)
    amount_options = ctk.CTkOptionMenu(menu, values=amounts,
                                        command=optionmenu_callback,
                                        variable=amount_var)
    amount_options.grid(column=1, row=0, padx=5, pady=5, sticky="sw")

    times = numbers_to_labels(time_minutes_choices)
    time_label = ctk.CTkLabel(menu, text='Limit czasu (minuty)', width=40, height=28, fg_color='transparent')
    time_label.grid(column=0, row=1, padx=5, pady=5, sticky="ne")
    time_var = ctk.StringVar(value=times[time_minutes_def_ind])
    def optionmenu_callback(choice):
        nonlocal menu
        print('optionmenu dropdown clicked:', choice)
        menu.time_minutes = int(choice)
    time_options = ctk.CTkOptionMenu(menu, values=times,
                                             command=optionmenu_callback,
                                             variable=time_var)
    time_options.grid(column=1, row=1, padx=5, pady=5, sticky="nw")

    if (not select_source):        
        start_button = ctk.CTkButton(menu, text='Start', font=ctk.CTkFont(size=int(master.winfo_width()*0.015)), command=forward_function)
        start_button.grid(column=0, row=2, columnspan=2, pady=5, sticky="n")
        return menu

    source_select_frame = ctk.CTkFrame(menu, fg_color="transparent")
    source_select_frame.grid(column=0, row=2, columnspan=2, pady=5, sticky="n")
    default_mode_button = ctk.CTkButton(source_select_frame, text='Wbudowane', font=ctk.CTkFont(size=int(master.winfo_width()*0.015)), 
                                                command=lambda: forward_function("default"))
    default_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)

    internet_mode_button = ctk.CTkButton(source_select_frame, text='Z internetu', font=ctk.CTkFont(size=int(master.winfo_width()*0.015)), 
                                                command=lambda: forward_function("internet"))
    internet_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)
    
    file_mode_button = ctk.CTkButton(source_select_frame, text='Z pliku...', font=ctk.CTkFont(size=int(master.winfo_width()*0.015)), 
                                            command=lambda: forward_function("file"))
    file_mode_button.pack(side="left", expand=True, ipadx=10, ipady=10, padx=5)
    
    return menu