import random
import tkinter as tk

class cards():
    def __init__(self):
        self.card_symbol = ["Cloves", "Diamonds", "Hearts", "Spades"]
        self.deck = []
    
    def create_deck(self):
        royals = ["Jack", "Queen", "King", "Ace"]
        for suit in self.card_symbol:
            for num in range(2, 11):
                self.deck.append(f"{num} of {suit}")
            for royal in royals:
                self.deck.append(f"{royal} of {suit}")

        

    def show_deck(self):
        for i in self.deck:
            print(f"{i}")

    def shuffle_deck(self):
        for i in range(1,10):
            for k in range(1, len(self.deck) - 1):
                r = random.randint(0,len(self.deck) - 1)
                l = self.deck[r]
                self.deck[r] = self.deck[k]
                self.deck[k] = l
    def get_rid_used_cards(self, *args):
        for i in args:
            self.deck.remove(i)

    def give_hand(self):
        i = random.randint(0,len(self.deck) - 1)
        k = random.randint(0,len(self.deck) - 1)
        while i == k:
            k = random.randint(0,len(self.deck) - 1)
        return self.deck[i],self.deck[k]
    
    def delete_deck(self):
        self.deck = []
    def give_flop(self):
        flop = []
        for i in range(0,4):
            flop.append(self.deck[i])
        return flop[0],flop[1],flop[2]
        #fourth and fifth cards
    def give_BR(self):
        BR = []
        BR.append(self.deck[0])
        return BR[0]
    def burn(self):
        self.deck.pop(0)
        print("Burning card...")

class Poker:                    #default blinds 5/10
    def __init__(self):
        self.players = []
        self.small_blind = 10
        self.big_blind = 20
        self.pot_size = 0
        self.game_state = "Pre-Flop"
        self.round = 1
        self.player_turn = 0
        self.community_cards = []
    
    def add_player(self, player):
        self.players.append(player)
    def add_comminity_cards(self, cards):
        for i in cards:
            self.community_cards.append(i)
    def show_community_cards(self):
        for i in self.community_cards:
            print(f"{i}", end=", ")
        print()
    def change_blind_state(self):
        blind_states = []
        for i in self.players:
            blind_states.append(i.blind_state)
        for k in range(0, len(blind_states)):
            if blind_states[k] == 1:
                blind_states[k] = 0
                blind_states[k-1] = 1
            elif blind_states[k] == 2:
                blind_states[k] = 1
                blind_states[k-1] = 2
            else:
                blind_states[k] = 0

    def give_blinds(self):
        m = random.randint(0, len(self.players) - 1)
        for i in self.players:
            if i == m:
                i.blind_state = 1
            elif i == m + 1:
                i.blind_state = 2
            else:
                i.blind_state = 0
        for i in self.players:
            if i.blind_state == 1:
                print(f"{i.name} is small blind!")
                i.pot_state()
                self.pot_size += self.small_blind
                i.reduce_balance(self.small_blind)
            elif i.blind_state == 2:
                print(f"{i.name} is big blind!")
                i.pot_state()
                self.pot_size += self.big_blind
                i.reduce_balance(self.big_blind)
        for i in range(0, len(self.players)):
            if self.players[i].blind_state == 2:
                self.player_turn[i+1] = self.players[i].turn == 1
                
    
    def bet_round(self):
        for i in self.players:
            if i.turn == 1:
                print(f"{i.name} it's your turn!")
                print("Your hand:")
                i.show_hand()
                print("Your balance:")
                i.show_balance()
                print("Pot size: " + str(self.pot_size))
                print("Betting...")
                #here
                x = input("Do you want to call, raise or fold? (c/r/f)")
                if x == "c":
                    i.reduce_balance(self.pot_size)
                    self.pot_size += self.pot_size
                elif x == "r":
                    y = int(input("How much do you want to raise?"))
                    i.raise_pot(y)
                    self.pot_size += y
                elif x == "f":
                    i.folded = True
                else:
                    print("Invalid input!")
                    continue
       
    
   
    
