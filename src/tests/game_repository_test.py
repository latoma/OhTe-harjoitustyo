import unittest
from unittest.mock import Mock
from repositories.game_repository import GameRepository

# LLM generated
class TestGameRepository(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.mock_connection = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_scoreboard_repository = Mock()

        self.game_repository = GameRepository(
            self.mock_connection,
            self.mock_scoreboard_repository
        )

    def test_find_all(self):
        self.game_repository.find_all()

        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM games ORDER BY total_score DESC"
        )
        self.mock_cursor.fetchall.assert_called_once()

    def test_create_saves_game_with_score(self):
        test_score = 100
        expected_game_id = 1
        self.mock_cursor.lastrowid = expected_game_id

        result = self.game_repository.create(test_score)

        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO games (total_score) VALUES (?)",
            (test_score,)
        )
        self.mock_connection.commit.assert_called_once()
        self.assertEqual(result, expected_game_id)
