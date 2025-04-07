from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.utils.extensions import db  # Assuming this is how db is imported elsewhere
from app.models.models import User
import re
import logging

# Blueprints
user_bp_register = Blueprint('user_bp_register', __name__)
user_bp_theme = Blueprint('user_bp_theme', __name__)

# ------------------------
# Utility Validators
# ------------------------

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validate_password_strength(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

# ------------------------
# Register User Route
# ------------------------

@user_bp_register.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Basic validation
        if not all([username, email, password]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        if not validate_email(email):
            return jsonify({"status": "error", "message": "Invalid email format"}), 400

        if not validate_password_strength(password):
            return jsonify({
                "status": "error",
                "message": "Password must be at least 8 characters long, include uppercase, lowercase, number, and special character."
            }), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"status": "error", "message": "Username already exists"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"status": "error", "message": "Email already registered"}), 400

        # Create and commit new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }), 201

    except Exception as e:
        logging.exception("Error registering user")
        return jsonify({"status": "error", "message": "Internal server error. Please try again later."}), 500

# ----------------------
# User Theme Toggle Route
# ----------------------

@user_bp_theme.route('/change-theme', methods=['POST'])
@login_required
def change_theme():
    try:
        new_theme = 'dark' if current_user.theme == 'light' else 'light'
        current_user.theme = new_theme
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": f"Theme changed to {new_theme}",
            "theme": new_theme
        }), 200
    except Exception as e:
        logging.exception("Error changing theme")
        return jsonify({"status": "error", "message": "Failed to change theme. Please try again."}), 500
