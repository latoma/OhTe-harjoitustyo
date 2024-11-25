from tkinter import Tk, Frame, Button, Label


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="white")
        self.setup_ui()

    def setup_ui(self):
        self.title("Yahtzee")
        self.geometry("800x600")
