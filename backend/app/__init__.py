from flask import Flask, request, jsonify
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
from app.models.models import User, Habit
from werkzeug.security import generate_password_hash  # Secure password hashing

# Initialize Flask extensions
mongo = PyMongo()
migrate = Migrate()

def create_app():
    # Load environment variables
    load_dotenv()

    # Set up configuration
    env = os.getenv('FLASK_ENV', 'development')
    if env not in config:
        raise ValueError(f"Invalid FLASK_ENV: {env}. Must be one of {list(config.keys())}.")
    
    app = Flask(__name__)
    app.config.from_object(config[env])

    # Set database URIs
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI")

    # Log missing database URIs instead of abruptly crashing
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        app.logger.warning("Warning: SQLALCHEMY_DATABASE_URI is not set. Database connection may fail.")
    if not app.config['MONGO_URI']:
        app.logger.warning("Warning: MONGO_URI is not set. MongoDB connection may fail.")

    # Initialize extensions
    db.init_app(app)
    mongo.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (ensure authentication is first)
    app.register_blueprint(auth_bp)
    app.register_blueprint(completion_bp)
    app.register_blueprint(habit_bp)
    app.register_blueprint(reminder_routes)

    # **Seed Default Data**
    @app.before_first_request
    def seed_default_data():
        with app.app_context():
            try:
                # Seed MySQL Data
                if not User.query.first():  # Prevent duplicate users
                    admin = User(username="admin", email="admin@example.com")
                    admin.password = generate_password_hash("admin123", method='sha256')
                    db.session.add(admin)
                    db.session.commit()
                    app.logger.info("✅ Default user created successfully.")

                if not Habit.query.first():
                    default_habit = Habit(name="Drink Water", user_id=1)
                    db.session.add(default_habit)
                    db.session.commit()
                    app.logger.info("✅ Default habit created.")

                # Seed MongoDB Data
                if mongo.db.habits.count_documents({}) == 0:
                    mongo.db.habits.insert_one({"name": "Exercise", "description": "Daily workout routine"})
                    app.logger.info("✅ Default MongoDB habit inserted.")
            except Exception as e:
                app.logger.error(f"⚠️ Error during seeding: {e}")

    # **Logging Configuration**
    log_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG if app.config['DEBUG'] else logging.INFO)
    handler.setFormatter(log_formatter)
    app.logger.addHandler(handler)

    # **Custom Error Handlers**
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error(f"404 Not Found: {request.url}")
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Internal Server Error: {error}")
        return jsonify({"message": "Internal server error"}), 500

    return app
