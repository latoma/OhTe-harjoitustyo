from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
      DROP TABLE IF EXISTS games
    ''')

    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE games (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_score INTEGER
        )
    ''')

    connection.commit()

def initialize_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
