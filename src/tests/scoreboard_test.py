import unittest
from game.scoreboard import Scoreboard
from unittest.mock import Mock

class TestScoreboard(unittest.TestCase):
    def setUp(self):
        self.scoreboard = Scoreboard()
        self.mock_dice = Mock()

    def test_initial_scores_are_none(self):
        scores = self.scoreboard.get_scores()
        self.assertTrue(all(score is None for score in scores.values()))

    def test_get_and_set_score(self):
        self.scoreboard.set_score("ykköset", 3)
        self.assertEqual(self.scoreboard.get_score("ykköset"), 3)

    def test_total_score_sum_of_all_scores(self):
        scores = {"ykköset": 3, "kakkoset": 6, "kolmoset": 9}
        for label, score in scores.items():
            self.scoreboard.set_score(label, score)
        self.assertEqual(self.scoreboard.get_total_score(), 18)

    def test_upper_section_scoring(self):
        test_cases = [
            ([1,1,1,2,3], "ykköset", 3),
            ([2,2,2,2,1], "kakkoset", 8),
            ([3,3,3,1,2], "kolmoset", 9),
            ([4,4,1,2,3], "neloset", 8),
            ([5,5,5,1,2], "vitoset", 15),
            ([6,6,6,6,1], "kutoset", 24)
        ]

        for dice_values, label, expected in test_cases:
            self.mock_dice.get_values.return_value = dice_values
            scores = self.scoreboard.get_possible_scores(self.mock_dice)
            self.assertEqual(scores[label], expected)

    def test_pair_scoring(self):
        test_cases = [
            ([1,1,2,3,4], 2),
            ([5,5,5,6,6], 12),
            ([1,2,3,4,5], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("yksi_pari", dice_values),
                expected
            )

    def test_two_pairs_scoring(self):
        test_cases = [
            ([1,1,2,2,3], 6),
            ([5,5,6,6,6], 22),
            ([1,1,2,3,4], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("kaksi_paria", dice_values),
                expected
            )

    def test_three_of_a_kind_scoring(self):
        test_cases = [
            ([1,1,1,2,3], 3),
            ([5,5,5,5,6], 15),
            ([1,2,3,4,5], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("kolmiluku", dice_values),
                expected
            )

    def test_four_of_a_kind_scoring(self):
        test_cases = [
            ([1,1,1,1,2], 4),
            ([5,5,5,5,5], 20),
            ([1,1,1,2,3], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("nelosluku", dice_values),
                expected
            )

    def test_full_house_scoring(self):
        test_cases = [
            ([1,1,1,2,2], 7),
            ([5,5,5,6,6], 27),
            ([1,1,1,1,2], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("täyskäsi", dice_values),
                expected
            )

    def test_small_straight_scoring(self):
        test_cases = [
            ([1,2,3,4,5], 15),
            ([2,3,4,5,6], 0),
            ([1,2,2,4,5], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("pieni_suora", dice_values),
                expected
            )

    def test_large_straight_scoring(self):
        test_cases = [
            ([2,3,4,5,6], 20),
            ([1,2,3,4,5], 0),
            ([2,3,3,5,6], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("iso_suora", dice_values),
                expected
            )

    def test_chance_scoring(self):
        test_cases = [
            ([1,2,3,4,5], 15),
            ([6,6,6,6,6], 30)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("sattuma", dice_values),
                expected
            )

    def test_yatzy_scoring(self):
        test_cases = [
            ([5,5,5,5,5], 50),
            ([1,1,1,1,2], 0)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("yatzy", dice_values),
                expected
            )

    def test_get_possible_scores(self):
        self.mock_dice.get_values.return_value = [1,1,1,2,2]
        scores = self.scoreboard.get_possible_scores(self.mock_dice)
        self.assertGreater(len(scores), 0)
        self.assertIn("täyskäsi", scores)

        self.scoreboard.set_score("täyskäsi", 7)
        scores = self.scoreboard.get_possible_scores(self.mock_dice)
        self.assertNotIn("täyskäsi", scores)
