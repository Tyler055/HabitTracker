from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from models import User
from forms import LoginForm

# Define Blueprint for authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for logging in the user.
    """
    # Redirect if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))  # Redirect to the index if already logged in

    form = LoginForm()  # Initialize the login form
    if form.validate_on_submit():  # Check if the form was submitted and is valid
        # Check if the user exists by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # If the user exists and the password matches
        if user and check_password_hash(user.password, form.password.data):
            remember = form.remember.data  # Get the value of the "Remember me" checkbox
            login_user(user, remember=remember)  # Log in the user
            
            flash('Login successful!', 'success')
            
            # Redirect to the 'next' URL (if provided), or to the index page
            next_page = request.args.get('next')
            return redirect(next_page or url_for('views.index'))
        else:
            flash('Login failed. Check your email and/or password.', 'danger')  # Invalid credentials

    return render_template('auth/login.html', form=form)  # Render the login template with the form


@auth.route('/logout')
@login_required
def logout():
    """
    Route to log out the current user.
    """
    logout_user()  # Log out the user
    flash('You have been logged out.', 'info')  # Flash a message indicating the user has been logged out
    return redirect(url_for('auth.login'))  # Redirect to the login page
