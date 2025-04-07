import os
import logging
from flask import Flask, current_app, render_template, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy import text
from config import config
from app.utils.extensions import db, mongo, mail, jwt, login_manager  

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Environment & Config
    env = os.getenv('APP_MODE', 'development')
    if env not in config:
        raise ValueError(f"Invalid APP_MODE: {env}. Must be one of {list(config.keys())}.")
    app.config.from_object(config[env])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_DB_URL") or config[env].SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MONGO_URI'] = os.getenv("MONGO_DB_URI") or config[env].MONGO_URI
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy
    Migrate(app, db)  # Initialize Flask-Migrate
    mongo.init_app(app)  # Initialize MongoDB
    jwt.init_app(app)  # Initialize JWT
    mail.init_app(app)  # Initialize Flask-Mail
    login_manager.init_app(app)  # Initialize Flask-Login

    # Flask-Login config
    login_manager.login_view = 'auth_bp.login'
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.models import User
        return User.query.get(int(user_id))

    # Enable CORS
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    allowed_origins = frontend_url.split(",")
    CORS(app, origins=allowed_origins, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Database check (only in dev)
    @app.before_request
    def check_database_connection():
        if app.config['APP_MODE'] == 'development':
            try:
                db.session.execute(text('SELECT 1'))
                app.logger.info("Database connection successful")
            except Exception as e:
                app.logger.error(f"Database connection failed: {e}")
                raise Exception("Database connection failed.")

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.habit_routes import habit_bp
    from app.routes.completion_routes import completion_bp
    from app.routes.reminder_routes import reminder_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(habit_bp, url_prefix="/habits")
    app.register_blueprint(completion_bp, url_prefix="/completion")
    app.register_blueprint(reminder_bp, url_prefix="/reminder")

    # Test routes
    @app.route('/test-page', methods=['GET'])
    def test_page():
        current_app.logger.info("Rendering test-page.html")
        return render_template('test-page.html')

    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Success! Backend is working."})

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error): return {"message": "Bad request"}, 400
    @app.errorhandler(401)
    def unauthorized(error): return {"message": "Unauthorized"}, 401
    @app.errorhandler(403)
    def forbidden(error): return {"message": "Forbidden"}, 403
    @app.errorhandler(404)
    def not_found(error): return {"message": "Resource not found"}, 404
    @app.errorhandler(405)
    def method_not_allowed(error): return {"message": "Method Not Allowed"}, 405
    @app.errorhandler(500)
    def internal_error(error): return {"message": "Internal server error"}, 500

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token"}), 401

    # Logging config
    log_level = logging.INFO if app.config['APP_MODE'] != 'production' else logging.ERROR
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level,
        handlers=[logging.StreamHandler()]
    )

    # Serve React frontend
    REACT_BUILD_DIR = os.getenv("REACT_BUILD_DIR", "frontend/build")

    @app.route('/', methods=['GET'])
    def index():
        """Serve frontend index.html (in dev mode only)"""
        if app.config.get('APP_MODE') == 'development':
            return send_from_directory(REACT_BUILD_DIR, 'index.html')
        return jsonify({"message": "Welcome to the Habit Tracker!"})

    @app.route('/static/<path:path>', methods=['GET'])
    def serve_static(path):
        return send_from_directory(os.path.join(REACT_BUILD_DIR, "static"), path)

    @app.route('/<path:path>', methods=['GET'])
    def serve_react_app(path):
        if path.startswith("api/"):
            return jsonify({"message": "API route not found."}), 404
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

    return app
