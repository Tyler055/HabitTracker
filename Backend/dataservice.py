import sqlite3
import os
from flask import g
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

# Define path to SQLite database file
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'habitDatabase.sqlite')


# --- Database Connection Management ---

def get_db_connection():
    """
    Create a new SQLite connection and store it in Flask's `g` object.
    Ensures each request reuses the same connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH, timeout=10, check_same_thread=False)
        g.db.row_factory = sqlite3.Row  # Allow column access by name
    return g.db


def close_db_connection(e=None):
    """
    Closes the database connection when the request ends.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    """
    Register teardown logic for the Flask app to close DB connection.
    """
    app.teardown_appcontext(close_db_connection)


def init_db():
    """
    Initialize the database tables (users, goals, notifications).
    Called once during setup or app start.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Create users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT UNIQUE,
        reset_token TEXT,
        reset_token_expiry TEXT
    )''')

    # Create goals table
    cur.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        text TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        sort_order INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # Create user_settings table
    cur.execute('''CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        theme TEXT DEFAULT 'light',
        email_notifications INTEGER DEFAULT 1,
        push_notifications INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # Create notifications table
    cur.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    conn.commit()


# --- User Management ---

def create_user(username, password, email=None):
    if find_user_by_username(username) or (email and find_user_by_email(email)):
        raise ValueError("User with this username or email already exists.")
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                (username, hashed_password, email))
    conn.commit()
    return "User created successfully."


def verify_password(stored_hash, provided_password):
    return check_password_hash(stored_hash, provided_password)


def update_user_password(user_id, new_password):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(new_password)
    cur.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()
    return "Password updated successfully."


def update_user_reset_token(user_id, token, expiration):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(''' 
        UPDATE users
        SET reset_token = ?, reset_token_expiry = ?
        WHERE id = ?
    ''', (token, expiration, user_id))
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


# --- Reset Token Management ---

def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


def generate_reset_expiry():
    return (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')


def set_reset_token_for_user(user_id):
    reset_token = generate_reset_token()
    reset_token_expiry = generate_reset_expiry()
    return update_user_reset_token(user_id, reset_token, reset_token_expiry)


def verify_reset_token(reset_token):
    user = find_user_by_reset_token(reset_token)
    if user:
        expiry_time = datetime.strptime(user['reset_token_expiry'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() < expiry_time:
            return True
    return False


def reset_user_password(reset_token, new_password):
    if verify_reset_token(reset_token):
        user = find_user_by_reset_token(reset_token)
        if user:
            user_id = user['id']
            update_user_password(user_id, new_password)
            clear_reset_token(user_id)
            return "Password reset successfully."
    return "Invalid or expired reset token."


def clear_reset_token(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?',
                (None, None, user_id))
    conn.commit()
    return "Reset token cleared."


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

    # Clear old goals
    cur.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))

    # Insert new ones
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


# --- Notification System ---

def create_notification(user_id, message, time=None):
    if time is None:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


# --- Email Credential Access (Optional) ---

def get_email_credentials():
    """
    Retrieve email credentials from environment variables.
    This is used for sending emails securely via Flask-Mail or smtplib.
    """
    email = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")

    if not email or not password:
        raise ValueError("Email credentials not found in environment variables.")

    return {
        'email': email,
        'password': password
    }
