import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
from basic_logic import add_task_db, fetch_data_by_date,toggle_task_status,delete_task_by_id,fetch_data
task_ids=[]

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
task_list.bind("<Double-Button-1>", lambda event: mark_complete())  # Bind double-click to mark complete


def show_tasks(event=None,selected_date=None):#it is showing tasks for selected date in listbox
    global task_ids
    date = selected_date if selected_date else cal.get_date()
    task_list.delete(0, tk.END)
    task_ids.clear()  # Clear the list of task IDs
    tasks = fetch_data_by_date(date)
    if not tasks:
        return
    else:
        for task, status, imp,task_id in tasks:
            task_ids.append(task_id)  # Store the task ID
            label = f"{task}{'⭐ ' if imp else ''} ({   'Completed' if status else 'Not Completed'})"
            task_list.insert(tk.END, label)

cal.bind("<<CalendarSelected>>", show_tasks)

def delete_task():#deleting task from database and refreshing the listbox and calendar
    selected = task_list.curselection()
    if not selected:
        return
    index = selected[0]
    if index >= len(task_ids):
        messagebox.showerror("Error", "Invalid task selection.")
        return
    
    confirm=messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
    if not confirm:
        return
    task_id = task_ids[index]  # Get the task ID using the index    

    delete_task_by_id(task_id)  # Delete the task from the database
    show_tasks()  # Refresh the task list to reflect the change
    load_all_tasks()  # Refresh the calendar events
delete_btn = tk.Button(root, text="Delete Task 🗑️", command=delete_task, state="disabled")
delete_btn.pack(pady=5)

def on_select(event):
    if task_list.curselection():
        delete_btn.config(state="normal")
    else:
        delete_btn.config(state="disabled")
task_list.bind("<<ListboxSelect>>", on_select)

    

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


def mark_complete():
    selected=task_list.curselection()
    if not selected:
        return
    
    index=selected[0]
    if index >= len(task_ids):
        messagebox.showerror("Error", "Invalid task selection.")
        return
    task_id=task_ids[index]  # Get the task ID using the index
    toggle_task_status(task_id)  # Toggle the status in the database
    show_tasks()  # Refresh the task list to reflect the change


para_box=tk.Text(root,width=50,height=5, font=("Arial", 12))
para_box.pack(pady=10)
para_box.insert(tk.END, "Double click on a task to mark it as completed or not completed.\n")
para_box.config(state=tk.DISABLED)  # Make the text box read-only




load_all_tasks()
show_tasks()  # Show tasks for the initially selected date
root.mainloop()

