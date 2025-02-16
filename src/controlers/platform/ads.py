from flask import Response

from src.flask_app import app
from src.csv_generator import generate_csv
from src.data_fetchers import get_accounts, get_fields, get_insights


@app.route("/<platform>", methods=["GET"])
def get_ads_by_platform(platform: str) -> Response:
    """Returns a specific plataform ads in a csv file"""
    accounts = get_accounts(platform)
    fields = get_fields(platform)
    field_names = [field.value for field in fields]
    
    ads_data = []
    for account in accounts:
        insights = get_insights(platform, account.id, account.token, field_names)
        
        for insight in insights:
            insight.data["Account Name"] = account.name
            insight.data["Platform"] = platform
            ads_data.append(insight.data)
    
    csv_data = generate_csv(ads_data, ["Platform", "Account Name"] + field_names)
    return Response(csv_data, mimetype="text/csv")
