from flask import Blueprint, request, jsonify
from app.utils.extensions import db
from app.models.models import HabitCompletion, Habit, User
from datetime import datetime
import logging

completion_bp = Blueprint('completion_bp', __name__)

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Get all completions
@completion_bp.route('/completions', methods=['GET'])
def get_completions():
    try:
        # Retrieve all completions from the database
        completions = HabitCompletion.query.all()

        # Return an empty list if no completions exist
        if not completions:
            return jsonify({"status": "success", "data": []}), 200

        # Format the result into a list of dictionaries
        result = [
            {
                "habit_id": completion.habit_id,
                "user_id": completion.user_id,
                "completed_at": completion.completed_at.strftime('%Y-%m-%d %H:%M:%S')  # Assuming 'completed_at' is a datetime column
            } for completion in completions
        ]

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logger.error(f"Error retrieving completions: {str(e)}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


# Mark a habit as completed
@completion_bp.route('/habits/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    try:
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')

        # Validate input
        if not user_id:
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        # Retrieve habit and user from DB
        habit = Habit.query.get(habit_id)
        user = User.query.get(user_id)

        # Check if habit and user exist
        if not habit or not user:
            return jsonify({"status": "error", "message": "Invalid habit or user ID"}), 404

        # Create and add completion record
        completion = HabitCompletion(habit_id=habit.id, user_id=user.id, completed_at=datetime.utcnow())
        db.session.add(completion)
        db.session.commit()

        logger.info(f"User {user_id} marked habit {habit_id} as completed.")
        return jsonify({"status": "success", "message": "Habit marked as completed"}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error completing habit {habit_id} for user {user_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


# Get all completions for a specific user
@completion_bp.route('/users/<int:user_id>/completions', methods=['GET'])
def get_user_completions(user_id):
    try:
        # Retrieve completions for user
        completions = HabitCompletion.query.filter_by(user_id=user_id).all()

        # Return empty list if no completions found
        if not completions:
            return jsonify({"status": "success", "data": []}), 200

        # Format the result into a list of dictionaries
        result = [
            {
                "habit_id": completion.habit_id,
                "completed_at": completion.completed_at.strftime('%Y-%m-%d %H:%M:%S')
            } for completion in completions
        ]

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logger.error(f"Error retrieving completions for user {user_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


# Reset (delete) all completions for a user
@completion_bp.route('/users/<int:user_id>/completions/reset', methods=['POST'])
def reset_user_completions(user_id):
    try:
        # Retrieve completions for user
        completions = HabitCompletion.query.filter_by(user_id=user_id).all()

        # If no completions, return a message
        if not completions:
            return jsonify({"status": "error", "message": "No completions found for this user"}), 404

        # Delete all completions
        for completion in completions:
            db.session.delete(completion)
        db.session.commit()

        logger.info(f"All completions reset for user {user_id}.")
        return jsonify({"status": "success", "message": "All habit completions reset"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error resetting completions for user {user_id}: {str(e)}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
