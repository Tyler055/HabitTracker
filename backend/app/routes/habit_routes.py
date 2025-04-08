from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Habit, HabitCompletion
from app.utils.extensions import db
from datetime import date, timedelta
from app.schemes.schema import habit_schema, habits_schema
from app.utils.utils import get_user_from_identity
from sqlalchemy import Enum, func
from flask_cors import cross_origin
from collections import defaultdict

habit_bp = Blueprint('habit_bp', __name__, url_prefix="/habits")

# Utility to extract the user from the JWT token
def get_current_user():
    try:
        user_id = get_jwt_identity()
        return get_user_from_identity(user_id)
    except Exception:
        return None

# Pagination utility
def paginate(query, page, per_page):
    return query.paginate(page, per_page, False)

# Frequency enum
class FrequencyEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

# ---------------- GET Habits ----------------
@habit_bp.route('/', methods=['GET'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def get_habits():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    frequency = request.args.get('frequency')
    completed_today = request.args.get('completed_today')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    habits_query = Habit.query.filter_by(user_id=user.id, is_active=True)

    if frequency:
        if frequency not in [e.value for e in FrequencyEnum]:
            return jsonify({'error': 'Invalid frequency'}), 400
        habits_query = habits_query.filter_by(frequency=frequency)

    if completed_today is not None:
        today = date.today()
        if completed_today.lower() == 'true':
            habits_query = habits_query.filter(Habit.completions.any(HabitCompletion.date_completed == today))
        elif completed_today.lower() == 'false':
            habits_query = habits_query.filter(~Habit.completions.any(HabitCompletion.date_completed == today))
        else:
            return jsonify({'error': 'Invalid completed_today value'}), 400

    habits = paginate(habits_query, page, per_page)

    return jsonify({
        'habits': habits_schema.dump(habits.items),
        'total': habits.total,
        'pages': habits.pages,
        'current_page': habits.page,
        'per_page': habits.per_page
    }), 200

# ---------------- POST Habit ----------------
@habit_bp.route('/', methods=['POST'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def add_habit():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    errors = habit_schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    frequency = data.get('frequency', FrequencyEnum.DAILY.value)
    if frequency not in [e.value for e in FrequencyEnum]:
        return jsonify({'error': 'Invalid frequency'}), 400

    habit = Habit(
        user_id=user.id,
        name=data['name'],
        description=data.get('description'),
        frequency=frequency
    )
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit_schema.dump(habit)), 201

# ---------------- PATCH Habit ----------------
@habit_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def update_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=True).first()
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    frequency = data.get('frequency')

    if frequency and frequency not in [e.value for e in FrequencyEnum]:
        return jsonify({'error': 'Invalid frequency'}), 400

    if name:
        habit.name = name
    if description:
        habit.description = description
    if frequency:
        habit.frequency = frequency

    db.session.commit()
    return jsonify(habit_schema.dump(habit)), 200

# ---------------- DELETE Habit ----------------
@habit_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def delete_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=True).first()
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404

    habit.soft_delete()
    db.session.commit()
    return jsonify({'message': 'Habit soft-deleted'}), 200

# ---------------- Restore Habit ----------------
@habit_bp.route('/restore/<int:id>', methods=['PATCH'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def restore_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=False).first()
    if not habit:
        return jsonify({'error': 'Habit not found or not deleted'}), 404

    habit.restore()
    db.session.commit()
    return jsonify({'message': 'Habit restored'}), 200

# ---------------- Complete Habit (Toggle) ----------------
@habit_bp.route('/complete/<int:id>', methods=['POST'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def complete_habit(id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit = Habit.query.filter_by(id=id, user_id=user.id, is_active=True).first()
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

# ---------------- Bulk Complete ----------------
@habit_bp.route('/complete_bulk', methods=['POST'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def bulk_complete_habits():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    habit_ids = request.get_json().get('habit_ids', [])
    if not isinstance(habit_ids, list) or not habit_ids:
        return jsonify({'error': 'habit_ids must be a non-empty list'}), 400

    today = date.today()
    completed = []
    for habit_id in habit_ids:
        habit = Habit.query.filter_by(id=habit_id, user_id=user.id, is_active=True).first()
        if habit:
            exists = HabitCompletion.query.filter_by(habit_id=habit.id, date_completed=today).first()
            if not exists:
                db.session.add(HabitCompletion(habit_id=habit.id, date_completed=today))
                completed.append(habit.id)

    db.session.commit()
    return jsonify({'message': f'Completed {len(completed)} habits', 'completed_ids': completed}), 200

# ---------------- Stats Endpoint ----------------
@habit_bp.route('/stats', methods=['GET'])
@jwt_required()
@cross_origin(origins=["http://localhost:3000"], supports_credentials=True)
def habit_stats():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    period = request.args.get('period', '7d')
    if period not in ['7d', '30d']:
        return jsonify({'error': 'Invalid period. Use "7d" or "30d"'}), 400

    days = 7 if period == '7d' else 30
    start_date = date.today() - timedelta(days=days - 1)

    completions = db.session.query(
        HabitCompletion.date_completed,
        func.count(HabitCompletion.id)
    ).join(Habit).filter(
        Habit.user_id == user.id,
        HabitCompletion.date_completed >= start_date
    ).group_by(HabitCompletion.date_completed).order_by(HabitCompletion.date_completed).all()

    stats = [{'date': d.isoformat(), 'count': c} for d, c in completions]
    return jsonify({'stats': stats}), 200
