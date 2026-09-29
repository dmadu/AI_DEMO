from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON body required"}), 400

    identifier = data.get('identifier') or data.get('username') or data.get('email')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"error": "Missing identifier (username or email) or password"}), 400

    # Query user by username or email
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401

@api_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"logged_in_as": user.username}), 200
