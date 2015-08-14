__author__ = 'minhoryang'
import requests
import eventlet
import json

WEB_HOOK_URL = "https://hooks.slack.com/services/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"

# TODO : TOO LONG TO SYNCRONOUS. SO NEED TO PULL THIS ASYNC HEAVEN LIKE celery.
def push(message="", channel="#progress"):
    payload = {
        "username": "Server.py",
        "icon_emoji": ":heartbeat:",
        #"channel": channel,
        "text": message
    }
    def request(payload):
        if payload:
            requests.post(WEB_HOOK_URL, data=json.dumps(payload))
    r = eventlet.spawn_n(request).run(payload)
    return
