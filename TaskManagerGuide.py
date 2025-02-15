import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from datetime import datetime

tasks = []

# Function to add a new task
def add_task():
    task = task_entry.get()
    if task:
        due_date = askstring("Due Date", "Enter due date (YYYY-MM-DD) or leave blank:")
        priority = askstring("Priority", "Enter priority (High/Medium/Low) or leave blank:")
        category = askstring("Category", "Enter category or leave blank:")
        task_details = {
            "task": task,
            "completed": False,
            "due_date": due_date if due_date else "No due date",
            "priority": priority if priority else "No priority",
            "category": category if category else "No category"
        }
        tasks.append(task_details)
        update_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to delete a task
def delete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        tasks.pop(selected_task_index[0])
        update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")

# Function to mark a task as complete
def complete_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        tasks[selected_task_index[0]]["completed"] = True
        update_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected!")

# Function to search tasks based on the keyword
def search_tasks():
    keyword = search_entry.get()
    if keyword:
        search_results = [task for task in tasks if keyword.lower() in task["task"].lower()]
        task_listbox.delete(0, tk.END)
        for task in search_results:
            status = "Completed" if task["completed"] else "Pending"
            task_listbox.insert(tk.END, f'{task["task"]} [{status}] - Due: {task["due_date"]} - Priority: {task["priority"]} - Category: {task["category"]}')
    else:
        messagebox.showwarning("Warning", "Search keyword cannot be empty!")

# Function to update the task list in the listbox
def update_tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        task_listbox.insert(tk.END, f'{task["task"]} [{status}] - Due: {task["due_date"]} - Priority: {task["priority"]} - Category: {task["category"]}')

# Function to clear all tasks
def clear_all_tasks():
    tasks.clear()
    update_tasks()

# Function to apply hover effects to buttons
def on_enter(event):
    event.widget.config(bg="#3e8e41")

def on_leave(event):
    event.widget.config(bg="#4CAF50")

# Create the main window
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x650")  # Adjust the window size to give more space
root.configure(bg="#f4f4f9")

# Define custom fonts and styling
label_font = ('Arial', 14, 'bold')
button_font = ('Arial', 12, 'bold')
entry_font = ('Arial', 12)
listbox_font = ('Arial', 12)

# Create and place the widgets using grid
task_label = tk.Label(root, text="Enter a task:", font=label_font, bg="#f4f4f9")
task_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="w")

task_entry = tk.Entry(root, width=50, font=entry_font, relief="solid", bd=2, fg="black", bg="#ffffff")
task_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

add_button = tk.Button(root, text="Add Task", command=add_task, font=button_font, bg="#4CAF50", fg="white", relief="raised", padx=10, pady=10)
add_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
add_button.bind("<Enter>", on_enter)
add_button.bind("<Leave>", on_leave)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, font=button_font, bg="#f44336", fg="white", relief="raised", padx=10, pady=10)
delete_button.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
delete_button.bind("<Enter>", on_enter)
delete_button.bind("<Leave>", on_leave)

complete_button = tk.Button(root, text="Complete Task", command=complete_task, font=button_font, bg="#8BC34A", fg="white", relief="raised", padx=10, pady=10)
complete_button.grid(row=4, column=0, pady=10, padx=20, sticky="ew")
complete_button.bind("<Enter>", on_enter)
complete_button.bind("<Leave>", on_leave)

search_label = tk.Label(root, text="Search tasks:", font=label_font, bg="#f4f4f9")
search_label.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="w")

search_entry = tk.Entry(root, width=50, font=entry_font, relief="solid", bd=2, fg="black", bg="#ffffff")
search_entry.grid(row=6, column=0, columnspan=2, pady=10, padx=20)

search_button = tk.Button(root, text="Search", command=search_tasks, font=button_font, bg="#2196F3", fg="white", relief="raised", padx=10, pady=10)
search_button.grid(row=7, column=0, pady=10, padx=20, sticky="ew")
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)

clear_button = tk.Button(root, text="Clear All Tasks", command=clear_all_tasks, font=button_font, bg="#FF9800", fg="white", relief="raised", padx=10, pady=10)
clear_button.grid(row=8, column=0, pady=10, padx=20, sticky="ew")
clear_button.bind("<Enter>", on_enter)
clear_button.bind("<Leave>", on_leave)

task_listbox = tk.Listbox(root, width=70, height=10, font=listbox_font, bg="#ffffff", selectmode=tk.SINGLE, bd=2, relief="solid")
task_listbox.grid(row=9, column=0, columnspan=2, pady=20, padx=20)

# Start the main loop
root.mainloop()
