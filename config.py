import os
from dotenv import load_dotenv

# Load environment variables from .env only if not in production
if os.environ.get("FLASK_ENV") != "production":
    load_dotenv()

class Config:
    # Mandatory environment variables
    SECRET_KEY = os.environ.get("JWT_Secret")
    MONGO_URI = os.environ.get("MONGO_URI")

    # Optional debug flag
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

    # Ensure required variables are set
    if not SECRET_KEY:
        raise Exception("SECRET_KEY (JWT_Secret) is not set in environment variables!")
    if not MONGO_URI:
        raise Exception("MONGO_URI is not set in environment variables!")
