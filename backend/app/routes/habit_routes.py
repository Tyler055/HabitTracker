from flask import Flask, Blueprint, request, jsonify
from models import db, Habit

# Initialize Flask app
app = Flask(__name__)

# Blueprint for Habit routes
habit_bp = Blueprint('habit_bp', __name__)

# Route to get all habits
@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        habits = Habit.query.all()  # Get all habits from the database
        return jsonify([habit.name for habit in habits])  # Return a list of habit names
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

# Route to add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()  # Get JSON data from the request
        if not data or 'name' not in data:  # Validate input
            return jsonify({"error": "Invalid request, habit name is required"}), 400

        new_habit = Habit(name=data["name"])  # Create a new habit object
        db.session.add(new_habit)  # Add the habit to the session
        db.session.commit()  # Commit the transaction to the database
        
        return jsonify({"message": "Habit added successfully!", "habit": {"id": new_habit.id, "name": new_habit.name}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

# Route to delete a habit by ID
@habit_bp.route('/api/habits/<int:id>', methods=['DELETE'])
def delete_habit(id):
    try:
        habit = Habit.query.get(id)  # Get habit by ID
        if not habit:
            return jsonify({"error": "Habit not found"}), 404
        
        db.session.delete(habit)  # Delete the habit
        db.session.commit()  # Commit the transaction to the database
        return jsonify({"message": "Habit deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

# Route to reset all habits (e.g., for clearing out habits)
@habit_bp.route('/api/habits/reset', methods=['POST'])
def reset_habits():
    try:
        Habit.query.delete()  # Delete all habits
        db.session.commit()  # Commit the transaction to the database
        return jsonify({"message": "All habits have been reset."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

# Register the habit blueprint
app.register_blueprint(habit_bp)

# Main route (optional, but can be used to check if the server is working)
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Habit Tracker API!"}), 200

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
