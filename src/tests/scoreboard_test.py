# src/tests/scoreboard_test.py
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
        self.scoreboard.set_score("ones", 3)
        self.assertEqual(self.scoreboard.get_score("ones"), 3)

    def test_total_score_sum_of_all_scores(self):
        scores = {"ones": 3, "twos": 6, "threes": 9}
        for label, score in scores.items():
            self.scoreboard.set_score(label, score)
        self.assertEqual(self.scoreboard.get_total_score(), 18)

    def test_upper_section_scoring(self):
        test_cases = [
            ([1,1,1,2,3], "ones", 3),
            ([2,2,2,2,1], "twos", 8),
            ([3,3,3,1,2], "threes", 9),
            ([4,4,1,2,3], "fours", 8),
            ([5,5,5,1,2], "fives", 15),
            ([6,6,6,6,1], "sixes", 24)
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
                self.scoreboard.calculate_score("a_pair", dice_values),
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
                self.scoreboard.calculate_score("two_pairs", dice_values),
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
                self.scoreboard.calculate_score("three_of_a_kind", dice_values),
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
                self.scoreboard.calculate_score("four_of_a_kind", dice_values),
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
                self.scoreboard.calculate_score("full_house", dice_values),
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
                self.scoreboard.calculate_score("small_straight", dice_values),
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
                self.scoreboard.calculate_score("large_straight", dice_values),
                expected
            )

    def test_chance_scoring(self):
        test_cases = [
            ([1,2,3,4,5], 15),
            ([6,6,6,6,6], 30)
        ]

        for dice_values, expected in test_cases:
            self.assertEqual(
                self.scoreboard.calculate_score("chance", dice_values),
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
        self.assertIn("full_house", scores)

        self.scoreboard.set_score("full_house", 7)
        scores = self.scoreboard.get_possible_scores(self.mock_dice)
        self.assertNotIn("full_house", scores)

if __name__ == '__main__':
    unittest.main()
