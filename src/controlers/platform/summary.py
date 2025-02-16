from flask import Response

from src.flask_app import app
from src.csv_generator import generate_csv
from src.api_endpoints import INSIGHTS, ACCOUNTS, FIELDS
from src.request_utils import fetch_api

@app.route("/<platform>/resumo", methods=["GET"])
def get_summary_by_platform(platform: str) -> Response:
    """Retorna um resumo agregado dos anúncios por conta dentro da plataforma."""
    accounts_response = fetch_api(ACCOUNTS, {"platform": platform})
    accounts = accounts_response.get("accounts", []) if isinstance(accounts_response, dict) else []
    fields_response = fetch_api(FIELDS, {"platform": platform})
    fields = fields_response.get("fields", []) if isinstance(fields_response, dict) else []
    field_names = [field.get("value", "") for field in fields]
    
    summary_data = {}
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
        
        if account_name not in summary_data:
            summary_data[account_name] = {"Platform": platform, "Account Name": account_name}
        
        for field in field_names:
            values = [float(i[field]) for i in insights if i.get(field) and str(i[field]).replace(".", "", 1).isdigit()]
            summary_data[account_name][field] = sum(values) if values else ""
    
    csv_data = generate_csv(summary_data.values(), ["Platform", "Account Name"] + field_names)
    return Response(csv_data, mimetype="text/csv")
