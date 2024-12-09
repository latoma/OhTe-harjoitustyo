from tkinter import Label, DISABLED, Button
from constants.labels import LABEL_NAMES, LABEL_KEYS
from game.scoreboard import Scoreboard

class ScoreboardUI:
    def __init__(self, root, scoreboard: Scoreboard, test_mode=False):
        self.root = root
        self.scoreboard = scoreboard
        self.score_labels = []
        self.bonus_label = None
        self.test_mode = test_mode
        self.selection_disabled = True
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
            score_label = Label(self.root, text="", relief="groove",
                              state=DISABLED, bg="white", font=("TkDefaultFont", 12) )
            score_label.grid(row=row, column=2, sticky="ew", padx=5, pady=2)
            self.score_labels.append(score_label)

            row += 1

        # Total score label
        Label(self.root, text="Kokonaistulos:",
            font=("TkDefaultFont", 12, "bold")).grid(
            row=row+1, column=1, sticky="w", padx=5
        )

        self.total_score_label = Label(self.root, text="-", relief="groove",
                                    bg="white",font=("TkDefaultFont", 12, "bold")
                                 )
        self.total_score_label.grid(
            row=row+1, column=2, sticky="ew",
            padx=5
        )

    def render_score_options(self, dice, last_throw=False):
        possible_scores = self.scoreboard.get_possible_scores(dice)

        # Go through all labels and render correct display
        for i, key in enumerate(LABEL_KEYS):
            current_score = self.scoreboard.get_score(key)
            if current_score is not None:
                # Display an existing score
                self.score_labels[i].config(
                    text=str(current_score),
                    relief="sunken",
                    fg="black",
                    font=("TkDefaultFont", 12, "bold")
                )
                self.root.select_buttons[i].grid_remove()

            # Display remaining possible scores
            elif key in possible_scores and not self.selection_disabled:
                score = possible_scores[key]
                self.score_labels[i].config(
                    text=str(score),
                    relief="groove"
                )
                # Selection button becomes active if score is possible
                if score > 0:
                    self.root.select_buttons[i].config(
                        text="Valitse",
                        state="normal",
                        bg="green"
                    )
                elif last_throw:
                    self.root.select_buttons[i].config(
                        text="Valitse",
                        state="normal",
                        bg="red"
                    )
                # Hide selection button if score is 0
                else:
                    self.root.select_buttons[i].config(
                        text="",
                        state=DISABLED,
                        bg="white"
                    )

    def update_score(self, label, score):
        # Update score label
        index = LABEL_KEYS.index(label)
        self.score_labels[index].config(
            text=str(score),
            relief="sunken"
        )
        # Disable selection button
        self.root.select_buttons[index].config(state=DISABLED)

        # Update total score
        total = self.scoreboard.get_total_score()
        self.total_score_label.config(text=str(total))

        # Check if enough points for bonus
        if self.scoreboard.has_points_for_bonus():
            self.bonus_label.config(text="+50", font=("TkDefaultFont", 12))

    def enable_select_buttons(self):
        for button in self.root.select_buttons:
            button.config(state="normal")
        self.selection_disabled = False

    def disable_select_buttons(self):
        for button in self.root.select_buttons:
            button.config(state=DISABLED, bg="white")
        self.selection_disabled = True
