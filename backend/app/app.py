from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from config import config  # Import your config
from routes.habit_routes import habit_bp  # Import habit blueprint
from models import db  # Import your database model (if separate)

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment (from .env or default)
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])  # Select the config based on the environment variable

# Set the database URI dynamically (SQLite default if not set)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///habit_tracker.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Debugging: Print out the database URI to ensure it's loaded correctly
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize the database with the Flask app
db.init_app(app)

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Register Blueprints (routes)
app.register_blueprint(habit_bp)

# Simple home route to check if the server is up
@app.route('/')
def home():
    return "Welcome to the Habit Tracker API!"

# Run the application
if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)), debug=os.getenv("DEBUG", "True") == "True")
