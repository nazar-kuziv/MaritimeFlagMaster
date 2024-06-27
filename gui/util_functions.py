import customtkinter as ctk
import tksvg

# def change_scale_size(event):
#     if event.widget == event.widget.winfo_toplevel():
#         event.widget.scale_size = event.height if event.height < event.width else event.width
#         print(event.widget.scale_size)

def loading_widget(master):
    loading = ctk.CTkLabel(master, text='Ładowanie...', font=ctk.CTkFont(size=int(master.winfo_width()*0.03)), fg_color='transparent')
    loading.place(relx=0.5, rely=0.5, anchor="center")
    return loading
        