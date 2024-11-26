from tkinter import Tk, Button

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="white")
        self.title("Yahtzee")
        self.geometry("800x600")
        self.roll_button = Button(self, text="Heitä nopat")
        self.roll_button.grid(row=2, column=2)

    def set_roll_command(self, command):
        self.roll_button.configure(command=command)
