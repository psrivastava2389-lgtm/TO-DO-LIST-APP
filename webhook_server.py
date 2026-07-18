from flask import Flask, request
from basic_logic import sync_calender
from google_auth import get_calendar_service
import uuid

channel_id = str(uuid.uuid4())

request = { 
    "id": channel_id,  # unique ID
    "type": "web_hook",
    "address": "https://snowiness-tantrum-empty.ngrok-free.dev/webhook"
}

response = get_calendar_service().events().watch(
    calendarId='primary',
    body=request
).execute()

print(response)

app = Flask(__name__)

   
@app.route('/webhook', methods=['POST'])
def webhook():
    print("Notification received!")

  


    print("Change detected!")

    # Call your sync function here
    sync_calender()


    return '', 200





if __name__ == "__main__":
    app.run(port=5000)