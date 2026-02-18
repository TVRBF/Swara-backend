import os
from flask import Flask
from flask_cors import CORS
from config import Config

# Import all blueprints
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from routes.chatbot_routes import chatbot_bp
from routes.reminder_routes import reminder_bp

from pymongo import MongoClient

# -----------------------------
# Initialize Flask app
# -----------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# -----------------------------
# Setup MongoDB client
# -----------------------------
try:
    client = MongoClient(
        Config.MONGO_URI,
        tls=True,  # Force TLS/SSL
        serverSelectionTimeoutMS=10000  # 10 seconds timeout
    )
    # Test connection
    client.admin.command("ping")
    print("✅ Successfully connected to MongoDB")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise e

# Optional: you can access your default DB like this
db = client.get_database()  # Defaults to database in URI

# -----------------------------
# Register blueprints
# -----------------------------
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(chatbot_bp, url_prefix="/api/student")
app.register_blueprint(reminder_bp, url_prefix="/api/reminders")

# -----------------------------
# Root endpoint
# -----------------------------
@app.route("/")
def home():
    return "Smart Student Onboarding API is running!"

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
