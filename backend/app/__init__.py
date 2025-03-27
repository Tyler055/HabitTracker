# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .config import config  # Assuming you have separate config files
from .extensions import db  # This import is relative
from .routes.habit_routes import habit_bp  # Blueprint import here

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize the Flask app
    app = Flask(__name__)

    # Load configuration based on environment
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])  # Select config based on environment

    # Set the database URI dynamically from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "mysql://root:password@localhost/habit-tracker")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid overhead in modification tracking

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints (import here to avoid circular imports)
    from app.routes.habit_routes import habit_bp  # Import blueprint after app initialization
    app.register_blueprint(habit_bp)

    return app
