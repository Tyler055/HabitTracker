from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.__init__ import db
from models.models import User

user_bp = Blueprint('user_bp', __name__)

# Route to register a user
@user_bp.route('/register', methods=['POST'])
def register_user():
    # Get data from request
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if all fields are provided
    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    
    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(password, method='sha256')

        # Create the new user
        new_user = User(username=username, email=email, password=hashed_password)
        
        # Add to database and commit
        db.session.add(new_user)
        db.session.commit()

        # Return a successful response with user details (excluding password)
        return jsonify({
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }), 201

    except Exception as e:
        # Return an error if something goes wrong
        return jsonify({"error": str(e)}), 500
