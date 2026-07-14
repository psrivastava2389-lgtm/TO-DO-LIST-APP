import time
import datetime
from plyer import notification
from basic_logic import fetch_data

reminded_tasks = set()

def check_reminders():
    global reminded_tasks
    today = datetime.date.today().strftime("%Y-%m-%d")
    print(f"Checking reminders for {today}...")  # Debugging line
    tasks = fetch_data()

    for task in tasks:
        task_name = task[0]
        status = task[1]
        due_date = task[3]
        task_id = task[4]  

        if due_date == today and status == 0:
            if task_id not in reminded_tasks:
                notification.notify(
                    title="Reminder 🔔",
                    message=f"{task_name} is due today!",
                    timeout=5
                )
                reminded_tasks.add(task_id)


while True:
    check_reminders()
    time.sleep(5)  # check every 60 seconds