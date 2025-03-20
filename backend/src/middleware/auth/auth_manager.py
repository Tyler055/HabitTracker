from flask import jsonify, session, redirect, url_for, flash
from auth.auth_utils import hash_password, verify_password
from auth.tokens import create_token

# Temporary user database (Replace with a real database)
users_db = {}

def register_user(data):
    """
    Handles user registration. Supports both JSON API requests and form-based signup.
    """
    email = data.get("email")
    password = data.get("password")

    # Check if user already exists
    if email in users_db:
        flash("Email already registered.", 'danger')  # For form-based registration
        return jsonify({"message": "User already exists"}), 400

    # Hash the password before saving
    hashed_pw = hash_password(password)
    users_db[email] = {"password": hashed_pw}

    flash("Signup successful! Please log in.", 'success')  # For form-based
    return jsonify({"message": "User registered successfully"}), 201  # API Response

def login_user(data):
    """
    Handles user login. Supports both JSON API requests and form-based login.
    """
    email = data.get("email")
    password = data.get("password")

    # Get the stored password for the given email
    stored_password = users_db.get(email, {}).get("password")

    # Check if password is correct
    if not stored_password or not verify_password(stored_password, password):
        flash("Invalid email or password", 'danger')  # For form-based login
        return jsonify({"message": "Invalid credentials"}), 401  # API Response

    # Store session for the logged-in user (for form-based login)
    session['user'] = email

    # Generate JWT token for API-based authentication
    token = create_token(email)

    flash("Login successful!", 'success')  # For form-based login
    return jsonify({"message": "Login successful", "token": token}), 200  # API Response

def logout_user():
    """
    Handles user logout.
    """
    # Remove the session data
    session.pop('user', None)

    flash("You have been logged out.", 'success')  # For form-based logout
    return jsonify({"message": "Logged out successfully"}), 200  # API Response
