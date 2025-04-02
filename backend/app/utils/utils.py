import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
import os
from flask_mail import Mail, Message
from flask import current_app

# Ensure Flask-Mail is properly initialized in create_app()
mail = Mail()

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
    expire_days = int(os.getenv("JWT_EXPIRE_DAYS", 7))  # Configurable via .env
    access_token = create_access_token(identity=user_id, expires_delta=timedelta(days=expire_days))
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
    Sends an email using Flask-Mail.
    """
    try:
        if not current_app:
            raise RuntimeError("Flask application context is required to send emails.")

        if not hasattr(current_app, 'mail'):
            raise RuntimeError("Mail instance not initialized. Make sure mail.init_app(app) is called in create_app().")

        msg = Message(subject=subject, recipients=[to], body=body)
        mail.send(msg)  # Sending email through Flask-Mail
        current_app.logger.info(f"✅ Email sent to {to} with subject: {subject}")
    except Exception as e:
        current_app.logger.error(f"⚠️ Error sending email: {e}")
