import unittest
from unittest.mock import patch
from game.yatzy import Yatzy
from database_connection import get_database_connection


class TestYatzyIntegration(unittest.TestCase):
    def setUp(self):
        self.yatzy = Yatzy(use_test_db=True)

    def test_roll_dice_integration(self):
        initial_throws = self.yatzy.throws_left
        initial_values = self.yatzy.dice.get_values()
        initial_scores = self.yatzy.scoreboard.get_possible_scores(self.yatzy.dice)

        # First roll
        self.yatzy.roll_dice()

        self.assertEqual(self.yatzy.throws_left, initial_throws - 1)

        new_values = self.yatzy.dice.get_values()
        self.assertNotEqual(initial_values, new_values)

        new_scores = self.yatzy.scoreboard.get_possible_scores(self.yatzy.dice)
        self.assertNotEqual(initial_scores, new_scores)

        # Hold first die
        self.yatzy.dice.get_dice()[0].toggle_hold_status()

        # Second roll
        self.yatzy.roll_dice()
        self.assertEqual(self.yatzy.throws_left, initial_throws - 2)
        self.assertEqual(self.yatzy.dice.get_values()[0], new_values[0])
        self.assertEqual(self.yatzy.dice.get_dice()[0].in_hold(), True)

        # Third and last roll
        self.yatzy.roll_dice()

        self.assertEqual(self.yatzy.throws_left, 0)
        self.assertEqual(self.yatzy.main_window.roll_button['state'], 'disabled')
        for die in self.yatzy.dice.get_dice():
            self.assertEqual(die.is_locked(), True)

    def test_select_score_integration(self):
        self.yatzy.roll_dice()
        self.yatzy.roll_dice()
        self.yatzy.roll_dice()

        possible_scores = self.yatzy.scoreboard.get_possible_scores(self.yatzy.dice)
        selected_label = list(possible_scores.keys())[0]
        initial_score = self.yatzy.scoreboard.get_total_score()

        self.yatzy.select_score(selected_label)

        new_score = self.yatzy.scoreboard.get_total_score()
        if new_score != 0:
            self.assertNotEqual(initial_score, new_score)
        self.assertEqual(self.yatzy.throws_left, 3)

    def tearDown(self):
        connection = get_database_connection(test=True)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM scoreboards")
        cursor.execute("DELETE FROM games")
        connection.commit()
        connection.close()
        self.yatzy.main_window.destroy()
