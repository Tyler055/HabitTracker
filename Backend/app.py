import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')  # Static folder is inside Backend/
)

# Set the secret key for session management
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# Function to get a MySQL connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='for_flask',
        password='25FlaskOnly25@',
        database='habit_tracker'
    )
    return conn

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('habit_tracker'))  # Redirect to habit tracker if logged in
    else:
        return redirect(url_for('login'))  # Redirect to login if not logged in


@app.route('/habit_tracker')
def habit_tracker():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return send_from_directory('../WebApp', 'habit.html')
        session.pop('user_id', None)
    return redirect(url_for('auth', mode='login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Generate a hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        # Check if the user already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user:
            flash('Username already exists!', 'Failed')
            conn.close()
            return redirect(url_for('login'))  # Redirect to login page
        
        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash('User created successfully!', 'success')
        return redirect(url_for('login'))  # Redirect to login page after signup

    return render_template('auth.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        # Check if the username exists and the password matches
        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            session['user_id'] = user[0]  # Store user_id in session
            return redirect(url_for('home'))  # Redirect to home page after successful login
        else:
            flash('Invalid username or password!', 'Failed')
            return redirect(url_for('signup'))  # Redirect to signup if login fails

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from session
    flash('You have been logged out.', 'message')
    return redirect(url_for('login'))  # Redirect to login page after logout

if __name__ == '__main__':
    app.run(debug=True)
