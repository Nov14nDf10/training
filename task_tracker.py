import json
import os
import argparse

# Inisialisasi file JSON jika belum ada
if not os.path.exists("tasks.json"):
    with open("tasks.json", "w") as file:
        json.dump([], file)

# Fungsi untuk memuat tugas dari file JSON
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Jika file JSON kosong atau tidak valid, kembalikan daftar tugas kosong
        return []

# Fungsi untuk menyimpan tugas ke file JSON
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

# Fungsi untuk menambah tugas
def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description, "status": "not done"})
    save_tasks(tasks)

# Fungsi untuk memperbarui tugas
def update_task(index, description):
    tasks = load_tasks()
    tasks[index]["description"] = description
    save_tasks(tasks)

# Fungsi untuk menghapus tugas
def delete_task(index):
    tasks = load_tasks()
    tasks.pop(index)
    save_tasks(tasks)

# Fungsi untuk menandai tugas
def mark_task(index, status):
    tasks = load_tasks()
    tasks[index]["status"] = status
    save_tasks(tasks)

# Fungsi untuk daftar tugas
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    for index, task in enumerate(tasks):
        print(f"{index + 1}. {task['description']} [{task['status']}]")

# Antarmuka Baris Perintah
parser = argparse.ArgumentParser(description="Task Tracker CLI")
parser.add_argument("action", choices=["add", "update", "delete", "mark", "list"])
parser.add_argument("--description", help="Description of the task")
parser.add_argument("--index", type=int, help="Index of the task (1-based)")
parser.add_argument("--status", choices=["not done", "in progress", "done"], help="Status of the task")

args = parser.parse_args()

if args.action == "add" and args.description:
    add_task(args.description)
elif args.action == "update" and args.index and args.description:
    update_task(args.index - 1, args.description)
elif args.action == "delete" and args.index:
    delete_task(args.index - 1)
elif args.action == "mark" and args.index and args.status:
    mark_task(args.index - 1, args.status)
elif args.action == "list":
    list_tasks(args.status)
else:
    print("Invalid command or missing arguments.")
