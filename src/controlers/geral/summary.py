from flask import Response, jsonify

from src.flask_app import app
from src.csv_generator import generate_csv
from src.api_endpoints import INSIGHTS, ACCOUNTS, FIELDS, PLATFORMS
from src.request_utils import fetch_api


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
        accounts_response = fetch_api(ACCOUNTS, {"platform": platform_name})

        if not accounts_response or "accounts" not in accounts_response:
            continue

        accounts = accounts_response["accounts"]
        fields_response = fetch_api(FIELDS, {"platform": platform_name})

        if not fields_response or "fields" not in fields_response:
            continue

        fields = fields_response["fields"]
        platform_field_names = [field.get("value", "") for field in fields]
        field_names.update(platform_field_names)

        if platform_name not in summary_data:
            summary_data[platform_name] = {"Platform": platform_name}

        for account in accounts:
            account_token = account["token"]
            insights_response = fetch_api(INSIGHTS, {
                "platform": platform_name,
                "account": account.get("id", ""),
                "token": account_token,
                "fields": ",".join(platform_field_names)
            })

            if not insights_response or "insights" not in insights_response:
                continue

            insights = insights_response["insights"]
            for field in platform_field_names:
                values = [float(i[field]) for i in insights if i.get(field) and str(i[field]).replace(".", "", 1).isdigit()]
                summary_data[platform_name][field] = sum(values) if values else ""

    csv_data = generate_csv(summary_data.values(), ["Platform"] + sorted(field_names))
    return Response(csv_data, mimetype="text/csv")