import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
import random

load_dotenv()

SLACK_TOKEN = os.getenv("TOKEN")
SIGNING_SECRET = os.getenv("SECRET")

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
    channel_id = data.get("channel_id")

    #random languages generator
    languages = ["JavaScript", "TypeScript", "Python", "PostgreSQL", "Java", "Ruby", "C", "C++", "C#", "PostgreSQL", "NoSQL", "MySQL", "Go", "PHP", "Kotlin", "Swift", "R"]
    randomLanguage = random.choice(languages)

    #random winner generator helper
    def randomWinner(user1, user2):
        users = [user1, user2]
        winner = random.choice(users)
        return winner

    winner = randomWinner

    #get real name/display name of message sender
    senderRealName = ""
    senderDisplayName = ""

    getSenderUsername = client.api_call("users.list")
    if getSenderUsername['ok']:
        for item in getSenderUsername['members']:
            if user_id == item["id"]:
                senderRealName = item["profile"]["real_name"]
                senderDisplayName = item["profile"]["display_name"]
        
    #get all users list in team data
    getUserListRequest = client.api_call("users.list")
    if getUserListRequest['ok']:
        foundUser = False
        #messages displayed
        for item in getUserListRequest['members']:
            if item["id"] in text:
                challengedUserDisplayName = item["profile"]["display_name"]
                challengedUserRealName = item["profile"]["real_name"]
                if (senderDisplayName != ""):
                    if (item["profile"]["display_name"] != ""):
                        client.chat_postMessage(channel=channel_id, text=f"{senderDisplayName} challenged {challengedUserDisplayName} to a {randomLanguage} battle!")
                        client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        client.chat_postMessage(channel=channel_id, text=f"{winner(senderDisplayName, challengedUserDisplayName)}!!! 🎉🎉🎉")
                        foundUser = True
                    elif (item["profile"]["display_name"] == ""):
                        client.chat_postMessage(channel=channel_id, text=f"{senderDisplayName} challenged {challengedUserRealName} to a {randomLanguage} battle!!")
                        client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        client.chat_postMessage(channel=channel_id, text=f"{winner(senderDisplayName, challengedUserRealName)}!!! 🎉🎉🎉")
                        foundUser = True
                elif (senderDisplayName == ""):
                    if (item["profile"]["display_name"] != ""):
                        client.chat_postMessage(channel=channel_id, text=f"{senderRealName} challenged {challengedUserDisplayName} to a {randomLanguage} battle!!")
                        client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        client.chat_postMessage(channel=channel_id, text=f"{winner(senderRealName, challengedUserDisplayName)}!!! 🎉🎉🎉")
                        foundUser = True
                    elif (item["profile"]["display_name"] == ""):
                        client.chat_postMessage(channel=channel_id, text=f"{senderRealName} challenged {challengedUserRealName} to a {randomLanguage} battle!!")
                        client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        client.chat_postMessage(channel=channel_id, text=f"{winner(senderRealName, challengedUserDisplayName)}!!! 🎉🎉🎉")
                        foundUser = True
        if foundUser == False:
            client.chat_postMessage(channel=channel_id, text="User not found! 😐 \nPlease select an user in channel using '@' (ex: @username)! 😎")
                   
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)