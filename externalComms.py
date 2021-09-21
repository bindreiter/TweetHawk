import requests
import json

def post_message_to_slack(text, slack_channel, slack_token, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'username': "test",
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

