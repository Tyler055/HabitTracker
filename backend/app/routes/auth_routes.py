from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
import logging
import datetime
import re
from app.utils.extensions import db
from app.models.models import User
from app.forms import SignupForm, LoginForm

auth_bp = Blueprint('auth_bp', __name__)

# ---------------------
# Utility Functions
# ---------------------

def validate_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

def validate_password_strength(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

def handle_error(message, status_code=400):
    logging.error(message)
    return jsonify({"status": "error", "message": message}), status_code

# ---------------------
# API Signup Route
# ---------------------

@auth_bp.route('/signup', methods=['POST'])
def api_signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return handle_error("All fields are required")

        if not validate_email(email):
            return handle_error("Invalid email format")

        if not validate_password_strength(password):
            return handle_error(
                "Password must be at least 8 characters long, include uppercase, lowercase, number, and special character.")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return handle_error("Username or email already exists")

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id, expires_delta=datetime.timedelta(days=1))
        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "access_token": access_token,
            "username": new_user.username
        }), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# ---------------------
# API Login Route (Updated)
# ---------------------

@auth_bp.route('/login', methods=['POST'])
def login_user_api():
    try:
        data = request.get_json()
        identifier = data.get('identifier')  # Can be email OR username
        password = data.get('password')

        if not all([identifier, password]):
            return handle_error("Email or username and password are required")

        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "access_token": access_token,
                "username": user.username
            }), 200
        else:
            return handle_error("Invalid credentials", 401)

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# ---------------------
# Form Login Route
# ---------------------

@auth_bp.route('/login-form', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Replace with your dashboard route if needed
        else:
            flash('Invalid credentials', 'danger')
    return render_template('auth/login_signup.html', form=form)

# ---------------------
# Form Signup Route
# ---------------------

@auth_bp.route('/signup-form', methods=['GET', 'POST'])
def signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('auth/login_signup.html', form=form)

# ---------------------
# Logout Route
# ---------------------

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.login_form'))
