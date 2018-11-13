import sqlite3
from contextlib import contextmanager


#  @contextmanager converts functions into context managers
@contextmanager
def db_connect(db):
    # initialize a connection
    connection = sqlite3.connect(db)
    # makes the queries and store results
    cursor = connection.cursor()
    yield cursor
    connection.commit()
    connection.close()
