from pymongo import MongoClient, errors
from app.config import settings

try:
    # Initialize MongoDB client
    client = MongoClient(settings.MONGO_URL)
    
    # Test connection
    print("Connecting to MongoDB...")
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
    
    # Access the database
    db = client[settings.DB_NAME]

    # Define collections
    users_collection = db["users"]
    loans_collection = db["loans"]

except errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
