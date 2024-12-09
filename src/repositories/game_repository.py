
class GameRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM games ORDER BY total_score DESC")
        return cursor.fetchall()

    def create(self, total_score):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO games (total_score) VALUES (?)",
            (total_score, )
        )
        self._connection.commit()
        return True

    def save_game(self, scoreboard):
        """Save game's total score to database"""
        total_score = scoreboard.get_total_score()
        return self.create(total_score)
