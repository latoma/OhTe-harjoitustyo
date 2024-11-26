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

    def start(self):
        self.__main_window.mainloop()

    def roll_dice(self):
        self.__dice.roll_dice()
        self.__dice_ui.update_display()
        self.__scoreboard_ui.render_score_options(self.__dice)

