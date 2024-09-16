# database.py

import sqlite3

DATABASE = 'database.sqlite3'

def get_connection():
    return sqlite3.connect(DATABASE)

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()
