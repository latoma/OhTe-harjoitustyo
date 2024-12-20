class ScoreboardRepository:
    """ Luokka joka vastaa pelien pistetaulukon tallentamisesta ja hakemisesta tietokannasta

    Attributes:
        connection: tietokantayhteys
    """
    def __init__(self, connection):
        """ Konstruktori, alustaa pistetaulukkorepositorion

        Args:
            connection: tietokantayhteys
        """
        self._connection = connection

    def create(self, game_id, scoreboard):
        """ Tallentaa pistetaulukon tietokantaan ja palauttaa sen id:n

        Args:
            game_id: pelin id
            scoreboard: pistetaulukko
        """
        cursor = self._connection.cursor()
        scores = ','.join(str(score) for score in scoreboard.get_scores_as_list())

        cursor.execute(
            "INSERT INTO scoreboard (game_id, scores) VALUES (?, ?)",
            (game_id, scores)
        )
        self._connection.commit()
        return cursor.lastrowid

    def find_by_game_id(self, game_id):
        """ Hakee pistetaulukon pelin id:n perusteella

        Args:
            game_id: pelin id
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT * FROM scoreboard WHERE game_id = ?",
            (game_id,)
        )
        return cursor.fetchone()
