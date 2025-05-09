import sqlite3
import os
from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random secret key

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'habitDatabase.sqlite')

# Configure Flask-Mail (make sure to replace these with actual email credentials)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'darkneuralai@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')  # Use environment variable for email password
app.config['MAIL_DEFAULT_SENDER'] = 'darkneuralai@gmail.com'

mail = Mail(app)

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

    # Users table creation
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT UNIQUE,
        reset_token TEXT,
        reset_token_expiry TEXT
    )''')

    # Goals table creation
    cur.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        text TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        sort_order INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # Notifications table creation
    cur.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    conn.commit()

# --- User Management ---
# In dataservice.py
def find_user_by_id(user_id):
    conn = get_db_connection()
    return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def create_user(username, password, email=None):
    if find_user_by_username(username) or (email and find_user_by_email(email)):
        raise ValueError("User with this username or email already exists.")
    
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (username, hashed_password, email))
    conn.commit()

def verify_password(stored_hash, provided_password):
    return check_password_hash(stored_hash, provided_password)

def update_user_password(user_id, new_password):
    hashed_password = generate_password_hash(new_password)
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
    conn.commit()

def find_user_by_username(username):
    return get_db_connection().execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

def find_user_by_email(email):
    return get_db_connection().execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def find_user_by_reset_token(reset_token):
    return get_db_connection().execute('SELECT * FROM users WHERE reset_token = ?', (reset_token,)).fetchone()

# --- Reset Token Management ---
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

# --- Goal Management ---
def get_goals_by_category(user_id, category):
    return get_db_connection().execute(
        'SELECT id, text, completed FROM goals WHERE user_id = ? AND category = ? ORDER BY sort_order',
        (user_id, category)).fetchall()

def save_goals_for_category(user_id, category, goals):
    conn = get_db_connection()
    conn.execute('DELETE FROM goals WHERE user_id = ? AND category = ?', (user_id, category))
    for index, goal in enumerate(goals):
        conn.execute('''INSERT INTO goals (user_id, category, text, completed, sort_order)
                       VALUES (?, ?, ?, ?, ?)''',
                    (user_id, category, goal['text'], int(goal.get('completed', False)), index))
    conn.commit()

def update_goal(goal_id, new_text, new_completed):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET text = ?, completed = ? WHERE id = ?',
                 (new_text, int(new_completed), goal_id))
    conn.commit()

def toggle_goal_completion(goal_id):
    conn = get_db_connection()
    conn.execute('UPDATE goals SET completed = 1 - completed WHERE id = ?', (goal_id,))
    conn.commit()

def reset_all_goals(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM goals WHERE user_id = ?', (user_id,))
    conn.commit()

# --- Notification System ---
def create_notification(user_id, message, time=None):
    if time is None:
        time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    conn.execute('INSERT INTO notifications (user_id, message, time) VALUES (?, ?, ?)',
                 (user_id, message, time))
    conn.commit()

def get_notifications(user_id):
    cur = get_db_connection().cursor()
    cur.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC', (user_id,))
    return [{'id': row['id'], 'message': row['message'], 'time': row['time']} for row in cur.fetchall()]

def delete_notification(notification_id, user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE id = ? AND user_id = ?', (notification_id, user_id))
    conn.commit()

def clear_notifications(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    conn.commit()

# --- Flask Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')

        try:
            create_user(username, password, email)
            flash("User created successfully", 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('auth.html')  # Ensure this points to the 'auth.html' template

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user_by_username(username)

        if user and verify_password(user['password'], password):
            session['user_id'] = user['id']
            flash("Login successful", 'success')
            return redirect(url_for('dashboard'))  # Redirect to a dashboard or another page after successful login
        else:
            flash("Invalid username or password", 'danger')

    return render_template('auth.html')  # Ensure this points to the 'auth.html' template

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully", 'success')
    return redirect(url_for('login'))

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = find_user_by_reset_token(token)
    if not user or not verify_reset_token(token):
        flash("Invalid or expired token", 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        if reset_user_password(token, new_password):
            flash("Password reset successfully", 'success')
            return redirect(url_for('login'))
        else:
            flash("Error resetting password", 'danger')
    
    return render_template('recover.html')  # Ensure this points to the 'recover.html' template

@app.route('/dashboard')
def dashboard():
    # This page can show the user's goals and notifications
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    goals = get_goals_by_category(user_id, 'daily')  # Example category
    notifications = get_notifications(user_id)
    return render_template('base.html', goals=goals, notifications=notifications)
