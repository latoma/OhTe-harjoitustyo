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
        scores = {"ykköset": 5, "kakkoset": 10, "kolmoset": 15, "neloset": 20, "vitoset": 25, "kutoset": 30,
                 "yksi_pari": 6, "kaksi_paria": 12, "kolmiluku": 9, "neliluku": 12, "täyskäsi": 7, "pieni_suora": 15,
                 "iso_suora": 20, "sattuma": 30, "yatzy": 50
                 }
        for label, score in scores.items():
            self.scoreboard.set_score(label, score)
        self.assertEqual(self.scoreboard.get_total_score(), 266)

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

    def test_invalid_label(self):
        dice_values = [1, 2, 3, 4, 5]
        self.assertEqual(
            self.scoreboard.calculate_score("invalid_label", dice_values),
            0
        )

    def test_get_possible_scores(self):
        self.mock_dice.get_values.return_value = [1,1,1,2,2]
        scores = self.scoreboard.get_possible_scores(self.mock_dice)
        self.assertGreater(len(scores), 0)
        self.assertIn("täyskäsi", scores)

        self.scoreboard.set_score("täyskäsi", 7)
        scores = self.scoreboard.get_possible_scores(self.mock_dice)
        self.assertNotIn("täyskäsi", scores)

    def test_has_points_for_bonus(self):
        test_cases = [
            ({"ykköset": 5, "kakkoset": 10, "kolmoset": 15,}, False),
            ({"ykköset": 5, "kakkoset": 10, "kolmoset": 15, "neloset": 20, "vitoset": 25, "kutoset": 30}, True),
            ({"ykköset": 3, "kakkoset": 6, "kolmoset": 9, "neloset": 12, "vitoset": 15, "kutoset": 18}, True),
            ({"ykköset": 5, "kakkoset": 0, "kolmoset": 3, "neloset": 0, "vitoset": 25, "kutoset": 30}, True),
            ({"ykköset": 3, "kakkoset": 0, "kolmoset": 3, "neloset": 0, "vitoset": 25, "kutoset": 30}, False),
        ]
        for scores, expected in test_cases:
            for label, score in scores.items():
                self.scoreboard.set_score(label, score)
            print(self.scoreboard.get_total_score(), self.scoreboard.has_points_for_bonus())
            self.assertEqual(self.scoreboard.has_points_for_bonus(), expected)

    def test_get_scores_as_list(self):
        test_cases = [
            (
                {"ykköset": 5, "kakkoset": 10, "kolmoset": 15},
                [5, 10, 15, None, None, None, None, None, None, None, None, None, None, None, None]
            ),
            (
                {"ykköset": 5, "kakkoset": 10, "kolmoset": 15, "neloset": 20, "vitoset": 25, "kutoset": 30},
                [5, 10, 15, 20, 25, 30, None, None, None, None, None, None, None, None, None]
             ),
            (
                {"ykköset": 5, "kakkoset": 10, "kolmoset": 15, "neloset": 20, "vitoset": 25, "kutoset": 30,
                 "yksi_pari": 6, "kaksi_paria": 12, "kolmiluku": 9, "neliluku": 12, "täyskäsi": 7, "pieni_suora": 15,
                 "iso_suora": 20, "sattuma": 30, "yatzy": 50
                 },
                [5, 10, 15, 20, 25, 30, 6, 12, 9, 12, 7, 15, 20, 30, 50]
            ),
            (
                {"ykköset": 0, "kakkoset": 0, "kolmoset": 0, "neloset": 0, "vitoset": 0, "kutoset": 0,
                 "yksi_pari": 0, "kaksi_paria": 0, "kolmiluku": 0, "neliluku": 0, "täyskäsi": 0, "pieni_suora": 0,
                 "iso_suora": 0, "sattuma": 0, "yatzy": 0
                 },
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            )
        ]
        for scores, expected in test_cases:
            for label, score in scores.items():
                self.scoreboard.set_score(label, score)
            self.assertEqual(self.scoreboard.get_scores_as_list(), expected)
