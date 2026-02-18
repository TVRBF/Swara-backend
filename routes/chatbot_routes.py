from flask import Blueprint, request, jsonify
from functools import wraps
from utils.jwt_utils import decode_token

chatbot_bp = Blueprint("chatbot_bp", __name__)

# ------------------------------
# JWT Middleware
# ------------------------------
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token missing"}), 401

        token = auth_header.split(" ")[1]
        token_data = decode_token(token)

        if not token_data or token_data.get("role") != "student":
            return jsonify({"message": "Invalid token"}), 403

        request.user_id = token_data["user_id"]
        return f(*args, **kwargs)

    return decorator


# ------------------------------
# Simple AI Responses
# ------------------------------
responses = {
    "hello": "Hello! How can I help you with onboarding today?",
    "orientation": "Orientation is scheduled on the first Monday of the semester.",
    "email setup": "You can set up your college email via the Student Portal -> Email Setup section.",
    "documents": "Please upload all required documents in the Documents section of your dashboard."
}


@chatbot_bp.route("/chat", methods=["POST"])
@token_required
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()

    reply = "Sorry, I didn't understand that. Please ask something related to onboarding."

    for key in responses:
        if key in message:
            reply = responses[key]
            break

    return jsonify({"reply": reply})
