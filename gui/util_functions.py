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
    def __init__(self, master: ctk.CTkBaseClass, **kwargs):
        super().__init__(master, **kwargs)

    @abstractmethod
    def draw(self):
        """Draws GUI elements

        Automatically adds a _top_menu_ frame with a _BreadcrumbTrail_
        """
        self._top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self._top_menu.pack(fill="x")
        self.update_idletasks()
        self.breadcrumb = BreadcrumbTrailWidget(self._top_menu)
        self.breadcrumb.pack(side="left", anchor="nw")

import gui.results as Results # here to avoid circular import
class AppQuizPage(AppPage):
    """Base class for quiz pages
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.session = None
        self.question = None

    @abstractmethod
    def show_question(self):
        pass

    @abstractmethod
    def next_question(self):
        pass
        
    session = None

    def finish(self, message: str = None, **kwargs):
        if (message is not None):
            kwargs["message"] = message
        page = Results.Results(self.master, self.session, fg_color="transparent", **kwargs)
        change_page(page)
    
    def add_skip_button(self, command: Callable, **kwargs):
        skip_button = ctk.CTkButton(self._top_menu, text='Pomiń', width=0, command=command, **kwargs)
        skip_button.pack(side="right", padx=5)
        return skip_button

class ISkippablePage(ABC):
    """Interface for skippable pages
    """
    @abstractmethod
    def skip_command(self):
        pass

    @abstractmethod
    def show_next_button(self):
        pass

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