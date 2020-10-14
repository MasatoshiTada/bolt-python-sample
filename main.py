import logging
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from slack import WebClient
import os


logging.basicConfig(level=logging.DEBUG)
app = App()


@app.command("/hello-bolt-python-heroku")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


# この関数がないと動かない
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    logging.info("slack_events is called!!")
    return handler.handle(request)


@app.message("hello")
def message_hello(message, say):
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    response = client.conversations_members(channel="C01CFRN1KFX")
    user_ids = response["members"]
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
        text=f"Hey there <@{user_ids}>!"
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Listen for a shortcut invocation
@app.shortcut("open_modal")
def open_modal(ack, body, client):
    # Acknowledge the command request
    ack();
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "My App"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Welcome to a modal with _blocks_"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click me!"},
                        "action_id": "button_abc"
                    }
                },
                {
                    "type": "input",
                    "block_id": "input_c",
                    "label": {"type": "plain_text", "text": "What are your hopes and dreams?"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "dreamy_input",
                        "multiline": True
                    }
                }
            ]
        }
    )

# heroku login
# heroku create
# git remote add heroku https://git.heroku.com/tada-bolt-python-sample.git

# export SLACK_BOT_TOKEN=xxx
# export SLACK_SIGNING_SECRET=xxx
# heroku config:set SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
# heroku config:set SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET
# git checkout -b main
# git add .
# git commit -m'Initial commit for my awesome Slack app'
# git push heroku main
