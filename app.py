from flask import Flask
from flask_cors import CORS
from config import Config
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from routes.chatbot_routes import chatbot_bp
from routes.reminder_routes import reminder_bp   # ✅ ADD THIS

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(chatbot_bp, url_prefix="/api/student")
app.register_blueprint(reminder_bp, url_prefix="/api/reminders")   # ✅ ADD THIS

# Root endpoint
@app.route("/")
def home():
    return "Smart Student Onboarding API is running!"

if __name__ == "__main__":
    app.run(debug=True)
