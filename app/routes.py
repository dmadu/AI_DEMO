from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Welcome to the API"})

@main.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()
    # Depending on how user identity is stored (id or username/email), retrieve user
    user = User.query.get(current_user_id) if hasattr(User, 'query') else None
    if not user:
        # If identity is stored as username or email
        if isinstance(current_user_id, int):
            user = User.query.get(current_user_id)
        else:
            user = User.query.filter_by(username=current_user_id).first() or User.query.filter_by(email=current_user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "message": "Welcome to your dashboard!"
        }
    }), 200
