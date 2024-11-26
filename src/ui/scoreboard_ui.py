from tkinter import Label, Button, DISABLED, S

LABEL_NAMES = [
  'Ones (5)', 'Twos (10)', 'Threes (15)', 'Fours (20)', 'Fives (25)', 'Sixes (30)',
  'A Pair (12)', 'Two pairs (22)', 'Three Of A Kind (18)', 'Four Of A Kind (24)',
  'Full House (28)', 'Small Straight (15)', 'Large Straight (20)', 'Chance (30)',
  'Yatzy (50)'
]

class ScoreboardUI:
    def __init__(self, root):
        self.root = root
        self.score_labels = []
        self.select_buttons = []
        self.bonus_label = None
        self.setup_scoreboard()

    def setup_scoreboard(self):
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
