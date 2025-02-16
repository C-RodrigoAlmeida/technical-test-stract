from flask import Flask, jsonify, Response
from src.exceptions import ExternalAPIError

def setup_error_handlers(app: Flask) -> None:
    @app.errorhandler(ExternalAPIError)
    def handle_external_api_error(error: ExternalAPIError) -> Response:
        app.logger.warning("Error while requesting %s: %s", error.endpoint, error.message)
        response = jsonify({"error": str(error)})
        response.status_code = error.status_code
        return response
