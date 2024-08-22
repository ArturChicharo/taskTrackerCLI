import os
import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--add", help="Type task description in quotation marks", required=False)

args = parser.parse_args()

file_path = "taskTrackerJSON.json"

# Formatting time to dd-mm-yy HH:MM
current_time = datetime.now()
formatted_time = current_time.strftime('%H:%M %d %B %Y')

def addTask():
    tasks = args.add

    if not os.path.exists(file_path):
        tasks = [
            {
                "id": 1,
                "description": args.add,
                "status": "todo",
                "createdAt": formatted_time,
                "updatedAt": formatted_time
            }
        ]

        with open(file_path, 'w') as file:
            json.dump(tasks, file, indent=4)
    else:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

            last_id = max(item['id'] for item in data) if data else 0

            new_task = {
                'id': last_id + 1,
                'description': args.add,
                'status': 'todo',
                "createdAt": formatted_time,
                "updatedAt": formatted_time
            }

            data.append(new_task)
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

if args.add:
    addTask()