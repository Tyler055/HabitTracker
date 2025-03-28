from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .config import config
from .extensions import db
from app.routes.auth_routes import auth_bp
from app.routes.completion_routes import completion_bp

migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(ActiveConfig)

    env = os.getenv('FLASK_ENV', 'development')
    if env not in config:
        raise ValueError(f"Invalid FLASK_ENV: {env}")

    app.config.from_object(config[env])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.habit_routes import habit_bp
    app.register_blueprint(auth_bp) 
    app.register_blueprint(completion_bp)  
    app.register_blueprint(habit_bp) 

    return app
