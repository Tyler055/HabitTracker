from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from app.config import config
from app.extensions import db
from app.routes.auth_routes import auth_bp
from app.routes.completion_routes import completion_bp
from app.routes.habit_routes import habit_bp

migrate = Migrate()

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Set the environment for configuration
    env = os.getenv('FLASK_ENV', 'development')
    if env not in config:
        raise ValueError(f"Invalid FLASK_ENV: {env}")

    # Initialize the Flask app with the selected configuration
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Set the database URI and other configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and migration
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(auth_bp) 
    app.register_blueprint(completion_bp)  
    app.register_blueprint(habit_bp) 

    return app
