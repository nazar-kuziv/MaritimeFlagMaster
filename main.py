import tksvg
import requests
import tkinter as tk
import threading

from logic.alphabet import Alphabet
from logic.flags import Flag
from gui.main_window import MainWindow

def check_internet(callback):
    """
    Checks for an internet connection.

    Parameters:
    callback (function): The callback function to call with the result.
    """

    def check():
        try:
            response = requests.get("https://api.quotable.io/random?maxLength=50", timeout=5)
            if response.status_code == 200:
                callback(True)
            else:
                callback(False)
        except requests.ConnectionError:
            callback(False)
        except requests.Timeout:
            callback(False)

    threading.Thread(target=check).start()


def handle_internet_status(status):
    """
    Handles the result of the internet connection check.

    Parameters:
    status (bool): True if the internet connection is successful, False otherwise.
    """
    if status:
        print("Connected to the internet")
    else:
        print("No internet connection")


# Set up the Tkinter window
app = MainWindow()

check_internet(handle_internet_status)

app.mainloop()