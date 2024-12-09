import sys
from game.yatzy import Yatzy
from initialize_database import initialize_database

if __name__ == "__main__":
    initialize_database()
    test_mode = "--test-mode" in sys.argv
    game = Yatzy(test_mode=test_mode)
    game.start()
