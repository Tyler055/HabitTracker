import sqlite3
import os
from flask import g
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

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

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            reset_token TEXT,
            reset_token_expiry TEXT
        )
    ''')

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

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            email_notifications INTEGER DEFAULT 1,
            push_notifications INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()

# --- User Management ---

def create_user(username, password, email=None):
    if find_user_by_username(username) or (email and find_user_by_email(email)):
        raise ValueError("User with this username or email already exists.")
    
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    cur.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                (username, hashed_password, email))
    conn.commit()
    return "User created successfully."

def verify_password(stored_hash, provided_password):
    return check_password_hash(stored_hash, provided_password)

def update_user_password(user_id, new_password):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
    cur.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()
    return "Password updated successfully."

def update_user_reset_token(user_id, token, expiration):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?', 
                (token, expiration, user_id))
    conn.commit()
    return "Reset token updated successfully."

def find_user_by_username(username):
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

def find_user_by_email(email):
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def find_user_by_id(user_id):
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def find_user_by_reset_token(reset_token):
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE reset_token = ?', (reset_token,)).fetchone()

# --- Goal Management ---

def get_goals_by_category(user_id, category):
    conn = get_db_connection()
    return conn.execute(
        'SELECT id, text, completed FROM goals WHERE user_id = ? AND category = ? ORDER BY sort_order',
        (user_id, category)
    ).fetchall()

def save_goals_for_category(user_id, category, goals):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))

    for index, goal in enumerate(goals):
        cur.execute('''
            INSERT INTO goals (user_id, category, text, completed, sort_order)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, goal['text'], int(goal.get('completed', False)), index))

    conn.commit()
    return "Goals saved successfully."

def update_goal(goal_id, new_text, new_completed):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE goals SET text = ?, completed = ? WHERE id = ?',
                (new_text, int(new_completed), goal_id))
    conn.commit()
    return 'Goal updated successfully.'

def toggle_goal_completion(goal_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE goals SET completed = 1 - completed WHERE id = ?', (goal_id,))
    conn.commit()
    return 'Goal completion toggled.'

def reset_all_goals(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()
    return "All goals reset successfully."

# --- Notification Management ---

def create_notification(user_id, message, time=None):
    if time is None:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    existing = get_notifications(user_id)
    if any(note['message'] == message for note in existing):
        return "Notification already exists."

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notifications (user_id, message, time) VALUES (?, ?, ?)',
                (user_id, message, time))
    conn.commit()
    return "Notification created."

def get_notifications(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC', (user_id,))
    return [{'id': row['id'], 'message': row['message'], 'time': row['time']} for row in cur.fetchall()]

def delete_notification(notification_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notifications WHERE id = ? AND user_id = ?', (notification_id, user_id))
    conn.commit()
    return "Notification deleted."

def clear_notifications(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.commit()
    return "All notifications cleared."

# --- Email Credential Access ---

def get_email_credentials():
    email = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")

    if not email or not password:
        raise ValueError("Email credentials not found in environment variables.")

    return {
        'email': email,
        'password': password
    }
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    init_app(app)
    with app.app_context():
        init_db()
        print("Database initialized.")

