import os
from flask import Flask, jsonify, send_from_directory, current_app, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from sqlalchemy import text
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()
jwt = JWTManager()
mail = Mail()

# Import routes for modularity
from app.__init__ import db
from app.routes.auth_routes import auth_bp
from app.routes.habit_routes import habit_bp
from app.routes.completion_routes import completion_bp
from app.routes.reminder_routes import reminder_bp
from app.models.models import Habit  # Import the Habit model

def create_app():
    """
    Factory function to create and configure the Flask application instance.
    """
    # Load environment variables from .env file for configuration
    load_dotenv()

    # Retrieve the app mode (development, production, testing) from the environment variable
    env = os.getenv('APP_MODE', 'development')  # Default to 'development' if not specified
    if env not in config:
        raise ValueError(f"Invalid APP_MODE: {env}. Must be one of {list(config.keys())}.")

    # Initialize the Flask app
    app = Flask(__name__)

    # Load configuration from the appropriate environment settings
    app.config.from_object(config[env])

    # Set up app configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_DB_URL") or config[env].SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI") or config[env].MONGO_URI
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize the extensions with the Flask app instance
    db.init_app(app)  # Initialize SQLAlchemy with app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app
    mongo.init_app(app)  # Initialize PyMongo with app
    jwt.init_app(app)  # Initialize JWT with app
    mail.init_app(app)  # Initialize Flask-Mail with app

    # Set up CORS to allow cross-origin requests
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    allowed_origins = frontend_url.split(",")  # Allow multiple frontend URLs if necessary
    CORS(app, origins=allowed_origins)

    # Add the initialization code to be run before every request
    @app.before_request
    def initialize_app():
        if app.config['APP_MODE'] != 'production':  # Run the check only in development
            try:
                db.session.execute(text('SELECT 1'))
                app.logger.info("SQLAlchemy database connection successful")
            except Exception as e:
                app.logger.error(f"Database connection failed: {e}")
                raise Exception("Database connection failed. Please check your configuration.")

    # Register blueprints for routing (API or views)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(habit_bp, url_prefix="/habits")
    app.register_blueprint(completion_bp, url_prefix="/completion")
    app.register_blueprint(reminder_bp, url_prefix="/reminder")

    # Global error handlers for common HTTP errors
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

    # JWT error handling
    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token"}), 401

    # Enable logging for better error tracking
    log_level = logging.INFO if app.config['APP_MODE'] != 'production' else logging.ERROR
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level,
        handlers=[logging.StreamHandler()]
    )

    # API Test Endpoint
    @app.route('/api', methods=['GET'])
    def api_home():
        return jsonify({"message": "Welcome to the Habit Tracker API!"})

    # Route to fetch all habits
    @app.route('/habits', methods=['GET'])
    def get_habits():
        habits = Habit.query.all()
        return jsonify({'habits': [habit.to_dict() for habit in habits]})

    # Route to fetch a single habit by id
    @app.route('/habits/<int:id>', methods=['GET'])
    def get_habit(id):
        habit = Habit.query.get(id)
        if habit is None:
            return jsonify({'message': 'Habit not found'}), 404
        return jsonify(habit.to_dict())

    # Route to fetch habits with pagination and filtering
    @app.route('/habits/fetch', methods=['GET'])
    def fetch_habits():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        try:
            habits = Habit.query.filter_by(deleted_at=None).paginate(page, per_page, False)
            habit_data = [{"id": habit.id, "name": habit.name, "completed": habit.completed, "frequency": habit.frequency} for habit in habits.items]
            return jsonify({"habits": habit_data, "total": habits.total, "pages": habits.pages}), 200
        except Exception as e:
            current_app.logger.error(f"Error fetching habits: {str(e)}")
            return jsonify({"message": "Error fetching habits."}), 500

    # Test MongoDB connection
    @app.route("/test-mongo", methods=['GET'])
    def test_mongo():
        try:
            mongo.db.command('ping')  # This checks the MongoDB connection
            return "MongoDB is connected and operational!"
        except Exception as e:
            current_app.logger.error(f"MongoDB connection error: {str(e)}")
            return f"Error connecting to MongoDB: {str(e)}", 500

    # Flask HTML Test Page (testing backend functionality)
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Success! Backend is working."})

    # Render a test page (for debugging purposes)
    @app.route('/test-page', methods=['GET'])
    def test_page():
        current_app.logger.info("Rendering test-page.html")
        return render_template('test-page.html')

    # Serve React Frontend (Production-ready serving of the app)
    REACT_BUILD_DIR = os.getenv("REACT_BUILD_DIR", "frontend/build")

    @app.route('/', methods=['GET'])
    def index():
        """ Serve React frontend's index.html page """
        if app.config.get('APP_MODE') == 'development':
            return send_from_directory(REACT_BUILD_DIR, 'index.html')
        return jsonify({"message": "Welcome to the Habit Tracker!"})

    # Route to serve static assets for React frontend
    @app.route('/static/<path:path>', methods=['GET'])
    def serve_static(path):
        """ Serve React static files """
        return send_from_directory(f"{REACT_BUILD_DIR}/static", path)

    # Serve React Frontend for all paths that are not API-related
    @app.route('/<path:path>', methods=['GET'])
    def serve_react_app(path):
        """ Catch-all route to serve the React app for any non-API route """
        if path.startswith("api/"):
            return jsonify({"message": "API route not found."}), 404
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

    return app
