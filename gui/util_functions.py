import customtkinter as ctk
from abc import ABC, abstractmethod
from typing import Self, Type

# def change_scale_size(event):
#     if event.widget == event.widget.winfo_toplevel():
#         event.widget.scale_size = event.height if event.height < event.width else event.width
#         print(event.widget.scale_size)

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

def loading_widget(master):
    """Shows some loading text in the middle of the screen
    :return: the placed label with the text
    :rtype: CTkLabel
    """
    loading = ctk.CTkLabel(master, text='Ładowanie...', font=ctk.CTkFont(size=int(master.winfo_width()*0.03)), fg_color='transparent')
    loading.place(relx=0.5, rely=0.5, anchor="center")
    return loading

_page_names: list[str] = []
_page_class: list[Type[AppPage]] = []

def add_breadcrumb(name: str, to_class: Type[AppPage]):
    """Add a page (frame) breadcrumb for the breadcrumb trail widget

    :param name: the name of the button visible in the GUI
    :type name: str
    :param function: the page that should be shown when clicking on the button;
    :type function: Type[AppPage]
    """
    # print(f"Adding breadcrumb {name} of class {to_class}")
    _page_names.append(name)
    _page_class.append(to_class)

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
            button = ctk.CTkButton(self, text=page, font=ctk.CTkFont(size=int(master.winfo_toplevel().winfo_width()*0.013)), text_color=("gray10", "#DCE4EE"), fg_color="transparent", width=0, command=lambda index = i: previous_page(self.winfo_toplevel(), index), **kwargs)
            if (_page_class[i] is None or i >= len(_page_class) - 1):
                button.configure(state="disabled")
            button.pack(side="left", padx=5)

            if (i < len(_page_names) - 1):
                arrow = ctk.CTkLabel(self, text='〉', font=ctk.CTkFont(size=int(master.winfo_toplevel().winfo_width()*0.018), weight='bold'), fg_color='transparent')
                arrow.pack(side="left")
    
    # def change_page(self, index: int):
    #     """Changes the page (frame) and calls the exit function of the current one

    #     :param index: index of the page in the trail that is going to be shown (from 0)
    #     :type index: int
    #     """
    #     # print("Breadcrumb Change page called by", inspect.stack()[1])
    #     for i in range(index + 1, len(_page_class)):
    #         delete_breadcrumb()
    #     self.master.exit(_page_class[index])

_current_page: ctk.CTkBaseClass = None

def _change_page(page: AppPage) -> ctk.CTkBaseClass:
    """Creates and shows an app page; internal use only

    :return: the page object
    :rtype: ctk.CTkBaseClass
    """
    global _current_page
    if (_current_page is None): # (29.07.2024) Pylance thinks the code below is unreachable lol
        _current_page = ctk.CTkFrame(page.winfo_toplevel(), fg_color="transparent")
        _current_page.place(relwidth=1, relheight=1)
    page.lower(_current_page)
    page.place(relwidth=1, relheight=1)
    page.draw()
    page.update()

    _current_page.destroy()
    _current_page = page
    return _current_page

def new_page(page: AppPage, breadcrumb_name: str) -> ctk.CTkBaseClass:
    """Creates and shows a new app page not clicked from a breadcrumb
    
    :return: the new page object
    :rtype: ctk.CTkBaseClass
    """
    # print(f"Adding new page {page.__class__} to breadcrumb trail")
    add_breadcrumb(breadcrumb_name, page.__class__)
    return _change_page(page)

def previous_page(master: ctk.CTkBaseClass, index: int) -> ctk.CTkBaseClass:
    for i in range(index + 1, len(_page_class)):
            delete_breadcrumb()
    return _change_page(_page_class[index](master))