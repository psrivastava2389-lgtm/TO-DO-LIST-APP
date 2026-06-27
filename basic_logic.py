import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="123456")
curr= mydb.cursor()



def show_tasks():

    curr.execute("select * from tasks")
    tasks = curr.fetchall()
    if not tasks:
        print("No tasks found.\n")
    else:
        print("s.no\tTask\tStatus")
        for i,task in enumerate(tasks, start=1):
            print(i, task[0], "Completed" if task[1] else "Not Completed")




def add_task():
    task = input("Enter new task: ")
    
    
    
    print("Task added!\n")
    curr.execute("insert into tasks (task_name,status) values (%s, %s)", (task, 0))
    mydb.commit()


def delete_task():
    show_tasks()
    curr.execute("select * from tasks")
    tasks = curr.fetchall()
    
            
    if tasks:
        try:
            num = int(input("Enter task serial number to delete: "))
            for i,task in enumerate(tasks, start=1):
                if i==num:
                    removed = task[0]
                    curr.execute("delete from tasks where task_name=%s", (task[0],))
                    mydb.commit()
                    print(f"Deleted task: {removed}\n")
                
            if num<1 or num>i:
                print("Invalid task number.\n")
        except ValueError:
            print("Please enter a valid number.\n")
    else:
        print("No tasks to delete.\n")




def main():
    
    curr.execute("use to_do_list")
    



    

    while True:
        print("==== TO-DO LIST ====")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Exit")
        

        choice = input("Enter your choice: ")

        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            print("Goodbye!")
            break
        

        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()