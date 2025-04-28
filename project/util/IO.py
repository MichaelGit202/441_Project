#wrapper between flask and app
from .flask_utils import add_chat_message, toggle_input, listen_for_input, app


def chatroom_output(msg):
    with app.app_context():
        add_chat_message(msg)

def get_user_input():
    with app.app_context():
        toggle_input()
        resp = listen_for_input()
        toggle_input()
    return resp["text"]

def cmd_output(msg):
    print(msg[1])




