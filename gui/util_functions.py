import customtkinter as ctk
import tksvg
from collections.abc import Callable
from abc import ABC, abstractmethod
from typing import Self
import inspect

# def change_scale_size(event):
#     if event.widget == event.widget.winfo_toplevel():
#         event.widget.scale_size = event.height if event.height < event.width else event.width
#         print(event.widget.scale_size)

class AppPage(ABC):
    """Abstract class of every CTkFrame that acts as a new application page (e.g. for breadcrumbs)
    """
    @abstractmethod
    def __init__(self, page_name: str = "Start"):
        add_breadcrumb(page_name, self)

    @abstractmethod
    def start(self):
        """The function to call when wanting to show the page

        Automatically adds a _top_menu_ frame with a _BreadcrumbTrail_
        """
        self.top_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.top_menu.pack(anchor="w", fill="x")
        self.breadcrumb = BreadcrumbTrail(self.top_menu)
        self.breadcrumb.pack(side="left")

    @abstractmethod
    def exit(self, to_class: Self):
        """Exits the page and calls a new one, needs to be implemented

        :param to_class: the new page's inititation function
        :type to_class: AppPage
        """
        pass

def loading_widget(master):
    """Shows some loading text in the middle of the screen
    :return: the placed label with the text
    :rtype: CTkLabel
    """
    loading = ctk.CTkLabel(master, text='Ładowanie...', font=ctk.CTkFont(size=int(master.winfo_width()*0.03)), fg_color='transparent')
    loading.place(relx=0.5, rely=0.5, anchor="center")
    return loading

_page_names = []
_page_object = []

def add_breadcrumb(name: str, to_class: AppPage):
    """Add a page (frame) breadcrumb for the breadcrumb trail widget

    :param name: the name of the button visible in the GUI
    :type name: str
    :param function: the page that should be shown when clicking on the button;
    :type function: Callable
    """
    print(f"Adding breadcrumb {name} of class {to_class}")
    _page_names.append(name)
    _page_object.append(to_class)

def delete_breadcrumb():
    """Delete the last breadcrumb from the breadcrumb trail widget
    """
    if (len (_page_names) <= 0): return
    _page_names.pop()
    _page_object.pop()

class BreadcrumbTrail(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        """A frame containing a clickable breadcrumb trail of previous pages (frames)

        """
        super().__init__(master, **kwargs, fg_color="transparent")
        print(f"Creating breadcrumb trail of {len(_page_names)}, master {master}")

        for i, page in enumerate(_page_names):
            button = ctk.CTkButton(self, text=page, font=ctk.CTkFont(size=int(master.winfo_width()*0.013)), text_color=("gray10", "#DCE4EE"), fg_color="transparent", width=0, command=lambda index = i: self.change_page(index), **kwargs)
            if (_page_object[i] is None or i >= len(_page_object) - 1):
                button.configure(state="disabled")
            button.pack(side="left", padx=5)

            if (i < len(_page_names) - 1):
                arrow = ctk.CTkLabel(self, text='〉', font=ctk.CTkFont(size=int(master.winfo_width()*0.018), weight='bold'), fg_color='transparent')
                arrow.pack(side="left")
    
    def change_page(self, index: int):
        """Changes the page (frame) and calls the exit function of the current one

        :param index: index of the page in the trail that is going to be shown (from 0)
        :type index: int
        """
        # print("Breadcrumb Change page called by", inspect.stack()[1])
        for i in range(index + 1, len(_page_object)):
            delete_breadcrumb()
        self.master.exit(_page_object[index])