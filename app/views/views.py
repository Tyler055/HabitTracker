import re
from flask import jsonify, session, flash, request
from app.middleware.auth.auth_utils import hash_password, verify_password
from app.middleware.auth.tokens import create_token, generate_reset_token, verify_reset_token

# Placeholder for user database (Replace with actual DB)
users_db = {}

# Helper to validate email format
def validate_email(email):
    """Validate the email format using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Register User
def register_user(data):
    email = data.get("email")
    password = data.get("password")

    if not validate_email(email):
        return jsonify({"message": "Invalid email format"}), 400

    if email in users_db:
        return jsonify({"message": "User already exists"}), 400

    users_db[email] = {"password": hash_password(password)}
    return jsonify({"message": "User registered successfully"}), 201

# Login User
def login_user(data):
    email = data.get("email")
    password = data.get("password")
    stored_password = users_db.get(email, {}).get("password")

    if not stored_password or not verify_password(stored_password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    session['user'] = email
    token = create_token(email)
    return jsonify({"message": "Login successful", "token": token}), 200

# Logout User
def logout_user():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200

# Request Password Reset
def request_password_reset(data):
    email = data.get("email")
    if email not in users_db:
        return jsonify({"message": "User not found"}), 404

    token = generate_reset_token(email)
    return jsonify({"message": "Password reset link sent", "token": token}), 200

# Reset Password
def reset_password(data):
    token = data.get("token")
    new_password = data.get("password")

    email = verify_reset_token(token)
    if not email:
        return jsonify({"message": "Invalid or expired token"}), 400

    users_db[email] = {"password": hash_password(new_password)}
    return jsonify({"message": "Password reset successfully"}), 200
