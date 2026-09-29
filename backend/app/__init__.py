from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object('backend.app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from backend.app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app
