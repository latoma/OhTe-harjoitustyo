from tkinter import Label, Button, DISABLED, Button, Toplevel
from constants.labels import LABEL_NAMES, LABEL_KEYS, SCORE_EXPLANATION
from game.scoreboard import Scoreboard

class ScoreboardUI:
    """ Luokka joka vastaa tulostaulun käyttöliittymästä

    Attributes:
        root: pääikkuna
        scoreboard: pistetaulukko
        score_labels: lista pistetulosten label
        bonus_label: bonuspisteiden label
        test_mode: testitila
        selection_disabled: valintojen estäminen
    """
    def __init__(self, root, scoreboard: Scoreboard, test_mode=False):
        """ Konstruktori, alustaa tulostaulun käyttöliittymän

        Args:
            root: pääikkuna
            scoreboard: pistetaulukko
            test_mode: testitila
        """
        self.root = root
        self.scoreboard = scoreboard
        self.score_labels = []
        self.bonus_label = None
        self.test_mode = test_mode
        self.selection_disabled = True
        self.__setup_scoreboard()

    def __setup_scoreboard(self):
        """ Alustaa tulostaulun """
        row = 3
        for category in LABEL_NAMES:
            # Helper function for showing explanations
            def show_explanation(category=category):
                explanation_window = Toplevel(self.root)
                explanation_window.title("Selitys")
                Label(explanation_window, text=f"{SCORE_EXPLANATION[category]}").pack(padx=10, pady=10)
                Button(explanation_window, text="Sulje", command=explanation_window.destroy).pack(pady=5)

                # LLM-generated code for centering the window
                self.root.update_idletasks()
                x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (explanation_window.winfo_reqwidth() // 2)
                y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (explanation_window.winfo_reqheight() // 2)
                explanation_window.geometry(f"+{x}+{y}")

            # Add row for bonus after upper section rows
            if row == 9:
                Button(self.root, text="?", font=("TkDefaultFont", 10), command=lambda: show_explanation(category='Bonus')).grid(row=row, column=0, sticky="e", padx=5)
                Label(self.root, text="Bonus (+50 jos 63p)").grid(row=row, column=1, sticky="e", padx=5, pady=5)
                self.bonus_label = Label(self.root, text="-", width=10, bg="white")
                self.bonus_label.grid(row=row, column=2, sticky="ew", padx=5)
                row += 1

            # Explanation button
            Button(self.root, text="?", font=("TkDefaultFont", 10), command=show_explanation).grid(row=row, column=0, sticky="e", padx=5)

            # Category label
            Label(self.root, text=category).grid(row=row, column=1, sticky="e", padx=5)

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

    def render_score_options(self, possible_scores, last_throw=False):
        """ Päivittää tulostaulukkoon piste-vaihtoehdot ja sen valitsemisnäppäimen.
            Jos viimeinen heitto, myös nollan pisteen valinnat ovat mahdollisia.

        Args:
            last_throw: viimeinen heitto
        """
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
        """ Päivittää pistetuloksen ja estää valinnan uudelleen

        Args:
            label: valittu kategoria
            score: pistemäärä
        """
        # Update score label
        index = LABEL_KEYS.index(label)
        self.score_labels[index].config(
            text=str(score),
            relief="sunken",
            font=("TkDefaultFont", 12, "bold")
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
