from flask import Blueprint, request, jsonify
from app.middleware.auth.auth_manager import (
    register_user, login_user, logout_user, 
    request_password_reset, reset_password
)

# Define the Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# User registration route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

# User login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

# User logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return logout_user()

# Password reset request route
@auth_bp.route('/request-password-reset', methods=['POST'])
def request_reset():
    data = request.get_json()
    return request_password_reset(data)

# Password reset route
@auth_bp.route('/reset-password', methods=['POST'])
def reset():
    data = request.get_json()
    return reset_password(data)
