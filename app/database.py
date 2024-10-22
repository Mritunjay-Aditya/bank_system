from pymongo import MongoClient, errors
from app.config import settings

try:
    client = MongoClient(settings.MONGO_URL)
    print("Connecting to MongoDB...")
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
    
    db = client[settings.DB_NAME]
    users_collection = db["users"]
    loans_collection = db["loans"]

except errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
