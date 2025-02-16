from flask import Response, jsonify

from src.flask_app import app
from src.csv_generator import generate_csv
from src.api_endpoints import INSIGHTS, ACCOUNTS, FIELDS, PLATFORMS
from src.request_utils import fetch_api


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
        accounts_response = fetch_api(ACCOUNTS, {"platform": platform_name})
        if not accounts_response or "accounts" not in accounts_response:
            continue

        accounts = accounts_response["accounts"]
        fields_response = fetch_api(FIELDS, {"platform": platform_name})
        if not fields_response or "fields" not in fields_response:
            continue

        fields = fields_response["fields"]
        field_names = [field.get("value", "") for field in fields]
        all_fields.update(field_names)

        for account in accounts:
            account_token = account["token"]
            insights_response = fetch_api(INSIGHTS, {
                "platform": platform_name,
                "account": account.get("id", ""),
                "token": account_token,
                "fields": ",".join(field_names)
            })

            if not insights_response or "insights" not in insights_response:
                continue

            for insight in insights_response["insights"]:
                insight["Platform"] = platform_name
                insight["Account Name"] = account["name"]
                if platform_name == "ga4" and "spend" in insight and "clicks" in insight:
                    insight["cost_per_click"] = round(float(insight["spend"]) / float(insight["clicks"]), 2) if float(insight["clicks"]) > 0 else ""
                all_ads.append(insight)

    csv_data = generate_csv(all_ads, ["Platform", "Account Name"] + sorted(all_fields))
    return Response(csv_data, mimetype="text/csv")
