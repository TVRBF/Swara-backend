from flask import Blueprint, request, jsonify
from functools import wraps
from utils.jwt_utils import decode_token
from models.reminder import create_reminder, get_reminders, update_reminder

reminder_bp = Blueprint("reminder_bp", __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token missing"}), 401

        token = auth_header.split(" ")[1]
        token_data = decode_token(token)

        if not token_data:
            return jsonify({"message": "Invalid token"}), 403

        request.user_id = token_data["user_id"]
        return f(*args, **kwargs)

    return decorator


# Create reminder
@reminder_bp.route("/", methods=["POST"])
@token_required
def add_reminder():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    reminder = create_reminder(
        request.user_id,
        title,
        description,
        due_date
    )

    return jsonify(reminder), 201


# Get reminders
@reminder_bp.route("/", methods=["GET"])
@token_required
def fetch_reminders():
    reminders = get_reminders(request.user_id)
    return jsonify(reminders)


# Update completion
@reminder_bp.route("/<reminder_id>", methods=["PUT"])
@token_required
def mark_complete(reminder_id):
    data = request.get_json()
    completed = data.get("completed", True)

    update_reminder(reminder_id, completed)
    return jsonify({"message": "Reminder updated"})
