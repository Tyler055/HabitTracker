import sqlite3
from datetime import datetime, timedelta, timezone
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = 'habitDatabase.sqlite'


# --- Database Connection Management ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection(conn):
    if conn:
        conn.close()

# --- User Management ---
def find_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    close_db_connection(conn)
    return user

def create_user(username, password, email=None):
    if find_user_by_username(username) or (email and find_user_by_email(email)):
        raise ValueError("User with this username or email already exists.")
    
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (username, hashed_password, email))
    conn.commit()
    close_db_connection(conn)

def update_user_password(user_id, new_password):
    hashed_password = generate_password_hash(new_password)
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()
    close_db_connection(conn)

def find_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    close_db_connection(conn)
    return user

def find_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    close_db_connection(conn)
    return user

def find_user_by_reset_token(reset_token):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE reset_token = ?', (reset_token,)).fetchone()
    close_db_connection(conn)
    return user


# --- Password Reset Management ---
def generate_reset_token():
    return secrets.token_urlsafe(24)

def generate_reset_expiry():
    return (datetime.now(timezone.utc) + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

def set_reset_token_for_user(user_id):
    token = generate_reset_token()
    expiry = generate_reset_expiry()
    update_user_reset_token(user_id, token, expiry)

def update_user_reset_token(user_id, token, expiration):
    conn = get_db_connection()
    conn.execute('UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?',
                 (token, expiration, user_id))
    conn.commit()
    close_db_connection(conn)

def verify_reset_token(reset_token):
    user = find_user_by_reset_token(reset_token)
    if not user:
        return False
    try:
        expiry_time = datetime.strptime(user['reset_token_expiry'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) < expiry_time
    except Exception:
        return False

def reset_user_password(reset_token, new_password):
    if verify_reset_token(reset_token):
        user = find_user_by_reset_token(reset_token)
        if user:
            update_user_password(user['id'], new_password)
            clear_reset_token(user['id'])
            return True
    return False

def clear_reset_token(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET reset_token = NULL, reset_token_expiry = NULL WHERE id = ?', (user_id,))
    conn.commit()
    close_db_connection(conn)


# --- Goal Management ---
def get_goals_by_category(user_id, category):
    conn = get_db_connection()
    goals = conn.execute('SELECT id, text, completed FROM goals WHERE user_id = ? AND category = ? ORDER BY sort_order',
                         (user_id, category)).fetchall()
    close_db_connection(conn)
    return goals

def save_goals_for_category(user_id, category, goals):
    conn = get_db_connection()
    conn.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))
    for index, goal in enumerate(goals):
        conn.execute('''INSERT INTO goals (user_id, category, text, completed, sort_order)
                       VALUES (?, ?, ?, ?, ?)''',
                    (user_id, category, goal['text'], int(goal.get('completed', False)), index))
    conn.commit()
    close_db_connection(conn)

def update_goal(goal_id, new_text, new_completed):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET text = ?, completed = ? WHERE id = ?',
                 (new_text, int(new_completed), goal_id))
    conn.commit()
    close_db_connection(conn)

def toggle_goal_completion(goal_id):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET completed = 1 - completed WHERE id = ?', (goal_id,))
    conn.commit()
    close_db_connection(conn)

def reset_all_goals(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()
    close_db_connection(conn)


# --- Notification Management ---
def create_notification(user_id, message, time=None):
    if time is None:
        time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    conn.execute('INSERT INTO notifications (user_id, message, time) VALUES (?, ?, ?)',
                 (user_id, message, time))
    conn.commit()
    close_db_connection(conn)

def get_notifications(user_id):
    conn = get_db_connection()
    notifications = conn.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    close_db_connection(conn)
    return [{'id': row['id'], 'message': row['message'], 'time': row['time']} for row in notifications]

def delete_notification(notification_id, user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE id = ? AND user_id = ?', (notification_id, user_id))
    conn.commit()
    close_db_connection(conn)

def clear_notifications(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.commit()
    close_db_connection(conn)

