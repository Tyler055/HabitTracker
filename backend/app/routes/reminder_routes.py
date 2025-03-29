from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Reminder  # Assuming Reminder is a model in your app
from app import db

reminder_routes = Blueprint('reminder_routes', __name__)

# POST /reminders - Create a new reminder
@reminder_routes.route('/reminders', methods=['POST'])
@jwt_required()  # Protect the route with JWT authentication
def create_reminder():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user from the JWT token
    
    # Validate input
    if 'habit_id' not in data or 'reminder_time' not in data:
        return jsonify({'msg': 'Habit ID and reminder time are required'}), 400
    
    new_reminder = Reminder(
        habit_id=data['habit_id'],
        reminder_time=data['reminder_time'],
        user_id=user_id  # Link reminder to authenticated user
    )
    
    db.session.add(new_reminder)
    db.session.commit()
    
    return jsonify({'msg': 'Reminder created successfully', 'reminder': new_reminder.to_dict()}), 201


# GET /reminders - Get all reminders for the authenticated user
@reminder_routes.route('/reminders', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_reminders():
    user_id = get_jwt_identity()
    
    reminders = Reminder.query.filter_by(user_id=user_id).all()
    reminders_list = [reminder.to_dict() for reminder in reminders]  # Convert each reminder to a dict
    
    return jsonify({'reminders': reminders_list}), 200


# GET /reminders/<id> - Get a specific reminder by ID
@reminder_routes.route('/reminders/<int:id>', methods=['GET'])
@jwt_required()  # Protect the route with JWT authentication
def get_reminder(id):
    user_id = get_jwt_identity()
    
    reminder = Reminder.query.filter_by(id=id, user_id=user_id).first()
    if reminder is None:
        return jsonify({'msg': 'Reminder not found'}), 404
    
    return jsonify({'reminder': reminder.to_dict()}), 200


# PUT /reminders/<id> - Update an existing reminder
@reminder_routes.route('/reminders/<int:id>', methods=['PUT'])
@jwt_required()  # Protect the route with JWT authentication
def update_reminder(id):
    user_id = get_jwt_identity()
    
    reminder = Reminder.query.filter_by(id=id, user_id=user_id).first()
    if reminder is None:
        return jsonify({'msg': 'Reminder not found'}), 404
    
    data = request.get_json()
    
    if 'reminder_time' in data:
        reminder.reminder_time = data['reminder_time']
    
    db.session.commit()
    
    return jsonify({'msg': 'Reminder updated successfully', 'reminder': reminder.to_dict()}), 200


# DELETE /reminders/<id> - Delete a reminder by ID
@reminder_routes.route('/reminders/<int:id>', methods=['DELETE'])
@jwt_required()  # Protect the route with JWT authentication
def delete_reminder(id):
    user_id = get_jwt_identity()
    
    reminder = Reminder.query.filter_by(id=id, user_id=user_id).first()
    if reminder is None:
        return jsonify({'msg': 'Reminder not found'}), 404
    
    db.session.delete(reminder)
    db.session.commit()
    
    return jsonify({'msg': 'Reminder deleted successfully'}), 200
