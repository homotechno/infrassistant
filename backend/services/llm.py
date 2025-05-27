"""
LLM communication module for interacting with the GigaChat API.
Handles request construction and asynchronous calls to the model endpoint.
"""

import aiohttp
import ssl
from backend.utils.auth import get_access_token
from backend.config import GIGA_MODEL, BASE_URL_GIGA

# Disable SSL verification (only for internal/self-signed certs)
ssl_context = ssl._create_unverified_context()


async def call_gigachat(messages: list[dict]) -> str:
    """
    Sends a list of messages to the GigaChat API and returns the model's response.

    Args:
        messages (list of dict): Dialog context formatted for the API (role: system/user, content: str).

    Returns:
        str: Model-generated response text.
    """
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": GIGA_MODEL,
        "messages": messages,
        "temperature": 0,
        "repetition_penalty": 1.1,
        "stream": False,
        "update_interval": 0
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BASE_URL_GIGA}/chat/completions",
            json=payload,
            headers=headers,
            ssl=ssl_context
        ) as response:
            response.raise_for_status()
            result = await response.json()
            return result["choices"][0]["message"]["content"].strip()
