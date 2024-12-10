from ui.main_window import MainWindow
from ui.dice_ui import DiceUI
from ui.scoreboard_ui import ScoreboardUI
from game.dice import Dice
from game.scoreboard import Scoreboard
from repositories.game_repository import GameRepository
from repositories.scoreboard_repository import ScoreboardRepository
from database_connection import get_database_connection
from ui.leaderboard_ui import LeaderboardUI

class Yatzy:
    """A game of Yatzy is performed here"""

    def __init__(self, test_mode=False):
        self.__test_mode = test_mode
        self.__main_window = MainWindow(test_mode)
        db_connection = get_database_connection()
        self.__scoreboard_repository = ScoreboardRepository(db_connection)
        self.__game_repository = GameRepository(db_connection, self.__scoreboard_repository)

        self.__leaderboard_ui = LeaderboardUI(
            self.__main_window,
            self.__game_repository,
            self.__scoreboard_repository
            )

        self.__dice = Dice()
        self.__dice_ui = DiceUI(self.__main_window, self.__dice)

        self.__scoreboard = Scoreboard()
        self.__scoreboard_ui = ScoreboardUI(self.__main_window, self.__scoreboard, test_mode)

        self.__main_window.set_roll_command(self.roll_dice)

        self.__throws_left = 3

        self.__round = 1

        self.__main_window.set_select_commands(
            lambda key: lambda: self.select_score(key)
        )

        if test_mode:
            self.__main_window.set_save_score_command(
                lambda: self.end_game()
            )

    def start(self):
        self.__main_window.mainloop()

    def roll_dice(self):
        if self.__throws_left >= 3:
            self.__scoreboard_ui.enable_select_buttons()
            self.__dice.unlock_dice()
            self.__dice_ui.update_hold_buttons()

        if self.__throws_left > 0:
            self.__dice.roll_dice()
            self.__dice_ui.update_display()

            self.__throws_left -= 1
            if self.__test_mode: self.__throws_left += 1
            self.__main_window.update_throws_left(self.__throws_left)

            self.__scoreboard_ui.render_score_options(
                self.__dice,
                last_throw=self.__throws_left == 0 or self.__test_mode
                )

        if self.__throws_left == 0:
            # Make roll button visibly disabled
            self.__main_window.roll_button.config(
                state="disabled",
                relief="sunken",
                bg="lightgray"
            )
            # Lock dice so they can't be held
            self.__dice.lock_dice()
            self.__dice_ui.update_hold_buttons()


    def select_score(self, label):
        score = self.__scoreboard.calculate_score(label, self.__dice.get_values())
        self.__scoreboard.set_score(label, score)
        self.__scoreboard_ui.disable_select_buttons()
        self.__scoreboard_ui.update_score(label, score)
        self.__scoreboard_ui.render_score_options(self.__dice)
        self.__throws_left = 3
        self.__main_window.update_throws_left(self.__throws_left)
        self.__dice_ui.prepare_dice_for_next_round()

        self.__main_window.roll_button.config(
            state="normal",
            relief="raised",
        )
        self.__round += 1

        # Check if game is over
        if self.__round > 15:
            self.end_game()

    def end_game(self):
        """Save game and scoreboard data separately when game ends"""
        total_score = self.__scoreboard.get_total_score()

        game_id = self.__game_repository.create(total_score)

        self.__scoreboard_repository.create(game_id, self.__scoreboard)

        self.__leaderboard_ui.update_scores()
        self.__main_window.create_new_game_button(self.start_new_game)


    def start_new_game(self):
        self.__main_window.remove_new_game_button()

        self.__scoreboard = Scoreboard()
        self.__scoreboard_ui = ScoreboardUI(self.__main_window, self.__scoreboard, self.__test_mode)

        self.__dice = Dice()
        self.__dice_ui = DiceUI(self.__main_window, self.__dice)

        self.__throws_left = 3
        self.__main_window.update_throws_left(self.__throws_left)
        self.__main_window.roll_button.config(
            state="normal",
            relief="raised",
        )

        self.__scoreboard_ui.render_score_options(self.__dice)
        self.__round = 1
