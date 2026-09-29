import re
from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

EMAIL_REGEX = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one numeric digit."
    if not re.search(r'[^A-Za-z0-9]', password):
        return "Password must contain at least one special character."
    return None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload or missing Content-Type application/json."}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields: username, email, and password are required."}), 400

    # Validate email format
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format."}), 400

    # Validate password complexity
    pwd_error = validate_password(password)
    if pwd_error:
        return jsonify({"error": pwd_error}), 400

    # Check existing user or email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken."}), 409

    # Hash password and save
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred."}), 500

    return jsonify({
        "message": "User registered successfully.",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }), 201
