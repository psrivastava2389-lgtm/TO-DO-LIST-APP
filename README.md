# TO-DO-LIST-APP with Google Calender Sync
<br>
> A TO_DO list desktop based application to track daily tasks, recieve notification for tasks as well as contains google calender imtegration.
<br>
##Description
<br>
This is a desktop-based application that allows user to add a task and track it accordingly. It also provides background reminders for the tasks as it's due time reaches. It is also integrated with google calender and allows 2 way sync of data.
<br>
Features:
<br>
1) Task Management (Add, edit, delete, mark important, mark complete).
2) Desktop Notifications for due task (1hr before an important task and 2 hr before a normal task).
3) Google calender integration (user's tasks are visible on google calender too).
4) Real-time sync using webhook system.
<br>
#GUI(Tkinter)
The application use Tkinter, python's built in GUI library, to provide simple and interactice interface.
### GUI Features:
- Task input field
- Task list display
- Buttons for add/delete/update
- Menu to perform different tasks
- Visual indication of important tasks

#Flask
The application uses Flask to built lightweight server (webhook_server.py) that sits, wait and listen for updates from google calender on any changes in it.
- Handles webhook requests
- Receives event change notifications
- Triggers database sync

#Ngrok
Webhooks require a public URL , Ngrok is used to expose the application's local server made using flask to the internet. Google sends updates to this public URL set up by Ngrok, which are then forwarded to my loacl app.


## How Real-Time Sync Works

1. Task created in app -> added to Google Calendar  
2. Google Calendar detects changes  
3. Webhook (Flask server) receives notification  
4. App updates MySQL database accordingly



#TECH STACK
- Python
- Tkinter (GUI)
- MySQL (Database)
- Flask (Webhook server)
- Ngrok (Public URL Tunneling)
- Plyer (NOtifications)


#PROJECT STRUCTURE
├── gui_app.py # Tkinter GUI
├── backend.py # Database logic
├── reminder.py # Background notifications
├── webhook.py # Flask webhook server
├── google_auth.py # Google API authentication
├── schema.sql # Database schema
├── README.md
├── .gitignore


#SETUP INSTRUCTIONS
1) Clone repository
   git clone <your-repo-link>
   cd project

