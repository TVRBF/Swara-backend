from flask import Blueprint, request, jsonify
from flask_cors import CORS
from models.task import get_tasks_for_student, update_task
from utils.jwt_utils import decode_token

student_bp = Blueprint("student_bp", __name__)
CORS(student_bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Middleware: decode token
def token_required(f):
    def decorator(*args, **kwargs):
        # Skip auth for preflight requests
        if request.method == "OPTIONS":
            return f(*args, **kwargs)

        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token missing"}), 401
        token_data = decode_token(token)
        if not token_data or token_data["role"] != "student":
            return jsonify({"message": "Invalid token"}), 403
        request.user_id = token_data["user_id"]
        return f(*args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator

# Get student tasks
@student_bp.route("/tasks", methods=["GET", "OPTIONS"])
@token_required
def get_tasks():
    if request.method == "OPTIONS":
        return jsonify({}), 200  # preflight response
    tasks = get_tasks_for_student(request.user_id)
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["student_id"] = str(task["student_id"])
    return jsonify({"tasks": tasks})

# Update task completion
@student_bp.route("/tasks/<task_id>", methods=["PUT", "OPTIONS"])
@token_required
def complete_task(task_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200  # preflight response
    data = request.json
    update_task(task_id, data.get("completed", False))
    return jsonify({"message": "Task updated"})
