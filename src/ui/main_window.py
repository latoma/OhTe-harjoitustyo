from tkinter import Tk, Button, DISABLED
from constants.labels import LABEL_NAMES, LABEL_KEYS

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="white")
        self.title("Yahtzee")
        self.geometry("800x600")

        #Roll button
        self.roll_button = Button(self, text="Heitä nopat")
        self.roll_button.grid(row=2, column=2)

        # Score selection buttons
        self.select_buttons = []
        self.create_score_buttons()

    def create_score_buttons(self):
        row = 3
        for _ in LABEL_NAMES:
            # Skip bonus row
            if row == 9:
                row += 1

            select_button = Button(
                self,
                text="",
                state=DISABLED,
                relief="flat",
                bg="white"
            )
            select_button.grid(row=row, column=3, padx=5)
            self.select_buttons.append(select_button)
            row += 1

    def set_roll_command(self, command):
        self.roll_button.configure(command=command)

    def set_select_commands(self, command_factory):
        for i, key in enumerate(LABEL_KEYS):
            self.select_buttons[i].configure(
                command=command_factory(key)
            )
