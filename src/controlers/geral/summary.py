from flask import Response, jsonify

from src.flask_app import app
from src.csv_generator import generate_csv
from src.data_fetchers import get_accounts, get_fields, get_insights
from src.request_utils import fetch_api
from src.api_endpoints import PLATFORMS

@app.route("/geral/resumo", methods=["GET"])
def get_general_summary() -> Response:
    """Retorna um resumo agregado dos anúncios por plataforma."""
    response = fetch_api(PLATFORMS)
    if not response or "platforms" not in response:
        return jsonify({"error": "Falha ao obter plataformas"}), 500

    platforms = response["platforms"]
    summary_data = {}
    field_names = set()

    for platform in platforms:
        platform_name = platform.get("value", "Unknown")
        accounts = get_accounts(platform_name)
        fields = get_fields(platform_name)
        platform_field_names = [field.value for field in fields]
        field_names.update(platform_field_names)

        if platform_name not in summary_data:
            summary_data[platform_name] = {"Platform": platform_name}

        for account in accounts:
            insights = get_insights(platform_name, account.id, account.token, platform_field_names)

            for field in platform_field_names:
                values = [float(insight.data[field]) for insight in insights if insight.data.get(field) and str(insight.data[field]).replace(".", "", 1).isdigit()]
                summary_data[platform_name][field] = sum(values) if values else ""

    csv_data = generate_csv(summary_data.values(), ["Platform"] + sorted(field_names))
    return Response(csv_data, mimetype="text/csv")