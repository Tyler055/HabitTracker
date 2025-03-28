from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
import jwt
import datetime
from app.config import ActiveConfig

auth_bp = Blueprint('auth_bp', __name__)

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
        new_user.password = password
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

        if user and user.check_password(password):
            token = generate_token(user.id)
            return jsonify({"status": "success", "message": "Login successful", "token": token}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
