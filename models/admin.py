from pymongo import MongoClient
from config import Config
from utils.password_utils import hash_password

client = MongoClient(Config.MONGO_URI)
db = client["smart_student_onboarding"]

admins_collection = db["admins"]

# Create a new admin
def create_admin(name, email, password):
    admin = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": "admin",
        "created_at": None
    }
    admins_collection.insert_one(admin)
    return admin

# Find admin by email
def find_admin_by_email(email):
    return admins_collection.find_one({"email": email})
