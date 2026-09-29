import os
from flask import Flask
from dotenv import load_dotenv
from src.extensions import db, migrate, bcrypt, jwt

load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://postgres:postgres@localhost:5432/postgres'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY',
        'fallback-jwt-secret-key'
    )

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'database': 'configured'},

    return app
