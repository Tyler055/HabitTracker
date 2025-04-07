from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configurations from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_DB_URL')  # Ensure your .env file has this variable
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance reasons

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Register routes, blueprints, etc.
    # e.g., from .views import views
    # app.register_blueprint(views)

    return app
