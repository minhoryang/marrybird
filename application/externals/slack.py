__author__ = 'minhoryang'
import requests
import json

WEB_HOOK_URL = "https://hooks.slack.com/services/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"

def push(message="", channel="#progress"):
    payload = {
        "username": "Server.py",
        "icon_emoji": ":heartbeat:",
        #"channel": channel,
        "text": message
    }
    r = requests.post(WEB_HOOK_URL, data=json.dumps(payload))