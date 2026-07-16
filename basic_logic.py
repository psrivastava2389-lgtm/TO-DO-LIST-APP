from google_auth import get_calendar_service
from datetime import datetime, timedelta

import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
curr= mydb.cursor()
def fetch_data():
    curr.execute("select * from tasks")
    tasks = curr.fetchall()
    return tasks

def fetch_data_reminder():
    mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
    curr= mydb.cursor()
    curr.execute("select * from tasks")
    tasks = curr.fetchall()
    curr.close()
    return tasks


def add_event(summary, description, due_date):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': due_date.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (due_date + timedelta(hours=1)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
    'useDefault': False,
    'overrides': [
        {'method': 'popup', 'minutes': 10},
    ],
}
    }

    event = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    print("Event created:", event.get('htmlLink'))
    











def add_task_db(task, due_date, important,due_time):
    add_event(
    summary=task,
    description="From To-Do App",
    due_date=datetime.strptime(f"{due_date} {due_time}", "%Y-%m-%d %H:%M")
)
    
    curr.execute(
        "INSERT INTO tasks (task_name, status, important, due_date, due_time) VALUES (%s, %s, %s, %s, %s)",
        (task, 0, important, due_date, due_time)
    )
    mydb.commit()

def fetch_data_by_date(date):
    curr.execute("SELECT task_name, status, important ,id,due_time FROM tasks WHERE due_date=%s", (date,))
    return curr.fetchall()

def delete_task_by_id(task_id): 
    curr.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    mydb.commit()


def edit_task_db(task_id,new_task_name):
    curr.execute("update tasks set task_name=%s where id=%s", (new_task_name, task_id))
    mydb.commit()

def toggle_importance_db(task_id):
    curr.execute("select important from tasks where id=%s", (task_id,))
    res=curr.fetchone()
    if not res:
        return
    
    new_importance = 0 if res[0] else 1

    curr.execute("update tasks set important=%s where id=%s", (new_importance, task_id))
    mydb.commit()

def edit_due_time_db(task_id,new_time):
    curr.execute("update tasks set due_time=%s where id=%s",(new_time,task_id))
    mydb.commit()
    





def toggle_task_status(id):
    curr.execute("select status from tasks where id=%s", (id,))
    res=curr.fetchone()
    if not res:
        return
    
    new_status = 0 if res[0] else 1

    curr.execute("update tasks set status=%s where id=%s", (new_status, id))
    mydb.commit()



    

    






