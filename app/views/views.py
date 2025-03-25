import re
from flask import jsonify, session, redirect, url_for, flash
from middleware.auth.auth_utils import hash_password, verify_password
from middleware.auth.tokens import create_token, revoke_token, is_token_revoked
from middleware.auth.tokens import generate_reset_token, verify_reset_token

# In-memory user DB (replace with real DB later)
users_db = {}

# Helper to validate email format
def validate_email(email):
    """Validate the email format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Register User
def register_user(data):
    email = data.get("email")
    password = data.get("password")

    if not validate_email(email):
        return jsonify({"message": "Invalid email format"}), 400

    if email in users_db:
        flash("Email already registered.", 'danger')
        return jsonify({"message": "User already exists"}), 400

    users_db[email] = {"password": hash_password(password)}
    flash("Signup successful! Please log in.", 'success')
    return jsonify({"message": "User registered successfully"}), 201

# Login User
def login_user(data):
    email = data.get("email")
    password = data.get("password")
    stored_password = users_db.get(email, {}).get("password")

    if not stored_password or not verify_password(stored_password, password):
        flash("Invalid email or password", 'danger')
        return jsonify({"message": "Invalid credentials"}), 401

    session['user'] = email
    token = create_token(email)
    flash("Login successful!", 'success')
    return jsonify({"message": "Login successful", "token": token}), 200

# Logout User
def logout_user():
    session.pop('user', None)
    flash("You have been logged out.", 'success')
    return jsonify({"message": "Logged out successfully"}), 200

# Password Reset (Generate and Verify Reset Token)
def request_password_reset(data):
    email = data.get("email")
    if email not in users_db:
        flash("No account found with this email.", 'danger')
        return jsonify({"message": "User not found"}), 404

    token = generate_reset_token(email)
    # Send the token to the user's email (simplified here as an example)
    flash(f"Password reset link sent to {email}.", 'info')
    return jsonify({"message": "Password reset link sent", "token": token}), 200

def reset_password(data):
    token = data.get("token")
    new_password = data.get("password")

    email = verify_reset_token(token)
    if not email:
        flash("The reset token is invalid or has expired.", 'danger')
        return jsonify({"message": "Invalid or expired token"}), 400

    users_db[email] = {"password": hash_password(new_password)}
    flash("Password has been reset successfully.", 'success')
    return jsonify({"message": "Password reset successfully"}), 200
