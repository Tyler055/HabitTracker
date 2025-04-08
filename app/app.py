import os
from flask import Flask, render_template
from config import get_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from dotenv import load_dotenv
import logging

# Load environment variables from the appropriate .env file
env = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path)

# Validate environment
valid_envs = ['development', 'production', 'testing']
if env not in valid_envs:
    raise ValueError(f"Invalid FLASK_ENV: {env}. Valid values are {', '.join(valid_envs)}.")

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

def create_app(config_name=None):
    """Factory function to create and configure the Flask app."""

    # Initialize Flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load configuration based on the environment
    config_obj = get_config()  # Fetch the config based on environment (development, production, etc.)
    app.config.from_object(config_obj)

    # Initialize all extensions
    _initialize_extensions(app)

    # Register blueprints for modular routing
    _register_blueprints(app)

    # Configure logging for the app
    _configure_logging(app)

    # Error handling
    _register_error_handlers(app)

    return app

def _initialize_extensions(app):
    """Initialize all Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Flask-Login session settings
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"

def _register_blueprints(app):
    """Register all blueprints with the app."""
    from .routes.auth import auth
    from .routes.chat import chat
    from .routes.files import files
    from .routes.main import main

    # Register blueprints for different modules
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(chat, url_prefix='/chat')
    app.register_blueprint(files, url_prefix='/files')
    app.register_blueprint(main)

def _configure_logging(app):
    """Configure logging based on the environment."""
    log_level = logging.DEBUG if app.config["DEBUG"] else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def _register_error_handlers(app):
    """Register error handlers for common HTTP errors."""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback any uncommitted transactions
        return render_template('500.html'), 500

# Flask-Login user loader function
@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database based on their user ID."""
    from models import User  # Import models here to avoid circular imports
    return User.query.get(int(user_id))

# SSL Handling for production environments
def run_app(app):
    """Run the Flask app with SSL in production if certificates are available."""
    ssl_cert = os.path.join(os.getcwd(), 'ssl', 'cert.pem')
    ssl_key = os.path.join(os.getcwd(), 'ssl', 'key.pem')
    is_production = app.config.get("ENV") == "production"

    if is_production and os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        app.run(ssl_context=(ssl_cert, ssl_key))  # Run with SSL in production
    else:
        app.run(debug=not is_production)  # Enable debug mode only in development

if __name__ == '__main__':
    app = create_app()  # No need to pass config_name as it automatically uses the environment variable
    run_app(app)
