from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Habit
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define the blueprint with a proper prefix ONCE
habit_bp = Blueprint('habit_bp', __name__, url_prefix="/habits")

# Route to get all habits (GET /habits)
@habit_bp.route('/', methods=['GET'])
@jwt_required()
def get_habits():
    try:
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()
        
        # Fetch all habits for the user
        habits = Habit.query.filter_by(user_id=user_id).all()

        # Prepare the habit data to send as a response
        habits_data = [{"id": habit.id, "name": habit.name} for habit in habits]

        return jsonify({
            "status": "success",
            "data": habits_data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error fetching habits: {str(e)}"
        }), 500


# Route to add a new habit (POST /habits)
@habit_bp.route('/', methods=['POST'])
@jwt_required()
def add_habit():
    try:
        # Get data from the request
        data = request.get_json()
        habit_name = data.get('name')

        # Validate that the habit name is provided
        if not habit_name:
            return jsonify({"status": "error", "message": "Habit name is required"}), 400

        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Check if the habit already exists for the user
        existing_habit = Habit.query.filter_by(name=habit_name, user_id=user_id).first()
        if existing_habit:
            return jsonify({"status": "error", "message": "Habit already exists"}), 400

        # Create a new habit and add it to the database
        new_habit = Habit(name=habit_name, user_id=user_id)
        db.session.add(new_habit)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit added successfully",
            "data": {"id": new_habit.id, "name": new_habit.name}
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error adding habit: {str(e)}"
        }), 500


# Route to delete a habit (DELETE /habits/<id>)
@habit_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_habit(id):
    try:
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Fetch the habit by ID and ensure it belongs to the user
        habit = Habit.query.filter_by(id=id, user_id=user_id).first()

        if not habit:
            return jsonify({
                "status": "error",
                "message": "Habit not found or not owned by user"
            }), 404

        # Delete the habit from the database
        db.session.delete(habit)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error deleting habit: {str(e)}"
        }), 500


# Route to reset all habits for the user (POST /habits/reset)
@habit_bp.route('/reset', methods=['POST'])
@jwt_required()
def reset_habits():
    try:
        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Delete all habits for the user
        Habit.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "All habits have been reset"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error resetting habits: {str(e)}"
        }), 500
