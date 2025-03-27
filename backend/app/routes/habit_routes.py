from flask import Blueprint, request, jsonify
from app import db
from models import Habit

habit_bp = Blueprint('habit_bp', __name__)

# Route to get all habits
@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        # Fetch all habits from the database
        habits = Habit.query.all()
        
        # Return a list of habit names
        return jsonify([habit.name for habit in habits])
    
    except Exception as e:
        # Handle potential errors
        return jsonify({"error": str(e)}), 500

# Route to add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()  # Get JSON data from the request
        habit_name = data.get('name')  # Extract habit name
        
        # Validate the input
        if not habit_name:
            return jsonify({"error": "Habit name is required"}), 400
        
        # Create a new habit object
        new_habit = Habit(name=habit_name)
        db.session.add(new_habit)  # Add the habit to the session
        db.session.commit()  # Commit the transaction to the database
        
        # Return the newly created habit as a response
        return jsonify({
            "id": new_habit.id,
            "name": new_habit.name
        }), 201
    
    except Exception as e:
        # Handle potential errors
        return jsonify({"error": str(e)}), 500

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
        # Handle potential errors
        return jsonify({"error": str(e)}), 500

# Route to reset all habits (optional route to clear all habits)
@habit_bp.route('/api/habits/reset', methods=['POST'])
def reset_habits():
    try:
        Habit.query.delete()  # Delete all habits
        db.session.commit()  # Commit the transaction to the database
        return jsonify({"message": "All habits have been reset."}), 200
    
    except Exception as e:
        # Handle potential errors
        return jsonify({"error": str(e)}), 500

# Register the habit blueprint
# In your app.py file, register this blueprint: app.register_blueprint(habit_bp)
