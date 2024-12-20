import os
import sqlite3

dirname = os.path.dirname(__file__)

def get_database_connection(test=False):
    db_file = "test_database.sqlite" if test else "database.sqlite"
    connection = sqlite3.connect(os.path.join(dirname, "..", "data", db_file))
    connection.row_factory = sqlite3.Row

    return connection
