from flask import render_template, redirect, url_for, flash
from app import app, db
from app.models.models import User
from flask_login import login_user
from .forms import SignupForm, LoginForm

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Create a new user
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)  # Assume you have a method to hash the password
        db.session.add(user)
        db.session.commit()

        flash("User created successfully!", "success")
        return redirect(url_for('login'))  # Redirect to login page after successful signup
    
    return render_template('signup.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):  # Assume you have a method to check the password
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))  # Redirect to the user dashboard or home
        
        flash("Invalid email or password", "danger")
    
    return render_template('login.html', form=form)

# Dashboard or home page route (after login)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
