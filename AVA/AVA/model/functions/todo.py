import os, re


PATH_TODO = "data\\todo\\todo.md"


def get_all_tasks():
    """
    Retrieve a list of all tasks from a to-do list file.

    Returns:
        list[dict[str, str]]: A list of dictionaries, each representing a task with keys "completed" and "task".
    """
    todo_directory = os.path.dirname(PATH_TODO)
    if not os.path.exists(todo_directory):
        os.makedirs(todo_directory)
    if not os.path.exists(PATH_TODO):
        with open(PATH_TODO, "w"):
            pass
    try:
        lines = None
        with open(PATH_TODO, "r") as file:
            lines = file.readlines()

        items = []
        for line in lines:
            matches = re.findall(r"\[( |x)\](.*)", line.strip())
            for match in matches:
                items.append({"completed": match[0] == "x", "task": match[1].strip()})

        return items
    except FileNotFoundError:
        print(f"{PATH_TODO} not found.")
        return []


def write_todo_file(tasks: str):
    """
    Write a list of tasks to a to-do list file.

    Parameters:
        tasks (str): A list of tasks to be written to the file. Each task is represented by a dictionary
        with keys "completed" and "task".

    The function overwrites the existing file with the provided tasks.
    """
    with open(PATH_TODO, "w") as file:
        for task in tasks:
            file.write(f"- [{'x' if task['completed'] else ' '}] {task['task']}\n")


def add_task(task_description: str):
    """
    Add a new task to the to-do list.

    Parameters:
        task_description (str): The description of the task to be added.

    Returns:
        bool: True if the task was added successfully, False otherwise.
    """
    tasks = get_all_tasks()
    tasks.append({"completed": False, "task": task_description})
    write_todo_file(tasks)
    return True


def update_task(task_index: int, updated_description: str):
    """
    Update the description of an existing task in the to-do list.

    Parameters:
        task_index (int): The index of the task to be updated.
        updated_description (str): The updated description for the task.

    Returns:
        bool: True if the task was updated successfully, False if the task index is out of range.
    """
    tasks = get_all_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index]["task"] = updated_description
        write_todo_file(tasks)
        return True
    else:
        return False


def remove_task(task_index: int):
    """
    Remove a task from the to-do list.

    Parameters:
        task_index (int): The index of the task to be removed.

    Returns:
        bool: True if the task was removed successfully, False if the task index is out of range.
    """
    tasks = get_all_tasks()
    if 0 <= task_index < len(tasks):
        removed_task = tasks.pop(task_index)
        write_todo_file(tasks)
        return True
    else:
        return False


def complete_task(task_index: int):
    """
    Mark a task as completed in the to-do list.

    Parameters:
        task_index (int): The index of the task to be marked as completed.

    Returns:
        bool: True if the task was marked as completed successfully, False if the task index is out of range.
    """
    tasks = get_all_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        write_todo_file(tasks)
        return True
    else:
        return False
