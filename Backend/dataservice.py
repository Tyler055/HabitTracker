import sqlite3
import os
from flask import g
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'habitDatabase.sqlite')

# --- Database Connection Management ---
def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH, timeout=10, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db_connection)

# --- Initialize Database and Tables ---
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create users table with soft-delete
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            reset_token TEXT,
            reset_token_expiry TEXT,
            deleted_at TEXT
        )
    ''')

    # Create goals table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            sort_order INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create user settings table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            email_notifications INTEGER DEFAULT 1,
            push_notifications INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create notifications table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Add indexes to optimize queries
    cur.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals (user_id)')

    conn.commit()

# --- User Management ---
def find_user_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ? AND deleted_at IS NULL', (username,))
    return cur.fetchone()

def find_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = ? AND deleted_at IS NULL', (email,))
    return cur.fetchone()

def create_user(username, password, email=None):
    try:
        if find_user_by_username(username) or (email and find_user_by_email(email)):
            raise ValueError("User with this identifier already exists.")
        conn = get_db_connection()
        hashed_password = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                     (username, hashed_password, email))
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError("Database Integrity Error: " + str(e))

def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.execute('DELETE FROM user_settings WHERE user_id = ?', (user_id,))
    conn.commit()

def delete_user_by_id(user_id):
    conn = get_db_connection()
    # Deleting user-related data from multiple tables to maintain integrity
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.execute('DELETE FROM user_settings WHERE user_id = ?', (user_id,))
    conn.commit()


def soft_delete_user(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET deleted_at = ? WHERE id = ?',
                 (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
    conn.commit()

def restore_user(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET deleted_at = NULL WHERE id = ?', (user_id,))
    conn.commit()

def find_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ? AND deleted_at IS NULL', (user_id,))
    return cur.fetchone()

def update_user_password(user_id, new_password):
    conn = get_db_connection()
    hashed_password = generate_password_hash(new_password)
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()

def update_user_reset_token(user_id, reset_token, expiry):
    conn = get_db_connection()
    conn.execute('UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?', 
                 (reset_token, expiry, user_id))
    conn.commit()

# --- Goal Management ---
def get_goals_by_category(user_id, category):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM goals WHERE user_id = ? AND category = ? ORDER BY sort_order', 
                (user_id, category))
    return [{'id': row['id'], 'category': row['category'], 'text': row['text'], 'completed': row['completed']} 
            for row in cur.fetchall()]

def save_goals_for_category(user_id, category, goals):
    conn = get_db_connection()
    cur = conn.cursor()
    for goal in goals:
        cur.execute('INSERT INTO goals (user_id, category, text, completed) VALUES (?, ?, ?, ?)', 
                    (user_id, category, goal['text'], goal.get('completed', 0)))
    conn.commit()

def reset_all_goals(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET completed = 0 WHERE user_id = ?', (user_id,))
    conn.commit()

# --- Notification Management ---
def get_notifications(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC', (user_id,))
    return [{'id': row['id'], 'message': row['message'], 'time': row['time']} for row in cur.fetchall()]

def create_notification(user_id, message):
    conn = get_db_connection()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('INSERT INTO notifications (user_id, message, time) VALUES (?, ?, ?)', 
                 (user_id, message, time))
    conn.commit()

def delete_notification(notification_id, user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE id = ? AND user_id = ?', (notification_id, user_id))
    conn.commit()

def clear_notifications(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.commit()

# --- Standalone Execution ---
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    init_app(app)
    with app.app_context():
        init_db()
        print("Database initialized.")
