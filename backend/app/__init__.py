from flask import Flask, request
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from config import config
from app.utils.extensions import db
from app.routes.completion_routes import completion_bp
from app.routes.habit_routes import habit_bp
from app.routes.auth_routes import auth_bp
from app.routes.reminder_routes import reminder_routes
from flask_pymongo import PyMongo
from app.models.models import User, Habit  # Import your models

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
    app.register_blueprint(reminder_routes)

    # Seed default data
    @app.before_first_request
    def seed_default_data():
        with app.app_context():
            # Default MySQL Data (SQLAlchemy)
            if not User.query.first():  # Avoid duplicate data
                admin = User(username="admin", email="admin@example.com")
                admin.password = "admin123"  # Will need hashing in real use
                db.session.add(admin)
                db.session.commit()
                app.logger.info("Default user created")

            if not Habit.query.first():
                default_habit = Habit(name="Drink Water", user_id=1)
                db.session.add(default_habit)
                db.session.commit()
                app.logger.info("Default habit created")

            # Default MongoDB Data (PyMongo)
            if mongo.db.habits.count_documents({}) == 0:
                mongo.db.habits.insert_one({"name": "Exercise", "description": "Daily workout routine"})
                app.logger.info("Default MongoDB habit inserted")

    # Set logging configuration
    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # Example of custom error handlers (Optional)
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
