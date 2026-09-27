from flask import Flask
from src.extensions import db, bcrypt
from src.routes import api_bp

def create_app(config_name=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/app_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
