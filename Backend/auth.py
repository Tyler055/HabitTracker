from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo
from dataservice import create_user, find_user_by_username, find_user_by_email, update_user_password, find_user_by_id, update_user_reset_token, find_user_by_reset_token
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

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = find_user_by_email(email)
        
        if not user:
            flash('Email not found in our records.', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        # Generate a reset token, save it, and send the reset email
        token = generate_reset_token()
        save_reset_token(user['id'], token)  # Save the token in the database
        send_reset_email(email, token)
        flash('Password reset instructions have been sent to your email.', 'info')
        return redirect(url_for('auth.login'))  # Redirect to login after success

    return render_template('forgot_password.html')  # Render the forgot-password form

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = find_user_by_reset_token(token)
    
    if not user or datetime.utcnow() > user['reset_token_expiry']:
        flash('Invalid or expired token.', 'error')
        return redirect(url_for('auth.forgot_password'))  # Redirect back to forgot password if invalid token

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords must match.', 'error')
        else:
            hashed_password = generate_password_hash(new_password)
            update_user_password(user['id'], hashed_password)
            flash('Password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))  # Redirect to login after password reset

    return render_template('reset_password.html', token=token)  # Render reset password form
