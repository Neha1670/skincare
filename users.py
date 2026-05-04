import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    if users:
        print("Users in DB:")
        for user in users:
            print(user)
    else:
        print("No users found!")
