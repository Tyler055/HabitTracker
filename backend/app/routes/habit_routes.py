from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user as login_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Habit, HabitCompletion
from app.__init__ import db
from datetime import date
from app.schemes.schema import habit_schema
from app.utils.utils import get_user_from_identity

habit_bp = Blueprint('habit_bp', __name__, url_prefix="/habits")

# Utility function to get the current user from either JWT or Flask-Login
def get_current_user():
    try:
        user_id = get_jwt_identity()  # Attempt to get user from JWT
        return get_user_from_identity(user_id)
    except Exception:
        # Fall back to Flask-Login if JWT fails
        return login_user if login_user.is_authenticated else None

# Route to get all habits (GET /habits)
@habit_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
@login_required
def get_habits():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    frequency = request.args.get('frequency')
    completed_today = request.args.get('completed_today')

    habits_query = Habit.query.filter_by(user_id=user.id, is_active=True)  # Use `is_active` instead of `deleted`

    # Filter by frequency if provided and valid
    if frequency:
        if frequency not in ['daily', 'weekly', 'monthly']:
            return jsonify({'error': 'Invalid frequency value. Valid values are "daily", "weekly", "monthly".'}), 400
        habits_query = habits_query.filter_by(frequency=frequency)

    # Filter by completed_today if provided and valid
    if completed_today is not None:
        if completed_today.lower() not in ['true', 'false']:
            return jsonify({'error': 'Invalid value for completed_today. Expected "true" or "false".'}), 400
        
        today = date.today()
        if completed_today.lower() == 'true':
            habits_query = habits_query.filter(Habit.completions.any(HabitCompletion.date_completed == today))
        elif completed_today.lower() == 'false':
            habits_query = habits_query.filter(~Habit.completions.any(HabitCompletion.date_completed == today))

    habits = habits_query.all()
    return jsonify([habit.to_dict() for habit in habits])

# Route to add a new habit (POST /habits)
@habit_bp.route('/', methods=['POST'])
@jwt_required(optional=True)
@login_required
def add_habit():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    errors = habit_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    habit = Habit(
        user_id=user.id,
        name=data['name'],
        description=data.get('description'),
        frequency=data.get('frequency', 'daily')  # Default frequency to 'daily' if not provided
    )
    db.session.add(habit)
    db.session.commit()

    return jsonify(habit.to_dict()), 201

# Route to delete a habit (DELETE /habits/<id>)
@habit_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required(optional=True)
@login_required
def delete_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=True).first()  # Use `is_active`
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404

    habit.soft_delete()  # Call the soft delete method
    db.session.commit()
    return jsonify({'message': 'Habit soft-deleted'}), 200

# Route to restore a habit (PATCH /habits/restore/<id>)
@habit_bp.route('/restore/<int:id>', methods=['PATCH'])
@jwt_required(optional=True)
@login_required
def restore_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=False).first()  # Use `is_active=False` for soft-deleted habits
    if not habit:
        return jsonify({'error': 'Habit not found or not deleted'}), 404

    habit.restore()  # Call the restore method
    db.session.commit()
    return jsonify({'message': 'Habit restored'}), 200

# Route to complete or remove completion of a habit (POST /habits/complete/<id>)
@habit_bp.route('/complete/<int:id>', methods=['POST'])
@jwt_required(optional=True)
@login_required
def complete_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=True).first()  # Use `is_active`
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404

    today = date.today()
    completion = HabitCompletion.query.filter_by(habit_id=habit.id, date_completed=today).first()

    if completion:
        db.session.delete(completion)
        db.session.commit()
        return jsonify({'message': 'Completion removed', 'completed': False}), 200
    else:
        new_completion = HabitCompletion(habit_id=habit.id, date_completed=today)
        db.session.add(new_completion)
        db.session.commit()
        return jsonify({'message': 'Habit marked as completed', 'completed': True}), 200
