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
task_entry = tk.Entry(root, width=30)
task_entry.pack()
important_var = tk.IntVar()

def add_task():#adding task to database and refreshing the listbox and calendar
    task = task_entry.get()
    if not task.strip():
        return  # Do not add empty tasks
    date = cal.get_date()
    important = important_var.get()
    important_var.set(0)  # Reset the checkbox after adding the task
    add_task_db(task, date, important)
    load_all_tasks()  # Refresh the calendar events
    show_tasks()
    task_entry.delete(0, tk.END)

# Important checkbox
tk.Checkbutton(root, text="Important ⭐", variable=important_var).pack()
tk.Button(root, text="Add Task", command=add_task).pack()



# Listbox
task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)


def show_tasks(event=None):#it is showing tasks for selected date in listbox
    date = cal.get_date()
    task_list.delete(0, tk.END)
    tasks = fetch_data_by_date(date)
    if not tasks:
        task_list.insert(tk.END, "No tasks for this date.")
    else:
        for task, status, imp in tasks:
            label = f"{task}{'⭐ ' if imp else ''} ({   'Completed' if status else 'Not Completed'})"
            task_list.insert(tk.END, label)

cal.bind("<<CalendarSelected>>", show_tasks)

def load_all_tasks():#marking all tasks in calendar
    from basic_logic import fetch_data
    tasks = fetch_data()

    cal.calevent_remove('all')  # ✅ clear once
    if not tasks:
        return
    for task in tasks:
        date = task[3]
        if date:
            mark_single_date(date)

    cal.tag_config("important", background="red")
    cal.tag_config("normal", background="blue")



def mark_single_date(date):#it is telling if any task is important or not for that date and marking it in calendar
    tasks = fetch_data_by_date(date)

    

    has_important = any(t[2] for t in tasks)

    if has_important:
        cal.calevent_create(date, "Important", "important")
    else:
        cal.calevent_create(date, "Task", "normal")



load_all_tasks()
show_tasks()  # Show tasks for the initially selected date
root.mainloop()

