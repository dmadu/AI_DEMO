from flask import Blueprint

bp = Blueprint("api", __name__)

@bp.route("/", methods=["GET"])
def index():
    return {"message": "Welcome to the Flask Clean Architecture API"}, 200
