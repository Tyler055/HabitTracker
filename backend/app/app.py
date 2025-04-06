import os
from flask import Flask, jsonify, render_template, send_from_directory, current_app, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from config import config
from app.utils.extensions import db, ma, mail, mongo  # Centralized extension objects
from app.routes.habit_routes import habit_bp
from app.routes.auth_routes import auth_bp
from app.models.models import Habit  # Import the Habit model

# Load environment variables from .env
load_dotenv()

# Initialize extensions
jwt = JWTManager()
migrate = Migrate()

# Global error handlers
def register_error_handlers(app):
    """Register custom error handlers for the application."""
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"message": "Internal server error"}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"message": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"message": "Forbidden"}), 403

def create_app(env_mode='development'):
    """App factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Load configuration based on the APP_MODE environment variable
    app_mode = os.getenv('APP_MODE', env_mode)  # Default to 'development'
    app.config.from_object(config.get(app_mode, config['development']))  # Load config from config.py

    # Allow frontend (React) to communicate with backend via CORS
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    CORS(app, origins=[frontend_url])
from flask_cors import cross_origin

@app.route('/habits', methods=['GET'])
@cross_origin(origins=["http://localhost:3000"])  # Allow requests from React frontend
def get_habits():
    habits = Habit.query.all()
    return jsonify({'habits': [habit.to_dict() for habit in habits]})

CORS(app, resources={r"/habits": {"origins": "*"}})
@app.route('/habits', methods=['OPTIONS'])
@cross_origin(origins=["http://localhost:3000"])  # Respond with CORS headers for OPTIONS requests
def options():
    return '', 200  # CORS preflight check pass

    # Ensure DATABASE_URL is set and assign it to SQLAlchemy URI
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT secret key and other settings
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Register blueprints for routes
    app.register_blueprint(habit_bp, url_prefix="/habits")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Register global error handlers
    register_error_handlers(app)

    # API Test Endpoint
    @app.route('/api')
    def home():
        return "Welcome to the Habit Tracker!"

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
    @app.route('/fetch_habits')
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
    @app.route("/test-mongo")
    def test_mongo():
        try:
            mongo.db.list_collection_names()  # Check if connection is working
            return "MongoDB is connected and operational!"
        except Exception as e:
            current_app.logger.error(f"MongoDB connection error: {str(e)}")
            return f"Error connecting to MongoDB: {str(e)}"

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

    # Route to serve React app for the home page
    @app.route('/')
    def index():
        if current_app.config.get('APP_MODE') == 'development':
            return send_from_directory(REACT_BUILD_DIR, 'index.html')
        return "Welcome to the Habit Tracker!"

    # Route to serve static assets for React frontend
    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory(f"{REACT_BUILD_DIR}/static", path)

    # Serve React Frontend for all paths that are not API-related
    @app.route('/<path:path>')
    def serve_react_app(path):
        if path.startswith("api/"):
            return jsonify({"message": "API route not found."}), 404
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

    return app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Ensure debug mode is only enabled for development and set `host='0.0.0.0'` for production
    app.run(debug=os.getenv('APP_MODE') == 'development', host='0.0.0.0', port=5000)
