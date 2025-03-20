import jwt
import datetime
from flask import current_app

def create_token(email, app=None):
    """
    Creates a JWT token for the user with an expiration time.
    - The token will expire in 1 hour.
    - The payload contains the user's email and expiration time.

    :param email: The email of the user
    :param app: The Flask app context to get the SECRET_KEY
    :return: JWT token as a string
    """
    try:
        # Ensure app is provided to access the configuration
        if app:
            secret_key = app.config.get('SECRET_KEY')
            if not secret_key:
                raise ValueError("SECRET_KEY is not set in the app config.")
        else:
            secret_key = current_app.config.get('SECRET_KEY') if current_app else None

        if not secret_key:
            raise ValueError("No secret key found, please configure SECRET_KEY in the app.")

        # Define the expiration time for the token (1 hour from now)
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        
        # Payload with user email and expiration time
        payload = {
            "email": email,
            "exp": expiration_time
        }
        
        # Generate the JWT token using the secret key and HS256 algorithm
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        return token
    
    except Exception as e:
        # Log the error or raise an exception if needed
        current_app.logger.error(f"Error generating JWT token: {e}")
        raise
