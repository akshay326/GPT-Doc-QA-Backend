import os
from typing import Any, Dict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize a Web API client
slack_token = os.getenv('SLACK_BOT_TOKEN')
client = WebClient(token=slack_token)


def send_message(
        message: Any, 
        channel: str
    ):
    assert message, 'Message cannot be empty'

    # if its a dict, convert to string
    if isinstance(message, dict):
        message = f'```{message}```'

    try:
        client.chat_postMessage(
            channel=channel,  
            text=message
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")