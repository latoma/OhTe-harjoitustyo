import random

class Dice:
    """
    Tämä luokka on tarkoitettu viiden nopan säilyttämiseen ja heittämiseen

    Attributes:
        __dice: lista viidestä nopasta
    """

    def __init__(self):
        self.__dice = [Die() for _ in range(5)]

    def get_dice(self):
        """
        palauttaa listan nopista
        """
        return self.__dice

    def get_values(self):
        """
        palauttaa listan noppien arvoista
        """
        return [die.get_value() for die in self.__dice]

    def roll_dice(self):
        """
        heittää kaikki nopat, jotka eivät ole pidossa
        """
        for die in self.__dice:
            if not die.in_hold():
                die.roll()

    def reset_holds(self):
        """
        nollaa kaikkien noppien pito-tilan
        """
        for die in self.__dice:
            die.reset_hold()

    def lock_dice(self):
        """
        lukitsee kaikki nopat niin, että niitä ei voi pitää
        """
        for die in self.__dice:
            die.lock()

    def unlock_dice(self):
        """
        avaa kaikkien noppien lukituksen niin, että niitä voi pitää
        """
        for die in self.__dice:
            die.unlock()


class Die:
    """
    Tämä luokka on tarkoitettu nopan arvon ja pito-tilan säilyttämiseen
    """

    def __init__(self):
        self.__value = 0
        self.__in_hold = False
        self.__locked = False

    def roll(self):
        """
        'heittää nopan', eli asettaa uuden satunnaisen nopan arvon
        """
        self.__value = random.randint(1, 6)

    def get_value(self):
        """
        palauttaa nopan arvon
        """
        return self.__value

    def in_hold(self):
        """
        palauttaa nopan pito-tilan
        """
        return self.__in_hold

    def toggle_hold_status(self):
        """
        vaihtaa nopan pito-tilan vastakkaiseksi
        """
        if self.__value == 0:
            return False

        self.__in_hold = not self.__in_hold
        return True

    def reset_hold(self):
        """
        nollaa nopan pito-tilan
        """
        self.__in_hold = False

    def lock(self):
        """
        lukitsee nopan niin, ettei sitä voi pitää
        """
        self.__locked = True

    def unlock(self):
        """
        avaa nopan lukituksen niin, että sitä voi pitää
        """
        self.__locked = False

    def is_locked(self):
        """
        palauttaa nopan lukitus-tilan
        """
        return self.__locked
