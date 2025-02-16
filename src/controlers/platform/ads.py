from flask import Response

from src.flask_app import app
from src.csv_generator import generate_csv
from src.api_endpoints import INSIGHTS, ACCOUNTS, FIELDS
from src.request_utils import fetch_api


@app.route("/<platform>", methods=["GET"])
def get_ads_by_platform(platform: str) -> Response:
    """Retorna os anúncios de uma plataforma específica em formato CSV."""
    accounts_response = fetch_api(ACCOUNTS, {"platform": platform})
    accounts = accounts_response.get("accounts", []) if isinstance(accounts_response, dict) else []
    fields_response = fetch_api(FIELDS, {"platform": platform})
    fields = fields_response.get("fields", []) if isinstance(fields_response, dict) else []
    field_names = [field.get("value", "") for field in fields]
    
    ads_data = []
    for account in accounts:
        account_name = account["name"]
        account_token = account["token"]
        insights_response = fetch_api(INSIGHTS, {
            "platform": platform,
            "account": account["id"],
            "token": account_token,
            "fields": ",".join(field_names)
        })
        insights = insights_response.get("insights", []) if isinstance(insights_response, dict) else []
        
        for insight in insights:
            insight["Account Name"] = account_name
            insight["Platform"] = platform
            ads_data.append(insight)
    
    csv_data = generate_csv(ads_data, ["Platform", "Account Name"] + field_names)
    return Response(csv_data, mimetype="text/csv")
