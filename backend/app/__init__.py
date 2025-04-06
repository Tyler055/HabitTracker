import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from sqlalchemy import text

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()
jwt = JWTManager()

# Import routes for modularity
from app.routes.auth_routes import auth_bp
from app.routes.habit_routes import habit_bp
from app.routes.completion_routes import completion_bp
from app.routes.reminder_routes import reminder_bp
from config import config

def create_app():
    """
    Factory function to create and configure the Flask application instance.
    """
    # Load environment variables from the .env file for configuration
    load_dotenv()

    # Retrieve the app mode (development, production, testing) from the environment variable
    env = os.getenv('APP_MODE', 'development')  # Default to 'development' if not specified
    if env not in config:
        raise ValueError(f"Invalid APP_MODE: {env}. Must be one of {list(config.keys())}.")

    # Initialize the Flask app
    app = Flask(__name__)

    # Load configuration from the appropriate environment settings
    app.config.from_object(config[env])

    # Set up database URIs and other necessary configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") or config[env].SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI") or config[env].MONGO_URI
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize the extensions with the Flask app instance
    db.init_app(app)  # Initialize SQLAlchemy with app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app
    mongo.init_app(app)  # Initialize PyMongo with app
    jwt.init_app(app)  # Initialize JWT with app

    # Set up CORS to allow cross-origin requests
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    CORS(app, origins=[frontend_url])

    # Flag to check if initialization logic has run
    initialized = False

    @app.before_request
    def before_request():
        nonlocal initialized
        if not initialized:
            # Run initialization code here
            print("This runs before the first request!")
            # Check database connection or setup any necessary resources
            try:
                # Explicitly declare the SQL statement as text
                db.session.execute(text('SELECT 1'))
                app.logger.info("SQLAlchemy database connection successful")
            except Exception as e:
                app.logger.error(f"Database connection failed: {e}")
                raise Exception("Database connection failed. Please check your configuration.")
            initialized = True

        # Optional: Seed default data for development/testing modes
        if app.config['APP_MODE'] in ['development', 'testing']:
            try:
                # Add default users, habits, or other necessary entities for testing/development
                pass  # Implement your seeding logic here
            except Exception as e:
                app.logger.error(f"Error during seeding: {e}")

    # Register blueprints for routing (API or views)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(habit_bp, url_prefix="/habits")
    app.register_blueprint(completion_bp, url_prefix="/completion")
    app.register_blueprint(reminder_bp, url_prefix="/reminder")

    # Custom error handlers for common HTTP errors
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"404 Error: {error}")
        return {"message": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Error: {error}")
        return {"message": "Internal server error"}, 500

    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning(f"400 Error: {error}")
        return {"message": "Bad request"}, 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        app.logger.warning(f"405 Error: {error}")
        return {"message": "Method Not Allowed"}, 405

    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.warning(f"401 Error: {error}")
        return {"message": "Unauthorized"}, 401

    @app.errorhandler(403)
    def forbidden(error):
        app.logger.warning(f"403 Error: {error}")
        return {"message": "Forbidden"}, 403

    # Enable logging for better error tracking
    log_level = logging.INFO if app.config['APP_MODE'] != 'production' else logging.ERROR
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level,
        handlers=[logging.StreamHandler()]
    )

    # Return the Flask app instance for usage
    return app
