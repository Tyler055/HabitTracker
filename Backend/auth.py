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
    update_user_password, find_user_by_id, update_user_reset_token,
    soft_delete_user, get_user_reset_token, clear_reset_token
)

# === Setup ===

auth_bp = Blueprint('auth', __name__)


# === Forms ===
class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators=[DataRequired()])
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


# === Helpers ===
def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def is_token_valid(user_id, token_value):
    """
    Validate the provided token for the user.
    """
    token_data = get_user_reset_token(user_id)
    if not token_data:
        return False
    if token_data.get('token') != token_value:
        return False
    expires = datetime.strptime(token_data.get('expires_at'), '%Y-%m-%d %H:%M:%S')
    return datetime.now() <= expires


def can_reset_password(user_id):
    token_data = get_user_reset_token(user_id)
    if not token_data:
        return True
    last_reset = datetime.strptime(token_data.get('created_at'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - last_reset >= timedelta(hours=24)

# === Routes ===
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    signup_form = SignupForm()

    if login_form.validate_on_submit():
        identifier = login_form.identifier.data.strip().lower()
        password = login_form.password.data
        user = find_user_by_username(identifier) or find_user_by_email(identifier)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful.', 'success')
            return redirect(url_for('views.habit_tracker'))
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

        if find_user_by_username(username):
            flash('Username already exists.', 'error')
        elif find_user_by_email(email):
            flash('Email already in use.', 'error')
        else:
            create_user(username, password, email)
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth.html', signup_form=signup_form, login_form=login_form, form_type='signup')


@auth_bp.route('/logout')
def logout():
    session.clear()
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
        if user and check_password_hash(user['password'], form.old_password.data):
            update_user_password(user_id, generate_password_hash(form.new_password.data))
            flash('Password changed successfully.', 'success')
            return redirect(url_for('auth.login'))
        flash('Old password is incorrect.', 'error')

    return render_template('change_password.html', form=form)


@auth_bp.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.pop('user_id', None)
    if user_id:
        soft_delete_user(user_id)
        flash('Account deleted successfully.', 'success')
    else:
        flash('No user logged in.', 'error')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to view your profile.', 'error')
        return redirect(url_for('auth.login'))

    user = find_user_by_id(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(user['password'], form.old_password.data):
            update_user_password(user_id, generate_password_hash(form.new_password.data))
            flash('Password updated successfully.', 'success')
        else:
            flash('Incorrect old password.', 'error')

    return render_template('profile.html', user=user, form=form)

@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    step = request.args.get('step', '1')

    if step == '1':
        form = IdentityForm()
        if form.validate_on_submit():
            username = form.username.data.strip().lower()
            email = form.email.data.strip().lower()
            user = find_user_by_username(username)

            if not user or (user['email'] or '').lower() != email:
                flash('No user found with that username and email combination.', 'error')
                return render_template('recover.html', form=form, recovery_step='1')

            if not can_reset_password(user['id']):
                flash('Password was recently reset. Please wait before trying again.', 'error')
                return render_template('recover.html', form=form, recovery_step='1')
            # Generate token and expiry by calling the function
            
            token, expires_at = update_user_reset_token(user['id'], expiry_duration_minutes=10)
            
            # Simulate sending email by printing to console
            print(f"[Password Reset] Verification code for {email}: {token}")


            # Store session variables for verification
            session['reset_user_id'] = user['id']
            session['reset_username'] = username
            session['reset_email'] = email

            flash(f'Verification code sent to {email} (check console output in this demo).', 'info')
            return redirect(url_for('auth.recover', step='2'))

        return render_template('recover.html', form=form, recovery_step='1')

    elif step == '2':
        if 'reset_user_id' not in session:
            flash('Session expired or invalid. Please start over.', 'error')
            return redirect(url_for('auth.recover'))

        form = CodeForm()
        if form.validate_on_submit():
            user_id = session['reset_user_id']
            code_entered = form.code.data.strip()

            if not is_token_valid(user_id, code_entered):
                flash('Invalid or expired verification code.', 'error')
                return render_template('recover.html', form=form, recovery_step='2')

            # Mark verification as complete
            session['verified_user_id'] = user_id
            flash('Code verified. You may now reset your password.', 'success')
            return redirect(url_for('auth.recover', step='3'))

        return render_template('recover.html', form=form, recovery_step='2')

    elif step == '3':
        if 'verified_user_id' not in session:
            flash('Unauthorized access. Please complete verification first.', 'error')
            return redirect(url_for('auth.recover'))

        form = PasswordResetForm()
        if form.validate_on_submit():
            user_id = session['verified_user_id']
            new_password = form.new_password.data

            # Update password properly (your function hashes inside)
            update_user_password(user_id, new_password)

            # Clear reset token after successful reset
            clear_reset_token(user_id)

            # Clear sensitive session info
            session.pop('reset_user_id', None)
            session.pop('reset_username', None)
            session.pop('reset_email', None)
            session.pop('verified_user_id', None)

            flash('Password reset successfully. You can now log in.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('recover.html', form=form, recovery_step='3')

    # Fallback for invalid steps
    flash('Invalid password recovery step.', 'error')
    return redirect(url_for('auth.recover'))