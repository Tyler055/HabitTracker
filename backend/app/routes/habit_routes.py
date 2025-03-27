from flask import Blueprint, request, jsonify
from models import db, Habit

habit_bp = Blueprint('habit_bp', __name__)

# Route to get all habits
@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()  # Get all habits from the database
    return jsonify([habit.name for habit in habits])  # Return a list of habit names

# Route to add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()  # Get JSON data from the request
        if not data or 'name' not in data:  # Validate input
            return jsonify({"error": "Invalid request"}), 400

        new_habit = Habit(name=data["name"])  # Create new habit object
        db.session.add(new_habit)  # Add to the session
        db.session.commit()  # Commit the transaction to the database
        
        return jsonify({"message": "Habit added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors
