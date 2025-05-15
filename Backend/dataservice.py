import sqlite3
import os
from flask import Flask, g
from datetime import datetime, timedelta
import secrets
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

# --- Database Initialization ---
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT UNIQUE,
        reset_token TEXT,
        reset_token_expiry TEXT,
        deleted_at TEXT
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        text TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        sort_order INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        theme TEXT DEFAULT 'light',
        email_notifications INTEGER DEFAULT 1,
        push_notifications INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        token_name TEXT NOT NULL,
        token_value TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS feature_flags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature_name TEXT NOT NULL,
        is_enabled INTEGER NOT NULL DEFAULT 1
    )''')

    cur.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals (user_id)')

    conn.commit()

# --- Feature Flag Management ---
def is_feature_enabled(feature_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT is_enabled FROM feature_flags WHERE feature_name = ?', (feature_name,))
    result = cur.fetchone()
    return result and result['is_enabled'] == 1

def insert_feature_flag(feature_name, is_enabled=1):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO feature_flags (feature_name, is_enabled) VALUES (?, ?)', (feature_name, is_enabled))
    conn.commit()

# --- Token Management ---
def insert_token(user_id, token_name, token_value):
    conn = get_db_connection()
    cur = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        'INSERT INTO tokens (user_id, token_name, token_value, created_at) VALUES (?, ?, ?, ?)',
        (user_id, token_name, token_value, created_at)
    )
    conn.commit()

def get_user_token(user_id, token_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tokens WHERE user_id = ? AND token_name = ?', (user_id, token_name))
    return cur.fetchone()

# --- User Management ---
def find_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ? AND deleted_at IS NULL', (user_id,))
    return cur.fetchone()

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
    if find_user_by_username(username) or (email and find_user_by_email(email)):
        raise ValueError("User with this identifier already exists.")
    conn = get_db_connection()
    hashed_password = generate_password_hash(password)
    conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (username, hashed_password, email))
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

def update_user_password(user_id, new_password):
    conn = get_db_connection()
    hashed_password = generate_password_hash(new_password)
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    insert_token(user_id, 'last_password_reset', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    conn.commit()

def update_user_reset_token(user_id, expiry_duration_minutes=60):
    # Generate a secure, one-time-use token
    reset_token = secrets.token_urlsafe(32)
    reset_token_expiry = (datetime.now() + timedelta(minutes=expiry_duration_minutes)).strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    conn.execute(
        'UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?',
        (reset_token, reset_token_expiry, user_id)
    )
    conn.commit()
    return reset_token, reset_token_expiry

def get_user_reset_token(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT reset_token, reset_token_expiry FROM users WHERE id = ?', (user_id,))
    result = cur.fetchone()
    
    if result:
        reset_token, reset_token_expiry = result
        # Check if the token is still valid
        if reset_token and reset_token_expiry:
            expires_at = datetime.strptime(reset_token_expiry, '%Y-%m-%d %H:%M:%S')
            if expires_at > datetime.now():
                return {
                    'token': reset_token,
                    'expires_at': reset_token_expiry,
                    'created_at': (expires_at - timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
                }
    
    return None


def clear_reset_token(user_id):
    """
    Remove reset token and expiry after successful reset or expiration.
    """
    conn = get_db_connection()
    conn.execute(
        'UPDATE users SET reset_token = NULL, reset_token_expiry = NULL WHERE id = ?',
        (user_id,)
    )
    conn.commit()

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
        cur.execute('''INSERT INTO goals (user_id, category, text, completed, sort_order) VALUES (?, ?, ?, ?, ?)''',
                    (user_id, category, goal['text'], int(goal.get('completed', False)), index))
    conn.commit()
    return 'Goals saved successfully.'

def update_goal(goal_id, new_text, new_completed):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET text = ?, completed = ? WHERE id = ?', (new_text, int(new_completed), goal_id))
    conn.commit()
    return 'Goal updated successfully.'

def toggle_goal_completion(goal_id):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET completed = 1 - completed WHERE id = ?', (goal_id,))
    conn.commit()
    return 'Goal completion toggled.'

def reset_all_goals(user_id):
    """
    Completely remove all goals for the given user.
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()
    return 'All goals reset successfully.'

# --- Notification Management ---
def create_notification(user_id, message, time=None):
    if time is None:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existing = get_notifications(user_id)
    if any(note['message'] == message for note in existing):
        return 'Notification already exists.'
    conn = get_db_connection()
    conn.execute('INSERT INTO notifications (user_id, message, time) VALUES (?, ?, ?)',
                 (user_id, message, time))
    conn.commit()
    return 'Notification created.'

def get_notifications(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC', (user_id,))
    return [{'id': row['id'], 'message': row['message'], 'time': row['time']} for row in cur.fetchall()]

def delete_notification(notification_id, user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE id = ? AND user_id = ?', (notification_id, user_id))
    conn.commit()
    return 'Notification deleted.'

def clear_notifications(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.commit()
    return 'All notifications cleared.'

# --- Email Credential Access ---
def get_email_credentials():
    email = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")
    if not email or not password:
        raise ValueError("Email credentials not found in environment variables.")
    return {'email': email, 'password': password}

# --- Standalone Execution ---
if __name__ == "__main__":
    app = Flask(__name__)
    init_app(app)
    with app.app_context():
        init_db()
        print("Database initialized.")