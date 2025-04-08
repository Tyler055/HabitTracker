import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Set the secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# Function to get a MySQL connection using mysql.connector
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
        return f"Welcome to the Habit Tracker, User ID: {session['user_id']}!"
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Generate a hashed password using pbkdf2:sha256 for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        # Check if user already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user:
            flash('Username already exists!', 'danger')
            conn.close()
            return redirect(url_for('signup'))
        
        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash('User created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        
        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
