from flask import jsonify, session, redirect, url_for, flash
from auth.auth_utils import hash_password, verify_password
from auth.tokens import create_token

# In-memory user DB (replace with real DB later)
users_db = {}

def register_user(data):
    email = data.get("email")
    password = data.get("password")

    if email in users_db:
        flash("Email already registered.", 'danger')
        return jsonify({"message": "User already exists"}), 400

    users_db[email] = {"password": hash_password(password)}
    flash("Signup successful! Please log in.", 'success')
    return jsonify({"message": "User registered successfully"}), 201

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

def logout_user():
    session.pop('user', None)
    flash("You have been logged out.", 'success')
    return jsonify({"message": "Logged out successfully"}), 200
