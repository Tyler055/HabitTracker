from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.utils.extensions import db
from app.models.models import Habit, HabitCompletion
from marshmallow import Schema, fields, ValidationError
from datetime import datetime

habit_bp = Blueprint('habit_bp', __name__)

# Marshmallow schema
class HabitSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    frequency = fields.String()

habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)

# Get all habits for the current user
@habit_bp.route('/api/habits', methods=['GET'])
@login_required
def get_habits():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        habits = Habit.query.filter_by(user_id=current_user.id, deleted_at=None).paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            "status": "success",
            "data": habits_schema.dump(habits.items),
            "total": habits.total
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching habits: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
@login_required
def add_habit():
    try:
        data = request.get_json()
        validated = habit_schema.load(data)

        if Habit.query.filter_by(user_id=current_user.id, name=validated['name'], deleted_at=None).first():
            return jsonify({"status": "error", "message": "Habit already exists"}), 400

        new_habit = Habit(name=validated['name'], user_id=current_user.id, frequency=validated.get('frequency', 'daily'))
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
@login_required
def update_habit(id):
    try:
        habit = Habit.query.filter_by(id=id, user_id=current_user.id, deleted_at=None).first()
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        data = request.get_json()
        validated = habit_schema.load(data)

        habit.name = validated['name']
        habit.frequency = validated.get('frequency', habit.frequency)
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

# Soft delete a habit
@habit_bp.route('/api/habits/<int:id>', methods=['DELETE'])
@login_required
def delete_habit(id):
    try:
        habit = Habit.query.filter_by(id=id, user_id=current_user.id, deleted_at=None).first()
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        habit.deleted_at = datetime.utcnow()  # Mark as soft deleted
        db.session.commit()

        return jsonify({"status": "success", "message": "Habit soft deleted"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Restore a habit
@habit_bp.route('/api/habits/<int:id>/restore', methods=['PUT'])
@login_required
def restore_habit(id):
    try:
        habit = Habit.query.filter_by(id=id, user_id=current_user.id).first()
        if not habit or habit.deleted_at is None:
            return jsonify({"status": "error", "message": "Habit not found or already active"}), 404

        habit.deleted_at = None  # Remove soft delete timestamp
        db.session.commit()

        return jsonify({"status": "success", "message": "Habit restored successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error restoring habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Track habit completion
@habit_bp.route('/api/habits/<int:id>/complete', methods=['POST'])
@login_required
def complete_habit(id):
    try:
        habit = Habit.query.filter_by(id=id, user_id=current_user.id, deleted_at=None).first()
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        # Check if the habit is already completed today
        if HabitCompletion.query.filter_by(user_id=current_user.id, habit_id=habit.id, completed_at=datetime.utcnow().date()).first():
            return jsonify({"status": "error", "message": "Habit already completed today"}), 400

        completion = HabitCompletion(habit_id=habit.id, user_id=current_user.id, completed_at=datetime.utcnow())
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

# Reset all habits for the current user
@habit_bp.route('/api/habits/reset', methods=['POST'])
@login_required
def reset_habits():
    try:
        Habit.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        return jsonify({"status": "success", "message": "All habits reset."}), 200
    except Exception as e:
        current_app.logger.error(f"Error resetting habits: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500
