from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from middleware.auth.auth_manager import login_user, register_user, logout_user

# Create Blueprint for authentication
auth = Blueprint('auth', __name__)

# Login route (Supports both API & Form submission)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:  # API Request (JSON)
            data = request.json
            response = login_user(data)
            if response.get("success"):
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        else:  # Form submission (Web form)
            email = request.form['email']
            password = request.form['password']
            response = login_user({"email": email, "password": password})
            if response.get("success"):
                flash("Login successful!", 'success')
                return redirect(url_for('dashboard.index'))  # Redirect to some dashboard or home
            else:
                flash("Invalid credentials. Please try again.", 'danger')
                return redirect(url_for('auth.login'))  # Stay on login page
    return render_template('login.html')  # For GET requests, render the login page

# Signup route (Supports both API & Form submission)
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.is_json:  # API Request (JSON)
            data = request.json
            response = register_user(data)
            if response.get("success"):
                return jsonify({"message": "User registered successfully"}), 201
            else:
                return jsonify({"message": "User already exists"}), 400
        else:  # Form submission (Web form)
            email = request.form['email']
            password = request.form['password']
            response = register_user({"email": email, "password": password})
            if response.get("success"):
                flash("Registration successful! You can now log in.", 'success')
                return redirect(url_for('auth.login'))  # Redirect to login page
            else:
                flash("User already exists. Please try a different email.", 'danger')
                return redirect(url_for('auth.signup'))  # Stay on signup page
    return render_template('signup.html')  # For GET requests, render the signup page

# Logout route (API or form)
@auth.route('/logout', methods=['POST'])
def logout():
    response = logout_user()
    if response.get("success"):
        flash("You have successfully logged out.", 'success')
        return redirect(url_for('auth.login'))  # Redirect to login page after logout
    else:
        flash("An error occurred while logging out.", 'danger')
        return redirect(url_for('dashboard.index'))  # Redirect to dashboard or home page
