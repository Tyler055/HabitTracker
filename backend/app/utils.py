import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
import os
from flask_mail import Message
from flask import current_app

# Function to hash passwords using bcrypt
def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt. Bcrypt automatically handles salting.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')  # Return the hashed password as a string

# Function to generate a JWT token for a user
def generate_jwt_token(user_id: int) -> str:
    """
    Generates a JWT access token with an expiration time.
    """
    access_token = create_access_token(identity=user_id, expires_delta=timedelta(days=7))
    return access_token

# Function to verify the password (compare hash and plain password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the plain password matches the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to generate a random string (useful for generating random tokens or other unique IDs)
def generate_random_string(length: int = 16) -> str:
    """
    Generates a random string of the specified length.
    """
    return os.urandom(length).hex()

# Function to send email (using Flask-Mail)
def send_email(to: str, subject: str, body: str):
    """
    A function to send emails using Flask-Mail.
    """
    try:
        msg = Message(subject=subject, recipients=[to])
        msg.body = body  # Text content of the email
        current_app.mail.send(msg)  # Sending email through Flask-Mail
        print(f"Email sent to {to} with subject: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")
