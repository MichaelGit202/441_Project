from flask import Flask, render_template, Response, request, jsonify
import time

app = Flask(__name__)

chat_history = []
disabled_by_backend = False
waiting_for_user = False

@app.route('/')
def index():
    return render_template('chat.html', disabled=disabled_by_backend)

@app.route('/send_message', methods=['POST'])
def get_user_input():
    data = request.get_json()
    user_message = data.get('message', '')

    add_chat_message(["user", user_message])
    #return jsonify({'reply': response})


# I would note that you should never do this in flask
def listen_for_input():
    last_message_count = len(chat_history)

    print("Waiting for user input...")

    while True:
        time.sleep(3)  # sleep so you don't burn CPU
        if len(chat_history) > last_message_count:
            new_message = chat_history[-1]
            #print(f"User responded: {new_message}")
            return new_message


@app.route('/stream')
def stream():
    def event_stream():
        """ Generator that streams new messages """

        # Infinite loop to keep pushing new messages
        previous_length = 0
        while True:
            if len(chat_history) > previous_length:
                new_messages = chat_history[previous_length:]
                for msg in new_messages:
                    yield f"data: {msg['sender']}: {msg['text']}\n\n"
                previous_length = len(chat_history)
            time.sleep(1)  # Sleep to avoid CPU spinning

    return Response(event_stream(), mimetype="text/event-stream")

def add_chat_message(msg):
    print("INSIDE OF ADD_CHAT_MSG")
    print(msg)
    chat_history.append({'sender': msg[0], 'text': msg[1]})


#here is a function that is called by a timer on the front end to update
# the UI, I hate this
@app.route('/get_chat_history')
def get_chat_history():
    return jsonify({'history': chat_history})


def toggle_input():
    global disabled_by_backend
    disabled_by_backend = not disabled_by_backend