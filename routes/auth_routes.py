from flask import Blueprint, request, jsonify
from models.student import (
    create_student,
    find_student_by_email,
    find_student_by_email_with_password,
    get_all_students,
    students_collection,
)
from models.admin import create_admin, find_admin_by_email
from models.task import tasks_collection
from utils.password_utils import verify_password
from utils.jwt_utils import generate_token
from datetime import datetime
import traceback

# Define the Blueprint
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

# ---------------------------
# Student signup
# ---------------------------
@auth_bp.route("/signup/student", methods=["POST"])
def student_signup():
    try:
        print("Student signup route hit")
        data = request.get_json()
        print("Request data:", data)

        if not data:
            return jsonify({"message": "Missing request body"}), 400
        if "name" not in data or "email" not in data or "password" not in data:
            return jsonify({"message": "Missing required fields"}), 400

        if find_student_by_email(data["email"]):
            return jsonify({"message": "Email already exists"}), 400

        student = create_student(data["name"], data["email"], data["password"])
        token = generate_token(str(student.get("_id", "")), student.get("role", "student"))

        print("Student created successfully:", student.get("_id"))
        return jsonify({"message": "Student created", "token": token}), 201

    except Exception as e:
        print("Student Signup Exception:")
        traceback.print_exc()
        return jsonify({"message": "Student signup failed", "error": str(e)}), 500

# ---------------------------
# Admin signup
# ---------------------------
@auth_bp.route("/signup/admin", methods=["POST"])
def admin_signup():
    try:
        print("Admin signup route hit")
        data = request.get_json()
        print("Request data:", data)

        if not data:
            return jsonify({"message": "Missing request body"}), 400
        if "name" not in data or "email" not in data or "password" not in data:
            return jsonify({"message": "Missing required fields"}), 400

        if find_admin_by_email(data["email"]):
            return jsonify({"message": "Email already exists"}), 400

        admin = create_admin(data["name"], data["email"], data["password"])
        token = generate_token(str(admin.get("_id", "")), admin.get("role", "admin"))

        print("Admin created successfully:", admin.get("_id"))
        return jsonify({"message": "Admin created", "token": token}), 201

    except Exception as e:
        print("Admin Signup Exception:")
        traceback.print_exc()
        return jsonify({"message": "Admin signup failed", "error": str(e)}), 500

# ---------------------------
# Login (student/admin)
# ---------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        print("Login route hit")
        data = request.get_json()
        print("Request data:", data)

        if not data:
            return jsonify({"message": "Missing request body"}), 400
        if "email" not in data or "password" not in data:
            return jsonify({"message": "Missing required fields"}), 400

        email = data["email"]
        password = data["password"]

        print("Looking up user by email:", email)
        user = find_student_by_email_with_password(email)
        user_type = "student"
        if not user:
            user = find_admin_by_email(email)
            user_type = "admin"

        if not user:
            print("User not found")
            return jsonify({"message": "User not found"}), 404

        if "password" not in user or not user["password"]:
            print("User has no password")
            return jsonify({"message": "User has no password set"}), 500

        if not verify_password(password, user["password"]):
            print("Incorrect password")
            return jsonify({"message": "Incorrect password"}), 401

        role = user.get("role", user_type)
        token = generate_token(str(user["_id"]), role)

        print(f"{role} logged in successfully:", user["_id"])
        return jsonify({"message": f"{role.capitalize()} logged in", "token": token}), 200

    except Exception as e:
        print("Login Exception:")
        traceback.print_exc()
        return jsonify({"message": "Login failed", "error": str(e)}), 500

# ---------------------------
# List all students (admin)
# ---------------------------
@auth_bp.route("/students", methods=["GET"])
def list_students():
    try:
        print("List students route hit")
        students = get_all_students()
        print("Number of students found:", len(students))
        return jsonify(students), 200
    except Exception as e:
        print("List Students Exception:")
        traceback.print_exc()
        return jsonify({"message": "Failed to fetch students", "error": str(e)}), 500

# ---------------------------
# Admin dashboard analytics
# ---------------------------
@auth_bp.route("/dashboard", methods=["GET"])
def admin_dashboard():
    try:
        print("Admin dashboard route hit")
        total_students = students_collection.count_documents({})
        tasks_completed = tasks_collection.count_documents({"completed": True})
        total_tasks = tasks_collection.count_documents({})
        avg_completion = round((tasks_completed / total_tasks * 100), 2) if total_tasks > 0 else 0

        recent_students_cursor = students_collection.find({}, {"password": 0}).sort("created_at", -1).limit(5)
        recent_students = []
        for s in recent_students_cursor:
            s["_id"] = str(s["_id"])
            recent_students.append(s)

        print("Dashboard data prepared")
        return jsonify({
            "total_students": total_students,
            "tasks_completed": tasks_completed,
            "avg_completion": avg_completion,
            "recent_students": recent_students
        }), 200

    except Exception as e:
        print("Dashboard Exception:")
        traceback.print_exc()
        return jsonify({"message": "Failed to fetch dashboard data", "error": str(e)}), 500
