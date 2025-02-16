from src.request_utils import fetch_api
from src.api_endpoints import ACCOUNTS, FIELDS, INSIGHTS
from src.schemas import Account, Field, Insight

def get_accounts(platform: str) -> list[Account]:
    accounts_response = fetch_api(ACCOUNTS, {"platform": platform})
    accounts_data = accounts_response.get("accounts", []) if isinstance(accounts_response, dict) else []
    return [Account(**account) for account in accounts_data]

def get_fields(platform: str) -> list[Field]:
    fields_response = fetch_api(FIELDS, {"platform": platform})
    fields_data = fields_response.get("fields", []) if isinstance(fields_response, dict) else []
    return [Field(value=field_data.get("value", "")) for field_data in fields_data]

def get_insights(platform: str, account_id: str, account_token: str, field_names: list[str]) -> list[Insight]:
    insights_response = fetch_api(INSIGHTS, {
        "platform": platform,
        "account": account_id,
        "token": account_token,
        "fields": ",".join(field_names)
    })
    insights_data = insights_response.get("insights", []) if isinstance(insights_response, dict) else []
    return [Insight(account_name="", platform=platform, data=insight) for insight in insights_data]