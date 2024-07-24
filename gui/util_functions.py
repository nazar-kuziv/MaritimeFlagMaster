import customtkinter as ctk
import tksvg
from collections.abc import Callable

# def change_scale_size(event):
#     if event.widget == event.widget.winfo_toplevel():
#         event.widget.scale_size = event.height if event.height < event.width else event.width
#         print(event.widget.scale_size)

def loading_widget(master):
    """Shows some loading text in the middle of the screen
    :return: the placed label with the text
    :rtype: CTkLabel
    """
    loading = ctk.CTkLabel(master, text='Ładowanie...', font=ctk.CTkFont(size=int(master.winfo_width()*0.03)), fg_color='transparent')
    loading.place(relx=0.5, rely=0.5, anchor="center")
    return loading

class BreadcrumbTrail(ctk.CTkFrame):
    def __init__(self, master, page_names: list[str], page_functions: list[Callable], **kwargs):
        """A frame containing a clickable breadcrumb trail of previous pages (frames)

        For a disabled button pass _None_ in that page_functions' index
        
        :param page_names: names of the buttons
        :type page_names: list[str]
        :param page_functions: what functions to call for each button
        :type page_functions: list[Callable]
        """
        super().__init__(master, **kwargs, fg_color="transparent")

        for i, page in enumerate(page_names):
            button = ctk.CTkButton(self, text=page, font=ctk.CTkFont(size=int(master.winfo_width()*0.013)), text_color=("gray10", "#DCE4EE"), fg_color="transparent", width=0, command=page_functions[i], **kwargs)
            if (page_functions[i] is None):
                button.configure(state="disabled")
            button.pack(side="left", padx=5)

            if (i < len(page_names) - 1):
                arrow = ctk.CTkLabel(self, text='〉', font=ctk.CTkFont(size=int(master.winfo_width()*0.02), weight='bold'), fg_color='transparent')
                arrow.pack(side="left")

