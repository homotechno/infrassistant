"""
Authentication module for obtaining access tokens for GigaChat API.
"""

import base64
import uuid
import requests
from backend.config import CLIENT_ID, CLIENT_SECRET


def get_access_token() -> str:
    """
    Fetches an access token from Sber OAuth server using client credentials.

    Returns:
        str: Access token for authenticating GigaChat API requests.

    Raises:
        requests.HTTPError: If the token request fails.
    """
    # Encode client credentials in base64
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_b64}",
        "RqUID": str(uuid.uuid4()),  # Unique request ID
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "scope": "GIGACHAT_API_PERS"
    }

    response = requests.post(
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
        headers=headers,
        data=data,
        verify=False  # WARNING: for production use, enable verification
    )

    response.raise_for_status()
    return response.json()["access_token"]
