import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MONGO_URL: str = os.getenv("MONGO_URL")
    DB_NAME: str = os.getenv("DB_NAME")

settings = Settings()
