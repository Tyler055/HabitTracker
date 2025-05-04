import sqlite3
import os
from flask import g
from werkzeug.security import generate_password_hash

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'habitDatabase.sqlite')

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
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT
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
    conn.commit()

def create_user(username, password, email=None):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute(
        'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
        (username, hashed_password, email)
    )
    conn.commit()

def find_user_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    return cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

def find_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    return cur.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def find_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    return cur.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def get_goals_by_category(user_id, category):
    conn = get_db_connection()
    cur = conn.cursor()
    goals = cur.execute('''SELECT text, completed FROM goals
                           WHERE user_id = ? AND category = ? ORDER BY sort_order''', 
                           (user_id, category)).fetchall()
    return goals

def save_goals_for_category(user_id, category, goals):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))
    for index, goal in enumerate(goals):
        cur.execute('''INSERT INTO goals (user_id, category, text, completed, sort_order)
                       VALUES (?, ?, ?, ?, ?)''', 
                    (user_id, category, goal['text'], int(goal.get('completed', False)), index))
    conn.commit()

def update_user_password(user_id, new_password):
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(new_password)
    cur.execute('''UPDATE users SET password = ? WHERE id = ?''', 
                (hashed_password, user_id))
    conn.commit()

def reset_all_goals(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()
