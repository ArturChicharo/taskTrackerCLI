import os
import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--add", help="Type task description", required=False, type=str)
parser.add_argument("-u", "--update", help="Specify task id and updated description with the format 'id:description'", required=False, type=str)
parser.add_argument("-d", "--delete", help="Delete task by id", required=False, type=int)
parser.add_argument("-mip", "--markinprogress", help="Marks specified id as in-progress", required=False, type=int)
parser.add_argument("-md", "--markdone", help="Marks specified id as done", required=False, type=int)
parser.add_argument("-l", "--list", help="List tasks based on argument 'all' 'done' 'notdone' 'inprogress'", required=False, type=str)

args = parser.parse_args()

file_path = "taskTrackerJSON.json"

# Formatting time to dd-mm-yy HH:MM
current_time = datetime.now()
formatted_time = current_time.strftime('%H:%M %d %B %Y')

def addTask():
    try:
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
    except Exception as e:
        print(f"An error occurred: {e}")

def updateTask():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        task_id_str, task_description_str = args.update.split(":", 1)
        task_id = int(task_id_str.strip())
        task_description = task_description_str.strip()

        for task in data:
            if task["id"] == task_id:
                task["description"] = task_description
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except ValueError:
        print("Invalid format for update. Use the format 'id:description'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def deleteTask():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        task_deleted = False

        for task in data:
            if task["id"] == args.delete:
                data.remove(task)
                task_deleted = True
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

            if task_deleted:
                print("Task successfully deleted.")
            else:
                print("No task exists with specified id.")

    except Exception as e:
        print(f"An error occurred: {e}")

def markInProgress():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        task_status_updated = False

        for task in data:
            if task["id"] == args.markinprogress:
                task["status"] = "In Progress"
                task["updatedAt"] = formatted_time
                task_status_updated = True
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

            if task_status_updated:
                print("Task status successfully updated.")
            else:
                print("No task exists with specified id.")

    except Exception as e:
        print(f"An error occurred: {e}")

def markDone():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        task_status_updated = False

        for task in data:
            if task["id"] == args.markdone:
                task["status"] = "Done"
                task["updatedAt"] = formatted_time
                task_status_updated = True
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

            if task_status_updated:
                print("Task status successfully updated.")
            else:
                print("No task exists with specified id.")

    except Exception as e:
        print(f"An error occurred: {e}")

def list():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        option = args.list.strip()
        tasks_to_list = True

        if option == "all":
            for task in data:
                print(task)
        elif option == "done":
            for task in data:
                if task["status"] == "Done":
                    print(task)
        elif option == "inprogress":
            for task in data:
                if task["status"] == "In Progress":
                    print(task)
        elif option == "notdone":
            for task in data:
                if task["status"] != "Done":
                    print(task)
        else:
            tasks_to_list = False
        
        if not tasks_to_list:
            print("No tasks with specified status exist.")

    except Exception as e:
        print(f"An error occurred: {e}")

if args.add:
    addTask()

if args.update:
    updateTask()

if args.delete:
    deleteTask()

if args.markinprogress:
    markInProgress()

if args.markdone:
    markDone()

if args.list:
    list()