import sqlite3

# Make sure this path matches your actual DB
conn = sqlite3.connect('instance/database.db')  # or wherever your DB is
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    print("Added 'reset_token' column.")
except sqlite3.OperationalError as e:
    print(f"Skipped 'reset_token': {e}")

try:
    cur.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME")
    print("Added 'reset_token_expiry' column.")
except sqlite3.OperationalError as e:
    print(f"Skipped 'reset_token_expiry': {e}")

conn.commit()
conn.close()
