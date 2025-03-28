from flask import Blueprint, request, jsonify

# Define Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Define Blueprint for habit completion routes
completion_bp = Blueprint('completion', __name__)

# Define Blueprint for reminder routes
reminder_routes = Blueprint('reminder', __name__)

from app.extensions import db
from app.models import User, Habit, HabitCompletion, Reminder
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import ActiveConfig
from flask_jwt_extended import jwt_required, get_jwt_identity

# Utility function to generate JWT token
def generate_token(user_id):
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, ActiveConfig.JWT_SECRET, algorithm='HS256')
        return token
    except Exception as e:
        return None


# User Registration
@auth_bp.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return jsonify({"status": "error", "message": "Username or email already exists"}), 400

        new_user = User(username=username, email=email)
        new_user.password = generate_password_hash(password)  # Hash password before storing it
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# User Login
@auth_bp.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({"status": "error", "message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):  # Check password hash
            token = generate_token(user.id)
            return jsonify({"status": "success", "message": "Login successful", "token": token}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Habit Completion - Mark Habit as Completed
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

        completion = HabitCompletion(habit_id=habit.id, user_id=user.id, completed_at=datetime.utcnow())
        db.session.add(completion)
        db.session.commit()

        return jsonify({"status": "success", "message": "Habit marked as completed"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Create Reminder
@reminder_routes.route('/reminders', methods=['POST'])
@jwt_required()
def create_reminder():
    data = request.get_json()
    user_id = get_jwt_identity()

    if 'habit_id' not in data or 'reminder_time' not in data:
        return jsonify({'msg': 'Habit ID and reminder time are required'}), 400

    new_reminder = Reminder(
        habit_id=data['habit_id'],
        reminder_time=data['reminder_time'],
        user_id=user_id
    )

    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({'msg': 'Reminder created successfully', 'reminder': new_reminder.to_dict()}), 201