class player:
    def __init__(self, name):
        self.name = name
        self.__balance = 1000
        self.__hand = []
        self.blind_state = 2
        self.turn = 0
        self.__hand_worth = 0
        self.folded = False
    def add_hand(self, hands):
        for i in hands:
            self.__hand.append(i)
    def reduce_balance(self, ammount):
        self.__balance -= ammount
            
    def show_hand(self):
        for i in self.__hand:
            print(f"{i}")
    def get_hand(self):
        return self.__hand
    def show_balance(self):
        print(self.__balance)
    def raise_pot(self, ammount):
        self.__balance -= ammount
    def pot_state(self):
        self.__balance -= self.blind_state
    def Get_final_Hand(self, cc, hand):
        total_hand = []
        for i in cc:
            total_hand.append(i)
        for k in hand:
            total_hand.append(k)
        return total_hand
    def sort_by_Suit(self, almost_final_hand):
        final_hand = []
        for i in almost_final_hand:
            if i[-3:] == "ves":
                final_hand.append(i)
            if i[-3:] == "nds":
                final_hand.append(i)
            if i[-3:] == "rts":
                final_hand.append(i)
            if i[-3:] == "des":
                final_hand.append(i)
        return final_hand

    def sort_by_number(self, total_hand):
        updated_cards = []
        for i in total_hand:
            if i[0] == "J":
                x = i.replace("Jack", "11")
                updated_cards.append(x)
            elif i[0] == "Q":
                x = i.replace("Queen", "12")
                updated_cards.append(x)
            elif i[0] == "K":
                x = i.replace("King", "13")
                updated_cards.append(x)
            elif i[0] == "A":
                x = i.replace("Ace", "14")
                updated_cards.append(x)
            else:
                updated_cards.append(i)
        new_cards = updated_cards.split(" ",1)
        for i in new_cards:
            i[0] = int(i[0])
        new_cards.sort()
        return new_cards
    def if_flush(self, final_hand):
        x = final_hand[0]
        y = final_hand[1]
        z = final_hand[2]
        a = final_hand[3]
        b = final_hand[4]
        c = final_hand[5]
        d = final_hand[6]
        flush = False
        for i in final_hand:
            if (x[-3:]  == y[-3:] and y[-3:] == z[-3:] and z[-3:] == a[-3:] and a[-3:] == b[-3:] ) or (y[-3:] == z[-3:] and z[-3:] == a[-3:] and a[-3:] == b[-3:] and b[-3:] == c[-3:]) or (z[-3:] == a[-3:] and a[-3:] == b[-3] and b[-3:] == c[-3:] and c[-3:] == d[-3:] ):
                flush = True
            else:
                flush = False
        return flush

    def check_hand_worth(self, total_hand):

        final_hand = self.sort_final_hand(total_hand)
        #index
        flush = self.if_flush(final_hand)
        if (flush): #Flush
            self.__hand_worth = 50



def poker_game():
    game_run = True
    game_start = True
    while game_start:
        x = int(input("How many players? (2-10)" ))
        if x >= 2 and x <= 10:
            playerID = []
            pass
        else:
            continue
        for i in range(0,x):
            name = input("Enter your name: " )
            playerID.append(player(name))
            print("Player: "+ str(name) + " has been added.")
        print("Players:")
        for i in playerID:
            print(i.name)
        game_start = False
        while game_run:

            print()
            print("Starting game...")
            print("Dealing cards...") 
            c = cards()
            c.create_deck()
            c.shuffle_deck()
            for i in playerID:
                j,k = c.give_hand()
                hand =  []
                hand.append(j)
                hand.append(k)
                i.add_hand(hand)
                c.get_rid_used_cards(j,k)
            Game = Poker()

            for i in playerID:
                Game.add_player(i)
            Game.bet_round()
            print("Dealing flop...")
            c.burn()
            q,w,e = c.give_flop()
            c.get_rid_used_cards(q,w,e)
            Game.add_comminity_cards(q)
            Game.add_comminity_cards(w)
            Game.add_comminity_cards(e)
            Game.show_community_cards()
            c.burn()
            print("Dealing Bridge...")
            br = c.give_BR()
            c.get_rid_used_cards(br)
            Game.add_comminity_cards(br)
            Game.show_community_cards()
            c.burn()
            print("Dealing River...")
            ri = c.give_BR()
            c.get_rid_used_cards(ri)
            Game.add_comminity_cards(ri)
            Game.show_community_cards()
            print("Time to Compare hands!")
            for i in playerID:
                total_hand = i.Get_final_Hand(Game.community_cards, i.get_hand())
                print(f"{i.name} hand:")
                i.show_hand()
                print("Community cards:")
                Game.show_community_cards()
                print("Final hand:")
                i.Get_final_Hand(Game.community_cards, i.get_hand())
                i.sort_final_hand(total_hand)
                print("Hand worth: " + str(i.check_hand_worth(total_hand)))
            c.delete_deck()
            exit = input("Do you want to exit? (y/n)")
            if exit == "y":
                game_run = False
                print("Exiting game...")
            else:
                continue
poker_game()




            

    