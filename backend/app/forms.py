from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired, ValidationError
import re
from app.models.models import User  # Import User model to query the database

# Custom password strength validator
def password_strength(form, field):
    password = field.data
    if not re.search(r"[A-Z]", password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r"[0-9]", password):
        raise ValidationError('Password must contain at least one digit.')
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError('Password must contain at least one special character.')
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')

# Signup form with custom password validation
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message="Username is required"), 
        Length(min=4, max=25, message="Username must be between 4 and 25 characters"),
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"), 
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"), 
        Length(min=8, message="Password must be at least 8 characters long"), 
        password_strength
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"), 
        EqualTo('password', message="Passwords must match")
    ])

    def validate(self):
        """Custom validation logic (if necessary) can be added here."""
        if not super().validate():
            return False

        # Check if the username or email already exists in the database
        if User.query.filter_by(username=self.username.data).first():
            self.username.errors.append('Username already exists.')
            return False
        
        if User.query.filter_by(email=self.email.data.lower()).first():  # Email comparison is case-insensitive
            self.email.errors.append('Email already exists.')
            return False
        
        return True

# Login form with basic validation
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"), 
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember = BooleanField('Remember Me')
