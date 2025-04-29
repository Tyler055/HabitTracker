import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'habitDatabase.sqlite')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # ... (rest of init_db code) ...
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

def find_user_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_goals_by_category(user_id, category):
    conn = get_db_connection()
    cur = conn.cursor()
    goals = cur.execute('SELECT text, completed FROM goals WHERE user_id = ? AND category = ? ORDER BY sort_order', (user_id, category)).fetchall()
    conn.close()
    return goals

def save_goals_for_category(user_id, category, goals):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))
    for index, goal in enumerate(goals):
        cur.execute('INSERT INTO goals (user_id, category, text, completed, sort_order) VALUES (?, ?, ?, ?, ?)',
                       (user_id, category, goal['text'], int(goal.get('completed', False)), index))
    conn.commit()
    conn.close()

def reset_all_goals(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()