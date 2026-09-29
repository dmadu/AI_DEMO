import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    # Configuration loading
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/app_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.interface_adapters.controllers.health_controller import health_bp
    app.register_blueprint(health_bp, url_prefix='/api/v1')

    # Centralized Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": str(error.description) if hasattr(error, 'description') else "Bad request"
            }
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested resource was not found."
            }
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": {
                "code": "METHOD_NOT_ALLOWED",
                "message": "The method is not allowed for the requested URL."
            }
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred."
            }
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Handle custom or generic exceptions
        code = getattr(error, 'code', 500)
        message = getattr(error, 'message', str(error))
        
        if code == 500:
            message = "An internal server error occurred."

        return jsonify({
            "error": {
                "code": getattr(error, 'name', 'INTERNAL_SERVER_ERROR'),
                "message": message
            }
        }), code

    return app
