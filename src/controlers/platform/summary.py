from flask import Response

from src.flask_app import app
from src.csv_generator import generate_csv
from src.data_fetchers import get_accounts, get_fields, get_insights

@app.route("/<platform>/resumo", methods=["GET"])
def get_summary_by_platform(platform: str) -> Response:
    """Returns a agragated resume of ads by accounts for each platform."""
    accounts = get_accounts(platform)
    fields = get_fields(platform)
    field_names = [field.value for field in fields]
    
    summary_data = {}
    for account in accounts:
        insights = get_insights(platform, account.id, account.token, field_names)
        
        if account.name not in summary_data:
            summary_data[account.name] = {"Platform": platform, "Account Name": account.name}
        
        for field in field_names:
            values = [float(insight.data[field]) for insight in insights if insight.data.get(field) and str(insight.data[field]).replace(".", "", 1).isdigit()]
            summary_data[account.name][field] = sum(values) if values else ""
    
    csv_data = generate_csv(summary_data.values(), ["Platform", "Account Name"] + field_names)
    return Response(csv_data, mimetype="text/csv")
