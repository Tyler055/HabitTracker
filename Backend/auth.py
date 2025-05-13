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
    find_user_by_id, update_user_password, update_user_reset_token,
    delete_user
)

auth_bp = Blueprint('auth', __name__)

# ======================= Forms =======================
class LoginForm(FlaskForm):
    identity = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), EqualTo('new_password', message="Passwords must match.")])
    submit = SubmitField('Change Password')

class IdentityForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Code')

class CodeForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify Code')

class PasswordResetForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('new_password', message="Passwords must match.")])
    submit = SubmitField('Reset Password')

# ======================= Helper =======================
def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def can_reset_password(last_reset_time):
    if not last_reset_time:
        return True
    now = datetime.now(timezone.utc)
    last_time = datetime.fromisoformat(last_reset_time)
    eligible = now - last_time >= timedelta(hours=24)
    print(f"[DEBUG] Last reset: {last_time}, Now: {now}, Eligible: {eligible}")
    return eligible

# ======================= Routes =======================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    signup_form = SignupForm()

    if login_form.validate_on_submit():
        identity = login_form.identity.data.strip().lower()
        password = login_form.password.data
        print(f"[DEBUG] Login submitted for identity: {identity}")

        user = find_user_by_username(identity) or find_user_by_email(identity)
        print(f"[DEBUG] User found: {user['username'] if user else 'None'}")

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful.', 'success')
            return redirect(url_for('views.habit_tracker'))
        else:
            flash('Invalid username/email or password.', 'error')

    return render_template('auth.html', login_form=login_form, signup_form=signup_form, form_type='login')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    login_form = LoginForm()

    if signup_form.validate_on_submit():
        username = signup_form.username.data.strip().lower()
        email = signup_form.email.data.strip().lower()
        password = signup_form.password.data

        print(f"[DEBUG] Signup attempt for {username}, {email}")

        if find_user_by_username(username):
            flash('Username already exists.', 'error')
        elif find_user_by_email(email):
            flash('Email already in use.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            create_user(username, email, hashed_password)
            print(f"[DEBUG] User created: {username}")
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth.html', signup_form=signup_form, login_form=login_form, form_type='signup')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    print("[DEBUG] User logged out.")
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    user_id = session.get('user_id')

    if not user_id:
        flash('You must be logged in to change your password.', 'error')
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        user = find_user_by_id(user_id)
        print(f"[DEBUG] Password change request by user: {user['username'] if user else 'None'}")

        if user and check_password_hash(user['password'], form.old_password.data):
            new_hashed = generate_password_hash(form.new_password.data)
            update_user_password(user_id, new_hashed)
            print("[DEBUG] Password updated successfully.")
            flash('Password changed successfully.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Old password is incorrect.', 'error')

    return render_template('change_password.html', form=form)

@auth_bp.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if user_id:
        print(f"[DEBUG] Deleting user with ID: {user_id}")
        delete_user(user_id)
        session.pop('user_id', None)
        flash('Account deleted successfully.', 'success')
    else:
        flash('No user logged in.', 'error')
    return redirect(url_for('auth.login'))

@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    step = request.args.get('step', '1')
    print(f"[DEBUG] Password recovery step: {step}")

    if step == '1':
        form = IdentityForm()
        if form.validate_on_submit():
            username = form.username.data.strip().lower()
            email = form.email.data.strip().lower()
            print(f"[DEBUG] Recovery Step 1 submitted: {username}, {email}")

            user = find_user_by_username(username)

            if user and user['email'].lower() == email:
                if not can_reset_password(user.get('last_password_change')):
                    flash('Password can only be reset once every 24 hours.', 'error')
                    return redirect(url_for('auth.recover', step='1'))

                code = generate_verification_code()
                expiration = datetime.now(timezone.utc) + timedelta(minutes=10)
                update_user_reset_token(user['id'], code, expiration)

                session['reset_code'] = code
                session['reset_email'] = email
                session['verified_username'] = username

                print(f"[DEBUG] Verification code for {username}: {code} (expires {expiration})")
                flash(f'Verification code sent to {email}. (Simulated)', 'info')
                return redirect(url_for('auth.recover', step='2'))
            else:
                flash('Username and email do not match.', 'error')

        return render_template('recover.html', form=form, recovery_step='1')

    elif step == '2':
        if 'reset_code' not in session:
            flash('Start the recovery process again.', 'error')
            return redirect(url_for('auth.recover', step='1'))

        form = CodeForm()
        if form.validate_on_submit():
            print(f"[DEBUG] Submitted code: {form.code.data}, Expected: {session.get('reset_code')}")
            if form.code.data == session.get('reset_code'):
                return redirect(url_for('auth.recover', step='3'))
            else:
                flash('Invalid verification code.', 'error')

        return render_template('recover.html', form=form, recovery_step='2')

    elif step == '3':
        if 'verified_username' not in session:
            flash('Recovery session expired. Start over.', 'error')
            return redirect(url_for('auth.recover', step='1'))

        form = PasswordResetForm()
        if form.validate_on_submit():
            user = find_user_by_username(session['verified_username'])
            print(f"[DEBUG] Resetting password for: {user['username'] if user else 'Unknown'}")

            if user:
                new_hashed = generate_password_hash(form.new_password.data)
                update_user_password(user['id'], new_hashed, update_time=True)

                # Clear session
                session.pop('verified_username', None)
                session.pop('reset_code', None)
                session.pop('reset_email', None)

                print("[DEBUG] Password reset successful.")
                flash('Password successfully reset. You can now log in.', 'success')
                return redirect(url_for('auth.login'))

            flash('User not found for password reset.', 'error')
            return redirect(url_for('auth.recover', step='1'))

        return render_template('recover.html', form=form, recovery_step='3')

    flash('Invalid recovery step.', 'error')
    return redirect(url_for('auth.recover', step='1'))
