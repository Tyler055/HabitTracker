from flask import Blueprint, request, jsonify
from app import db
from models.models import Habit
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint for habit routes
habit_bp = Blueprint('habit_bp', __name__)

# Route to get all habits (API)
@habit_bp.route('/api/habits', methods=['GET'])
@jwt_required()  # Protect this route with JWT
def get_habits():
    try:
        user_id = get_jwt_identity()  # Get current user ID from JWT
        habits = Habit.query.filter_by(user_id=user_id).all()  # Fetch habits for the current user

        return jsonify({
            "status": "success",
            "data": [{"id": habit.id, "name": habit.name} for habit in habits]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Route to add a new habit (API)
@habit_bp.route('/api/habits', methods=['POST'])
@jwt_required()  # Protect this route with JWT
def add_habit():
    try:
        data = request.get_json()
        habit_name = data.get('name')

        if not habit_name:
            return jsonify({
                "status": "error",
                "message": "Habit name is required"
            }), 400

        user_id = get_jwt_identity()  # Get current user ID from JWT

        # Check if the habit already exists for the user
        if Habit.query.filter_by(name=habit_name, user_id=user_id).first():
            return jsonify({
                "status": "error",
                "message": "Habit already exists"
            }), 400

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
            "message": str(e)
        }), 500

# Route to delete a habit by ID (API)
@habit_bp.route('/api/habits/<int:id>', methods=['DELETE'])
@jwt_required()  # Protect this route with JWT
def delete_habit(id):
    try:
        user_id = get_jwt_identity()  # Get current user ID from JWT
        habit = Habit.query.filter_by(id=id, user_id=user_id).first()

        if not habit:
            return jsonify({
                "status": "error",
                "message": "Habit not found or not owned by user"
            }), 404

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

# Route to reset all habits for the current user (API)
@habit_bp.route('/api/habits/reset', methods=['POST'])
@jwt_required()  # Protect this route with JWT
def reset_habits():
    try:
        user_id = get_jwt_identity()  # Get current user ID from JWT
        Habit.query.filter_by(user_id=user_id).delete()
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
