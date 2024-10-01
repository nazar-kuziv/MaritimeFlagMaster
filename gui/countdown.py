import customtkinter as ctk
import time
from typing import Callable

class Countdown(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkBaseClass, timeString: str, finishFunction: Callable, **kwargs):
        """Frame containing a countdown label

        :param timeString: time in the format 'MM:SS' (minutes colon seconds)
        :type timeString: str
        :param finishFunction: function to call after countdown elapses
        :type finishFunction: Callable
        """
        super().__init__(master, **kwargs)
        m, s = timeString.split(":")
        self.seconds = int(m) * 60 + int(s)
        self.finishFunction = finishFunction

        self.timeStringVar = ctk.StringVar(self, timeString)
        self.timeLabel = ctk.CTkLabel(self, textvariable=self.timeStringVar, fg_color='transparent')
        self.timeLabel.pack()

        self.isRunning = True
    
    def startCountdown(self):
        self.countDown(self.seconds)

    def countDown(self, seconds: int):
        if (not self.isRunning):
            return
        self.seconds = seconds
        self.timeStringVar.set(time.strftime('%M:%S', time.gmtime(seconds)))
        if (seconds > 0):
            self.after(1000, self.countDown, seconds - 1)
        else:
            self.finishFunction()
    
    def pause(self):
        self.isRunning = False
    
    def resume(self):
        self.isRunning = True
        self.countDown(self.seconds)