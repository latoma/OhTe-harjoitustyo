import unittest
from game.dice import Dice, Die


class TestDice(unittest.TestCase):
    def test_dice_has_five_dice(self):
        dice = Dice()
        self.assertEqual(len(dice.get_dice()), 5)

    def test_die_rolls_between_1_and_6(self):
        die = Die()
        die.roll()
        self.assertTrue(1 <= die.get_value() <= 6)

    def test_cannot_hold_unused_die(self):
        die = Die()
        self.assertEqual(die.get_value(), 0)
        initial_hold = die.in_hold()
        die.toggle_hold_status()
        self.assertEqual(die.in_hold(), initial_hold)

    def test_can_hold_used_die(self):
        die = Die()
        die.roll()
        initial_hold = die.in_hold()
        die.toggle_hold_status()
        self.assertNotEqual(die.in_hold(), initial_hold)

    def test_roll_dice_rolls_unheld_dice(self):
        dice = Dice()
        dice.roll_dice()

        dice.get_dice()[0].toggle_hold_status()
        dice.get_dice()[4].toggle_hold_status()

        held_values = [
            dice.get_dice()[0].get_value(),
            dice.get_dice()[4].get_value()
        ]

        dice.roll_dice()

        self.assertEqual(dice.get_dice()[0].get_value(), held_values[0])
        self.assertEqual(dice.get_dice()[4].get_value(), held_values[1])

    def test_get_values_returns_correct_values(self):
        dice = Dice()
        expected_values = [1, 2, 3, 4, 5]
        for i, value in enumerate(expected_values):
            dice.get_dice()[i]._Die__value = value

        self.assertEqual(dice.get_values(), expected_values)

    def test_reset_holds_resets_all_holds(self):
        dice = Dice()
        for die in dice.get_dice():
            die.toggle_hold_status()

        dice.reset_holds()

        for die in dice.get_dice():
            self.assertFalse(die.in_hold())

    def test_lock_dice_locks_all_dice(self):
        dice = Dice()
        dice.lock_dice()
        for die in dice.get_dice():
            self.assertTrue(die.is_locked())

    def test_unlock_dice_unlocks_all_dice(self):
        dice = Dice()
        dice.unlock_dice()
        for die in dice.get_dice():
            self.assertFalse(die.is_locked())
