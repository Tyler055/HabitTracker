from flask import Blueprint, request, jsonify
from app import db
from models.models import User

user_bp = Blueprint('user_bp', __name__)

# Route to register a user
@user_bp.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"id": new_user.id, "username": new_user.username}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
