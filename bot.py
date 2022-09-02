from datetime import datetime, timedelta
import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
import random
import asyncio
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from threading import Timer


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
            client.chat_postMessage(channel=channel_id,text=f"Hello, *{user_displayname}*!\nWelcome to this _awesome_ channel! 😎")
        elif (user_realname):
            client.chat_postMessage(channel=channel_id,text=f"Hello, *{user_realname}*!\nWelcome to this _awesome_ channel! 😎")

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
                        client.chat_postMessage(channel=channel_id, text=f"*{senderDisplayName}* challenged *{challengedUserDisplayName}* to a *{randomLanguage}* battle!")
                        def winnerIsMessage():
                            client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        t1 = Timer(1.0, winnerIsMessage)
                        t1.start()
                        def winMessage():
                            client.chat_postMessage(channel=channel_id, text=f"*{winner(senderDisplayName, challengedUserDisplayName)}*!!! 🎉🎉🎉")
                        t2 = Timer(3.0, winMessage)
                        t2.start()
                        foundUser = True
                    elif (item["profile"]["display_name"] == ""):
                        client.chat_postMessage(channel=channel_id, text=f"*{senderDisplayName}* challenged *{challengedUserRealName}* to a *{randomLanguage}* battle!!")
                        def winnerIsMessage():
                            client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        t1 = Timer(1.0, winnerIsMessage)
                        t1.start()
                        def winMessage():
                            client.chat_postMessage(channel=channel_id, text=f"*{winner(senderDisplayName, challengedUserRealName)}*!!! 🎉🎉🎉")
                        t = Timer(3.0, winMessage)
                        t.start()
                        foundUser = True
                        foundUser = True
                elif (senderDisplayName == ""):
                    if (item["profile"]["display_name"] != ""):
                        client.chat_postMessage(channel=channel_id, text=f"*{senderRealName}* challenged *{challengedUserDisplayName}* to a *{randomLanguage}* battle!!")
                        def winnerIsMessage():
                            client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        t1 = Timer(1.0, winnerIsMessage)
                        t1.start()
                        def winMessage():
                            client.chat_postMessage(channel=channel_id, text=f"*{winner(senderRealName, challengedUserDisplayName)}*!!! 🎉🎉🎉")
                        t = Timer(3.0, winMessage)
                        t.start()
                        foundUser = True
                    elif (item["profile"]["display_name"] == ""):
                        client.chat_postMessage(channel=channel_id, text=f"*{senderRealName}* challenged *{challengedUserRealName}* to a *{randomLanguage}* battle!!")
                        def winnerIsMessage():
                            client.chat_postMessage(channel=channel_id, text="And the winner is...")
                        t1 = Timer(1.0, winnerIsMessage)
                        t1.start()
                        def winMessage():
                            client.chat_postMessage(channel=channel_id, text=f"*{winner(senderRealName, challengedUserRealName)}*!!! 🎉🎉🎉")
                        t = Timer(3.0, winMessage)
                        t.start()
                        foundUser = True
        if foundUser == False:
            client.chat_postMessage(channel=channel_id, text="User not found! 😐 \nPlease select an user in channel using '@' _(ex: @username)_! 🙂")
                   
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)