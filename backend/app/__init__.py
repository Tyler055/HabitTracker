from flask import Flask, request
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from config import config
from utils.extensions import db
from app.routes.auth_routes import auth_bp
from app.routes.completion_routes import completion_bp
from app.routes.habit_routes import habit_bp
from flask_pymongo import PyMongo

# Initialize Flask extensions
mongo = PyMongo()
migrate = Migrate()

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Set the environment for configuration (development, production, etc.)
    env = os.getenv('FLASK_ENV', 'development')
    if env not in config:
        raise ValueError(f"Invalid FLASK_ENV: {env}. Must be one of {list(config.keys())}.")

    # Initialize the Flask app with the selected configuration
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Set the database URI and other configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set MongoDB URI
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI")  # Mongo URI from .env file
    
    # Ensure both database URIs are set in the environment variables
    if not app.config['SQLALCHEMY_DATABASE_URI'] or not app.config['MONGO_URI']:
        raise ValueError("Database URIs are missing. Ensure both DATABASE_URL and MONGO_DB_URI are set in the .env file.")

    # Initialize the extensions (SQLAlchemy, MongoDB, and migration)
    db.init_app(app)  # Initialize SQLAlchemy
    mongo.init_app(app)  # Initialize MongoDB
    migrate.init_app(app, db)  # Initialize migration for SQLAlchemy

    # Register blueprints for different routes
    app.register_blueprint(auth_bp) 
    app.register_blueprint(completion_bp)  
    app.register_blueprint(habit_bp)

    # Set logging configuration (Optional)
    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # Example of custom configuration (Optional)
    # You can add custom error handlers or logging here
    # For example, if you want to log requests or errors
    @app.before_request
    def before_request():
        app.logger.info("Request received for %s", request.url)

    # Custom error handler for 404 errors
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error("Resource not found: %s", request.url)
        return {"message": "Resource not found"}, 404

    # Custom error handler for 500 errors
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("Internal server error: %s", str(error))
        return {"message": "Internal server error"}, 500

    return app
