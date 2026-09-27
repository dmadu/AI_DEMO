from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, 'description', 'Bad Request')
        if hasattr(error, 'data') and error.data:
            message = error.data.get('message', message)
        return jsonify({
            "error": "Bad Request",
            "message": str(message),
            "status_code": 400
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found",
            "status_code": 404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The method is not allowed for the requested URL",
            "status_code": 405
        }), 405

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Check if it's a standard HTTP exception
        if hasattr(e, 'code') and isinstance(e.code, int):
            status_code = e.code
            error_name = e.name if hasattr(e, 'name') else "Error"
            message = e.description if hasattr(e, 'description') else str(e)
            
            if status_code >= 500:
                logger.exception("Server error occurred: %s", str(e))
            else:
                logger.warning("Client error occurred: %s", str(e))
                
            return jsonify({
                "error": error_name,
                "message": message,
                "status_code": status_code
            }), status_code

        # Unhandled runtime or database exceptions (500)
        logger.exception("Unhandled exception occurred: %s", str(e))
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected internal server error occurred",
            "status_code": 500
        }), 500
