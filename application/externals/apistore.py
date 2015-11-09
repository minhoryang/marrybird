__author__ = 'minhoryang'

import requests
import json

WEB_HOOK_URL = "http://api.openapi.io/ppurio/1/message/sms/marrybird"


def push(message="", to=""):
    payload = {
        "dest_phone": to,
        "send_phone": "01062473590",
        "msg_body": message + " 메리버드 인증코드입니다",
    }
    headers = {
        "x-waple-authorization": "MzMzNy0xNDQ3MDM3MDI0MzQ0LWVjYzQzNzE2LTg1OTYtNDRjMC04NDM3LTE2ODU5NmI0YzAzNg==",
    }
    r = requests.post(WEB_HOOK_URL, data=json.dumps(payload), headers=headers)
    return (r.status_code, r.text)