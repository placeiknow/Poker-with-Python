import os

def score_interpreter(player):
    list_of_hand_types = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush",
                          "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]
    list_of_values_to_interpret = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                                   "Jack", "Queen", "King", "Ace"]
    hand_type = list_of_hand_types[player.score[0]]
    mod1 = list_of_values_to_interpret[player.score[1]]
    mod2 = list_of_values_to_interpret[player.score[2]]
    mod3 = list_of_values_to_interpret[player.score[3]]
    # High card
    if player.score[0] == 0:
        return hand_type + ": " + mod3
    # pair
    if player.score[0] == 1:
        return hand_type + ": " + mod1 + "s"
    # two pair
    if player.score[0] == 2:
        return hand_type + ": " + mod1 + "s" + " and " + mod2 + "s"
    # three of a kind
    if player.score[0] == 3:
        return hand_type + ": " + mod1 + "s"
    # straight
    if player.score[0] == 4:
        return hand_type + ": " + mod1 + " High"
    # flush
    if player.score[0] == 5:
        return hand_type + ": " + mod1 + " High"
    # full house
    if player.score[0] == 6:
        return hand_type + ": " + mod1 + "s" + " and " + mod2 + "s"
    # four of a kind
    if player.score[0] == 7:
        return hand_type + ": " + mod1 + "s"
    # strraight flush
    if player.score[0] == 8:
        return hand_type + ": " + mod1 + " High"
    # royal flush
    if player.score[0] == 9:
        return hand_type

def ask_app(question, game=""):
    print("asking...")
    print(question)
    answer = ""
    
    # These will be set by main.py
    globals_dict = getattr(ask_app, 'globals', None)
    
    if globals_dict:
        game_info_q = globals_dict.get('game_info_q')
        game_event = globals_dict.get('game_event')
        response_q = globals_dict.get('response_q')
        
        if game != "" and game_info_q:
            game_info_q.put(game)
        
        if game_event:
            game_event.wait()
            
        if response_q and not response_q.empty():
            answer = response_q.get()
            
        if game_event:
            game_event.clear()

    return answer

def update_gui(game1):
    print("updating gui...")
    print(game1)
    
    globals_dict = getattr(update_gui, 'globals', None)
    
    if globals_dict:
        game_info_q = globals_dict.get('game_info_q')
        if game_info_q:
            game_info_q.put(game1)

def play(game):

    globals_dict = getattr(play, 'globals', None)
    game_info_q = None
    
    if globals_dict:
        game_info_q = globals_dict.get('game_info_q')
    
    game.deck.shuffle()
    game.cards = []  
    game.round_ended = False
    
    # Initialize the game
    game.establish_player_attributes()
    game.deal_hole()
    
    if game_info_q:
        game_info_q.put(game)
    update_gui(game)
    
    game.print_round_info()
    game.act_one()
    game.print_round_info()
    

    if game_info_q:
        game_info_q.put(game)
    update_gui(game)
    


    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)

    if not game.round_ended:
        game.deal_flop()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)
    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)
        
    if not game.round_ended:
        game.deal_turn()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)
    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)
        
    if not game.round_ended:
        game.deal_river()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)
    if not game.round_ended:
        game.ask_players()
        game.print_round_info()
        if game_info_q:
            game_info_q.put(game)
        update_gui(game)
        
    if not game.round_ended:
        game.score_all()
        game.print_round_info()
    
    game.find_winners()
    if game_info_q:
        game_info_q.put(game)

    game.print_round_info()
    game.round_ended = True
    print(game.winners, game.winner, [player for player in game.list_of_players_not_out if player.win])
    game.end_round()


def get_card_image_path(card_name):
    """
    Get the absolute path to a card image file.
    
    Args:
        card_name: The name of the card (e.g., "Ace of Spades")
        
    Returns:
        The absolute path to the card image file
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "cards", f"{card_name}.png")

def load_card_image(card_name, size=(55, 85)):
    """
    Load a card image and resize it.
    
    Args:
        card_name: The name of the card
        size: The size to resize the image to
        
    Returns:
        The loaded and resized image
    """
    from PIL import Image
    try:
        path = get_card_image_path(card_name)
        return Image.open(path).resize(size, Image.LANCZOS)
    except Exception as e:
        print(f"Error loading card image {card_name}: {e}")
        # Return a default/blank card image
        try:
            return Image.open(get_card_image_path("default0")).resize(size, Image.LANCZOS)
        except:
            # If even the default fails, create a blank image
            from PIL import Image, ImageDraw
            img = Image.new('RGB', size, color='green')
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), size], outline='white')
            return img