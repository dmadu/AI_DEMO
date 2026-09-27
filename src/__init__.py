from flask import Flask
from src.errors import register_error_handlers

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Register error handlers
    register_error_handlers(app)
    
    @app.route('/')
    def index():
        return "Hello, World!"

    @app.route('/error-500')
    def trigger_error():
        raise RuntimeError("Database connection failed")

    @app.route('/error-400')
    def trigger_validation_error():
        from werkzeug.exceptions import BadRequest
        raise BadRequest("Invalid request parameters")

    return app
