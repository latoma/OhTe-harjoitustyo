from ui.main_window import MainWindow
from ui.dice_ui import DiceUI
from ui.scoreboard_ui import ScoreboardUI
from game.dice import Dice
from game.scoreboard import Scoreboard

class Yatzy:
    """A game of Yatzy is performed here"""

    def __init__(self):
        self.__main_window = MainWindow()

        self.__dice = Dice()
        self.__dice_ui = DiceUI(self.__main_window, self.__dice)

        self.__scoreboard = Scoreboard()
        self.__scoreboard_ui = ScoreboardUI(self.__main_window, self.__scoreboard)

        self.__main_window.set_roll_command(self.roll_dice)

        self.__throws_left = 3

        self.__main_window.set_select_commands(
            lambda key: lambda: self.select_score(key)
        )

    def start(self):
        self.__main_window.mainloop()

    def roll_dice(self):
        if self.__throws_left > 0:
            self.__dice.roll_dice()
            self.__dice_ui.update_display()
            self.__throws_left -= 1
            self.__main_window.update_throws_left(self.__throws_left)
            self.__scoreboard_ui.render_score_options(self.__dice)

        if self.__throws_left == 0:
            # Make roll button visibly disabled
            self.__main_window.roll_button.config(
                state="disabled",
                relief="sunken",
                bg="lightgray"
            )


    def select_score(self, label):
        score = self.__scoreboard.calculate_score(label, self.__dice.get_values())
        self.__scoreboard.set_score(label, score)
        self.__scoreboard_ui.update_score(label, score)
        self.__scoreboard_ui.render_score_options(self.__dice)
        self.__throws_left = 3
        self.__main_window.update_throws_left(self.__throws_left)
        self.__dice_ui.reset_holds()

        self.__main_window.roll_button.config(
            state="normal",
            relief="raised",
            bg="SystemButtonFace"
        )
