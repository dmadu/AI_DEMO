from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from backend.app.models.user import User
from backend.app import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid credentials"}), 401

    username = data.get('username') or data.get('email')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Invalid credentials"}), 401

    # Support lookup by username or email depending on User model attributes
    user = User.query.filter((User.username == username) | (User.email == username)).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
