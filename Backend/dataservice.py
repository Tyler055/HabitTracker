
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='for_flask',
        password='25FlaskOnly25@',
        database='habit_tracker'
    )

def user_exists(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM users WHERE username = %s', (username,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def create_user(username, password):
    hashed = generate_password_hash(password, method='pbkdf2:sha256')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (username, password) VALUES (%s, %s)',
        (username, hashed)
    )
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, password FROM users WHERE username = %s', (username,))
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row[1], password):
        return row[0]
    return None
