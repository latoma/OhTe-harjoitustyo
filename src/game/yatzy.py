from ui.main_window import MainWindow
from ui.dice_ui import DiceUI
from ui.scoreboard_ui import ScoreboardUI
from ui.leaderboard_ui import LeaderboardUI
from game.dice import Dice
from game.scoreboard import Scoreboard
from repositories.game_repository import GameRepository
from repositories.scoreboard_repository import ScoreboardRepository
from database_connection import get_database_connection
from tkinter import simpledialog

class Yatzy:
    """ Pääluokka, joka hallinnoi pelin kulkua ja käyttöliittymää """

    def __init__(self, test_mode=False):
        """ Konstruktori, alustaa pelin ja sen käyttöliittymän

        Args:
            test_mode: testitila käytössä
        """
        self.__test_mode = test_mode
        self.__main_window = MainWindow(test_mode)
        db_connection = get_database_connection()
        self.__scoreboard_repository = ScoreboardRepository(db_connection)
        self.__game_repository = GameRepository(db_connection)

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
        """
        Heittää nopat ja päivittää käyttöliittymän tilan.

        Jos kyseessä on ensimmäinen heitto:
            -> Vapauta edellisen kierroksen hold-statukset nopilta.
        -> Noppien heitto
        -> Vähentää jäljellä olevien heittojen määrään.
        -> Aktivoi heittoanimaatio
        Animaation jälkeen:
        -> Renderöi pistevaihtoehdot.
        -> Aktivoi valintapainikkeet.

        Jos heittoja ei ole enää jäljellä:
            -> Deaktivoi heittopainike
            -> Lukitse nopat
        """

        if self.__throws_left == 3:
            self.__scoreboard_ui.enable_select_buttons()
            self.__dice.unlock_dice()
            self.__dice_ui.update_hold_buttons()

        self.__scoreboard_ui.disable_select_buttons()
        self.__dice.roll_dice()

        self.__throws_left -= 1
        if self.__test_mode:
            self.__throws_left += 1
        self.__main_window.update_throws_left(self.__throws_left)

        def after_animation():
            self.__scoreboard_ui.enable_select_buttons()
            possible_scores = self.__scoreboard.get_possible_scores(self.__dice)
            self.__scoreboard_ui.render_score_options(
                possible_scores=possible_scores,
                last_throw=self.__throws_left == 0 or self.__test_mode
            )

            if self.__throws_left == 0:
                self.__main_window.roll_button.config(
                    state="disabled",
                    relief="sunken",
                    bg="lightgray"
                )
                self.__dice.lock_dice()
                self.__dice_ui.update_hold_buttons()

        self.__dice_ui.animate_roll(after_animation)

        if self.__throws_left == 0:
            self.__main_window.roll_button.config(
                state="disabled",
                relief="sunken",
                bg="lightgray"
            )
            self.__dice.lock_dice()
            self.__dice_ui.update_hold_buttons()


    def select_score(self, label):
        """
        - Valitsee pistemäärän ja päivittää pistetaulun ja heittojen määrän.
        - Valmistelee nopat seuraavaa kierrosta varten.
        - Lopettaa pelin, jos kierrokset loppuvat.

        Args:
            label: valinta-näppäimen kategoria
        """
        score = self.__scoreboard.calculate_score(label, self.__dice.get_values())
        self.__scoreboard.set_score(label, score)
        self.__scoreboard_ui.disable_select_buttons()
        self.__scoreboard_ui.update_score(label, score)
        self.__throws_left = 3
        self.__main_window.update_throws_left(self.__throws_left)
        self.__dice_ui.prepare_dice_for_next_round()

        self.__main_window.roll_button.config(
            state="normal",
            relief="raised",
        )
        self.__round += 1

        if self.__round > 15:
            self.end_game()

    def end_game(self):
        """ Lopettaa pelin, kysyy käyttäjän nimimerkin ja tallentaa tuloksen tietokantaan """
        total_score = self.__scoreboard.get_total_score()

        player_name = simpledialog.askstring("Peli päättyi", "Nimimerkki:")
        if player_name:
            game_id = self.__game_repository.create(player_name, total_score)
            self.__scoreboard_repository.create(game_id, self.__scoreboard)
            self.__leaderboard_ui.update_scores()
            self.__main_window.create_new_game_button(self.start_new_game)

    def start_new_game(self):
        """ Aloittaa uuden pelin """
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
