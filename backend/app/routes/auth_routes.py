from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import re
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.models import User
from app.forms import SignupForm, LoginForm

# Define Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Centralized error handler with logging
def handle_error(message, status_code=400):
    logging.error(message)  # Log the error message
    return jsonify({"status": "error", "message": message}), status_code

# Rate Limiter setup
limiter = Limiter(app=None, key_func=get_remote_address)

# Email validation function
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Password strength validation function
def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# User Registration (API Route)
@auth_bp.route('/signup', methods=['POST'])
def api_signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return handle_error("All fields are required")

        # Validate email format
        if not validate_email(email):
            return handle_error("Invalid email format")

        # Validate password strength
        if not validate_password_strength(password):
            return handle_error("Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.")

        # Check if user already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return handle_error("Username or email already exists")

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password before saving
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# User Login with Rate Limiting (API Route)
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 login attempts per minute
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return handle_error("Email and password are required")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Use check_password method in User model
            access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
            return jsonify({"status": "success", "message": "Login successful", "token": access_token}), 200
        else:
            return handle_error("Invalid credentials", 401)

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Get Current User Info (Protected Route)
@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return handle_error("User not found", 404)

        return jsonify({
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200

    except Exception as e:
        return handle_error(str(e), 500)

# User Registration (Form Route)
@auth_bp.route('/signup-form', methods=['GET', 'POST'])
def signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        # Your signup logic (e.g., create user, hash password, save to db)
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password before saving
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup_form.html', form=form)

# Login Route (Form Route)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard or desired page
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login_signup.html', form=form, title="Login", form_action='login')

# Signup Route (Form Route)
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Hash the password
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        login_user(user)  # Automatically log the user in after signup
        return redirect(url_for('dashboard'))  # Redirect to dashboard or desired page
    return render_template('auth/login_signup.html', form=form, title="Signup", form_action='signup')

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
