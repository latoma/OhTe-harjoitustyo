import unittest
from unittest.mock import Mock
from repositories.scoreboard_repository import ScoreboardRepository

class TestScoreboardRepository(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.mock_connection = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.scoreboard_repository = ScoreboardRepository(self.mock_connection)

    def test_find_by_game_id_success(self):
        game_id = 1
        expected_scoreboard = (1, "10,20,30", 60)
        self.mock_cursor.fetchone.return_value = expected_scoreboard

        result = self.scoreboard_repository.find_by_game_id(game_id)

        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM scoreboards WHERE game_id = ?",
            (game_id,)
        )
        self.assertEqual(result, expected_scoreboard)

    def test_find_by_game_id_fail_is_none(self):
        game_id = 999
        self.mock_cursor.fetchone.return_value = None

        result = self.scoreboard_repository.find_by_game_id(game_id)

        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM scoreboards WHERE game_id = ?",
            (game_id,)
        )
        self.assertIsNone(result)

    def test_create_saves_scoreboard(self):
      game_id = 1
      mock_scoreboard = Mock()
      mock_scoreboard.get_scores_as_list.return_value = [10, 20, 30]
      mock_scoreboard.get_total_score.return_value = 60
      expected_id = 42
      self.mock_cursor.lastrowid = expected_id

      result = self.scoreboard_repository.create(game_id, mock_scoreboard)

      self.mock_cursor.execute.assert_called_once_with(
          "INSERT INTO scoreboards (game_id, scores, total_score) VALUES (?, ?, ?)",
          (game_id, "10,20,30", 60)
      )
      self.mock_connection.commit.assert_called_once()
      self.assertEqual(result, expected_id)
