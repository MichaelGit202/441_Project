from main import prepare_game, run_console_chat
from util.flask_utils import app
from threading import Thread

def start_flask():
    app.run(debug=False, use_reloader=False)  # Important: disable reloader or it runs twice

if __name__ == '__main__':
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True  # Flask server will stop when main program exits
    flask_thread.start()

    # Now the rest of your code runs
    seed = '441_AI_Project'
    agents = prepare_game()
    run_console_chat(seed=seed, agents=agents)