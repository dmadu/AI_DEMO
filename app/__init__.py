from flask import Flask
from app.extensions import db, pcrypt
from app.routes import api_bp

def create_app(config_name=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    db.init_app(app)
    pcrypt.init_app(app)

    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
