from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User  # Import User model here

# Define Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Centralized error handler
def handle_error(message, status_code=400):
    return jsonify({"status": "error", "message": message}), status_code

# Test route
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "success", "message": "Auth route is working!"}), 200

# User Registration
@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return handle_error("All fields are required")

        # Check if user already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return handle_error("Username or email already exists")

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password before saving
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# User Login
@auth_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return handle_error("Email and password are required")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Use check_password method in User model
            access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
            return jsonify({"status": "success", "message": "Login successful", "token": access_token}), 200
        else:
            return handle_error("Invalid credentials", 401)

    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Get Current User Info (Protected Route)
@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return handle_error("User not found", 404)

        return jsonify({
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200

    except Exception as e:
        return handle_error(str(e), 500)

# Logout Route (Optional - Frontend handles token removal)
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    return jsonify({"status": "success", "message": "User logged out successfully"}), 200

