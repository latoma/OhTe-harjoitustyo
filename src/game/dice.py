import random

class Dice:
    """
    This class is used to store and roll five dice
    """
    def __init__(self):
        self.__dice = [Die() for _ in range(5)]

    def get_dice(self):
        """
        returns the list of dice
        """
        return self.__dice

    def roll_dice(self):
        """
        rolls all dice that are not in hold status
        """
        for die in self.__dice:
            if not die.in_hold():
                die.roll()

class Die:
    """
    This class is used to store a die's value and hold status
    """
    def __init__(self):
        # value as an integer
        self.__value = 0

        self.__in_hold = False

    def roll(self):
        """
        'rolls the die', meaning it sets a new random dice value
        """
        self.__value = random.randint(1, 6)

    def get_value(self):
        """
        returns the die's value
        """
        return self.__value

    def in_hold(self):
        """
        returns the die's hold status
        """
        return self.__in_hold

    def toggle_hold_status(self):
        """
        toggles Die's hold status to the opposite
        """
        if self.__value == 0:
            return False
        
        self.__in_hold = not self.__in_hold
        return True
