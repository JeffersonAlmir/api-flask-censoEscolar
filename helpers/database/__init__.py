import sqlite3
import psycopg2
from flask import g

from helpers.application import app


def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            host="localhost",
            port=5434,
            database="censo_escolar",
            user="postgres",
            password="123456"
        )
    return db
 
@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def connectDb():
    conn = psycopg2.connect(
        host="localhost",
        port=5434,
        database="censo_escolar",
        user="postgres",
        password="123456"
    )
    return conn
