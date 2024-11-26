from constants.labels import LABEL_KEYS

class Scoreboard:
    """
    A class to keep track of scores in a Yatzy game.
    """
    def __init__(self):
        self.__scores = {label: None for label in LABEL_KEYS}

    def get_scores(self):
        return self.__scores

    def set_score(self, label, score):
        self.__scores[label] = score

    def get_score(self, label):
        return self.__scores[label]

    def get_total_score(self):
        total_score = 0
        for score in self.__scores.values():
            if score is None:
                continue
            total_score += score
        return total_score

    def get_possible_scores(self, dice):
        dice_values = dice.get_values()
        possible_scores = {}
        for key in LABEL_KEYS:
            if self.__scores[key] is None:
                possible_scores[key] = self.calculate_score(key, dice_values)
        return possible_scores

    def calculate_score(self, label, dice_values):
        if label in ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']:
            value = LABEL_KEYS.index(label)+1
            return value * dice_values.count(value)
        elif label == 'a_pair':
            return self.calculate_n_of_a_kind_score(2, dice_values)
        elif label == 'two_pairs':
            return self.calculate_two_pairs_score(dice_values)
        elif label == 'three_of_a_kind':
            return self.calculate_n_of_a_kind_score(3, dice_values)
        elif label == 'four_of_a_kind':
            return self.calculate_n_of_a_kind_score(4, dice_values)
        elif label == 'full_house':
            return self.calculate_full_house_score(dice_values)
        elif label == 'small_straight':
            return self.calculate_small_straight_score(dice_values)
        elif label == 'large_straight':
            return self.calculate_large_straight_score(dice_values)
        elif label == 'chance':
            return sum(dice_values)
        elif label == 'yatzy':
            if dice_values.count(dice_values[0]) == 5:
                return 50
        return 0

    def calculate_n_of_a_kind_score(self, n, dice_values):
        score = 0
        for value in dice_values:
            if dice_values.count(value) >= n:
                score = max(score, n * value)
        return score

    def calculate_two_pairs_score(self, dice_values):
        pairs = set()
        for value in dice_values:
            if 2 <= dice_values.count(value) <= 3:
                pairs.add(value)
        if len(pairs) == 2:
            return sum(pairs) * 2
        return 0

    def calculate_full_house_score(self, dice_values):
        has_two_pairs = self.calculate_two_pairs_score(dice_values) > 0
        has_three_of_a_kind = self.calculate_n_of_a_kind_score(3, dice_values) > 0

        if has_two_pairs and has_three_of_a_kind:
            return sum(dice_values)
        return 0

    def calculate_small_straight_score(self, dice_values):
        for i in range(1, 6):
            if dice_values.count(i) != 1:
                return 0
        return 15

    def calculate_large_straight_score(self, dice_values):
        for i in range(2, 7):
            if dice_values.count(i) != 1:
                return 0
        return 20
