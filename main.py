from gui.main_window import *
import gui.util_functions as Util

# Set up the Tkinter window
app = MainWindow()
app.update()
print(f"MAIN WINDOW WIDTH: {app.winfo_width()}")
main_menu = Util.new_page(MainMenu, "Start", master=app, fg_color="transparent")

app.mainloop()