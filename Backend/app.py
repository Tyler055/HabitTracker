import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from dataservice import get_db_connection, init_db, save_goal

# Project setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'WebApp', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# Route to home page, redirecting to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the username already exists
        cur.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        if cur.fetchone():
            flash('Username already exists!', 'error')
            conn.close()
            return redirect(url_for('signup'))

        # Insert the new user into the users table
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash('Signup successful—please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth.html', mode='signup')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        conn.close()

        if row and check_password_hash(row[1], password):
            session['user_id'] = row[0]
            return redirect(url_for('habit_tracker'))

        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    return render_template('auth.html', mode='login')

# Route for habit tracker page
@app.route('/habit_tracker')
def habit_tracker():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('habit.html')

# Route for user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('login'))

# Route to save a new goal
@app.route('/save_goal', methods=['POST'])
def save_goal_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    goal_text = request.form['goal']
    category = request.form['category']

    # Save goal to the database
    goal_data = {
        'text': goal_text,
        'category': category,
        'user_id': session['user_id']
    }
    save_goal(goal_data)

    flash('Goal saved successfully!', 'success')
    return redirect(url_for('habit_tracker'))

# Route to view all goals
@app.route('/goals')
def goals():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    goals = conn.execute('SELECT * FROM goals WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('goals.html', goals=goals)

if __name__ == '__main__':
    init_db()  # Ensure the DB is initialized
    app.run(debug=True)
