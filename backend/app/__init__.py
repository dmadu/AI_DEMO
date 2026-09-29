import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load

load()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    # Configuration
    env = config_name or os.getenv('FLASK_ENV', 'development')
    
    # Default settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql+psycopg2://postgres:postgres@localhost:5432/app_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register health check / db test route
    @app.route('/health', methods=['GET'])
    def health_check():
        try:
            # Test database connection
            db.session.execute(db.text('SELECT 1'))
            db_status = "connected"
        except Exception as e:
            db_status = f"disconnected: {str(e)}"
            
        return jsonify({
            "status": "healthy",
            "database": db_status
        }), 200 if db_status == "connected" else 500

    return app
