from flask import Flask, request, jsonify
from config import config  # Importing config from config.py
from models import db, Habit  # Importing db and Habit from models.py
from routes.habit_routes import habit_bp  # Import blueprint from habit_routes.py
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])  # Select the config based on the environment variable

# Set the database URI dynamically (using SQLite as default if not set)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///habit_tracker.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Debugging: Print out the database URI to ensure it's loaded correctly
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize the database with the Flask app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(habit_bp)

# Define a simple home route
@app.route('/')
def home():
    return "Hello, Flask!"

# API route to add a habit
@app.route('/api/add-habit', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Invalid request"}), 400

        new_habit = Habit(name=data["name"])
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({"message": "Habit added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    app.run(port=os.getenv("PORT", 5000), debug=os.getenv("DEBUG", "True") == "True")  # Default to port 5000 if not specified
