import customtkinter as ctk
import tksvg

def change_scale_size(event):
    if event.widget == event.widget.winfo_toplevel():
        event.widget.scale_size = event.height if event.height < event.width else event.width
        print(event.widget.scale_size)
        