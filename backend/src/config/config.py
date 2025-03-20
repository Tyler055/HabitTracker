import os
import logging
from dotenv import load_dotenv

# Load environment variables from the appropriate .env file
env = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path)

class Config:
    """Base configuration with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))  # Default to a random secret key for production
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

class MasterConfig:
    """Master configuration class that integrates all environments."""
    def __init__(self, env=None):
        # Default to development if not provided
        self.env = env or os.getenv('FLASK_ENV', 'development')
        
        # Dynamically load the environment class
        self.config_class = {
            'development': DevelopmentConfig,
            'testing': TestingConfig,
            'production': ProductionConfig
        }.get(self.env, DevelopmentConfig)

        self.config = self.config_class()
        
        # Ensure required environment variables are set
        self._check_required_env_vars()
        
    def _check_required_env_vars(self):
        """Ensure all required environment variables are set."""
        required_vars = ['SECRET_KEY', 'MAIL_USERNAME', 'MAIL_PASSWORD']
        
        # Ensure the correct database variable is checked based on the environment
        db_var = {
            'development': 'DEV_DATABASE_URL',
            'testing': 'TEST_DATABASE_URL',
            'production': 'PROD_DATABASE_URL'
        }.get(self.env, 'DEV_DATABASE_URL')  # Default to dev if env is unknown
        
        required_vars.append(db_var)
        
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"❌ {var} is missing! Please check your .env.{self.env} file.")

    def get_config(self):
        """Return the current configuration object."""
        return self.config

# Default configuration object
config = MasterConfig().get_config()
