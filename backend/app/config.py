import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "smart-compliance-backend"
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    ENV: str = os.getenv("ENV", "development")

settings = Settings()
