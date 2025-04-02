from tkinter import Tk, Frame, Canvas, Label, Entry, Button, OptionMenu, StringVar
from PIL import Image, ImageTk
import time
import queue
from utils.helpers import score_interpreter

class App(Tk):
    def __init__(self, globals_dict=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.game_object = object
        self.globals_dict = globals_dict

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        from gui.pages import StartPage, GamePage
        list_of_frames = [StartPage, GamePage]

        for F in list_of_frames:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.fresh = True
        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        print("waiting")
        if not self.fresh:
            time.sleep(0.1)
            if self.globals_dict:
                game_info_q = self.globals_dict.get('game_info_q')
                if game_info_q and not game_info_q.empty():
                    frame.update(game_info_q.get())
        self.fresh = False
        frame.tkraise()