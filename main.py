import logging
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)
app = App()


@app.command("/hello-bolt-python-heroku")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    logging.info("slack_events is called!!")
    return handler.handle(request)


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# heroku login
# heroku create
# git remote add heroku https://git.heroku.com/xxx.git

# export SLACK_BOT_TOKEN=xxx
# export SLACK_SIGNING_SECRET=xxx
# heroku config:set SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
# heroku config:set SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET
# git checkout -b main
# git add .
# git commit -m'Initial commit for my awesome Slack app'
# git push heroku main
