import logging
import requests
from typing import Any
from urllib.parse import urljoin
from collections import defaultdict
from src.schemas.pagination import Pagination
from src.exceptions import ExternalAPIError
from src.settings import API_BASE_URL, API_TOKEN

logger = logging.getLogger(__name__)
PAGINATION_PROPERTY = "pagination"


def fetch_api_once(endpoint: str, params: dict[str, str] | None = None, page: str | None = None) -> dict[str, Any]:
    """Handles external API communication"""
    headers = {"Authorization": API_TOKEN}
    full_url = urljoin(API_BASE_URL, endpoint)

    # Add the page parameter if provided
    if page is not None:
        params["page"] = page

    logger.debug("Requesting: %s", full_url)

    try:
        response = requests.get(full_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise ExternalAPIError(full_url, "External API timed out", 504)
    except requests.exceptions.ConnectionError:
        raise ExternalAPIError(full_url, "External API is unavailable", 502)
    except requests.exceptions.HTTPError:
        if 500 <= response.status_code < 600:
            raise ExternalAPIError(full_url, "Upstream API error", 502)
        else:
            raise ExternalAPIError(full_url, f"Upstream API returned {response.status_code}", response.status_code)
    except Exception as exc:
        logger.error("Unknown API exception on: %s", full_url, exc_info=exc)
        raise ExternalAPIError(full_url, "An unexpected error occurred", 500)

def fetch_api(endpoint: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """Handles external communication and pagination"""
    current_response = fetch_api_once(endpoint=endpoint, params=params)
    if PAGINATION_PROPERTY not in current_response:
        return current_response

    pagination_config = Pagination(**current_response.pop(PAGINATION_PROPERTY))
    
    response = defaultdict(list)
    response.update(current_response)

    for page in range(2, pagination_config.total + 1):
        current_response = fetch_api_once(endpoint=endpoint, params=params, page=page)
        for key in set(current_response.keys()) - {PAGINATION_PROPERTY}:
            response[key].extend(current_response[key])

    return response
