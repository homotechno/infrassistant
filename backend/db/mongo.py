"""
MongoDB client initialization for storing and retrieving incident reports.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

# Initialize asynchronous MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Access the target database and collection
database = client[MONGO_DB]
incident_collection = database[MONGO_COLLECTION]
