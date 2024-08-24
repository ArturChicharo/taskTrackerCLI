TODO = "To do"
IN_PROGRESS = "In Progress"
DONE = "Done"

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any

# Set up the argument parser
parser = argparse.ArgumentParser()

# Define CLI arguments
parser.add_argument("-a", "--add", help="Add a new task. Example: -a 'Task description'", required=False, type=str)
parser.add_argument("-u", "--update", help="Update a task description. Use format 'id:description'. Example: -u '2:New description'", required=False, type=str)
parser.add_argument("-d", "--delete", help="Delete a task by ID. Example: -d 2", required=False, type=int)
parser.add_argument("-mip", "--markinprogress", help="Mark a task as 'in-progress' by ID. Example: -mip 2", required=False, type=int)
parser.add_argument("-md", "--markdone", help="Mark a task as 'done' by ID. Example: -md 2", required=False, type=int)
parser.add_argument("-l", "--list", help="List tasks. Options: 'all', 'done', 'notdone', 'inprogress'. Example: -l done", required=False, type=str)

args = parser.parse_args()

# Define the JSON file path
file_path = "taskTrackerJSON.json"

# Formatting current time to dd-mm-yy HH:MM
current_time = datetime.now()
formatted_time = current_time.strftime('%H:%M %d %B %Y')

def readFile() -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        data = []
        return data
    
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data: List[Dict[str, Any]] = []
    return data

def writeToFile(data: List[Dict[str, Any]]):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def addTask():
    try:
        data = readFile()

        last_id = max(item['id'] for item in data) if data else 0

        new_task = {
            'id': last_id + 1,
            'description': args.add,
            'status': TODO,
            "createdAt": formatted_time,
            "updatedAt": formatted_time
        }

        data.append(new_task)
        
        writeToFile(data)
        print(f"New task has been added with ID {new_task['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

def updateTask():
    try:
        data = readFile()
        
        # Extract task ID and new description
        task_id_str, task_description_str = args.update.split(":", 1)
        task_id = int(task_id_str.strip())
        task_description = task_description_str.strip()

        # Update the specified task
        task_found = False
        for task in data:
            if task["id"] == task_id:
                task["description"] = task_description
                task_found = True
        
        writeToFile(data)
        if task_found:
            print(f"Task with ID {task_id} has been updated. New task description: '{task_description}'")
        else:
            print(f"Error: There is no task with ID {task_id}")
    except ValueError:
        print("Invalid format for update. Use the format 'id:description'")
    except Exception as e:
        print(f"An error occurred: {e}")

def deleteTask():
    try:
        data = readFile()
        
        task_deleted = False

        # Remove the specified task
        for task in data:
            if task["id"] == args.delete:
                data.remove(task)
                task_deleted = True
        
        writeToFile(data)

        if task_deleted:
            print(f"Task with ID {args.delete} successfully deleted")
        else:
            print(f"No task exists with ID {args.delete}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Verify if task already has the status
def markInProgress():
    try:
        data = readFile()
        
        task_status_updated = False

        # Update the status of the specified task
        for task in data:
            if task["id"] == args.markinprogress:
                if task["status"] == IN_PROGRESS:
                    print(f"Task with ID {args.markinprogress} is already marked as '{IN_PROGRESS}'")
                    return
                else:
                    task["status"] = IN_PROGRESS
                    task["updatedAt"] = formatted_time
                    task_status_updated = True
        
        writeToFile(data)

        if task_status_updated:
            print(f"Task with ID {args.markinprogress} successfully updated to '{IN_PROGRESS}'")
        else:
            print(f"No task exists with ID {args.markinprogress}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Verify if task already has the status
def markDone():
    try:
        data = readFile()
        
        task_status_updated = False

        # Update the status of the specified task
        for task in data:
            if task["id"] == args.markdone:
                if task["status"] == DONE:
                    print(f"Task with ID {args.markdone} is already marked as '{DONE}'")
                    return
                else:
                    task["status"] = DONE
                    task["updatedAt"] = formatted_time
                    task_status_updated = True
        
        writeToFile(data)

        if task_status_updated:
            print(f"Task with ID {args.markdone} successfully updated to '{DONE}'")
        else:
            print(f"No task exists with ID {args.markdone}")

    except Exception as e:
        print(f"An error occurred: {e}")

def list():
    try:
        data = readFile()
        tasks_to_list: List[Dict[str, Any]] = []
        
        option = args.list.strip()
        tasks_exist = True

        # List tasks based on user input
        if option == "all":
            for task in data:
                tasks_to_list.append(task)
        elif option == "done":
            for task in data:
                if task["status"] == DONE:
                    tasks_to_list.append(task)
        elif option == "inprogress":
            for task in data:
                if task["status"] == IN_PROGRESS:
                    tasks_to_list.append(task)
        elif option == "notdone":
            for task in data:
                if task["status"] != DONE:
                    tasks_to_list.append(task)
        else:
            tasks_exist = False
        
        if not tasks_exist:
            print(f"No tasks with '{option}' status exist.")
        else:
            displayTable(tasks_to_list)

    except Exception as e:
        print(f"An error occurred: {e}")

def displayTable(data: List[Dict[str, Any]]):
    # Extract the headers from the first dictionary
    headers = data[0].keys()
    
    # Calculate the maximum width for each column
    column_widths = {header: max(len(header), max(len(str(row[header])) for row in data)) for header in headers}

    # Create the header row
    header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
    separator_row = "-+-".join("-" * column_widths[header] for header in headers)
    
    # Display the header row
    print(header_row)
    print(separator_row)
    
    # Create each data row
    for row in data:
        print(" | ".join(str(row[header]).ljust(column_widths[header]) for header in headers))

# Execute functions based on provided arguments
if args.add:
    addTask()
elif args.update:
    updateTask()
elif args.delete:
    deleteTask()
elif args.markinprogress:
    markInProgress()
elif args.markdone:
    markDone()
elif args.list:
    list()