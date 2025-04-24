import sqlite3

DB_NAME = 'habitDatabase.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with users and goals tables."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Create users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create goals table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed BOOLEAN NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_goal(goal_data):
    """Save a goal to the goals table in the database."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert the goal into the goals table
    cur.execute('''
        INSERT INTO goals (text, completed)
        VALUES (?, ?)
    ''', (goal_data['text'], goal_data['completed']))

    conn.commit()
    conn.close()
