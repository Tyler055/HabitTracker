from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.extensions import db
from app.models.models import HabitReminder, Habit  # Assuming Habit is the model for habits
from datetime import datetime
from dateutil.parser import parse  # To parse ISO 8601 datetime strings

reminder_bp = Blueprint('reminder_bp', __name__)

# Utility function for error handling
def handle_error(msg, status_code, error=None):
    response = {'msg': msg}
    if error:
        response['error'] = str(error)
    return jsonify(response), status_code

# POST /reminders - Create a new reminder
@reminder_bp.route('/reminders', methods=['POST'])
@jwt_required()  # Protect the route with JWT authentication
def create_reminder():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user from the JWT token
    
    # Validate input
    if 'habit_id' not in data or 'reminder_time' not in data:
        return handle_error('Habit ID and reminder time are required', 400)
    
    # Validate reminder_time format (assuming it's in ISO 8601 format)
    try:
        reminder_time = parse(data['reminder_time'])  # Parse the ISO 8601 string into datetime object
    except ValueError:
        return handle_error('Invalid reminder time format. Please use ISO 8601 format.', 400)

    # Check if the habit exists
    habit = Habit.query.filter_by(id=data['habit_id'], user_id=user_id).first()
    if habit is None:
        return handle_error('Habit not found', 404)
    
    new_reminder = HabitReminder(
        habit_id=data['habit_id'],
        reminder_time=reminder_time,
        user_id=user_id  # Link reminder to authenticated user
    )
    
    try:
        db.session.add(new_reminder)
        db.session.commit()
        return jsonify({'msg': 'Reminder created successfully', 'reminder': new_reminder.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return handle_error('Error creating reminder', 500, e)

# GET /reminders - Get all reminders for the authenticated user
@reminder_bp.route('/reminders', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_reminders():
    user_id = get_jwt_identity()
    
    reminders = HabitReminder.query.filter_by(user_id=user_id).all()
    reminders_list = [reminder.to_dict() for reminder in reminders]  # Convert each reminder to a dict
    
    return jsonify({'reminders': reminders_list}), 200

# GET /reminders/<id> - Get a specific reminder by ID
@reminder_bp.route('/reminders/<int:id>', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_reminder(id):
    user_id = get_jwt_identity()
    
    reminder = HabitReminder.query.filter_by(id=id, user_id=user_id).first()
    if reminder is None:
        return handle_error('Reminder not found', 404)
    
    return jsonify({'reminder': reminder.to_dict()}), 200

# PUT /reminders/<id> - Update an existing reminder
@reminder_bp.route('/reminders/<int:id>', methods=['PUT'])
@jwt_required()  # Protect the route with JWT authentication
def update_reminder(id):
    user_id = get_jwt_identity()
    
    reminder = HabitReminder.query.filter_by(id=id, user_id=user_id).first()
    if reminder is None:
        return handle_error('Reminder not found', 404)
    
    data = request.get_json()
    
    if 'reminder_time' in data:
        # Validate reminder_time format
        try:
            reminder.reminder_time = parse(data['reminder_time'])  # Parse new reminder time
        except ValueError:
            return handle_error('Invalid reminder time format. Please use ISO 8601 format.', 400)
    
    try:
        db.session.commit()
        return jsonify({'msg': 'Reminder updated successfully', 'reminder': reminder.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error('Error updating reminder', 500, e)

# DELETE /reminders/<id> - Delete a reminder by ID
@reminder_bp.route('/reminders/<int:id>', methods=['DELETE'])
@jwt_required()  # Protect the route with JWT authentication
def delete_reminder(id):
    user_id = get_jwt_identity()
    
    reminder = HabitReminder.query.filter_by(id=id, user_id=user_id).first()
    if reminder is None:
        return handle_error('Reminder not found', 404)
    
    try:
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({'msg': 'Reminder deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error('Error deleting reminder', 500, e)