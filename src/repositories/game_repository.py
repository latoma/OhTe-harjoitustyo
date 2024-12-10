class GameRepository:
    """ Luokka joka vastaa pelien tallentamisesta ja hakemisesta tietokannasta

    Attributes:
        connection: tietokantayhteys
    """
    def __init__(self, connection):
        """ Konstruktori, alustaa pelirepositorion

        Args:
            connection: tietokantayhteys
        """
        self._connection = connection

    def find_all(self):
        """ Hakee kaikki pelit ja järjestää ne kokonaispisteiden mukaan laskevaan järjestykseen """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM games ORDER BY total_score DESC")
        return cursor.fetchall()

    def create(self, total_score):
        """ Tallentaa uuden pelin tietokantaan ja palauttaa sen id:n

        Args:
            total_score: pelin kokonaispisteet
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO games (total_score) VALUES (?)",
            (total_score,)
        )
        self._connection.commit()
        return cursor.lastrowid # Return the id of the last row inserted
