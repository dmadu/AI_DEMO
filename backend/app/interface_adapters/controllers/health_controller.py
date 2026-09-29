from flask import Blueprint, jsonify
from app import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "backend-api"
    }), 200
