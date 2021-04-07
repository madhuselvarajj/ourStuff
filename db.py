import sqlite3
from flask import current_app, g

db_name = "ourStuff.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(db_name)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()