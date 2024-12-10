class GameRepository:
    def __init__(self, connection, scoreboard_repository):
        self._connection = connection
        self._scoreboard_repository = scoreboard_repository

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM games ORDER BY total_score DESC")
        return cursor.fetchall()

    def create(self, total_score):
        """Save game data and return game_id"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO games (total_score) VALUES (?)",
            (total_score,)
        )
        self._connection.commit()
        return cursor.lastrowid # Return the id of the last row inserted
