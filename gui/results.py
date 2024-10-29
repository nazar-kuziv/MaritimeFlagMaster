import customtkinter as ctk
import gui.util_functions as Util
from logic.modes.session import Session

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Results(Util.AppPage):
    def __init__(self, master: ctk.CTkBaseClass, session: Session, message: str = "Brawo! Oto twój wynik:", **kwargs):
        super().__init__(master, **kwargs)
        self.message = message
        self.session = session

    def draw(self):
        super().draw()

        self.message = ctk.CTkLabel(self, text=self.message, fg_color='transparent')
        self.message.pack(side="top")

        self.plot_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.plot_frame.pack(side="top")

        fig = self.session.get_statistics()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()