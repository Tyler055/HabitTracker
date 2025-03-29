from flask import Blueprint, request, jsonify
from app.utils.extensions import db
from app.models.models import HabitCompletion, Habit, User
from datetime import datetime

completion_bp = Blueprint('completion_bp', __name__)

# Mark a habit as completed
@completion_bp.route('/api/habits/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        habit = Habit.query.get(habit_id)
        user = User.query.get(user_id)

        if not habit or not user:
            return jsonify({"status": "error", "message": "Invalid habit or user ID"}), 404

        completion = HabitCompletion(habit_id=habit.id, user_id=user.id)
        db.session.add(completion)
        db.session.commit()

        return jsonify({"status": "success", "message": "Habit marked as completed"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Get all completions for a user
@completion_bp.route('/api/users/<int:user_id>/completions', methods=['GET'])
def get_user_completions(user_id):
    try:
        completions = HabitCompletion.query.filter_by(user_id=user_id).all()
        result = [
            {
                "habit_id": completion.habit_id,
                "completed_at": completion.completed_at.strftime('%Y-%m-%d %H:%M:%S')
            } for completion in completions
        ]

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Reset (delete) all completions for a user
@completion_bp.route('/api/users/<int:user_id>/completions/reset', methods=['POST'])
def reset_user_completions(user_id):
    try:
        completions = HabitCompletion.query.filter_by(user_id=user_id).all()
        for completion in completions:
            db.session.delete(completion)
        db.session.commit()

        return jsonify({"status": "success", "message": "All habit completions reset"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
