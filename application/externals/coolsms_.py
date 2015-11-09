from coolsms.sender import Sender

# API key and secret from http://coolsms.co.kr/service_setup
API_KEY = 'NCS56402A021A477'
API_SECRET = '5E21E3F824F2D577310ED963A4C5366C'

def push(message="", to=""):
    sender = Sender(API_KEY, API_SECRET)
    return sender.send(
        '01062473590',  # from
        to,  # to
        "[메리버드] " + message + " 인증번호를 입력해주세요"
    )

