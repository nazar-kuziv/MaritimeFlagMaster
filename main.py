import tksvg
import tkinter as tk

from logic.alphabet import Alphabet
from logic.flags import Flag

window = tk.Tk()
a = Alphabet.get_flags_for_flashcards()
print(a[0])
if isinstance(a[0], Flag):
    svg_image = tksvg.SvgImage(file="graphics/" + a[0].img_path)
else:
    svg_image = tksvg.SvgImage(file="graphics/" + a[0].flags[0].img_path)

label = tk.Label(image=svg_image)
label.pack()
window.mainloop()