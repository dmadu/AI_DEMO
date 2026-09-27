import os
from flask import Flask
from src.config import config
from src.extensions import db, migrate, bcrypt

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app
