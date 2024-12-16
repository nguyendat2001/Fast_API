from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
# load_dotenv()

class Settings(BaseSettings):
    DB_CONNECTION_STRING: str = ""
    HASH_SALT: str = ""
    ROOT_PATH: str = "/content/FAST_API"

    # class Config:
    #     env_file = ".env"  # Specify the .env file location

# Initialize settings
settings = Settings()