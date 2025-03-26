from flask import Flask, request, jsonify
from config.config import config
from models import db, Habit  # Assuming Habit model is inside models.py
from routes.habit_routes import habit_bp
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
app.config.from_object('config.Config')  # Assuming Config class is in config.py

# Set the database URI dynamically based on the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Debugging: Print out the database URI to ensure it's loaded correctly
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize database and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Register Blueprints (assuming habit_bp is defined in habit_routes.py)
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
