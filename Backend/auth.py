from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from datetime import datetime, timedelta, timezone
import random
import string

from dataservice import (
    create_user, find_user_by_username, find_user_by_email,
    update_user_password, find_user_by_id, update_user_reset_token
)

# ======================= Blueprint =======================
auth_bp = Blueprint('auth', __name__)

# ======================= Forms =======================
class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Step 1 Form: Identity Entry
class IdentityForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Code')

# Step 2 Form: Verification Code Entry
class CodeForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify Code')

# Step 3 Form: Password Reset
class PasswordResetForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')

# ======================= Helper Function =======================
def generate_verification_code(length=6):
    """Generate a random verification code consisting of digits."""
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ======================= Routes =======================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data.strip()
        password = form.password.data

        user = find_user_by_username(identifier) or find_user_by_email(identifier)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful.', 'success')
            return redirect(url_for('main.dashboard'))  # Replace with actual dashboard
        else:
            flash('Invalid username/email or password.', 'error')

    return render_template('auth.html', form=form, form_type='login')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data

        if find_user_by_username(username):
            flash('Username already exists.', 'error')
        elif find_user_by_email(email):
            flash('Email already in use.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            create_user(username, email, hashed_password)
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth.html', form=form, form_type='signup')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    step = request.args.get('step', '1')
    form = None

    if step == '1':
        form = IdentityForm()
        if form.validate_on_submit():
            username = form.username.data.strip()
            email = form.email.data.strip()
            user = find_user_by_username(username)

            if user and user['email'] == email:
                code = generate_verification_code()
                expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
                update_user_reset_token(user['id'], code, expiration)

                session['reset_code'] = code
                session['reset_email'] = email
                session['verified_username'] = username
                flash(f'Verification code sent to {email}. (Simulated)', 'info')

                form = CodeForm()
                return render_template('recover.html',form=form, recovery_step='2', verification_code=code)
            else:
                flash('Username and email do not match.', 'error')
        return render_template('recover.html', form=form, recovery_step='1')

    elif step == '2':
        form = CodeForm()
        if form.validate_on_submit():
            username = session.get('verified_username')
            user = find_user_by_username(username)
            if user and user['reset_token'] == form.code.data:
                session['verified_user_id'] = user['id']
                return redirect(url_for('auth.recover', step='3'))
            else:
                flash('Invalid verification code.', 'error')
        return render_template('recover.html', form=form, recovery_step='2')

    elif step == '3':
        form = PasswordResetForm()
        if form.validate_on_submit():
            user_id = session.get('verified_user_id')
            if user_id:
                new_hashed = generate_password_hash(form.new_password.data)
                update_user_password(user_id, new_hashed)
                session.pop('verified_user_id', None)
                session.pop('reset_email', None)
                session.pop('verified_username', None)
                flash('Password successfully reset. You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Unauthorized access to password reset.', 'error')
                return redirect(url_for('auth.recover'))
        return render_template('recover.html', form=form, recovery_step='3')

    flash('Invalid recovery step.', 'error')
    return redirect(url_for('auth.recover', step='1'))
