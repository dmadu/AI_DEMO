import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError, SQLAlchemyError

db = SQLAlchemy()
migrate = Migrate()

logger = logging.getLogger(__name__)

def create_app(config_name=None):
    app = Flask(__name__)

    # Database configuration
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD', '')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'postgres')
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Centralized database connection and error handling
    @app.before_request
    def check_db_connection():
        try:
            db.session.execute(db.text('SELECT 1'))
        except (OperationalError, SQLAlchemyError) as e:
            logger.error(f"Database connection failure: {e}", exc_info=True)
            return jsonify({
                "error": "Database connection error",
                "message": "Unable to connect to the database. Please try again later."
            }), 500

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        logger.error(f"Database error occurred: {error}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "message": "An unexpected database error occurred."
        }), 500

    @app.route('/health')
    def health_check():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({"status": "healthy", "database": "connected"}), 200
        except Exception as e:
            logger.error(f"Health check failed: {e}", exc_info=True)
            return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

    return app
