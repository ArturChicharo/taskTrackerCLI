# Python Task Tracker CLI

A simple command-line interface (CLI) application for managing tasks. The tasks are stored in a JSON file for persistence.

## Features

- **Add Tasks:** Add new tasks to the task list with a description.
- **Update Tasks:** Modify the description of an existing task using its ID.
- **Delete Tasks:** Remove a task from the list using its ID.
- **Mark Tasks as In Progress:** Set a task's status to "In Progress" using its ID.
- **Mark Tasks as Done:** Set a task's status to "Done" using its ID.
- **List Tasks:** View tasks based on their status: all, done, in progress, or not done.

## Usage

### Command-line Arguments

- `-a, --add` : Add a new task. Example:
    ```bash
    python tasktrackercli.py -a "Buy groceries"
    ```

- `-u, --update` : Update an existing task description by ID. Example:
    ```bash
    python tasktrackercli.py -u "1:Pick up laundry"
    ```

- `-d, --delete` : Delete a task by ID. Example:
    ```bash
    python tasktrackercli.py -d 1
    ```

- `-mip, --markinprogress` : Mark a task as in-progress by ID. Example:
    ```bash
    python tasktrackercli.py -mip 1
    ```

- `-md, --markdone` : Mark a task as done by ID. Example:
    ```bash
    python tasktrackercli.py -md 1
    ```

- `-l, --list` : List tasks based on their status. Options: all, done, notdone, inprogress. Example:
    ```bash
    python tasktrackercli.py -l done
    ```