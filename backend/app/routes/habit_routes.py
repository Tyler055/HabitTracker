# app/routes/habit_routes.py

from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import Habit
from marshmallow import Schema, fields, ValidationError

habit_bp = Blueprint('habit_bp', __name__)

# Marshmallow schema for validation
class HabitSchema(Schema):
    name = fields.String(required=True)

habit_schema = HabitSchema()

# Get all habits with optional pagination
@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        habits = Habit.query.paginate(page=page, per_page=per_page, error_out=False)

        data = [{"id": habit.id, "name": habit.name} for habit in habits.items]
        return jsonify({"status": "success", "data": data, "total": habits.total}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching habits: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()
        validated = habit_schema.load(data)

        habit_name = validated['name']
        if Habit.query.filter_by(name=habit_name).first():
            return jsonify({"status": "error", "message": "Habit already exists"}), 400

        new_habit = Habit(name=habit_name)
        db.session.add(new_habit)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit added successfully",
            "data": {"id": new_habit.id, "name": new_habit.name}
        }), 201

    except ValidationError as ve:
        return jsonify({"status": "error", "message": ve.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error adding habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Update a habit by ID
@habit_bp.route('/api/habits/<int:id>', methods=['PUT'])
def update_habit(id):
    try:
        data = request.get_json()
        validated = habit_schema.load(data)

        habit = Habit.query.get(id)
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        habit.name = validated['name']
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit updated successfully",
            "data": {"id": habit.id, "name": habit.name}
        }), 200

    except ValidationError as ve:
        return jsonify({"status": "error", "message": ve.messages}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Delete a habit by ID
@habit_bp.route('/api/habits/<int:id>', methods=['DELETE'])
def delete_habit(id):
    try:
        habit = Habit.query.get(id)
        if not habit:
            return jsonify({"status": "error", "message": "Habit not found"}), 404

        db.session.delete(habit)
        db.session.commit()

        return jsonify({"status": "success", "message": "Habit deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting habit: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500

# Reset all habits (use with caution)
@habit_bp.route('/api/habits/reset', methods=['POST'])
def reset_habits():
    try:
        db.session.query(Habit).delete()  # Safe delete for cascading in future
        db.session.commit()
        return jsonify({"status": "success", "message": "All habits have been reset."}), 200
    except Exception as e:
        current_app.logger.error(f"Error resetting habits: {str(e)}")
        return jsonify({"status": "error", "message": "Server error"}), 500
