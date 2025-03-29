from flask import Blueprint, request, jsonify
from app import db
from models.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.utils import hash_password, verify_password  # Assuming hash_password and verify_password are utilities in 'utils'

# Create a Blueprint for auth routes
auth_bp = Blueprint('auth_bp', __name__)

# Route to register a new user
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "User already exists"}), 400

    # Hash the password before saving
    hashed_password = hash_password(password)

    new_user = User(username=username, password=hashed_password)  # Save the hashed password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "data": {"id": new_user.id, "username": new_user.username}
    }), 201

# Route to login and get a JWT token
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400
    
    user = User.query.filter_by(username=username).first()

    if not user or not verify_password(password, user.password):  # Verify password with hashed value
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    # Generate JWT token if authentication is successful
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "access_token": access_token
    }), 200

# Route to get the current user's information (Protected route)
@auth_bp.route('/api/me', methods=['GET'])
@jwt_required()  # This protects the route, requiring a valid JWT
def me():
    current_user_id = get_jwt_identity()  # Get the user ID from the JWT
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    return jsonify({
        "status": "success",
        "data": {"id": user.id, "username": user.username}
    })
