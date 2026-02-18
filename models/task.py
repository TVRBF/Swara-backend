from pymongo import MongoClient
from config import Config
from bson.objectid import ObjectId

client = MongoClient(Config.MONGO_URI)
db = client["smart_student_onboarding"]

tasks_collection = db["tasks"]

# Create a task
def create_task(student_id, title, description, completed=False):
    task = {
        "student_id": ObjectId(student_id),
        "title": title,
        "description": description,
        "completed": completed
    }
    tasks_collection.insert_one(task)
    return task

# Get tasks for a student
def get_tasks_for_student(student_id):
    return list(tasks_collection.find({"student_id": ObjectId(student_id)}))

# Update task completion
def update_task(task_id, completed):
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"completed": completed}})
