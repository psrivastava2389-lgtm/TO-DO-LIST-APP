from google_auth import get_calendar_service
from datetime import date,datetime, timedelta
from googleapiclient.errors import HttpError


import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
curr= mydb.cursor()


def fetch_data():
    mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
    curr= mydb.cursor()
    curr.execute("select * from tasks")
    tasks = curr.fetchall()
    curr.close()
    mydb.close()
    return tasks


def add_event(summary, description,imp, due_date):
    service = get_calendar_service()
    desc=f"{description}"
    event_color="11" if imp else "9"

    event = {
        'summary': summary,
        'extendedProperties': {
        'private': {
            'app': 'todo_app'
        }},
        'description': desc,
        'colorId':event_color,
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

    
    event_response = service.events().insert(calendarId='primary', body=event).execute()
    google_id = event_response.get('id') 
    

    print("Event created:", event.get('htmlLink'))
    return google_id

def delete_event(event_id):
    if not event_id:
        return
    try:
        service=get_calendar_service()
        service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute()
        print("successfully deleted event from google calender")
    
    except HttpError as error:
        if error.resp.status == 410:
            print("Event was already deleted directly from Google Calendar.")
        else:
            print(f"An error occurred connecting to Google Calendar: {error}")

def edit_event_name(event_id,new_description):
    
    if not event_id:
        return

    try:
        service = get_calendar_service()

        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        event['summary']=new_description
       
        service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event
        ).execute()

        print("Google Calendar event updated successfully!")
        
    except Exception as e:
        print(f"Failed to update Google Calendar event: {e}")


def edit_event_importance(id,new_imp):
    if not id:
        return

    try:
        service = get_calendar_service()

        event = service.events().get(calendarId='primary', eventId=id).execute()
        event_color="11" if new_imp else "9"
        event['colorId']=event_color
       
        service.events().update(
            calendarId='primary',
            eventId=id,
            body=event
        ).execute()

        print("Google Calendar event updated successfully!")
        
    except Exception as e:
        print(f"Failed to update Google Calendar event: {e}")

def edit_event_time(id,new_time,date):
    if not id:
        return

    try:
        service = get_calendar_service()

        event = service.events().get(calendarId='primary', eventId=id).execute()
        due_time=datetime.strptime(f"{date} {new_time}","%Y-%m-%d %H:%M")
        event['start']= {
            'dateTime': due_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        }  
        event['end']= {
            'dateTime': (due_time + timedelta(hours=1)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },     
        service.events().update(
            calendarId='primary',
            eventId=id,
            body=event
        ).execute()

        print("Google Calendar event updated successfully!")
        
    except Exception as e:
        print(f"Failed to update Google Calendar event: {e}")

def sync_calender():
    mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
    curr= mydb.cursor()
    
    events = get_calendar_service().events().list(calendarId='primary').execute()
    event_map={}    
    for e in events.get('items',[]):
        if e.get('extendedProperties',{}).get('private',{}).get('app')=='todo_app':
            event_map[e['id']]=e
    tasks = fetch_data()
   

    for task in tasks:
        if task[6] not in event_map :
            curr.execute("DELETE FROM tasks WHERE google_id=%s", (task[6],))
        else:
            e=event_map[task[6]]
            update_db(e.get('summary'),e.get('colorId'),e.get('id'),e.get('start',{}).get('dateTime'))
    mydb.commit()
    curr.close()
    mydb.close()


def update_db(name,color,g_id,time):
    mydb = mysql.connector.connect(host="localhost", user="root", password="123456",database="to_do_list")
    curr= mydb.cursor()

    imp='1' if color=='11' else 0
    due_time=(datetime.fromisoformat(time)).time()
    curr.execute("update tasks set task_name = %s, important=%s, due_time=%s where google_id=%s",(name,imp,due_time,g_id))
    mydb.commit()
            



        

    
        

    


    

    











def add_task_db(task, due_date, important,due_time):
    id=add_event(
    summary=task,
    description="From TO_DO app",
    imp=important,
    due_date=datetime.strptime(f"{due_date} {due_time}", "%Y-%m-%d %H:%M")
)
    
    curr.execute(
        "INSERT INTO tasks (task_name, status, important, due_date, due_time,google_id) VALUES (%s, %s, %s, %s, %s,%s)",
        (task, 0, important, due_date, due_time,id)
    )
    mydb.commit()

def fetch_data_by_date(date):
    curr.execute("SELECT task_name, status, important ,id,due_time FROM tasks WHERE due_date=%s", (date,))
    return curr.fetchall()

def delete_task_by_id(task_id): 
    curr.execute("select google_id from tasks where id=%s",(task_id,))
    res=curr.fetchone()
    if res:
        google_id=res[0]
        delete_event(google_id)
    curr.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    mydb.commit()


def edit_task_db(task_id,new_task_name):
    curr.execute("select google_id from tasks where id=%s",(task_id,))
    res=curr.fetchone()
    if not res:
        return
    g_id=res[0]
    edit_event_name(g_id,new_task_name)

    curr.execute("update tasks set task_name=%s where id=%s", (new_task_name, task_id))
    mydb.commit()

def toggle_importance_db(task_id):
    
    curr.execute("select important, google_id from tasks where id=%s", (task_id,))
    res=curr.fetchone()
    if not res:
        return
    
    new_importance = 0 if res[0] else 1
    g_id=res[1]
    if not g_id:
        return
    edit_event_importance(g_id,new_importance)

    curr.execute("update tasks set important=%s where id=%s", (new_importance, task_id))
    mydb.commit()

def edit_due_time_db(task_id,new_time):
    curr.execute("select google_id,due_date from tasks where id=%s",(task_id,))
    res=curr.fetchone()
    if not res:
        return
    g_id=res[0]
    date=res[1]
    edit_event_time(g_id,new_time,date)
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



    

    






