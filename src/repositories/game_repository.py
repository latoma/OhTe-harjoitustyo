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
        cursor.execute("SELECT * FROM game ORDER BY total_score DESC")
        return cursor.fetchall()

    def create(self, player_name, total_score):
        """ Tallentaa pelatun pelin tietokantaan ja palauttaa sen id:n

        Args:
            player_name: pelaajan nimi
            total_score: pelin kokonaispisteet
        """
        cursor = self._connection.cursor()

        if len(player_name) > 10:
            player_name = player_name[:10]

        cursor.execute(
            "INSERT INTO game (player_name, total_score) VALUES (?, ?)",
            (player_name ,total_score)
        )
        self._connection.commit()
        return cursor.lastrowid
