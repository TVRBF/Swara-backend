from flask import Blueprint, request, jsonify
from models.student import create_student, find_student_by_email, find_student_by_email_with_password, get_all_students, students_collection
from models.admin import create_admin, find_admin_by_email
from models.task import tasks_collection
from utils.password_utils import verify_password
from utils.jwt_utils import generate_token
from datetime import datetime

# Define the Blueprint
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

# ---------------------------
# Student signup
# ---------------------------
@auth_bp.route("/signup/student", methods=["POST"])
def student_signup():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data or "name" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    if find_student_by_email(data["email"]):
        return jsonify({"message": "Email already exists"}), 400

    student = create_student(data["name"], data["email"], data["password"])
    token = generate_token(str(student.get("_id", "")), student["role"])
    return jsonify({"message": "Student created", "token": token}), 201

# ---------------------------
# Admin signup
# ---------------------------
@auth_bp.route("/signup/admin", methods=["POST"])
def admin_signup():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data or "name" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    if find_admin_by_email(data["email"]):
        return jsonify({"message": "Email already exists"}), 400

    admin = create_admin(data["name"], data["email"], data["password"])
    token = generate_token(str(admin.get("_id", "")), admin["role"])
    return jsonify({"message": "Admin created", "token": token}), 201

# ---------------------------
# Login (student/admin)
# ---------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    user = find_student_by_email_with_password(data["email"]) or find_admin_by_email(data["email"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not verify_password(data["password"], user["password"]):
        return jsonify({"message": "Incorrect password"}), 401

    token = generate_token(str(user["_id"]), user["role"])
    return jsonify({"message": f"{user['role'].capitalize()} logged in", "token": token}), 200

# ---------------------------
# List all students (for admin)
# ---------------------------
@auth_bp.route("/students", methods=["GET"])
def list_students():
    students = get_all_students()
    return jsonify(students), 200

# ---------------------------
# Admin dashboard analytics
# ---------------------------
@auth_bp.route("/dashboard", methods=["GET"])
def admin_dashboard():
    # Total students
    total_students = students_collection.count_documents({})

    # Tasks completed
    tasks_completed = tasks_collection.count_documents({"completed": True})

    # Average completion %
    total_tasks = tasks_collection.count_documents({})
    avg_completion = round((tasks_completed / total_tasks * 100), 2) if total_tasks > 0 else 0

    # Recent students (latest 5 by creation date)
    recent_students_cursor = students_collection.find({}, {"password": 0}).sort("created_at", -1).limit(5)
    recent_students = []
    for s in recent_students_cursor:
        s["_id"] = str(s["_id"])  # convert ObjectId to string for JSON
        recent_students.append(s)

    return jsonify({
        "total_students": total_students,
        "tasks_completed": tasks_completed,
        "avg_completion": avg_completion,
        "recent_students": recent_students
    }), 200
