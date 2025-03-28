from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Habit, HabitCompletion, User
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

habit_bp = Blueprint('habit_bp', __name__)

# Marshmallow schema
class HabitSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)

habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)

# Get all habits for current user
@habit_bp.route('/api/habits', methods=['GET'])
@jwt_required()
def get_habits():
    try:
        current_user = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        habits = Habit.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page, error_out=False)

        data = habits_schema.dump(habits.items)
        return jsonify({"status": "success", "data": data, "total": habits.total}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching habits: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
@jwt_required()
def add_habit():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        validated = habit_schema.load(data)

        if Habit.query.filter_by(user_id=current_user, name=validated['name']).first():
            return jsonify({"status": "error", "message": "Habit already exists"}), 400

        new_habit = Habit(name=validated['name'], user_id=current_user)
        db.session.add(new_habit)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit added successfully",
            "data": habit_schema.dump(new_habit)
        }), 201

    except ValidationError as ve:
        return jsonify({"status": "error", "message": ve.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error adding habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Update a habit
@habit_bp.route('/api/habits/<int:id>', methods=['PUT'])
@jwt_required()
def update_habit(id):
    try:
        current_user = get_jwt_identity()
        habit = Habit.query.filter_by(id=id, user_id=current_user).first()
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        data = request.get_json()
        validated = habit_schema.load(data)

        habit.name = validated['name']
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit updated successfully",
            "data": habit_schema.dump(habit)
        }), 200

    except ValidationError as ve:
        return jsonify({"status": "error", "message": ve.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Delete a habit
@habit_bp.route('/api/habits/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_habit(id):
    try:
        current_user = get_jwt_identity()
        habit = Habit.query.filter_by(id=id, user_id=current_user).first()
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        db.session.delete(habit)
        db.session.commit()

        return jsonify({"status": "success", "message": "Habit deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Reset all habits for current user
@habit_bp.route('/api/habits/reset', methods=['POST'])
@jwt_required()
def reset_habits():
    try:
        current_user = get_jwt_identity()
        Habit.query.filter_by(user_id=current_user).delete()
        db.session.commit()
        return jsonify({"status": "success", "message": "All habits reset."}), 200
    except Exception as e:
        current_app.logger.error(f"Error resetting habits: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Track habit completion
@habit_bp.route('/api/habits/<int:id>/complete', methods=['POST'])
@jwt_required()
def complete_habit(id):
    try:
        current_user = get_jwt_identity()
        habit = Habit.query.filter_by(id=id, user_id=current_user).first()
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        completion = HabitCompletion(habit_id=habit.id, user_id=current_user, completed_at=datetime.utcnow())
        db.session.add(completion)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit marked as completed",
            "data": {
                "habit_id": habit.id,
                "completed_at": completion.completed_at.isoformat()
            }
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error completing habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500
