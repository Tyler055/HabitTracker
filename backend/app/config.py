from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with common settings."""
    APP_NAME = os.getenv("APP_NAME", "Habit-Tracker")
    PORT = int(os.getenv("PORT", 5000))

    # Secret Keys
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")

    if not SECRET_KEY or not JWT_SECRET or not JWT_REFRESH_SECRET:
        raise ValueError("Critical security keys (SECRET_KEY, JWT_SECRET) must be set.")

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Ensure email credentials are set
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        raise ValueError("Mail credentials must be set as environment variables.")

    # Upload Settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif").split(","))

    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"


class TestingConfig(Config):
    """Configuration for the testing environment."""
    APP_MODE = "test"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test.db")

    # Database URIs for testing
    MYSQL_TEST_URI = os.getenv("MYSQL_TEST_URI")
    MONGO_TEST_URI = os.getenv("MONGO_TEST_URI")

    if not MYSQL_TEST_URI or not MONGO_TEST_URI:
        raise ValueError("Test database URIs must be set as environment variables.")


class DevelopmentConfig(Config):
    """Configuration for the development environment."""
    APP_MODE = "development"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    # Database URIs for development
    MYSQL_DB_URI = os.getenv("MYSQL_DB_URI")
    MONGO_DB_URI = os.getenv("MONGO_DB_URI")

    if not MYSQL_DB_URI or not MONGO_DB_URI:
        raise ValueError("Development database URIs must be set as environment variables.")


class ProductionConfig(Config):
    """Configuration for the production environment."""
    APP_MODE = "production"
    DEBUG = False

    # Check for critical production-specific settings
    if not os.getenv("DATABASE_URL"):
        raise ValueError("Critical environment variable DATABASE_URL is missing in production.")
    
    if not os.getenv("MYSQL_PROD_URI") or not os.getenv("MONGO_PROD_URI"):
        raise ValueError("Production database URIs (MYSQL_PROD_URI, MONGO_PROD_URI) are missing.")
    
    if not os.getenv("REDIS_URL"):
        raise ValueError("Production Redis URL (REDIS_URL) is missing.")
    
    if not os.getenv("FLASK_SECRET_KEY"):
        raise ValueError("Production FLASK_SECRET_KEY is missing for security.")


# Configuration dictionary to select the correct environment
config = {
    "test": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Automatically select config based on APP_MODE
APP_MODE = os.getenv("APP_MODE", "development")
ActiveConfig = config.get(APP_MODE, DevelopmentConfig)  # Fix the assignment of ActiveConfig here
