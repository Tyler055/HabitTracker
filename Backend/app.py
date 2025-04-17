import os
import secrets
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Compute project root (one level up from Backend/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR   = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='for_flask',
        password='25FlaskOnly25@',
        database='habit_tracker'
    )

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        hashed = generate_password_hash(p, method='pbkdf2:sha256')

        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute('SELECT 1 FROM users WHERE username = %s', (u,))
        if cur.fetchone():
            flash('Username already exists!', 'error')
            conn.close()
            return redirect(url_for('signup'))

        cur.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (u, hashed)
        )
        conn.commit()
        conn.close()

        flash('Signup successful—please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth.html', mode='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute('SELECT id, password FROM users WHERE username = %s', (u,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row[1], p):
            session['user_id'] = row[0]
            return redirect(url_for('habit_tracker'))

        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    return render_template('auth.html', mode='login')


@app.route('/habit_tracker')
def habit_tracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('habit.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
