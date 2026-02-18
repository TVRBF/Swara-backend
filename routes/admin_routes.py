from flask import Blueprint, jsonify, request
from models.student import students_collection
from models.task import tasks_collection
from utils.jwt_utils import decode_token
from datetime import datetime
from bson.objectid import ObjectId

# Define the Blueprint with prefix
admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")

# ---------------------------
# Middleware: decode token for admin
# ---------------------------
def admin_token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token missing"}), 401
        token_data = decode_token(token)
        if not token_data or token_data.get("role") != "admin":
            return jsonify({"message": "Invalid token"}), 403
        request.admin_id = token_data["user_id"]
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

# ---------------------------
# Helper: serialize MongoDB documents
# ---------------------------
def serialize_doc(doc):
    """Convert ObjectId and datetime to strings for JSON serialization."""
    serialized = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            serialized[k] = str(v)
        elif isinstance(v, datetime):
            serialized[k] = v.isoformat()
        else:
            serialized[k] = v
    return serialized

# ---------------------------
# Get all students
# ---------------------------
@admin_bp.route("/students", methods=["GET"])
@admin_token_required
def get_students():
    students = list(students_collection.find({}, {"password": 0}))
    serialized_students = [serialize_doc(s) for s in students]
    return jsonify({"students": serialized_students})

# ---------------------------
# Analytics: task completion stats
# ---------------------------
@admin_bp.route("/analytics", methods=["GET"])
@admin_token_required
def get_analytics():
    # Total students
    total_students = students_collection.count_documents({})

    # Completed tasks
    completed_tasks = tasks_collection.count_documents({"completed": True})

    # Total tasks
    total_tasks = tasks_collection.count_documents({})

    # Average completion %
    avg_completion = round((completed_tasks / total_tasks * 100), 2) if total_tasks else 0

    # Recent students (latest 5 by creation date)
    recent_students_cursor = students_collection.find({}, {"password": 0}).sort("created_at", -1).limit(5)
    recent_students = [serialize_doc(s) for s in recent_students_cursor]

    return jsonify({
        "total_students": total_students,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "avg_completion": avg_completion,
        "recent_students": recent_students
    })
