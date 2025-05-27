"""
Configuration settings for the backend.
Loads environment variables and defines
global constants used across the application.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# === LLM Configuration ===
GIGA_MODEL = "GigaChat-Max"
BASE_URL_GIGA = "https://gigachat.devices.sberbank.ru/api/v1"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# === File Paths ===
GLOSSARY_PATH = Path(__file__).resolve().parent / "glossary.json"
CHROMA_PATH = Path(__file__).resolve().parent / "chroma_db"

# === MongoDB Configuration ===
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = "tks"
MONGO_COLLECTION = "incident_report"
