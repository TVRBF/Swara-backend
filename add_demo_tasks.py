from models.task import create_task
from bson.objectid import ObjectId

# ✅ Student ObjectId
student_id = "6995a952a69a63a287f5cc11"

# Demo tasks
demo_tasks = [
    ("Submit Documents", "Upload all admission documents"),
    ("Attend Orientation", "Join the college orientation session"),
    ("Set up College Email", "Activate your student email account"),
    ("Complete Profile", "Fill personal and academic details")
]

# Insert tasks (as ObjectId)
for title, description in demo_tasks:
    create_task(student_id, title, description, completed=False)

print(f"✅ Added {len(demo_tasks)} demo tasks for student {student_id}")
