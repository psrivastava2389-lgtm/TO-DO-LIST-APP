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
<br>
2) Desktop Notifications for due task (1hr before an important task and 2 hr before a normal task).
<br>
3) Google calender integration (user's tasks are visible on google calender too).
<br>
4) Real-time sync using webhook system.
<br>


#GUI(Tkinter)
<br>
The application use Tkinter, python's built in GUI library, to provide simple and interactice interface.
<br>
### GUI Features:
<br>
- Task input field
<br>
- Task list display
<br>
- Buttons for add/delete/update
<br>
- Menu to perform different tasks
<br>
- Visual indication of important tasks
<br>


#Flask
<br>
The application uses Flask to built lightweight server (webhook_server.py) that sits, wait and listen for updates from google calender on any changes in it.
<br>
- Handles webhook requests
<br>
- Receives event change notifications
<br>
- Triggers database sync
<br>


#Ngrok
<br>
Webhooks require a public URL , Ngrok is used to expose the application's local server made using flask to the internet. Google sends updates to this public URL set up by Ngrok, which are then forwarded to my loacl app.
<br>


## How Real-Time Sync Works
<br>

1. Task created in app -> added to Google Calendar  
<br>
2. Google Calendar detects changes  
<br>
3. Webhook (Flask server) receives notification  
<br>
4. App updates MySQL database accordingly
<br>


#TECH STACK
<br>
- Python
<br>
- Tkinter (GUI)
<br>
- MySQL (Database)
<br>
- Flask (Webhook server)
<br>
- Ngrok (Public URL Tunneling)
<br>
- Plyer (NOtifications)
<br>


#PROJECT STRUCTURE
<br>
├── gui_app.py # Tkinter GUI
<br>
├── basic_logic.py # Database logic
<br>
├── reminder_service.pyw # Background notifications
<br>
├── webhook_server.py # Flask webhook server
<br>
├── google_auth.py # Google API authentication
<br>
├── schema.sql # Database schema
<br>
├── README.md
<br>
├── .gitignore
<br>


#SETUP INSTRUCTIONS
<br>
1) Clone repository
<br>
   git clone <https://github.com/psrivastava2389-lgtm/TO-DO-LIST-APP.git>
   cd project
   <br>

3) Install dependencies
<br>
   pip install mysql-connector-python plyer flask pyngrok google-api-python-client google-auth-httplib2      google-auth-oauthlib
   <br>

5) Setup MySQL
<br>
   SOURCE schema.sql;
   <br>

7) Setup Google Calender API
<br>
   1. Go to Google Cloud Console  
<br>
   2. Create project  
<br>
   3. Enable Google Calendar API  
<br>
   4. Create OAuth credentials  
<br>
   5. Download `credentials.json`  
<br>
   6. Place it in project folder
<br>

9) Start Ngrok
<br>
   ngrok http 5000
   copy the HTTP URK and use in webhook setup
    <br>

11) Setup Notification system
   <br>
   1. run 'where pythonw' in CMD.
   <br>
   2. copy the URL and the file path of reminder_service.py in your project folder
   <br>
   3. open shell:startup in system
   <br>
   4. create new shortcut: URL of .pyw "file path"
    <br>
   5. save it.
 <br>

11) Run the application- run the required components simultaneously:
    <br>
   1. python gui_app.py
    <br>
   2. python webhook_server.py
    <br>
   3. ngrok http 5000
 <br>


##Important Notes
 <br>

- Do NOT upload:
   <br>
  - `credentials.json`
  - `token.json`
 <br>
- Each user must create their own Google API credentials
 <br>
- Ngrok URL changes every time unless using a paid plan
 <br>


#Future Improvements
 <br>

- Better UI design
 <br>
- Task categories
  <br>
- Cloud deployment
  <br>
- Persistent webhook hosting (instead of Ngrok)
  <br>


#AUTHOR 
<br>
Palak Srivastava
