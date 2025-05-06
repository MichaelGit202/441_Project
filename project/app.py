from util.game_utils import prepare_game, run_console_chat
from util.flask_utils import app
from threading import Thread
from util.rag import setup
import logging

def start_flask():
    #disabled the logging messages for prod
    logging.getLogger('werkzeug').disabled = True
    app.run(debug=False, use_reloader=False)  # Important disable reloader or it runs twice

if __name__ == '__main__':
    print("Rag chunking started.")
    #setup()
    print("Rag chunking complete.")
    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True  
    flask_thread.start()

    seed = '441_AI_Project'
    agents = prepare_game()
    run_console_chat(seed=seed, agents=agents)