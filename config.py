import os
from dotenv import load_dotenv

# Load .env only if running locally
if os.environ.get("FLASK_ENV") != "production":
    load_dotenv()  # This allows you to use .env locally

class Config:
    # Read environment variables
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MONGO_URI = os.environ.get("MONGO_URI")

    # Optional: add debug flag
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

    # Ensure mandatory variables are set
    if not SECRET_KEY:
        raise Exception("SECRET_KEY is not set in environment variables!")
    if not MONGO_URI:
        raise Exception("MONGO_URI is not set in environment variables!")

