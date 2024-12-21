from tkinter import simpledialog
from ui.main_window import MainWindow
from ui.dice_ui import DiceUI
from ui.scoreboard_ui import ScoreboardUI
from ui.leaderboard_ui import LeaderboardUI
from game.dice import Dice
from game.scoreboard import Scoreboard
from repositories.game_repository import GameRepository
from repositories.scoreboard_repository import ScoreboardRepository
from database_connection import get_database_connection

class Yatzy:
    """ Pääluokka, joka hallinnoi pelin kulkua ja käyttöliittymää """

    def __init__(self, test_mode=False, use_test_db=False):
        """ Konstruktori, alustaa pelin ja sen käyttöliittymän

        Args:
            test_mode: testitila käytössä
        """
        self.test_mode = test_mode
        self.main_window = MainWindow(test_mode)
        db_connection = get_database_connection(test=use_test_db)
        self.scoreboard_repository = ScoreboardRepository(db_connection)
        self.game_repository = GameRepository(db_connection)

        self.__leaderboard_ui = LeaderboardUI(
            self.main_window,
            self.game_repository,
            self.scoreboard_repository
        )

        self.dice = Dice()
        self.__dice_ui = DiceUI(self.main_window, self.dice)

        self.scoreboard = Scoreboard()
        self.__scoreboard_ui = ScoreboardUI(
            self.main_window,
            self.scoreboard,
            test_mode
        )

        self.main_window.set_roll_command(self.roll_dice)

        self.throws_left = 3

        self.round = 1

        self.main_window.set_select_commands(
            lambda key: lambda: self.select_score(key)
        )

        if test_mode:
            self.main_window.set_save_score_command(self.end_game)

    def start(self):
        self.main_window.mainloop()

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

        if self.throws_left == 3:
            self.__scoreboard_ui.enable_select_buttons()
            self.dice.unlock_dice()
            self.__dice_ui.update_hold_buttons()

        self.__scoreboard_ui.disable_select_buttons()
        self.dice.roll_dice()

        # Deactivate roll button during animation
        self.main_window.roll_button.config(
            state="disabled",
            relief="sunken",
            bg="lightgray"
        )

        self.throws_left -= 1

        if self.test_mode: # In test mode, there's endless throws
            self.throws_left += 1

        self.main_window.update_throws_left(self.throws_left)

        def after_animation():
            # If last throw, lock dice and keep roll button disabled
            if self.throws_left <= 0:
                self.dice.lock_dice()
                self.__dice_ui.update_hold_buttons()
            else:
                self.main_window.roll_button.config(
                    state="normal",
                    relief="raised",
                    bg="lightgray"
                )
            self.__scoreboard_ui.enable_select_buttons()
            possible_scores = self.scoreboard.get_possible_scores(self.dice)
            self.__scoreboard_ui.render_score_options(
                possible_scores=possible_scores,
                last_throw=self.throws_left == 0 or self.test_mode
            )


        if self.test_mode:
            self.__dice_ui.update_display()
            after_animation()
        else:
            self.__dice_ui.animate_roll(after_animation)


    def select_score(self, label):
        """
        - Valitsee pistemäärän ja päivittää pistetaulun ja heittojen määrän.
        - Valmistelee nopat seuraavaa kierrosta varten.
        - Lopettaa pelin, jos kierrokset loppuvat.

        Args:
            label: valinta-näppäimen kategoria
        """
        score = self.scoreboard.calculate_score(label, self.dice.get_values())
        self.scoreboard.set_score(label, score)
        self.__scoreboard_ui.disable_select_buttons()
        self.__scoreboard_ui.update_score(label, score)
        self.throws_left = 3
        self.main_window.update_throws_left(self.throws_left)
        self.__dice_ui.prepare_dice_for_next_round()

        self.main_window.roll_button.config(
            state="normal",
            relief="raised",
        )
        self.round += 1

        if self.round > 15:
            self.end_game()

    def end_game(self):
        """ Lopettaa pelin, kysyy käyttäjän nimimerkin ja tallentaa tuloksen tietokantaan """
        total_score = self.scoreboard.get_total_score()

        player_name = simpledialog.askstring("Peli päättyi", "Nimimerkki:")
        if player_name:
            game_id = self.game_repository.create(player_name, total_score)
            self.scoreboard_repository.create(game_id, self.scoreboard)
            self.__leaderboard_ui.update_scores()
        self.main_window.create_new_game_button(self.start_new_game)

    def start_new_game(self):
        """ Aloittaa uuden pelin """
        self.main_window.remove_new_game_button()
        self.main_window.reset_select_button_appearence()

        self.scoreboard.reset()
        self.__scoreboard_ui.reset()

        self.dice = Dice()
        self.__dice_ui = DiceUI(self.main_window, self.dice)

        self.throws_left = 3
        self.main_window.update_throws_left(self.throws_left)
        self.main_window.roll_button.config(
            state="normal",
            relief="raised",
        )

        self.main_window.set_select_commands(
            lambda key: lambda: self.select_score(key)
        )

        self.round = 1
