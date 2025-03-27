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

    MYSQL_URI = os.getenv("TEST_MYSQL_URI")
    MONGO_URI = os.getenv("TEST_MONGO_URI")


class DevelopmentConfig(Config):
    """Configuration for the development environment."""
    APP_MODE = "development"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    MYSQL_URI = os.getenv("DEV_MYSQL_URI")
    MONGO_URI = os.getenv("DEV_MONGO_URI")


class ProductionConfig(Config):
    """Configuration for the production environment."""
    APP_MODE = "production"
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///prod.db")

    MYSQL_URI = os.getenv("PROD_MYSQL_URI")
    MONGO_URI = os.getenv("PROD_MONGO_URI")

    # Ensure database credentials are set in production
    if not MYSQL_URI or not MONGO_URI:
        raise ValueError("Production database URIs must be set as environment variables.")

    # Production-specific configurations
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/production")

    # Caching (Redis)
    REDIS_URL = os.getenv("REDIS_URL")
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 300

    if not REDIS_URL:
        raise ValueError("REDIS_URL must be set in production.")

    # Flask Production Settings
    FLASK_ENV = "production"
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    if not FLASK_SECRET_KEY:
        raise ValueError("FLASK_SECRET_KEY must be set for production security.")


# Configuration dictionary to select the correct environment
config = {
    "test": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Automatically select config based on APP_MODE
APP_MODE = os.getenv("APP_MODE", "development")
ActiveConfig = config.get(APP_MODE, DevelopmentConfig)
