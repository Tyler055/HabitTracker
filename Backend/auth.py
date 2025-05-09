from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_mail import Message, Mail
from datetime import datetime, timedelta
from dataservice import (
    create_user, find_user_by_username, find_user_by_email,
    update_user_password, find_user_by_id, update_user_reset_token
)
import secrets

# Initialize the Flask-Mail extension
mail = Mail()

auth_bp = Blueprint('auth', __name__)

# ------------------- Forms -------------------

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])

class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])

class RecoverForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])

# ------------------- Helper Functions -------------------

def send_reset_email(user_email, token):
    msg = Message('Password Reset Request', recipients=[user_email])
    msg.body = f'Please use the following link to reset your password: http://127.0.0.1:5000/reset-password/{token}'
    mail.send(msg)

def generate_reset_token():
    return secrets.token_urlsafe(16)

def save_reset_token(user_id, token):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Set token expiry time (e.g., 1 hour)
    update_user_reset_token(user_id, token, expiration)

# ------------------- Routes -------------------

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data

        if find_user_by_username(username):
            flash(f'Username "{username}" is already taken.', 'error')
        elif email and find_user_by_email(email):
            flash(f'Email "{email}" is already registered.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            create_user(username, hashed_password, email)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth.html', form=form, form_type='signup')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip()
        password = form.password.data
        user = find_user_by_username(identifier) or find_user_by_email(identifier)

        if not user or not check_password_hash(user['password'], password):
            flash('Invalid username/email or password.', 'error')
        else:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('views.habit_tracker'))

    return render_template('auth.html', form=form, form_type='login')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    # Step 1: Username/Email validation (forgot password)
    if 'recovery_step' not in session:
        session['recovery_step'] = 1

    form = RecoverForm()

    if request.method == 'POST':
        if session['recovery_step'] == 1:
            username = form.username.data.strip()
            email = form.email.data.strip()
            user = find_user_by_username(username)

            if not user or user['email'] != email:
                flash('Invalid username/email combination.', 'error')
            else:
                token = generate_reset_token()
                save_reset_token(user['id'], token)
                send_reset_email(email, token)
                session['recovery_step'] = 2
                session['user_id'] = user['id']
                flash('Reset link has been sent to your email.', 'info')
                return redirect(url_for('auth.recover'))

        # Step 2: Verification code validation (reset password)
        elif session['recovery_step'] == 2:
            verification_code = form.verification_code.data.strip()
            user = find_user_by_id(session['user_id'])

            if verification_code != user['reset_token']:
                flash('Invalid verification code or token expired.', 'error')
            else:
                session['recovery_step'] = 3
                flash('Verification code is valid. Please enter a new password.', 'info')
                return redirect(url_for('auth.recover'))

        # Step 3: Password reset (change password)
        elif session['recovery_step'] == 3:
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            if new_password != confirm_password:
                flash('Passwords do not match.', 'error')
            else:
                hashed_password = generate_password_hash(new_password)
                update_user_password(session['user_id'], hashed_password)
                session.pop('recovery_step', None)
                session.pop('user_id', None)
                flash('Your password has been successfully updated!', 'success')
                return redirect(url_for('auth.login'))

    return render_template('recover.html', form=form)

