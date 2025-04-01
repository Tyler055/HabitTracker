import os
from flask import Flask, jsonify, render_template, send_from_directory
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from config import config
from app.utils.extensions import db, ma, mail, mongo  # Centralized extension objects
from app.routes.habit_routes import habit_bp
from app.routes.auth_routes import auth_bp

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

def create_app(env_name=None):
    app = Flask(__name__)
    
    # Allow frontend (React) to communicate with backend
    CORS(app, origins=["http://localhost:3000"])


    # Load config based on environment
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

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # MongoDB setup
    app.config["MONGO_URI"] = os.getenv("MONGO_PROD_URI")
    mongo.init_app(app)

    # Register blueprints (routes)
    app.register_blueprint(habit_bp, url_prefix="/api/habits")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Register global error handlers
    register_error_handlers(app)

    # API Endpoint Example
    @app.route('/api/data')
    def get_data():
        return jsonify({"message": "Hello from Flask!"})

    # Example of returning dynamic HTML content
    @app.route('/api/get_html')
    def get_html():
        dynamic_html = """
        <div>
            <h2>Dynamic Content from Flask</h2>
            <p>This content is generated by the backend (Flask) and displayed in the frontend (React).</p>
        </div>
        """
        return jsonify({"html": dynamic_html})

    # Test MongoDB connection
    @app.route("/test-mongo")
    def test_mongo():
        try:
            mongo.db.users.find_one()
            return "MongoDB is connected and the route works!"
        except Exception as e:
            return f"Error connecting to MongoDB: {str(e)}"

    # Route
    @app.route('/')
    def index():
        return render_template('index.html')  # Or any response you want to return

    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Success! Backend is working."})#return render_template('test.html')
    

    return app

# Serve the React frontend build
app = create_app()

@app.route('/')
def serve_react():
    return send_from_directory('frontend/build', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('frontend/build/static', path)

@app.route('/<path:path>')
def serve_react_app(path):
    return send_from_directory('frontend/build', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
