from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/dashboard', methods=['GET'])
@jwt_required()
public def dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        # Fallback if identity is stored differently (e.g., username or email dictionary/string)
        if isinstance(current_user_id, dict):
            user_email = current_user_id.get('email') or current_user_id.get('sub')
            user = User.query.filter_by(email=user_email).first() if user_email else None
        else:
            user = User.query.filter_by(email=current_user_id).first() or User.query.filter_by(username=current_user_id).first()

    if not user:
        return jsonify({
            "message": "Welcome to your dashboard!",
            "user": {
                "identity": current_user_id
            }
        }), 200

    return jsonify({
        "message": "Welcome to your dashboard!",
        "user": {
            "id": getattr(user, 'id', None),
            "username": getattr(user, 'username', None),
            "email": getattr(user, 'email', None)
        }
    }), 200
