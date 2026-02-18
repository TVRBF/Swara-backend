import json
import os
import sys

# Add the backend folder to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from app import app
from models.task import Task
from flask_sqlalchemy import SQLAlchemy

# Initialize db
db = SQLAlchemy(app)

# Path to your JSON seed file
SEED_FILE = os.path.join(os.path.dirname(__file__), 'tasks_seed.json')

def seed_tasks():
    with app.app_context():
        # Load tasks from JSON
        with open(SEED_FILE, 'r') as f:
            tasks_data = json.load(f)

        # Insert tasks into database
        for t in tasks_data:
            task = Task(
                title=t['title'],
                description=t['description'],
                deadline=t['deadline'],
                assigned_to=t['assigned_to'],
                completed=t['completed']
            )
            db.session.add(task)

        db.session.commit()
        print(f"Seeded {len(tasks_data)} tasks successfully!")

if __name__ == "__main__":
    seed_tasks()
