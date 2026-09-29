from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Missing request body"}), 400
        
    identifier = data.get('username') or data.get('email')
    password = data.get('password')
    
    if not identifier or not password:
        return jsonify({"error": "Username/email and password are required"}), 400
        
    # Query user by username or email
    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "message": "Login successful"
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
