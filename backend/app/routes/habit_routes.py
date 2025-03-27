# app/routes/habit_routes.py
from flask import Blueprint, request, jsonify
from app.extensions import db  # Import db from extensions.py
from app.models import Habit  # Import the Habit model

habit_bp = Blueprint('habit_bp', __name__)


# Route to get all habits
@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    try:
        habits = Habit.query.all()
        return jsonify({"status": "success", "data": [habit.name for habit in habits]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to add a new habit
@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    try:
        data = request.get_json()
        habit_name = data.get('name')

        if not habit_name:
            return jsonify({"status": "error", "message": "Habit name is required"}), 400

        if Habit.query.filter_by(name=habit_name).first():
            return jsonify({"status": "error", "message": "Habit already exists"}), 400

        new_habit = Habit(name=habit_name)
        db.session.add(new_habit)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Habit added successfully",
            "data": {
                "id": new_habit.id,
                "name": new_habit.name
            }
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to delete a habit by ID
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
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to reset all habits
@habit_bp.route('/api/habits/reset', methods=['POST'])
def reset_habits():
    try:
        Habit.query.delete()
        db.session.commit()
        return jsonify({"status": "success", "message": "All habits have been reset."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
