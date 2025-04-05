from flask import Blueprint, request, jsonify
from app import db
from models.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.utils import hash_password, verify_password

# Define the Blueprint with a prefix for better organization
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "User already exists"}), 400

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "data": {"id": new_user.id, "username": new_user.username}
    }), 201


# Login and generate JWT
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "access_token": access_token
    }), 200


# Get current logged-in user's info
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    return jsonify({
        "status": "success",
        "data": {"id": user.id, "username": user.username}
    }), 200
