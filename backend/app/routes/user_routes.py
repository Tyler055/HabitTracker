from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.__init__ import db
from models.models import User

# Blueprint for user registration
user_bp_register = Blueprint('user_bp_register', __name__)

# Route to register a user
@user_bp_register.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input fields
    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        # Hash the password before saving it
        hashed_password = generate_password_hash(password, method='sha256')

        # Create and save the user
        new_user = User(username=username, email=email)
        new_user.set_password(hashed_password)  # Set the password using a setter method

        db.session.add(new_user)
        db.session.commit()

        # Return successful response with user data (excluding password)
        return jsonify({
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }), 201

    except Exception as e:
        return jsonify({"error": "Internal server error. Please try again later."}), 500

# Blueprint for theme change
user_bp_theme = Blueprint('user_bp_theme', __name__)

# Route to update theme (Light/Dark)
@user_bp_theme.route('/change-theme', methods=['POST'])
@login_required
def change_theme():
    try:
        new_theme = 'dark' if current_user.theme == 'light' else 'light'
        current_user.theme = new_theme
        db.session.commit()
        flash(f'Theme changed to {new_theme}!', 'success')
        return redirect(url_for('home'))  # Redirect to home page or wherever you want
    except Exception as e:
        flash('Failed to change theme. Please try again.', 'danger')
        return redirect(url_for('home'))
