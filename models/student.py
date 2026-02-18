from pymongo import MongoClient
from datetime import datetime
from config import Config
from utils.password_utils import hash_password

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client["smart_student_onboarding"]
students_collection = db["students"]

# ---------------------------
# Create a new student
# ---------------------------
def create_student(name, email, password):
    """Create a new student and insert into MongoDB."""
    student = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": "student",
        "created_at": datetime.utcnow()
    }
    students_collection.insert_one(student)
    
    # Exclude password before returning
    student_copy = student.copy()
    student_copy.pop("password")
    return student_copy

# ---------------------------
# Find a student by email for public use (no password)
# ---------------------------
def find_student_by_email(email):
    """Return a student document by email, excluding password."""
    student = students_collection.find_one({"email": email})
    if student:
        student.pop("password", None)
    return student

# ---------------------------
# Find a student by email for login (includes password)
# ---------------------------
def find_student_by_email_with_password(email):
    """Return a student document by email, including password for login."""
    return students_collection.find_one({"email": email})

# ---------------------------
# Get all students
# ---------------------------
def get_all_students():
    """Return a list of all students, excluding passwords and Mongo _id."""
    students_cursor = students_collection.find({}, {"_id": 0, "password": 0})
    return list(students_cursor)
