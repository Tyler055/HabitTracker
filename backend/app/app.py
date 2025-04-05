import os
from flask import Flask, jsonify, render_template, send_from_directory, current_app
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from config import config
from app.utils.extensions import db, ma, mail, mongo  # Centralized extension objects
from app.routes.habit_routes import habit_bp
from app.routes.auth_routes import auth_bp
from app.models.models import Habit  # Import the Habit model

# Load environment variables
load_dotenv()

# Initialize extensions
jwt = JWTManager()
migrate = Migrate()

# Global error handlers
def register_error_handlers(app):
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
    app = Flask(__name__)

    # Load configuration based on the APP_MODE environment variable
    app_mode = os.getenv('APP_MODE', env_mode)  # Use APP_MODE to select the correct config
    app.config.from_object(config.get(app_mode, config['development']))  # Get config based on APP_MODE

    # Allow frontend (React) to communicate with backend
    CORS(app, origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")])

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

    # Register blueprints (routes)
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

    # Route to fetch habits from the database with filtering
    @app.route('/fetch_habits')
    def fetch_habits():
        try:
            habits = Habit.query.filter_by(deleted_at=None).all()
            if not habits:
                return jsonify({"message": "No habits found."}), 404
            
            habit_data = [{"id": habit.id, "name": habit.name, "completed": habit.completed, "frequency": habit.frequency} for habit in habits]
            return jsonify({"habits": habit_data}), 200

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
            return f"Error connecting to MongoDB: {str(e)}"

    # Flask HTML Test Page
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Success! Backend is working."})

    # Render test page
    @app.route('/test-page', methods=['GET'])
    def test_page():
        current_app.logger.info("Rendering test-page.html")
        return render_template('test-page.html')

    # Serve React Frontend
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
