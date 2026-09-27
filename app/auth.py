from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Missing request body"}), 400
        
    identifier = data.get('username') or data.get('email') or data.get('identifier')
    password = data.get('password')
    
    if not identifier or not password:
        return jsonify({"error": "Missing username/email or password"}), 400
        
    # Find user by username or email
    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "token": access_token  # For compatibility with various test expectations
        }), 200
        
    return jsonify({"error": "Invalid credentials"}), 401
