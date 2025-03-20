from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# Function to hash a password
def hash_password(password):
    """
    Hash the given password using werkzeug's secure hashing method.
    """
    return generate_password_hash(password)

# Function to verify if the password matches the hashed password
def verify_password(hashed_password, password):
    """
    Verify if the provided password matches the stored hashed password.
    """
    return check_password_hash(hashed_password, password)

# Example of creating a password reset token (optional)
# Here you can use libraries like `itsdangerous` to create and validate tokens for password resets.

def generate_reset_token(email):
    """
    Generate a secure token for password reset.
    This token is valid for a specific period (default is 3600 seconds or 1 hour).
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_reset_token(token, expiration=3600):
    """
    Verify the password reset token.
    Checks if the token is valid and not expired.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except Exception as e:
        return None  # Token expired or invalid
    return email
