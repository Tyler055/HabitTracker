from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from app.config import config
from app.extensions import db, ma, mail, mongo  # Centralized extension objects
from app.routes.habit_routes import habit_bp
from app.routes.auth_routes import auth_bp
from flask_pymongo import PyMongo

# Load environment variables
load_dotenv()

# Initialize extensions
jwt = JWTManager()
migrate = Migrate()


def create_app(env_name=None):
    app = Flask(__name__)

    # Load config by environment
    env = env_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    # Override DB URL from environment if provided
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "DATABASE_URL", app.config.get("SQLALCHEMY_DATABASE_URI")
    )
    
    # Ensure the DATABASE_URL is set
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize extensions only once
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    mongo.init_app(app)

    # MongoDB setup
    app.config["MONGO_URI"] = os.getenv("MONGO_PROD_URI")
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(habit_bp, url_prefix="/api/habits")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Register global error handlers
    register_error_handlers(app)

    # Root route
    @app.route("/")
    def home():
        return "Welcome to the Habit Tracker API!"
    
    # Test MongoDB route
    @app.route("/test-mongo")
    def test_mongo():
        try:
            # Try to access a collection in your MongoDB
            mongo.db.users.find_one()
            return "MongoDB is connected and the route works!"
        except Exception as e:
            return f"Error connecting to MongoDB: {str(e)}"

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"message": "Internal server error"}, 500
