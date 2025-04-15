import os
import secrets
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)  # Use default template and static file paths

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# SQLite Database Configuration
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'habit_tracker.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Database initialization
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error during database initialization: {e}")

def validate_password(password):
    """Password policy validation"""
    if len(password) < 1:  # Just check if not empty
        return False, "Password cannot be empty"
    return True, "Password is valid"

def validate_username(username):
    """Username validation"""
    if len(username) < 1:  # Just check if not empty
        return False, "Username cannot be empty"
    return True, "Username is valid"

@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return send_from_directory('../WebApp', 'habit.html')
        session.pop('user_id', None)
    return redirect(url_for('auth', mode='login'))

@app.route('/auth/<mode>', methods=['GET', 'POST'])
def auth(mode):
    if mode not in ['login', 'signup']:
        return redirect(url_for('auth', mode='login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if mode == 'signup':
            # Input validation
            username_valid, username_msg = validate_username(username)
            if not username_valid:
                flash(username_msg, 'danger')
                return redirect(url_for('auth', mode='signup'))

            password_valid, password_msg = validate_password(password)
            if not password_valid:
                flash(password_msg, 'danger')
                return redirect(url_for('auth', mode='signup'))

            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'danger')
                return redirect(url_for('auth', mode='signup'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            try:
                print(f"Attempting to register new user: {username}")
                db.session.add(new_user)
                db.session.commit()
                print(f"User registration successful: {username}")
                flash('User created successfully!', 'success')
                return redirect(url_for('auth', mode='login'))
            except Exception as e:
                db.session.rollback()
                print(f"User registration failed: {str(e)}")
                flash('An error occurred while creating your account. Please try again.', 'danger')
                return redirect(url_for('auth', mode='signup'))

        elif mode == 'login':
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!', 'danger')
                return redirect(url_for('auth', mode='login'))

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth', mode='login'))

# Routes for serving static files
@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('../WebApp/img', filename)

@app.route('/style.css')
def serve_css():
    return send_from_directory('../WebApp', 'style.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory('../WebApp', 'script.js')

@app.route('/Locations/<path:filename>')
def serve_locations(filename):
    return send_from_directory('../Locations', filename)

if __name__ == '__main__':
    app.run(debug=True)
