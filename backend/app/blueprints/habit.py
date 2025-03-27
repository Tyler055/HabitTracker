from flask import Blueprint, request, jsonify
from app import db  # Ensure you import db from your main app
from models import Habit  # Ensure you import your Habit model

# Create a Blueprint for habit routes
habit_bp = Blueprint('habit_bp', __name__)

# Route to get all habits (API)
@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        # Fetch all habits from the database
        habits = Habit.query.all()
        return jsonify({
            "status": "success",
            "data": [habit.name for habit in habits]  # List of habit names
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Route to add a new habit (API)
@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()  # Parse JSON from the request body
        habit_name = data.get('name')  # Extract the habit name

        # Validate input
        if not habit_name:
            return jsonify({
                "status": "error",
                "message": "Habit name is required"
            }), 400

        # Check if the habit already exists
        if Habit.query.filter_by(name=habit_name).first():
            return jsonify({
                "status": "error",
                "message": "Habit already exists"
            }), 400

        # Create a new habit
        new_habit = Habit(name=habit_name)
        db.session.add(new_habit)
        db.session.commit()

        # Return the new habit with its details
        return jsonify({
            "status": "success",
            "message": "Habit added successfully",
            "data": {
                "id": new_habit.id,
                "name": new_habit.name
            }
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Route to delete a habit by ID (API)
@habit_bp.route('/api/habits/<int:id>', methods=['DELETE'])
def delete_habit(id):
    try:
        habit = Habit.query.get(id)  # Fetch habit by its ID
        if not habit:
            return jsonify({
                "status": "error",
                "message": "Habit not found"
            }), 404

        # Delete the habit
        db.session.delete(habit)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Route to reset all habits (API)
@habit_bp.route('/api/habits/reset', methods=['POST'])
def reset_habits():
    try:
        # Delete all habits
        Habit.query.delete()
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "All habits have been reset"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Optional: Route to get all habits as a list (for regular views, not just API)
@habit_bp.route('/habits', methods=['GET'])
def index():
    try:
        habits = Habit.query.all()  # Fetch all habits from the database
        return jsonify({
            "status": "success",
            "data": [{"id": habit.id, "name": habit.name} for habit in habits]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
