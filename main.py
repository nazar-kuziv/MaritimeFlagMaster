import tksvg
import requests
import tkinter as tk
import threading

from logic.alphabet import Alphabet
from logic.flags import Flag


def check_internet(callback, url="https://www.google.com", timeout=5):
    """
    Checks for an internet connection.

    Parameters:
    callback (function): The callback function to call with the result.
    url (str): The URL to test the connection. Defaults to Google.
    timeout (int): The timeout in seconds for the request. Defaults to 5 seconds.
    """

    def check():
        try:
            response = requests.get(url, timeout=timeout)
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
window = tk.Tk()
window.title("Internet Connection Checker")

a = Alphabet.get_all_flags()
print(a[0])

# Ensure that tksvg.SvgImage is created correctly and attached to the label
if isinstance(a[0], Flag):
    svg_image = tksvg.SvgImage(file="graphics/" + a[0].img_path)
else:
    svg_image = tksvg.SvgImage(file="graphics/" + a[0].flags[0].img_path)

label = tk.Label(window, image=svg_image)
label.pack()

check_internet(handle_internet_status)

window.mainloop()
