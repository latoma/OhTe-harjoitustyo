from ui.main_window import MainWindow
from ui.dice_ui import DiceUI
from ui.scoreboard_ui import ScoreboardUI
from game.dice import Dice


class Yatzy:
    """A game of Yatzy is performed here"""

    def __init__(self):
        self.__main_window = MainWindow()
        self.__dice = Dice()
        self.__dice_ui = DiceUI(self.__main_window, self.__dice)
        self.__scoreboard_ui = ScoreboardUI(self.__main_window)

    def start(self):
        self.__main_window.mainloop()
