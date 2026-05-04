import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# ------------------ INIT DB ------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    print("Database initialized successfully!")

# Call DB init
init_db()

# ------------------ CHECK TABLE ------------------
with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

if tables:
    print("Database me tables hain:", tables)
else:
    print("Database me koi table nahi hai!")
