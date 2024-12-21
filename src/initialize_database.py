from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
      DROP TABLE IF EXISTS game;
    ''')

    cursor.execute('''
      DROP TABLE IF EXISTS scoreboard;
    ''')

    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE game (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            player_name VARCHAR(10),
            total_score INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE scoreboard (
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            scores TEXT,
            FOREIGN KEY (game_id) REFERENCES games(id)
        )
    ''')

    connection.commit()

def initialize_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)
    connection.close()
    print("Database initialized")

def initialize_test_database():
    connection = get_database_connection(test=True)
    drop_tables(connection)
    create_tables(connection)
    connection.close()
    print("Test database initialized")

if __name__ == "__main__":
    initialize_database()
    initialize_test_database()
