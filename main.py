import threading
import queue
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import App
from logic.game import Game
from utils.helpers import ask_app, update_gui, play

def main():
    # Ensure the accessiblity cards directory
    cards_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
    if not os.path.exists(cards_dir):
        print(f"Warning: Cards directory not found at {cards_dir}")
    
    game_event = threading.Event()
    response_q = queue.Queue()
    game_info_q = queue.Queue()
    end_update = threading.Event()
    
    # Global so that the imported modules cna use them
    globals_dict = {
        'game_event': game_event,
        'response_q': response_q,
        'game_info_q': game_info_q,
        'end_update': end_update
    }
    
    #pass globals to modules that need them
    ask_app.globals = globals_dict
    update_gui.globals = globals_dict
    play.globals = globals_dict
    
    def run_app():
        app = App(globals_dict)
        app.mainloop()

    def run_game_data():
        game0 = Game()

        while True:
            play(game0)


    t1 = threading.Thread(target=run_app)
    t1.start()
    t2 = threading.Thread(target=run_game_data)
    t2.start()

if __name__ == "__main__":
    main()