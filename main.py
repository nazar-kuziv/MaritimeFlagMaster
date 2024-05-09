import tksvg
import tkinter as tk

from logic.alphabet import Alphabet

a = Alphabet()
window = tk.Tk()
svg_image = tksvg.SvgImage(file="graphics/" + a._characters['0'].img_path)
label = tk.Label(image=svg_image)
label.pack()
window.mainloop()
