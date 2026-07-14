import tkinter as tk
from tkcalendar import Calendar
from tkinter import messagebox
from tkinter import simpledialog
from basic_logic import add_task_db, fetch_data_by_date,toggle_task_status,delete_task_by_id,fetch_data,toggle_importance_db,edit_task_db
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


def delete_task(event):#deleting task from database and refreshing the listbox and calendar
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

root.bind("<Delete>",delete_task)  # Bind the Delete key to delete_task function


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
    load_all_tasks()  # Refresh the calendar events to reflect the change


def edit_task():
    selected=task_list.curselection()
    if not selected:
        return
    index=selected[0]
    if index >= len(task_ids):
        messagebox.showerror("Error", "Invalid task selection.")
        return
    task_id=task_ids[index]  
    new_name=simpledialog.askstring("Edit Task", "Enter new task name:")

    if not new_name or not new_name.strip():
        messagebox.showerror("Error", "Task name cannot be empty.")
        return
    
    edit_task_db(task_id,new_name.strip())
    show_tasks()  # Refresh the task list to reflect the change
    load_all_tasks()  # Refresh the calendar events to reflect the change


def toggle_importance():
    selected=task_list.curselection()
    if not selected:
        return
    index=selected[0]
    task_id=task_ids[index]
    toggle_importance_db(task_id)  # Toggle the importance in the database
    show_tasks()  # Refresh the task list to reflect the change
    load_all_tasks()  # Refresh the calendar events to reflect the change


menu=tk.Menu(root,tearoff=0)

menu.add_command(label="Delete Task 🗑️", command=delete_task)
menu.add_separator()
menu.add_command(label="Edit Task ✏️", command=edit_task)
menu.add_separator()
menu.add_command(label="Mark Complete/Incomplete ✅", command=mark_complete)
menu.add_separator()
menu.add_command(label="Toggle Importance ⭐", command=toggle_importance)

def detect_menu(event):
    try:
        index=task_list.nearest(event.y)

        task_list.selection_clear(0, tk.END)
        task_list.selection_set(index)

        menu.tk_popup(event.x_root, event.y_root)
    
    finally:
        menu.grab_release()

task_list.bind("<Button-3>", detect_menu)  # Right-click to show the menu












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
        for i,(task, status, imp,task_id )in enumerate(tasks,start=1):
            task_ids.append(task_id)  # Store the task ID
            label = f"{i}. {task}{'⭐ ' if imp else ''} ({   'Completed' if status else 'Not Completed'})"
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










para_box=tk.Text(root,width=50,height=5, font=("Arial", 12))
para_box.pack(pady=10)
para_box.insert(tk.END, "1. Double click on a task to mark it as completed or not completed.\n")
para_box.insert(tk.END," \n")
para_box.insert(tk.END, "2. Right click to perform task functions.\n")
para_box.insert(tk.END," \n")
para_box.insert(tk.END, "3. Press the Delete key to delete a task.\n")
para_box.insert(tk.END," \n")

para_box.config(state=tk.DISABLED)  # Make the text box read-only




load_all_tasks()
show_tasks()  # Show tasks for the initially selected date
root.mainloop()

