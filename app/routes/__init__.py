import os
import logging
from flask import Flask
from config import MasterConfig
from utils.extensions import db, migrate, login_manager, mail, csrf

def create_app(config_name=None):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Default to the FLASK_ENV environment variable if config_name is not provided
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    config_obj = MasterConfig(env=config_name).get_config()
    app.config.from_object(config_obj)

    # Ensure required config variables are set
    _check_required_config(app.config)

    # Initialize extensions
    _initialize_extensions(app)

    # Register blueprints
    _register_blueprints(app)

    # Default home route
    @app.route('/')
    def home():
        """Render the home page."""
        return "Welcome to the Habit Tracker App!"

    return app

def _check_required_config(config):
    """Ensure that all required configuration variables are set."""
    required_vars = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'MAIL_USERNAME', 'MAIL_PASSWORD']
    missing_vars = [var for var in required_vars if not config.get(var)]

    if missing_vars:
        raise ValueError(f"Missing required config variables: {', '.join(missing_vars)}")

def _initialize_extensions(app):
    """Initialize all Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Session protection for Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"

    # Import User model here to avoid circular import issues
    from models import User
    login_manager.user_loader(lambda user_id: User.query.get(int(user_id)))

def _register_blueprints(app):
    """Register all blueprints with the app."""
    from routes.auth import auth
    from routes.chat import chat
    from routes.files import files
    from routes.main import main

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(chat, url_prefix='/chat')
    app.register_blueprint(files, url_prefix='/files')
    app.register_blueprint(main)

def _configure_logging():
    """Configure logging for the app."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(filename='logs/app.log', 
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())  # Also log to console

def run_app(app):
    """Run the Flask app with SSL in production if certificates are available."""
    ssl_cert = os.path.join(os.getcwd(), 'ssl', 'cert.pem')
    ssl_key = os.path.join(os.getcwd(), 'ssl', 'key.pem')
    is_production = app.config.get("ENV") == "production"

    if is_production:
        if os.path.exists(ssl_cert) and os.path.exists(ssl_key):
            app.run(ssl_context=(ssl_cert, ssl_key))
        else:
            logging.warning("⚠️ SSL certificates missing! Running without SSL.")
            app.run(debug=False)
    else:
        app.run(debug=True)

if __name__ == '__main__':
    app = create_app()
    _configure_logging()  # Set up logging
    run_app(app)
