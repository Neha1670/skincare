# show_users.py
import sqlite3
import os
from werkzeug.security import check_password_hash

# agar aapka file same folder me hai to yeh chal jayega
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def show_users():
    if not os.path.exists(DB_PATH):
        print("Database file users.db found nahi hua:", DB_PATH)
        return

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # tables list
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        print("Tables:", tables)

        # agar users table exist kare to data fetch karo
        try:
            c.execute("SELECT id, username, password FROM users;")
            rows = c.fetchall()
        except sqlite3.OperationalError as e:
            print("Error (table missing?):", e)
            return

        if not rows:
            print("Users table me koi data nahi hai.")
            return

        print("\nUsers table data:")
        for r in rows:
            uid, uname, phash = r
            print(f"ID: {uid}  |  Username: {uname}  |  PasswordHash: {phash[:40]}...")

        # optional: test first row password check (change '123' to password to test)
        test_password = "123"   # agar aap kisi known password test karna chaho to yahan badlo
        uname0, hash0 = rows[0][1], rows[0][2]
        ok = check_password_hash(hash0, test_password)
        print(f"\nPassword check for user '{uname0}' using test password '{test_password}': {ok}")

if __name__ == "__main__":
    show_users()
