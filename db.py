import psycopg2
import pygrametl


def connect():
    connection = psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="fklub_bi",
        user="fklub_admin",
        password="secretpassword",
    )
    return pygrametl.ConnectionWrapper(connection)
