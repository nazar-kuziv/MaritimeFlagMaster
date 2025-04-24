from gui.main_window import *
import logic.loading as Loading
from logic.alphabet import Alphabet
import gui.util_functions as Util
import warnings

# Ignore warnings for using tksvg.SvgImage
warnings.filterwarnings("ignore", message=".*SvgImage.*")

# Set up the Tkinter window
app = MainWindow()
app.update()
print(f"MAIN WINDOW WIDTH: {app.winfo_width()}")
main_menu = Util.new_page(MainMenu, "Start", master=app, fg_color="transparent")

# Load svg flags for makeimage
Loading.start_load_thread(Alphabet.load_flags)

# FOR DEV RUNNING///
import os, shutil
from logic.environment import Environment

def clear_tmp():
    try:
        with os.scandir(Environment.resource_path(f"static/tmp")) as entries:
            for entry in entries:
                if entry.is_file():
                    os.unlink(entry.path)
                else:
                    shutil.rmtree(entry.path)
            print("All files and subdirectories deleted successfully.")
    except OSError:
        print("Error occurred while deleting files and subdirectories.")
    app.destroy()

app.protocol("WM_DELETE_WINDOW", clear_tmp)
# ///FOR DEV RUNNING

app.mainloop()