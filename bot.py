import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import os
from dotenv import load_dotenv
from pathlib import Path

# dotenv_path = Path('./.env')
# load_dotenv(dotenv_path=dotenv_path)

# SLACK_TOKEN = os.getenv("SLACK_TOKEN")
# SIGNING_SECRET = os.getenv("SIGNING_SECRET")

SLACK_TOKEN="xoxb-4006136814037-3994581778295-FNUNmL9Y0792aOAXIFo0chOr"
SIGNING_SECRET="c5be448a167d1ded05cafa2bfd98cb6b"

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
 
client = slack.WebClient(token=SLACK_TOKEN)
BOT_ID = client.api_call("auth.test")["user_id"]

@ slack_event_adapter.on('message')
def message(payload):

    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
 
    #hi/hello command
    if text == "hi" or "hello" and user_id != BOT_ID:

        #gets username data 
        response = client.users_profile_get(user=user_id)
        assert response["ok"]
        user_realname = response['profile']["real_name"]
        user_displayname = response['profile']["display_name"]

        if (user_displayname != ""):
            client.chat_postMessage(channel=channel_id,text="Hello, " + user_displayname + "! \nWelcome to this awesome channel! 😎")
        elif (user_realname):
            client.chat_postMessage(channel=channel_id,text="Hello, " + user_realname + "! \nWelcome to this awesome channel! 😎")


#set routes
@app.route('/challenge', methods=["POST"])
def challenge():
    data = request.form
    text = data.get("text")
    user_id = data.get("user_id")
    print("TEXT", text, "userID", user_id)
    channel_id = data.get("channel_id")

    display_names = []
    real_names = []
    
    print("DISPLAY ", display_names, "REAL", real_names)

    client.chat_postMessage(channel=channel_id, text="I got the command")

    return Response(), 200

    

  
if __name__ == "__main__":
    app.run(debug=True)