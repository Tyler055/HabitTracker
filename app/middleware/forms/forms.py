from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

class LoginForm(FlaskForm):
    """
    Form for logging in a user.
    """
    email = StringField('Email', validators=[DataRequired(message="Email is required"), Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    remember = BooleanField('Remember me')  # Checkbox for "Remember me"
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """
    Form for signing up a new user.
    """
    username = StringField(
        'Username', 
        validators=[DataRequired(message="Username is required"), Length(min=4, max=120, message="Username must be between 4 and 120 characters")]
    )
    email = StringField('Email', validators=[DataRequired(message="Email is required"), Email(message="Invalid email format")])
    confirm_email = StringField(
        'Confirm Email', 
        validators=[DataRequired(message="Please confirm your email address"), Email(message="Invalid email format"), EqualTo('email', message="Emails must match")]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters long"),
            Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$', message='Password must contain letters and numbers')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(message="Please confirm your password"), EqualTo('password', message="Passwords must match")]
    )
    submit = SubmitField('Sign Up')
