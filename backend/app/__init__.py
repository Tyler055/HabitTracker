from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from app.routes.auth_routes import auth_bp
from app.routes.habit_routes import habit_bp
from app.routes.completion_routes import completion_bp
from app.routes.reminder_routes import reminder_routes
from config import config
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()

def create_app():
    # Load environment variables
    load_dotenv()

    # Set up configuration
    env = os.getenv('FLASK_ENV', 'development')
    if env not in config:
        raise ValueError(f"Invalid FLASK_ENV: {env}. Must be one of {list(config.keys())}.")
    
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Set up database URIs
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI")

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(habit_bp)
    app.register_blueprint(completion_bp)
    app.register_blueprint(reminder_routes)

    # Set FLASK_ENV based on APP_MODE
    if app.config['APP_MODE'] == 'development':
        app.config['FLASK_ENV'] = 'development'
    elif app.config['APP_MODE'] == 'test':
        app.config['FLASK_ENV'] = 'testing'
    else:
        app.config['FLASK_ENV'] = 'production'

    # Seed default data (Optional, only in development mode)
    @app.before_request
    def seed_default_data():
        if app.config['FLASK_ENV'] in ['development', 'testing']:
            try:
                # Add default users, habits, etc.
                pass
            except Exception as e:
                app.logger.error(f"Error during seeding: {e}")

    # Custom error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"message": "Internal server error"}, 500

    return app
