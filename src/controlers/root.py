from flask import jsonify, Response

from src.flask_app import app
from src.settings import AUTHOR_NAME, AUTHOR_EMAIL, AUTHOR_LINKEDIN

@app.route("/", methods=["GET"])
def home() -> Response:
    return jsonify({"name": AUTHOR_NAME, "email": AUTHOR_EMAIL, "linkedin": AUTHOR_LINKEDIN})
