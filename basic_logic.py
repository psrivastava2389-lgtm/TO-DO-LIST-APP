import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
curr= mydb.cursor()
def fetch_data():
    curr.execute("select * from tasks")
    tasks = curr.fetchall()
    return tasks








def add_task_db(task, due_date, important):
    
    curr.execute(
        "INSERT INTO tasks (task_name, status, important, due_date) VALUES (%s, %s, %s, %s)",
        (task, 0, important, due_date)
    )
    mydb.commit()

def fetch_data_by_date(date):
    curr.execute("SELECT task_name, status, important ,id FROM tasks WHERE due_date=%s", (date,))
    return curr.fetchall()

def delete_task_by_id(task_id):
    curr.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    mydb.commit()








def toggle_task_status(id):
    curr.execute("select status from tasks where id=%s", (id,))
    res=curr.fetchone()
    if not res:
        return
    
    new_status = 0 if res[0] else 1

    curr.execute("update tasks set status=%s where id=%s", (new_status, id))
    mydb.commit()



    

    






