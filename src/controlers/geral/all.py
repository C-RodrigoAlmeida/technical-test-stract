from flask import Response, jsonify

from src.flask_app import app
from src.csv_generator import generate_csv
from src.data_fetchers import get_accounts, get_fields, get_insights
from src.request_utils import fetch_api
from src.api_endpoints import PLATFORMS


@app.route("/geral", methods=["GET"])
def get_all_ads() -> Response:
    """Retorna todos os anúncios de todas as plataformas."""
    platforms = fetch_api(PLATFORMS)
    if not platforms or "platforms" not in platforms:
        return jsonify({"error": "Falha ao obter plataformas"}), 500

    all_ads = []
    all_fields = set()

    for platform in platforms["platforms"]:
        platform_name = platform.get("value", "Unknown")
        accounts = get_accounts(platform_name)
        fields = get_fields(platform_name)
        field_names = [field.value for field in fields]
        all_fields.update(field_names)

        for account in accounts:
            insights = get_insights(platform_name, account.id, account.token, field_names)

            for insight in insights:
                insight.data["Platform"] = platform_name
                insight.data["Account Name"] = account.name
                if platform_name == "ga4" and "spend" in insight.data and "clicks" in insight.data:
                    insight.data["cost_per_click"] = round(float(insight.data["spend"]) / float(insight.data["clicks"]), 2) if float(insight.data["clicks"]) > 0 else ""
                all_ads.append(insight.data)

    csv_data = generate_csv(all_ads, ["Platform", "Account Name"] + sorted(all_fields))
    return Response(csv_data, mimetype="text/csv")
