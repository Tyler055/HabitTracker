import jwt
import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# JWT Token Creation
def create_token(email, expiration=None, app=None):
    """Generate a JWT token with customizable expiration."""
    try:
        secret_key = app.config.get('SECRET_KEY') if app else current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("No secret key configured.")

        # Set expiration time (configurable)
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration or 3600)  # Default to 1 hour

        payload = {
            "email": email,
            "exp": expiration_time,
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    except Exception as e:
        current_app.logger.error(f"Error generating JWT token: {e}")
        raise Exception("An error occurred while generating the JWT token.")

# JWT Token Decoding
from jwt import ExpiredSignatureError, InvalidTokenError

def decode_token(token, app=None):
    """Decode and verify a JWT token, considering revocation status."""
    try:
        secret_key = app.config.get('SECRET_KEY') if app else current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("No secret key configured.")

        # Check if the token is revoked
        if is_token_revoked(token):
            current_app.logger.warning("Revoked JWT token.")
            return None

        # Decode the token
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        return payload  # If valid, return the decoded payload

    except ExpiredSignatureError:
        current_app.logger.warning("JWT token has expired.")
        return None

    except InvalidTokenError:
        current_app.logger.warning("Invalid JWT token.")
        return None

    except Exception as e:
        current_app.logger.error(f"Error decoding JWT token: {e}")
        return None

# Password Reset Token Generation and Verification
def generate_reset_token(email, expiration=None):
    """Generate a password reset token with customizable expiration."""
    expiration = expiration or current_app.config.get('RESET_TOKEN_EXPIRATION', 3600)  # Default to 1 hour
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_reset_token(token, expiration=None):
    """Verify the password reset token, with customizable expiration."""
    expiration = expiration or current_app.config.get('RESET_TOKEN_EXPIRATION', 3600)  # Default to 1 hour
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except Exception as e:
        current_app.logger.error(f"Error verifying reset token: {e}")
        return None

# Token Revocation (Optional)
revoked_tokens = set()

def revoke_token(token):
    """Mark a token as revoked."""
    revoked_tokens.add(token)
    current_app.logger.info(f"Token {token} has been revoked.")

def is_token_revoked(token):
    """Check if the token has been revoked."""
    return token in revoked_tokens
