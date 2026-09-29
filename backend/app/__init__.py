import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load

load()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    # Configuration
    database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}, 200

    return app
