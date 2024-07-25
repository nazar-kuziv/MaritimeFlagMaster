from gui.main_window import *

# Set up the Tkinter window
app = MainWindow()
main_menu = MainMenu(app, fg_color="transparent")
main_menu.pack()

app.mainloop()