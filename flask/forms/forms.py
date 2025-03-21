from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    """
    Form for logging in a user.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')  # Checkbox for "Remember me"
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """
    Form for signing up a new user.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
