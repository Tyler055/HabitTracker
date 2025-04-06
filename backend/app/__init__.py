import os
import logging
from flask import Flask, current_app, render_template, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, current_user
from dotenv import load_dotenv
from sqlalchemy import text
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()
jwt = JWTManager()
mail = Mail()
login_manager = LoginManager()

# Initialize Flask-Login
login_manager.login_view = 'auth_bp.login'  # Adjust the login endpoint

# Load environment variables from .env file for configuration
load_dotenv()

# Define Habit model
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    frequency = db.Column(db.String(20), default='daily')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('habits', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'completed': self.completed,
            'frequency': self.frequency,
            'user_id': self.user_id
        }

# Initialize the Flask app
def create_app():
    app = Flask(__name__)

    # Retrieve the app mode (development, production, testing) from the environment variable
    env = os.getenv('APP_MODE', 'development')
    if env not in config:
        raise ValueError(f"Invalid APP_MODE: {env}. Must be one of {list(config.keys())}.")
    
    # Load configuration from the appropriate environment settings
    app.config.from_object(config[env])

    # Set up app configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_DB_URL") or config[env].SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI") or config[env].MONGO_URI
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize the extensions with the Flask app instance
    db.init_app(app)
    migrate.init_app(app, db)
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Set up CORS
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    allowed_origins = frontend_url.split(",")
    CORS(app, origins=allowed_origins, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Database connection check before the first request
    @app.before_request
    def check_database_connection():
        if app.config['APP_MODE'] == 'development':
            try:
                db.session.execute(text('SELECT 1'))
                app.logger.info("Database connection successful")
            except Exception as e:
                app.logger.error(f"Database connection failed: {e}")
                raise Exception("Database connection failed.")

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.habit_routes import habit_bp
    from app.routes.completion_routes import completion_bp
    from app.routes.reminder_routes import reminder_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(habit_bp, url_prefix="/habits")
    app.register_blueprint(completion_bp, url_prefix="/completion")
    app.register_blueprint(reminder_bp, url_prefix="/reminder")

    # Test page route
    @app.route('/test-page', methods=['GET'])
    def test_page():
        current_app.logger.info("Rendering test-page.html")
        return render_template('test-page.html')

    # New test route to check backend working
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Success! Backend is working."})

    # Route to fetch all habits
    @app.route('/habits', methods=['GET'])
    def get_habits():
        habits = Habit.query.all()
        return jsonify({'habits': [habit.to_dict() for habit in habits]})

    # Route to add a new habit
    @app.route('/habits', methods=['POST'])
    @login_required  # Ensure user is logged in before they can add a habit
    def add_habit():
        data = request.get_json()

        # Validation checks (e.g., name, frequency)
        if not data.get('name'):
            return jsonify({"message": "Habit name is required!"}), 400
        
        new_habit = Habit(
            name=data['name'],
            completed=False,  # Default to False for a new habit
            frequency=data.get('frequency', 'daily'),  # Set frequency or default to 'daily'
            user_id=current_user.id  # Assuming a User model is linked to the Habit model
        )

        try:
            db.session.add(new_habit)
            db.session.commit()
            return jsonify({"message": "Habit added successfully!", "habit": new_habit.to_dict()}), 201
        except Exception as e:
            current_app.logger.error(f"Error adding habit: {str(e)}")
            return jsonify({"message": "Error adding habit."}), 500

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

    # Catch-all route to serve the React app for any non-API route
    @app.route('/<path:path>', methods=['GET'])
    def serve_react_app(path):
        """ Catch-all route to serve the React app for any non-API route """
        if path.startswith("api/"):
            return jsonify({"message": "API route not found."}), 404
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

    return app
