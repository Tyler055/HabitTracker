from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import re
import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Import the User model here to avoid circular imports
from app.models.models import User

# Define Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Centralized error handler with logging
def handle_error(message, status_code=400):
    logging.error(message)  # Log the error message
    return jsonify({"status": "error", "message": message}), status_code

# Test route
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "success", "message": "Auth route is working!"}), 200

# Email validation function
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Password strength validation function
def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Rate Limiter setup
limiter = Limiter(app=None, key_func=get_remote_address)

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

        # Validate email format
        if not validate_email(email):
            return handle_error("Invalid email format")

        # Validate password strength
        if not validate_password_strength(password):
            return handle_error("Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.")

        # Check if user already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return handle_error("Username or email already exists")

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password before saving
        from app import db  # Import db here inside the function to avoid circular imports
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except Exception as e:
        from app import db  # Import db here inside the function to avoid circular imports
        db.session.rollback()
        return handle_error(str(e), 500)

# User Login with Rate Limiting
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 login attempts per minute
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
        from app.__init__ import db  # Import db here inside the function to avoid circular imports
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

# Logging Configuration (app/__init__.py)
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
