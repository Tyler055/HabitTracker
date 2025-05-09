from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo
from dataservice import create_user, find_user_by_username, find_user_by_email, update_user_password, find_user_by_id, update_user_reset_token
from flask_mail import Message, Mail
import random
import string
from datetime import datetime, timedelta

# Initialize the Flask-Mail extension
mail = Mail()

auth_bp = Blueprint('auth', __name__)

# ChangePasswordForm defined once
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])

class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Helper function to send a password reset email
def send_reset_email(user_email, token):
    msg = Message('Password Reset Request', recipients=[user_email])
    msg.body = f'Please use the following link to reset your password: http://127.0.0.1:5000/reset-password/{token}'
    mail.send(msg)

# Helper function to generate a password reset token
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Helper function to save the reset token and expiry in the database
def save_reset_token(user_id, token):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Set token expiry time (e.g., 1 hour)
    update_user_reset_token(user_id, token, expiration)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()  # Use the correct form here
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form.get('email', '').strip()
        password = request.form['password']
        password_confirm = request.form.get('password_confirm')

        # Validate form inputs
        if not username or not password:
            flash('Username and password are required.', 'error')
        elif password != password_confirm:
            flash('Passwords must match.', 'error')
        elif find_user_by_username(username):
            flash(f'Username "{username}" is already taken.', 'error')
        elif email and find_user_by_email(email):
            flash(f'Email "{email}" is already registered.', 'error')
        else:
            hashed_password = generate_password_hash(password)  # Hash the password before saving
            create_user(username, hashed_password, email)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Use the correct form for login
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        user = find_user_by_username(identifier) or find_user_by_email(identifier)

        if not user or not check_password_hash(user['password'], password):
            flash('Invalid username/email or password.', 'error')
        else:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('views.habit_tracker'))

    return render_template('auth.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))  # Ensure correct URL for login

    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = find_user_by_id(session['user_id'])
        if not check_password_hash(user['password'], form.old_password.data):
            flash('Old password is incorrect.', 'error')
        elif form.new_password.data != form.confirm_password.data:
            flash('New passwords do not match.', 'error')
        else:
            update_user_password(user['id'], form.new_password.data)
            flash('Password updated successfully.', 'success')
            return redirect(url_for('auth.profile'))  # Redirect to profile after success

    return render_template('profile.html', form=form)

@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    # If the session doesn't exist or the recovery flow is not started, start from Step 1
    if 'recovery_step' not in session:
        session['recovery_step'] = 1
        session['email'] = None
        session['username'] = None
        session['verification_code'] = None

    # Step 1: Verify Identity (Username and Email)
    if session['recovery_step'] == 1:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']

            # Query the database to verify the username and email
            user = find_user_by_username(username)

            if user and user['email'] == email:
                session['username'] = username
                session['email'] = email

                # Generate a secure verification code
                verification_code = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8))
                session['verification_code'] = verification_code

                # Print the verification code to the terminal (not the browser)
                print(f"Generated verification code: {verification_code}")  # This will show in the terminal

                # Simulate sending the verification code via email
                flash(f'A verification code has been sent to {email}.', 'info')

                # Move to Step 2
                session['recovery_step'] = 2
                return redirect(url_for('auth.recover'))

            else:
                flash('Invalid username or email.', 'danger')

        return render_template('recover.html', step=1)

    # Step 2: Enter Verification Code
    elif session['recovery_step'] == 2:
        if request.method == 'POST':
            entered_code = request.form['verification_code']

            if entered_code == session['verification_code']:
                # Code is correct, move to Step 3 (password reset)
                session['recovery_step'] = 3
                return redirect(url_for('auth.recover'))
            else:
                flash('Invalid verification code.', 'danger')

        return render_template('recover.html', step=2)

    # Step 3: Reset Password
    elif session['recovery_step'] == 3:
        if request.method == 'POST':
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if new_password == confirm_password:
                # Hash the new password and update the user in the database
                hashed_password = generate_password_hash(new_password)

                # Update the user's password in the database
                user = find_user_by_username(session['username'])
                update_user_password(user['id'], hashed_password)

                flash('Password reset successfully!', 'success')
                session.clear()  # Clear the session
                return redirect(url_for('auth.login'))

            else:
                flash('Passwords do not match.', 'danger')

        return render_template('recover.html', step=3)
