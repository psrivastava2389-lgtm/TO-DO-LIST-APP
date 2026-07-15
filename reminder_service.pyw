import time
from datetime import date
from datetime import datetime,timedelta
from plyer import notification
from basic_logic import fetch_data_reminder

reminded_tasks = set()

def check_reminders():
    global reminded_tasks
    today = date.today()
    now=datetime.now()
    
    



    print(f"Checking reminders for {today}...")  # Debugging line
    
    tasks = fetch_data_reminder()
    
    
    

    for task in tasks:
        task_name = task[0]
        status = task[1]
        imp=task[2]
        due_date = task[3]
        task_id = task[4]
        input_time=task[5]
        due_time=datetime.strptime(f"{due_date} {input_time}","%Y-%m-%d %H:%M:%S")
        
        
        if due_date == today and status == 0:
            if imp:
                rem_time=due_time-timedelta(hours=2)
            else:
                rem_time=due_time-timedelta(hours=1)
   
            if task_id not in reminded_tasks and rem_time <= now < due_time:
                print(f"Sending reminder for task: {task_name}")  # Debugging line
                
                notification.notify(
                    title="Reminder 🔔",
                    message=f"{task_name} is due today! at {input_time}",
                    timeout=5
                )
                reminded_tasks.add(task_id)


while True:
    check_reminders()
    time.sleep(30)  # check every 60 seconds