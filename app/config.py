import os
import logging
from dotenv import load_dotenv

# Load environment variables based on FLASK_ENV (default: development)
env = os.getenv('FLASK_ENV', 'development')
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path)

class Config:
    """Base configuration with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # Default to a random secret key if not set
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    REMEMBER_COOKIE_DURATION = 30 * 24 * 60 * 60  # 30 days for persistent logins
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # File Uploads
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))

    # Security Headers (e.g., HSTS, CSP)
    SECURITY_HEADERS = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; object-src 'none';"
    }

    # Logging Configuration
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG' if env == 'development' else 'ERROR')
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///instance/dev.db')  # Use development DB (SQLite for dev)
    SQLALCHEMY_ECHO = True  # Log SQL queries for debugging

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')  # In-memory DB for testing
    SQLALCHEMY_ECHO = False  # No need to log queries

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL', 'postgresql://user:password@localhost/prod_db')
    SESSION_COOKIE_SECURE = True  # Force HTTPS for session cookies
    SQLALCHEMY_ECHO = False  # Disable query logging in production

# Return the appropriate configuration based on the FLASK_ENV
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    return config_map.get(env, DevelopmentConfig)

# Ensure required environment variables are set
def check_required_env_vars():
    required_vars = ['SECRET_KEY', 'MAIL_USERNAME', 'MAIL_PASSWORD']
    db_var = {
        'development': 'DEV_DATABASE_URL',
        'testing': 'TEST_DATABASE_URL',
        'production': 'PROD_DATABASE_URL'
    }.get(os.getenv('FLASK_ENV', 'development'), 'DEV_DATABASE_URL')  # Default to dev if env is unknown
    required_vars.append(db_var)

    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"❌ {var} is missing! Please check your .env.{os.getenv('FLASK_ENV')} file.")

# Load the configuration object
config = get_config()

# Ensure all required environment variables are available
check_required_env_vars()
