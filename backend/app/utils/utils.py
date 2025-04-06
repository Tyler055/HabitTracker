# utils.py

import os
import bcrypt
from datetime import timedelta
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_mail import Mail, Message
from app.models.models import User

# Initialize Flask-Mail (make sure to call mail.init_app(app) in create_app)
mail = Mail()


# -------------------- Password Hashing --------------------
def hash_password(password: str) -> str:
    """Hash a password using bcrypt (with automatic salting)."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed one."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# -------------------- JWT Token Generation --------------------
def generate_jwt_token(user_id: int) -> str:
    """Generate a JWT token for the given user ID."""
    expire_days = int(os.getenv("JWT_EXPIRE_DAYS", 7))  # Default to 7 days
    return create_access_token(identity=user_id, expires_delta=timedelta(days=expire_days))


# -------------------- Random String Generator --------------------
def generate_random_string(length: int = 16) -> str:
    """Generate a secure random hexadecimal string of given byte length."""
    return os.urandom(length).hex()


# -------------------- Email Sending --------------------
def send_email(to: str, subject: str, body: str):
    """
    Send an email using Flask-Mail.
    Requires app context and mail to be initialized.
    """
    try:
        if not current_app:
            raise RuntimeError("Flask application context is required to send emails.")

        msg = Message(subject=subject, recipients=[to], body=body)
        mail.send(msg)
        current_app.logger.info(f"✅ Email sent to {to}")
    except Exception as e:
        current_app.logger.error(f"⚠️ Failed to send email to {to}: {e}")


# -------------------- User Retrieval --------------------
def get_user_from_identity(user_id: int):
    """
    Retrieve a user by ID.
    Used typically with JWT identity lookups.
    """
    return User.query.get(user_id)
