import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_required_env_variable(var_name):
    """Raise error if an environment variable is missing."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable '{var_name}' is missing. Please set it in your .env file or environment.")
    return value

class BaseConfig:
    """Base configuration class for shared settings."""
    APP_NAME = os.getenv("APP_NAME", "Habit-Tracker")
    PORT = int(os.getenv("PORT", 5000))

    # Security settings
    SECRET_KEY = get_required_env_variable("SECRET_KEY")
    JWT_SECRET = get_required_env_variable("JWT_SECRET")
    JWT_REFRESH_SECRET = get_required_env_variable("JWT_REFRESH_SECRET")

    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USERNAME = get_required_env_variable("MAIL_USERNAME")
    MAIL_PASSWORD = get_required_env_variable("MAIL_PASSWORD")

    # File upload settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif").split(","))

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"

    # MongoDB settings (used for MongoDB database in app)
    MONGO_URI = get_required_env_variable("MONGO_DB_URI")

class TestingConfig(BaseConfig):
    """Testing-specific configuration."""
    APP_MODE = "test"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test.db")
    MYSQL_URI = get_required_env_variable("MYSQL_TEST_URI")
    MONGO_URI = get_required_env_variable("MONGO_TEST_URI")  # Mongo URI for testing environment

class DevelopmentConfig(BaseConfig):
    """Development-specific configuration."""
    APP_MODE = "development"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    MYSQL_URI = get_required_env_variable("MYSQL_DB_URI")  # MySQL URI for dev environment
    MONGO_URI = get_required_env_variable("MONGO_DB_URI")  # Mongo URI for dev environment

class ProductionConfig(BaseConfig):
    """Production-specific configuration."""
    APP_MODE = "production"
    DEBUG = False
    DATABASE_URL = get_required_env_variable("DATABASE_URL")
    MYSQL_URI = get_required_env_variable("MYSQL_PROD_URI")  # MySQL URI for production environment
    MONGO_URI = get_required_env_variable("MONGO_PROD_URI")  # Mongo URI for production environment
    REDIS_URL = get_required_env_variable("REDIS_URL")  # Redis URI for caching or background tasks
    SECRET_KEY = get_required_env_variable("SECRET_KEY")
    FLASK_SECRET_KEY = get_required_env_variable("FLASK_SECRET_KEY")  # Optional for additional secret use

# Config Selector: Select the appropriate config based on the APP_MODE
config = {
    "test": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Active Config Detection
APP_MODE = os.getenv("APP_MODE", "development")
ActiveConfig = config.get(APP_MODE, DevelopmentConfig)

# The ActiveConfig is the one to be used in your app (e.g., `app.config.from_object(ActiveConfig)`)
