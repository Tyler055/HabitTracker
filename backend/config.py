import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def get_required_env_variable(var_name):
    """Raise error if environment variable is missing."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"{var_name} must be set in environment variables.")
    return value

class BaseConfig:
    """Base configuration."""
    APP_NAME = os.getenv("APP_NAME", "Habit-Tracker")
    PORT = int(os.getenv("PORT", 5000))

    SECRET_KEY = get_required_env_variable("SECRET_KEY")
    JWT_SECRET = get_required_env_variable("JWT_SECRET")
    JWT_REFRESH_SECRET = get_required_env_variable("JWT_REFRESH_SECRET")

    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = get_required_env_variable("MAIL_USERNAME")
    MAIL_PASSWORD = get_required_env_variable("MAIL_PASSWORD")

    # Upload
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif").split(","))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"


class TestingConfig(BaseConfig):
    APP_MODE = "test"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test.db")
    MYSQL_URI = get_required_env_variable("MYSQL_TEST_URI")
    MONGO_URI = get_required_env_variable("MONGO_TEST_URI")


class DevelopmentConfig(BaseConfig):
    APP_MODE = "development"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    MYSQL_URI = get_required_env_variable("MYSQL_DB_URI")
    MONGO_URI = get_required_env_variable("MONGO_DB_URI")


class ProductionConfig(BaseConfig):
    APP_MODE = "production"
    DEBUG = False
    DATABASE_URL = get_required_env_variable("DATABASE_URL")
    MYSQL_URI = get_required_env_variable("MYSQL_PROD_URI")
    MONGO_URI = get_required_env_variable("MONGO_PROD_URI")
    REDIS_URL = get_required_env_variable("REDIS_URL")
    FLASK_SECRET_KEY = get_required_env_variable("FLASK_SECRET_KEY")


# Config Selector
config = {
    "test": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Active Config Detection
APP_MODE = os.getenv("APP_MODE", "development")
ActiveConfig = config.get(APP_MODE, DevelopmentConfig)
