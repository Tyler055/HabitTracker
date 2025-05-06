import sqlite3
import os
from flask import g
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'habitDatabase.sqlite')

def get_db_connection():
    """Helper function to get a database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH, timeout=10, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db_connection(e=None):
    """Helper function to close the database connection after request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Initializes the Flask app by setting up teardown for DB connection."""
    app.teardown_appcontext(close_db_connection)

def init_db():
    """Initialize the database and create necessary tables."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Create users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT UNIQUE
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
    # Create notifications table
    cur.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    conn.commit()

# --- User functions ---

def create_user(username, password, email=None):
    """Creates a new user in the database."""
    if find_user_by_username(username) or (email and find_user_by_email(email)):
        raise ValueError("User with this username or email already exists.")
    
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, hashed_password, email))
    conn.commit()
    return "User created successfully."

def verify_password(stored_hash, provided_password):
    """Verify a stored password hash with a provided password."""
    return check_password_hash(stored_hash, provided_password)

def update_user_password(user_id, new_password):
    """Updates the user's password."""
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(new_password)
    cur.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()
    return "Password updated successfully."

def find_user_by_username(username):
    """Finds a user by their username."""
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

def find_user_by_email(email):
    """Finds a user by their email."""
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def find_user_by_id(user_id):
    """Finds a user by their user_id."""
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

# --- Goal functions ---

def get_goals_by_category(user_id, category):
    """Gets all goals by category for a specific user."""
    conn = get_db_connection()
    return conn.execute('SELECT id, text, completed FROM goals WHERE user_id = ? AND category = ? ORDER BY sort_order', 
                        (user_id, category)).fetchall()

def save_goals_for_category(user_id, category, goals):
    """Saves goals to the database for a specific category."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))
    for index, goal in enumerate(goals):
        cur.execute('INSERT INTO goals (user_id, category, text, completed, sort_order) VALUES (?, ?, ?, ?, ?)',
                    (user_id, category, goal['text'], int(goal.get('completed', False)), index))
    conn.commit()
    return "Goals saved successfully."

def update_goal(goal_id, new_text, new_completed):
    """Updates an existing goal."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE goals SET text = ?, completed = ? WHERE id = ?', (new_text, int(new_completed), goal_id))
    conn.commit()
    return 'Goal updated successfully.'

def toggle_goal_completion(goal_id):
    """Toggles the completion status of a goal."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE goals SET completed = 1 - completed WHERE id = ?', (goal_id,))
    conn.commit()
    return 'Goal completion toggled.'

def reset_all_goals(user_id):
    """Resets all goals for a specific user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()
    return "All goals reset successfully."

# --- Notification functions ---

def create_notification(user_id, message, time=None):
    """Creates a new notification for a user."""
    if time is None:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notifications (user_id, message, time) VALUES (?, ?, ?)", (user_id, message, time))
    conn.commit()
    return "Notification created."

def get_notifications(user_id):
    """Gets all notifications for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC", (user_id,))
    return [{'id': row['id'], 'message': row['message'], 'time': row['time']} for row in cur.fetchall()]

def delete_notification(notification_id, user_id):
    """Deletes a single notification by ID for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notifications WHERE id = ? AND user_id = ?", (notification_id, user_id))
    conn.commit()
    return "Notification deleted."

def clear_notifications(user_id):
    """Clears all notifications for a user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
    conn.commit()
    return "All notifications cleared."
