from tkinter import Label, Button, DISABLED, S
from constants.labels import LABEL_NAMES, LABEL_KEYS

class ScoreboardUI:
    def __init__(self, root, scoreboard):
        self.root = root
        self.scoreboard = scoreboard
        self.score_labels = []
        self.select_buttons = []
        self.bonus_label = None
        self.__setup_scoreboard()

    def __setup_scoreboard(self):
        row = 3
        for category in LABEL_NAMES:
            # Add bonus row after upper section
            if row == 9:
                Label(self.root, text="Bonus (+50 if sum ≥ 63)").grid(row=row, column=1, sticky="w", padx=5)
                self.bonus_label = Label(self.root, text="-", width=10, bg="white")
                self.bonus_label.grid(row=row, column=2, sticky="ew", padx=5)
                row += 1

            # Category label
            Label(self.root, text=category).grid(row=row, column=1, sticky="w", padx=5)

            # Score label
            score_label = Label(self.root, text="", width=10, relief="groove",
                                state=DISABLED, bg="white")
            score_label.grid(row=row, column=2, sticky="ew", padx=5)
            self.score_labels.append(score_label)

            # Select button
            select_button = Button(self.root, text="Valitse", state=DISABLED,
                                    relief="flat", bg="white")
            select_button.grid(row=row, column=3, padx=5)
            self.select_buttons.append(select_button)

            row += 1

    def render_score_options(self, dice):
        possible_scores = self.scoreboard.get_possible_scores(dice)
        for i, key in enumerate(LABEL_KEYS):
            if key in possible_scores:
                self.score_labels[i].config(text=str(possible_scores[key]))
                self.select_buttons[i].config(state="normal")
            else:
                self.score_labels[i].config(text="")
                self.select_buttons[i].config(state=DISABLED)


