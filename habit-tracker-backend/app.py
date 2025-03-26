from flask import Flask, request, jsonify
from config import config
from models import db, Habit  # Assuming Habit model is inside models.py
from routes.habit_routes import habit_bp
import os
from dotenv import load_dotenv
load_dotenv()


# Initialize Flask app
app = Flask(__name__)

# Load configuration based on environment
config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

print(f"Database URI: {config['SQLALCHEMY_DATABASE_URI']}")  # Debugging

# Initialize database
db.init_app(app)

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
    app.run(port=config["PORT"], debug=config["DEBUG"])
