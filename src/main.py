import sys
from game.yatzy import Yatzy

if __name__ == "__main__":
    test_mode = "--test-mode" in sys.argv
    game = Yatzy(test_mode=test_mode)
    game.start()
