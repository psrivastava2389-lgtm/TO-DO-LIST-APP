import tkinter as tk
from tkcalendar import Calendar
from basic_logic import add_task_db, fetch_data_by_date

root = tk.Tk()
root.title("To-Do Calendar")
root.geometry("500x500")

# Calendar
cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
cal.pack(side="left", pady=20,fill="both", expand=True)

# Entry
task_entry = tk.Entry(root, width=40)
task_entry.pack()
def add_task():
    task = task_entry.get()
    date = cal.get_date()
    important = important_var.get()

    add_task_db(task, date, important)

    mark_calendar(date, important)
    show_tasks()

    task_entry.delete(0, tk.END)
tk.Button(root, text="Add Task", command=add_task).pack()

# Important checkbox
important_var = tk.IntVar()
tk.Checkbutton(root, text="Important ⭐", variable=important_var).pack()

# Listbox
task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)


def show_tasks(event=None):
    date = cal.get_date()
    tasks = fetch_data_by_date(date)

    task_list.delete(0, tk.END)

    for task, status, imp in tasks:
        if not task.strip():
            continue
        label = f"{'⭐ ' if imp else ''}{task} ({   'Completed' if status else 'Not Completed'})"
        task_list.insert(tk.END, label)

cal.bind("<<CalendarSelected>>", show_tasks)

def load_all_tasks():
    from basic_logic import fetch_data
    tasks = fetch_data()

    for task in tasks:
        date = task[3]   # due_date column
        important = task[2]

        if date:
            mark_calendar(date, important)

def mark_calendar(date, important):
    task=fetch_data_by_date(date)
    if not task[0][0].strip():
        return
    if important:
        cal.calevent_create(date, "Important", "important")
        cal.tag_config("important", background="red")
    else:
        cal.calevent_create(date, "Task", "normal")
        cal.tag_config("normal", background="blue")

load_all_tasks()
root.mainloop()

