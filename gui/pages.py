import sys
import os
# Add project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tkinter import Frame, Canvas, Label, Entry, Button, OptionMenu, StringVar
from PIL import Image, ImageTk
import time
from utils.helpers import score_interpreter

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.globals_dict = controller.globals_dict

        height = 500
        width = 800
        canvas = Canvas(self, height=height, width=width, bg="light green")
        canvas.pack()

        left_frame = Frame(canvas, bg='green', bd=5)
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor='nw')
        name_frame = Frame(left_frame, bg="light green", bd=5)
        name_frame.place(relx=0.5, rely=0.17, relwidth=0.9, relheight=0.7, anchor="n")
        self.entry_p0 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p0.place(relwidth=0.5, relheight=0.2)
        self.entry_p1 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p1.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.2)
        self.entry_p2 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p2.place(relx=0, rely=0.2, relwidth=0.5, relheight=0.2)
        self.entry_p3 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p3.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.2)
        self.entry_p4 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p4.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.2)
        self.entry_p5 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p5.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.2)
        self.entry_p6 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p6.place(relx=0, rely=0.6, relwidth=0.5, relheight=0.2)
        self.entry_p7 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p7.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.2)
        self.entry_p8 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p8.place(relx=0, rely=0.8, relwidth=0.5, relheight=0.2)
        self.entry_p9 = Entry(name_frame, font=("Courier", 12), bd=3)
        self.entry_p9.place(relx=0.5, rely=0.8, relwidth=0.5, relheight=0.2)
        enter_player_label = Label(left_frame, text="Player Names:", font=("Courier", 12), bd=3)
        enter_player_label.place(relx=0.25, rely=0.07, relwidth=0.5, relheight=0.05)

        right_frame = Frame(canvas, bg='green', bd=5)
        right_frame.place(relx=1, rely=0, relwidth=0.5, relheight=1, anchor='ne')
        self.sc_label = Label(right_frame, text="Starting Chips:", font=("Courier", 12), bd=3)
        self.sc_label.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.05)
        self.sc_entry = Entry(right_frame, font=("Courier"), bd=3)
        self.sc_entry.place(relx=0.5, rely=0.17, relwidth=0.5, relheight=0.07, anchor="n")

        self.sb_label = Label(right_frame, text="Small-Blind Chips:", font=("Courier", 12), bd=3)
        self.sb_label.place(relx=0.25, rely=0.33, relwidth=0.5, relheight=0.05)
        self.sb_entry = Entry(right_frame, font=("Courier"), bd=3)
        self.sb_entry.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.07, anchor="n")

        self.bb_label = Label(right_frame, text="Big-Blind Chips:", font=("Courier", 12), bd=3)
        self.bb_label.place(relx=0.25, rely=0.56, relwidth=0.5, relheight=0.05)
        self.bb_entry = Entry(right_frame, font=("Courier"), bd=3)
        self.bb_entry.place(relx=0.5, rely=0.63, relwidth=0.5, relheight=0.07, anchor="n")
        self.bb_entry.bind("<Return>", lambda _: self.button_click(self.entry_p0.get(), self.entry_p1.get(),
                                                                   self.entry_p2.get(), self.entry_p3.get(),
                                                                   self.entry_p4.get(), self.entry_p5.get(),
                                                                   self.entry_p6.get(),
                                                                   self.entry_p7.get(), self.entry_p8.get(),
                                                                   self.entry_p9.get(), self.sc_entry.get(),
                                                                   self.sb_entry.get(), self.bb_entry.get()))

        button = Button(right_frame, text="START", font=("Courier", 12),
                        command=lambda: self.button_click(self.entry_p0.get(), self.entry_p1.get(),
                                                          self.entry_p2.get(), self.entry_p3.get(),
                                                          self.entry_p4.get(), self.entry_p5.get(),
                                                          self.entry_p6.get(),
                                                          self.entry_p7.get(), self.entry_p8.get(),
                                                          self.entry_p9.get(), self.sc_entry.get(),
                                                          self.sb_entry.get(), self.bb_entry.get()))
        button.place(relx=0.5, rely=0.9, relwidth=0.3, relheight=0.1, anchor="n")

    def button_click(self, entry0, entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entrysc,
                     entrysb, entrybb):
        entry_list = [entry0, entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entrysc,
                      entrysb, entrybb]
        player_entry_list = [entry0, entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9]
        print(player_entry_list)
        player_entry_list = list(set(player_entry_list))
        for player in player_entry_list[:]:  
            if player == "":
                player_entry_list.remove(player)
        print(player_entry_list)
        if len(player_entry_list) < 2:
            print("not enough players")
            return
        chip_entry_list = [entrysc, entrysb, entrybb]
        for chips in chip_entry_list:
            try:
                chips = int(chips)
            except ValueError:
                print("Value Error")
                return
            if chips == "" or chips <= 0:
                print("chip entry error")
                return
        if not int(entrysc) > int(entrybb) > int(entrysb):
            print("chip entry error2 ")
            return
        setup = {
            "players": player_entry_list,
            "chips": chip_entry_list
        }
        
        if self.globals_dict:
            response_q = self.globals_dict.get('response_q')
            game_event = self.globals_dict.get('game_event')
            if response_q and game_event:
                response_q.put(setup)
                game_event.set()
                
        from gui.pages import GamePage
        self.controller.show_frame(GamePage)


class GamePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.globals_dict = controller.globals_dict

        self.restart = False
        self.responses = []
        self.list_of_button_r = []
        height = 500
        width = 800
        canvas = Canvas(self, height=height, width=width, bg="light green")
        canvas.pack()

        left_frame = Frame(canvas, bg='green', bd=5)
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1, anchor='nw')
        name_frame = Frame(left_frame, bg="light green", bd=5)
        name_frame.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor="n")

        self.frame_p0 = Frame(name_frame, bd=3, relief="groove")
        self.frame_p0.place(relwidth=0.5, relheight=0.2)
        self.name_label_p0 = Label(self.frame_p0, font=("Courier", 10), bd=3)
        self.name_label_p0.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
        self.chips_label_p0 = Label(self.frame_p0, font=("Courier", 10), bd=3)
        self.chips_label_p0.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
        self.cards_frame_p0 = Frame(self.frame_p0, bd=3, relief="groove")
        self.cards_frame_p0.place(relx=0.38, relheight=1, relwidth=0.62)
        self.card1_p0 = Label(self.cards_frame_p0)
        self.card1_p0.place(relwidth=0.5, relheight=1)
        self.card2_p0 = Label(self.cards_frame_p0)
        self.card2_p0.place(relx=0.5, relwidth=0.5, relheight=1)
        self.stake_label_p0 = Label(self.frame_p0, bd=1, relief="groove")
        self.stake_label_p0.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)

        self.frame_p1 = Frame(name_frame, bd=3, relief="groove")
        self.frame_p1.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.2)
        self.name_label_p1 = Label(self.frame_p1, font=("Courier", 10), bd=3)
        self.name_label_p1.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
        self.chips_label_p1 = Label(self.frame_p1, font=("Courier", 10), bd=3)
        self.chips_label_p1.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
        self.cards_frame_p1 = Frame(self.frame_p1, bd=3, relief="groove")
        self.cards_frame_p1.place(relx=0.38, relheight=1, relwidth=0.62)
        self.card1_p1 = Label(self.cards_frame_p1)
        self.card1_p1.place(relwidth=0.5, relheight=1)
        self.card2_p1 = Label(self.cards_frame_p1)
        self.card2_p1.place(relx=0.5, relwidth=0.5, relheight=1)
        self.stake_label_p1 = Label(self.frame_p1, bd=1, relief="groove")
        self.stake_label_p1.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)
        
        self.frame_p2 = Frame(name_frame, bd=3, relief="groove")
        self.frame_p2.place(relx=0, rely=0.2, relwidth=0.5, relheight=0.2)  
        self.name_label_p2 = Label(self.frame_p2, font=("Courier", 10), bd=3)
        self.name_label_p2.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
        self.chips_label_p2 = Label(self.frame_p2, font=("Courier", 10), bd=3)
        self.chips_label_p2.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
        self.cards_frame_p2 = Frame(self.frame_p2, bd=3, relief="groove")
        self.cards_frame_p2.place(relx=0.38, relheight=1, relwidth=0.62)
        self.card1_p2 = Label(self.cards_frame_p2)
        self.card1_p2.place(relwidth=0.5, relheight=1)
        self.card2_p2 = Label(self.cards_frame_p2)
        self.card2_p2.place(relx=0.5, relwidth=0.5, relheight=1)
        self.stake_label_p2 = Label(self.frame_p2, bd=1, relief="groove")
        self.stake_label_p2.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)
                
        self.frame_p3 = Frame(name_frame, bd=3, relief="groove")
        self.frame_p3.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.2)  
        self.name_label_p3 = Label(self.frame_p3, font=("Courier", 10), bd=3)
        self.name_label_p3.place(relx=0, rely=0, relheight=(1 / 3), relwidth=0.38)
        self.chips_label_p3 = Label(self.frame_p3, font=("Courier", 10), bd=3)
        self.chips_label_p3.place(relx=0, rely=(1 / 3), relheight=(1 / 3), relwidth=0.38)
        self.cards_frame_p3 = Frame(self.frame_p3, bd=3, relief="groove")
        self.cards_frame_p3.place(relx=0.38, relheight=1, relwidth=0.62)
        self.card1_p3 = Label(self.cards_frame_p3)
        self.card1_p3.place(relwidth=0.5, relheight=1)
        self.card2_p3 = Label(self.cards_frame_p3)
        self.card2_p3.place(relx=0.5, relwidth=0.5, relheight=1)
        self.stake_label_p3 = Label(self.frame_p3, bd=1, relief="groove")
        self.stake_label_p3.place(relx=0, rely=(2 / 3), relheight=(1 / 3), relwidth=0.38)
        



        right_frame = Frame(canvas, bg='green', bd=5)
        right_frame.place(relx=1, rely=0, relwidth=0.5, relheight=1, anchor='ne')

        self.cc_frame = Frame(right_frame, bd=2, relief="raised")
        self.cc_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.cc_1 = Label(self.cc_frame, bg="green")
        self.cc_1.place(relwidth=(.50 / 3), relheight=1)
        card_d1 = ImageTk.PhotoImage(
            Image.open("cards\\default0.png").resize((55, 85), Image.LANCZOS))
        self.cc_1.image = card_d1
        self.cc_1.configure(image=card_d1)

        self.cc_2 = Label(self.cc_frame, bg="green")
        self.cc_2.place(relx=(.50 / 3), relwidth=(.50 / 3), relheight=1)
        card_d2 = ImageTk.PhotoImage(
            Image.open("cards\\default1.png").resize((55, 85), Image.LANCZOS))
        self.cc_2.image = card_d2
        self.cc_2.configure(image=card_d2)

        self.cc_3 = Label(self.cc_frame, bg="green")
        self.cc_3.place(relx=(.50 / 3) * 2, relwidth=(.50 / 3), relheight=1)
        card_d3 = ImageTk.PhotoImage(
            Image.open("cards\\default1.png").resize((55, 85), Image.LANCZOS))
        self.cc_3.image = card_d3
        self.cc_3.configure(image=card_d3)

        self.cc_4 = Label(self.cc_frame, bg="green")
        self.cc_4.place(relx=(.50 / 3) * 3, relwidth=0.25, relheight=1)
        card_d4 = ImageTk.PhotoImage(
            Image.open("cards\\default1.png").resize((55, 85), Image.LANCZOS))
        self.cc_4.image = card_d4
        self.cc_4.configure(image=card_d4)

        self.cc_5 = Label(self.cc_frame, bg="green")
        self.cc_5.place(relx=((.50 / 3) * 3) + 0.25, relwidth=0.25, relheight=1)
        card_d5 = ImageTk.PhotoImage(
            Image.open("cards\\default1.png").resize((55, 85), Image.LANCZOS))
        self.cc_5.image = card_d5
        self.cc_5.configure(image=card_d5)

        self.pot_label = Label(right_frame, text="pot: ", font=("Courier", 12), bd=3)
        self.pot_label.place(relx=0, rely=0.2, relwidth=0.5, relheight=0.04)

        self.action_frame = Frame(right_frame, bd=2, relief="raised", bg="green")
        self.action_frame.place(rely=0.5, relwidth=1, relheight=0.5)
        self.action_cover_label = Label(self.action_frame, bg="light green")
        self.action_cover_label.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.actor_label = Label(self.action_frame, text="Actor: ", font=("Courier", 12), bd=3)
        self.actor_label.place(relwidth=1, relheight=0.06)

        self.new_round_label = Label(self.action_frame, text="New Round?", font=("Courier", 9), bd=3)
        self.new_round_label.place(relx=0.8, rely=0.05, relheight=0.1, relwidth=0.2)
        self.button_y = Button(self.action_frame, text="Yes", command=lambda: self.action_input("yes"))
        self.button_y.place(relx=0.8, rely=0.15, relheight=0.1, relwidth=0.2)
        self.button_n = Button(self.action_frame, text="No", command=lambda: self.action_input("no"))
        self.button_n.place(relx=0.8, rely=0.25, relheight=0.1, relwidth=0.2)

        self.raise_entry = Entry(self.action_frame, font=("Courier", 9), bd=3)
        self.raise_entry.place(relx=0, rely=1, relheight=0.12, relwidth=0.22, anchor="sw")
        self.raise_button = Button(self.action_frame, text="RAISE", font=("Courier", 9), bd=3, command=lambda: self.action_input(self.raise_entry.get()))
        self.raise_button.place(relx=0.22, rely=1, relheight=0.12, relwidth=0.22, anchor="sw")

        self.winner_label = Label(self.action_frame, font=("Courier", 12), bd=3)
        self.winner_label.place(relx=0, rely=(1/3), relwidth=0.75, relheight=0.3)

    def update(self, game):
        self.new_round_label.lower(self.action_cover_label)
        self.button_y.lower(self.action_cover_label)
        self.button_n.lower(self.action_cover_label)
        self.raise_entry.lower(self.action_cover_label)
        self.raise_button.lower(self.action_cover_label)
        self.winner_label.lower(self.action_cover_label)
        if self.restart:
            card1 = ImageTk.PhotoImage(Image.open(str("cards\\default0.png")).resize((55, 85), Image.LANCZOS))
            self.cc_1.image = card1
            self.cc_1.configure(image=card1)

            card1 = ImageTk.PhotoImage(Image.open(str("cards\\default0.png")).resize((55, 85), Image.LANCZOS))
            self.cc_2.image = card1
            self.cc_2.configure(image=card1)

            card1 = ImageTk.PhotoImage(Image.open(str("cards\\default0.png")).resize((55, 85), Image.LANCZOS))
            self.cc_3.image = card1
            self.cc_3.configure(image=card1)

            card1 = ImageTk.PhotoImage(Image.open(str("cards\\default0.png")).resize((55, 85), Image.LANCZOS))
            self.cc_4.image = card1
            self.cc_4.configure(image=card1)

            card1 = ImageTk.PhotoImage(Image.open(str("cards\\default0.png")).resize((55, 85), Image.LANCZOS))
            self.cc_5.image = card1
            self.cc_5.configure(image=card1)
            self.restart = False            
        if game.round_ended:
            time.sleep(0.3)
            self.new_round_label.lift(self.action_cover_label)
            self.button_y.lift(self.action_cover_label)
            self.button_n.lift(self.action_cover_label)
            
            # Show all player cards at the end of the round
            for i in range(4):
                try:
                    if i < len(game.list_of_players) and len(game.list_of_players[i].cards) > 0:
                        # First card
                        card_attr = f"card1_p{i}"
                        if hasattr(self, card_attr):
                            card_path = f"cards\\{str(game.list_of_players[i].cards[0])}.png"
                            card_img = ImageTk.PhotoImage(Image.open(card_path).resize((55, 85), Image.LANCZOS))
                            getattr(self, card_attr).image = card_img
                            getattr(self, card_attr).configure(image=card_img)
                        
                        # Second card
                        if len(game.list_of_players[i].cards) > 1:
                            card_attr = f"card2_p{i}"
                            if hasattr(self, card_attr):
                                card_path = f"cards\\{str(game.list_of_players[i].cards[1])}.png"
                                card_img = ImageTk.PhotoImage(Image.open(card_path).resize((55, 85), Image.LANCZOS))
                                getattr(self, card_attr).image = card_img
                                getattr(self, card_attr).configure(image=card_img)
                except Exception as e:
                    print(f"Error loading cards for player {i} at round end: {e}")
            
            # Make sure all community cards are shown
            try:
                for i in range(min(5, len(game.cards))):
                    card_attr = f"cc_{i+1}"
                    if hasattr(self, card_attr):
                        card_path = f"cards\\{str(game.cards[i])}.png"
                        card_img = ImageTk.PhotoImage(Image.open(card_path).resize((55, 85), Image.LANCZOS))
                        getattr(self, card_attr).image = card_img
                        getattr(self, card_attr).configure(image=card_img)
            except Exception as e:
                print(f"Error loading community cards at round end: {e}")
                
            winners = []
            scores = []
            for player in game.list_of_players_not_out:
                if player.win:
                    winners.append(player)
                    scores.append(player.score)
            print(f"Winner is: {winners}")
            print(f"Scores: {scores}")
            if scores == [[]]:
                self.winner_label["text"] = "Winner: " + str(winners)
            else:
                try:
                    for player in game.list_of_players_not_out:
                        if player.win:
                            if player.score == max(scores):
                                self.winner_label["text"] = "Winner: " + str(winners) + "\n" + score_interpreter(player)
                except IndexError:
                    pass
            self.winner_label.lift(self.action_cover_label)

            self.restart = True

            return
        if game.need_raise_info:
            self.raise_entry.lift(self.action_cover_label)
            self.raise_button.lift(self.action_cover_label)
        try:
            card1 = ImageTk.PhotoImage(
                Image.open("cards\\" + str(game.cards[0]) + ".png").resize((55, 85), Image.LANCZOS))
            self.cc_1.image = card1
            self.cc_1.configure(image=card1)

            card1 = ImageTk.PhotoImage(
                Image.open("cards\\" + str(game.cards[1]) + ".png").resize((55, 85), Image.LANCZOS))
            self.cc_2.image = card1
            self.cc_2.configure(image=card1)

            card1 = ImageTk.PhotoImage(
                Image.open("cards\\" + str(game.cards[2]) + ".png").resize((55, 85), Image.LANCZOS))
            self.cc_3.image = card1
            self.cc_3.configure(image=card1)

            card1 = ImageTk.PhotoImage(
                Image.open("cards\\" + str(game.cards[3]) + ".png").resize((55, 85), Image.LANCZOS))
            self.cc_4.image = card1
            self.cc_4.configure(image=card1)

            card1 = ImageTk.PhotoImage(
                Image.open("cards\\" + str(game.cards[4]) + ".png").resize((55, 85), Image.LANCZOS))
            self.cc_5.image = card1
            self.cc_5.configure(image=card1)
        except IndexError:
            pass
        
        # Update player information
        try:
            self.name_label_p0["text"] = game.list_of_players[0]
            self.name_label_p1["text"] = game.list_of_players[1]
            self.name_label_p2["text"] = game.list_of_players[2]
            self.name_label_p3["text"] = game.list_of_players[3]
        except IndexError:
            pass
        
        try:
            self.chips_label_p0["text"] = "Chips:\n" + str(game.list_of_players[0].chips)
            self.chips_label_p1["text"] = "Chips:\n" + str(game.list_of_players[1].chips)
            self.chips_label_p2["text"] = "Chips:\n" + str(game.list_of_players[2].chips)
            self.chips_label_p3["text"] = "Chips:\n" + str(game.list_of_players[3].chips)
        except IndexError:
            pass
        
        # Update player cards - modified to only show current player's cards
        try:
            # First set all cards to default (face down)
            default_card_img = ImageTk.PhotoImage(Image.open("cards\\default0.png").resize((55, 85), Image.LANCZOS))
            
            for i in range(4):
                if hasattr(self, f"card1_p{i}"):
                    getattr(self, f"card1_p{i}").image = default_card_img
                    getattr(self, f"card1_p{i}").configure(image=default_card_img)
                
                if hasattr(self, f"card2_p{i}"):
                    getattr(self, f"card2_p{i}").image = default_card_img
                    getattr(self, f"card2_p{i}").configure(image=default_card_img)
            
            # Now show only the current player's cards
            current_player_index = game.list_of_players.index(game.acting_player)
            
            if current_player_index < 4 and len(game.acting_player.cards) > 0:
                # First card
                card_attr = f"card1_p{current_player_index}"
                if hasattr(self, card_attr):
                    card_path = f"cards\\{str(game.acting_player.cards[0])}.png"
                    card_img = ImageTk.PhotoImage(Image.open(card_path).resize((55, 85), Image.LANCZOS))
                    getattr(self, card_attr).image = card_img
                    getattr(self, card_attr).configure(image=card_img)
                
                # Second card
                if len(game.acting_player.cards) > 1:
                    card_attr = f"card2_p{current_player_index}"
                    if hasattr(self, card_attr):
                        card_path = f"cards\\{str(game.acting_player.cards[1])}.png"
                        card_img = ImageTk.PhotoImage(Image.open(card_path).resize((55, 85), Image.LANCZOS))
                        getattr(self, card_attr).image = card_img
                        getattr(self, card_attr).configure(image=card_img)
                        
        except Exception as e:
            print(f"Error in player card loading: {e}")
        
        # Update pot and actor information
        self.pot_label["text"] = "Pot: " + str(game.pot)
        if game.game_over:
            self.actor_label["text"] = "Winner!: " + str(game.winner.name)
            return
        print(f"round ended {game.round_ended}")

        self.actor_label["text"] = str(game.acting_player.name)

        variable = StringVar(self.action_frame)
        variable.initialize("ACTION")
        w = OptionMenu(self.action_frame, variable, *game.possible_responses)
        w.place(relx=0, rely=0.05, relheight=0.1, relwidth=0.3)
        button_go = Button(self.action_frame, text="GO", font=("Courier", 10), command=lambda: self.action_input(variable.get()))
        button_go.place(relx=1, rely=1, relheight=0.3, relwidth=0.3, anchor="se")

    def action_input(self, entry0):
        if self.globals_dict:
            response_q = self.globals_dict.get('response_q')
            game_event = self.globals_dict.get('game_event')
            game_info_q = self.globals_dict.get('game_info_q')
            
            if response_q and game_event:
                response_q.put(entry0)
                game_event.set()
                time.sleep(0.1)
                if game_info_q and not game_info_q.empty():
                    self.update(game_info_q.get())