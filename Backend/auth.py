from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from datetime import datetime, timedelta,  timezone
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


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Code')


class CodeForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify Code')


class PasswordResetForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')

# ======================= Routes =======================


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data
        password_confirm = form.password_confirm.data

        if find_user_by_username(username):
            flash(f'Username "{username}" is already taken.', 'error')
        elif email and find_user_by_email(email):
            flash(f'Email "{email}" is already registered.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            create_user(username, hashed_password, email)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth.html', form=form, mode='signup')


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

    return render_template('auth.html', form=form, mode='login')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('auth.login'))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = find_user_by_id(session['user_id'])
        if not check_password_hash(user['password'], form.old_password.data):
            flash('Old password is incorrect.', 'error')
        else:
            new_hashed = generate_password_hash(form.new_password.data)
            update_user_password(user['id'], new_hashed)
            flash('Password updated successfully.', 'success')
            return redirect(url_for('auth.profile'))

    return render_template('profile.html', form=form)


@auth_bp.route('/recover', methods=['GET', 'POST'])
def recover():
    step = request.args.get('step', '1')
    form = None

    if step == '1':
        form = EmailForm()
        if form.validate_on_submit():
            user = find_user_by_email(form.email.data)
            if user:
                code = generate_verification_code()
                expiration = datetime.utcnow() + timedelta(minutes=10)
                update_user_reset_token(user['id'], code, expiration)
                session['reset_email'] = form.email.data
                flash(f'Verification code sent to {form.email.data} (simulated).', 'info')
                return redirect(url_for('auth.recover', step='2'))
            else:
                flash('Email not found.', 'error')
        return render_template('recover.html', form=form, recovery_step='1')

    elif step == '2':
        form = CodeForm()
        if form.validate_on_submit():
            user = find_user_by_email(session.get('reset_email'))
            if user and user['reset_token'] == form.code.data and datetime.utcnow() < user['reset_token_expiration']:
                session['verified_user_id'] = user['id']
                return redirect(url_for('auth.recover', step='3'))
            else:
                flash('Invalid or expired code.', 'error')
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
                flash('Password successfully reset. You can now log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Unauthorized access to password reset.', 'error')
                return redirect(url_for('auth.recover'))
        return render_template('recover.html', form=form, recovery_step='3')

    flash('Invalid recovery step.', 'error')
    return redirect(url_for('auth.recover', step='1'))


# ======================= Utils =======================

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))


def find_user_by_email(email):
    return {'id': 1, 'email': email, 'reset_token': '123456', 'reset_token_expiration': datetime.now(timezone.utc) + timedelta(minutes=10)}


def update_user_reset_token(user_id, code, expiration):
    print(f"Updated reset token for user {user_id}: {code}, expires at {expiration}")


def update_user_password(user_id, new_hashed):
    print(f"Updated password for user {user_id} to {new_hashed}")
