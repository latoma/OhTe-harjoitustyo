from tkinter import Label, DISABLED
from constants.labels import LABEL_NAMES, LABEL_KEYS

class ScoreboardUI:
    def __init__(self, root, scoreboard):
        self.root = root
        self.scoreboard = scoreboard
        self.score_labels = []
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

            row += 1

    def render_score_options(self, dice):
        possible_scores = self.scoreboard.get_possible_scores(dice)
        # Go through all labels and render correct display
        for i, key in enumerate(LABEL_KEYS):
            current_score = self.scoreboard.get_score(key)
            if current_score is not None:
                # Display an already selected score
                self.score_labels[i].config(
                    text=str(current_score),
                    relief="sunken",
                    fg="black",
                    font=("TkDefaultFont", 10, "bold")
                )
                self.root.select_buttons[i].grid_remove()

            # Display possible scores for others
            elif key in possible_scores:
                score = possible_scores[key]
                self.score_labels[i].config(
                    text=str(score),
                    relief="groove"
                )
                # Selection button becomes active if score is possible
                if score > 0:
                    self.root.select_buttons[i].config(
                        text="Select",
                        state="normal",
                        bg="green"
                    )
                # Disable button is non-visible if score is 0
                else:
                    self.root.select_buttons[i].config(
                        text="",
                        state=DISABLED,
                        bg="white"
                    )

    def update_score(self, label, score):
        index = LABEL_KEYS.index(label)
        self.score_labels[index].config(
            text=str(score),
            relief="sunken"
        )
        self.root.select_buttons[index].config(state=DISABLED)
        print('Score updated:', label, score)
        print(self.scoreboard.get_scores())
