from flask import Blueprint, jsonify, request
from models import db, Habit

habit_bp = Blueprint('habit_bp', __name__)

@habit_bp.route('/api/habits', methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([habit.name for habit in habits])

@habit_bp.route('/api/habits', methods=['POST'])
def add_habit():
    habit_name = request.json.get('name')
    new_habit = Habit(name=habit_name)
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({"message": "Habit added successfully!"}), 201
