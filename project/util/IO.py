#wrapper between flask and app
from .flask_utils import add_chat_message, toggle_input, listen_for_input, app

#use this to output a response in the format of a message
#[source, text]
def chatroom_output(msg):
    with app.app_context():
        add_chat_message(msg)

#use this function to get the user input
def get_user_input():
    with app.app_context():
        toggle_input()
        try:
            resp = listen_for_input()
        except:
            print("listening for input failed")
            
        toggle_input()
    return resp["text"]

#use this to output a message but to the standard output 
def cmd_output(msg):
    print(msg[1])





