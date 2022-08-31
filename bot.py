import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN="xoxb-4006136814037-3994581778295-E5rvdQjanEUmU86S8s3jMCse"
SIGNING_SECRET="c5be448a167d1ded05cafa2bfd98cb6b"

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
 
client = slack.WebClient(token=SLACK_TOKEN)
@ slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    response = client.users_profile_get(user=user_id)
    assert response["ok"]
    user = response['profile']["real_name"]
    print("🟢🟢🟢🟢🟢 USER " , user)
 
    if text == "hi":
        client.chat_postMessage(channel=channel_id,text="Hello, " + user + "! \nWelcome to this awesome channel! 😎")
 
if __name__ == "__main__":
    app.run(debug=True)