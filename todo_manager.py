"""To-Do List Manager (menu-driven CLI).

- Add / view / delete / mark tasks done
- Tasks persist to tasks.json so they survive restarts
- Optional tags and due dates (extra credit)
- Logic functions are separate from I/O functions
"""

import json
from datetime import datetime

DATA_FILE = "tasks.json"


# ------------------------------------------------------------ file I/O ----


def load_tasks(path=DATA_FILE):
    """Load tasks from JSON. Returns [] if the file is missing or corrupt."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read task file. Starting with an empty list.")
        return []


def save_tasks(tasks, path=DATA_FILE):
    """Write tasks to JSON. Returns True on success."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return True
    except OSError as err:
        print(f"Error: could not save tasks ({err}).")
        return False


# --------------------------------------------------------------- logic ----


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def parse_due_date(text):
    """Return a normalized YYYY-MM-DD string, '' if blank, or raise ValueError."""
    text = text.strip()
    if not text:
        return ""
    return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")


def parse_tags(text):
    return sorted({t.strip().lower() for t in text.split(",") if t.strip()})


def add_task(tasks, title, due="", tags=None):
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    task = {"id": next_id(tasks), "title": title, "done": False,
            "due": due, "tags": tags or []}
    tasks.append(task)
    return task


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise KeyError(f"No task with ID {task_id}.")


def delete_task(tasks, task_id):
    tasks.remove(find_task(tasks, task_id))


def mark_done(tasks, task_id):
    find_task(tasks, task_id)["done"] = True


def filter_by_tag(tasks, tag):
    return [t for t in tasks if tag.lower() in t.get("tags", [])]


def is_overdue(task, today=None):
    if task["done"] or not task.get("due"):
        return False
    today = today or datetime.now().strftime("%Y-%m-%d")
    return task["due"] < today


# ----------------------------------------------------------- user I/O ----


def format_task(task):
    status = "[x]" if task["done"] else "[ ]"
    line = f"{task['id']:>3}. {status} {task['title']}"
    if task.get("due"):
        line += f"  (due {task['due']}{', OVERDUE' if is_overdue(task) else ''})"
    if task.get("tags"):
        line += "  #" + " #".join(task["tags"])
    return line


def show_tasks(tasks):
    if not tasks:
        print("  No tasks to show.")
        return
    for task in tasks:
        print(format_task(task))


def read_task_id(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("  Please enter a valid numeric ID.")
        return None


def handle_add(tasks):
    title = input("Task title: ")
    while True:
        try:
            due = parse_due_date(input("Due date YYYY-MM-DD (optional): "))
            break
        except ValueError:
            print("  Invalid date. Use YYYY-MM-DD, or leave blank.")
    tags = parse_tags(input("Tags, comma-separated (optional): "))
    try:
        task = add_task(tasks, title, due, tags)
        print(f"  Added: {format_task(task)}")
        return True
    except ValueError as err:
        print(f"  Error: {err}")
        return False


def handle_id_action(tasks, action, verb):
    task_id = read_task_id(f"ID of task to {verb}: ")
    if task_id is None:
        return False
    try:
        action(tasks, task_id)
        print(f"  Task {task_id} {verb} successful.")
        return True
    except KeyError as err:
        print(f"  Error: {err.args[0]}")
        return False


def print_menu():
    print("\n=== To-Do List Manager ===")
    print("1. Add task")
    print("2. View all tasks")
    print("3. Mark task done")
    print("4. Delete task")
    print("5. Filter by tag")
    print("6. Exit")


def main():
    tasks = load_tasks()
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        changed = False

        if choice == "1":
            changed = handle_add(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            changed = handle_id_action(tasks, mark_done, "mark done")
        elif choice == "4":
            changed = handle_id_action(tasks, delete_task, "delete")
        elif choice == "5":
            show_tasks(filter_by_tag(tasks, input("Tag: ").strip()))
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("  Invalid option. Please enter 1-6.")

        if changed:
            save_tasks(tasks)


if __name__ == "__main__":
    main()
