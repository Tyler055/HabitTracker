from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_required_env_variable(env_var_name):
    """Utility to get environment variables and raise an error if not found."""
    value = os.getenv(env_var_name)
    if not value:
        raise ValueError(f"{env_var_name} must be set in environment variables.")
    return value

class Config:
    """Base configuration class with common settings."""
    APP_NAME = os.getenv("APP_NAME", "Habit-Tracker")
    PORT = int(os.getenv("PORT", 5000))

    # Secret Keys
    SECRET_KEY = get_required_env_variable("SECRET_KEY")
    JWT_SECRET = get_required_env_variable("JWT_SECRET")
    JWT_REFRESH_SECRET = get_required_env_variable("JWT_REFRESH_SECRET")

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = get_required_env_variable("MAIL_USERNAME")
    MAIL_PASSWORD = get_required_env_variable("MAIL_PASSWORD")

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
    MYSQL_TEST_URI = get_required_env_variable("MYSQL_TEST_URI")
    MONGO_TEST_URI = get_required_env_variable("MONGO_TEST_URI")


class DevelopmentConfig(Config):
    """Configuration for the development environment."""
    APP_MODE = "development"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    # Database URIs for development
    MYSQL_DB_URI = get_required_env_variable("MYSQL_DB_URI")
    MONGO_DB_URI = get_required_env_variable("MONGO_DB_URI")


class ProductionConfig(Config):
    """Configuration for the production environment."""
    APP_MODE = "production"
    DEBUG = False

    # Check for critical production-specific settings
    DATABASE_URL = get_required_env_variable("DATABASE_URL")
    MYSQL_PROD_URI = get_required_env_variable("MYSQL_PROD_URI")
    MONGO_PROD_URI = get_required_env_variable("MONGO_PROD_URI")
    REDIS_URL = get_required_env_variable("REDIS_URL")
    FLASK_SECRET_KEY = get_required_env_variable("FLASK_SECRET_KEY")


# Configuration dictionary to select the correct environment
config = {
    "test": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Automatically select config based on APP_MODE
APP_MODE = os.getenv("APP_MODE", "development")  # Ensure default to "development"
ActiveConfig = config.get(APP_MODE, DevelopmentConfig)
