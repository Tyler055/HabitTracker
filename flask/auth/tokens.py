import jwt
import datetime
from flask import current_app

def create_token(email, app=None):
    try:
        secret_key = app.config.get('SECRET_KEY') if app else current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise ValueError("No secret key configured.")

        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        payload = {
            "email": email,
            "exp": expiration_time
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    except Exception as e:
        current_app.logger.error(f"Error generating JWT token: {e}")
        raise
