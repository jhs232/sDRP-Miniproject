import psycopg2
import pygrametl


def connect():
    connection = psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="db",
        user="admin",
        password="qwerty",
    )
    return pygrametl.ConnectionWrapper(connection)
