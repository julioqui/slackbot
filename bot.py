import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN="xoxb-4006136814037-3994581778295-BCR0vh1pitVcgWQvp71GD9Zs"
SIGNING_SECRET="c5be448a167d1ded05cafa2bfd98cb6b"

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel='#testing-slack-bot',text='Hello World!')

if __name__ == "__main__":
    app.run(debug=True)