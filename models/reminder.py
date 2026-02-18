from pymongo import MongoClient
from config import Config
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient(Config.MONGO_URI)
db = client["smart_student_onboarding"]

reminders_collection = db["reminders"]

def create_reminder(student_id, title, description, due_date):
    reminder = {
        "student_id": ObjectId(student_id),
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.utcnow()
    }
    result = reminders_collection.insert_one(reminder)
    reminder["_id"] = str(result.inserted_id)
    reminder["student_id"] = str(student_id)
    return reminder

def get_reminders(student_id):
    reminders = reminders_collection.find({"student_id": ObjectId(student_id)})
    result = []
    for r in reminders:
        r["_id"] = str(r["_id"])
        r["student_id"] = str(r["student_id"])
        result.append(r)
    return result

def update_reminder(reminder_id, completed):
    reminders_collection.update_one(
        {"_id": ObjectId(reminder_id)},
        {"$set": {"completed": completed}}
    )
