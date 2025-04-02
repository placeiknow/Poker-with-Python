import time
import itertools
from collections import Counter
from logic.deck import StandardDeck
from logic.player import Player
from utils.helpers import ask_app, score_interpreter

class Game(object):
    def __init__(self):
        self.need_raise_info = False
        self.game_over = False
        self.acting_player = Player()
        self.possible_responses = []
        self.round_counter = 0
        self.cards = []
        self.pot = 0
        self.pot_dict = {}
        self.pot_in_play = 0
        self.list_of_player_names = []
        self.dealer = Player()
        self.small_blind = Player()
        self.big_blind = Player()
        self.first_actor = Player()
        self.winners = []
        self.deck = StandardDeck()
        self.list_of_scores_from_eligible_winners = []
        self.setup = ask_app("Start?")
        while True:
            try:
                self.number_of_players = len(self.setup["players"])
                break
            except ValueError:
                print("Invalid response")
        if 1 < self.number_of_players < 11:
            pass
        else:
            print("Invalid number of players")
            from main import main
            main()
        self.list_of_players = [Player(name) for name in self.setup["players"] if name != ""]
        while True:
            try:
                self.starting_chips = int(self.setup["chips"][0])
                if self.starting_chips > 0:
                    break
                print("Invalid number, try greater than 0")
            except ValueError:
                print("Invalid response")
                continue
        for player in self.list_of_players:
            player.chips = self.starting_chips
        self.ready_list = []
        while True:
            try:
                self.small_blind_amount = int(self.setup["chips"][1])
                if self.starting_chips > self.small_blind_amount > 0:
                    break
                print("Invalid number: try bigger than zero, smaller than starting chips")
            except ValueError:
                print("Invalid response")
                continue
        while True:
            try:
                self.big_blind_amount = int(self.setup["chips"][2])
                if self.starting_chips > self.big_blind_amount > self.small_blind_amount:
                    break
                print("Invalid number: try bigger than small blind, smaller than starting chips")
            except ValueError:
                print("Invalid response")
                continue
        self.winner = None
        self.action_counter = 0
        self.attribute_list = ["d", "sb", "bb", "fa"]
        self.highest_stake = 0
        self.fold_list = []
        self.not_fold_list = []
        self.round_ended = False
        self.fold_out = False
        self.list_of_scores_eligible = []
        self.list_of_players_not_out = list(set(self.list_of_players))
        self.number_of_player_not_out = int(len(list(set(self.list_of_players))))

    def print_game_info(self):
        pass

    def print_round_info(self):
        print("\n")
        for player in self.list_of_players:
            print("\n")
            print(f"Name: {player.name}")
            print(f"Cards: {player.cards}")
            print(f"Player score: {player.score}")
            print(f"Chips: {player.chips}")
            print(f"Special Attributes: {player.list_of_special_attributes}")
            if player.fold:
                print(f"Folded")
            if player.all_in:
                print(f"All-in")
            print(f"Stake: {player.stake}")
            print(f"Stake-gap: {player.stake_gap}")
            print("\n")
        print(f"Pot: {self.pot}")
        print(f"Community cards: {self.cards}")
        print("\n")

    def establish_player_attributes(self):
        address_assignment = 0
        self.dealer = self.list_of_players_not_out[address_assignment]
        self.dealer.list_of_special_attributes.append("dealer")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.small_blind = self.list_of_players_not_out[address_assignment]
        self.small_blind.list_of_special_attributes.append("small blind")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.big_blind = self.list_of_players_not_out[address_assignment]
        self.big_blind.list_of_special_attributes.append("big blind")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.first_actor = self.list_of_players_not_out[address_assignment]
        self.first_actor.list_of_special_attributes.append("first actor")
        self.list_of_players_not_out.append(self.list_of_players_not_out.pop(0))

    def deal_hole(self):
        for player in self.list_of_players_not_out:
            self.deck.deal(player, 2)

    def deal_flop(self):
        self.deck.burn()
        self.deck.deal(self, 3)

    def deal_turn(self):
        self.deck.burn()
        print("\n--card burned--")
        self.deck.deal(self, 1)
        print(f"\nCommunity Cards: {self.cards}")

    def deal_river(self):
        self.deck.burn()
        print("\n--card burned--")
        self.deck.deal(self, 1)
        print(f"\n\nCommunity Cards: {self.cards}")

    def hand_scorer(self, player):
        seven_cards = player.cards + self.cards
        all_hand_combos = list(itertools.combinations(seven_cards, 5))
        list_of_all_score_possibilities = []
        for i in all_hand_combos:
            suit_list = []
            value_list = []
            for j in i:
                suit_list.append(j.suit)
                value_list.append(j.value)
            initial_value_check = list(reversed(sorted(value_list)))
            score1 = 0
            score2 = 0
            score3 = 0
            score4 = initial_value_check.pop(0)
            score5 = initial_value_check.pop(0)
            score6 = initial_value_check.pop(0)
            score7 = initial_value_check.pop(0)
            score8 = initial_value_check.pop(0)
            list_of_pair_values = []
            other_cards_not_special = []
            pair_present = False
            pair_value = int
            value_counter = dict(Counter(value_list))
            for value_name, count in value_counter.items():
                if count == 2:
                    pair_present = True
                    pair_value = value_name
                    list_of_pair_values.append(value_name)
            if pair_present:
                for value in value_list:
                    if value not in list_of_pair_values:
                        other_cards_not_special.append(value)
                other_cards_not_special = list(reversed(sorted(other_cards_not_special)))
                if len(set(list_of_pair_values)) == 1:
                    score1 = 1
                    score2 = max(list_of_pair_values)
                    try:
                        score3 = other_cards_not_special.pop(0)
                        score4 = other_cards_not_special.pop(0)
                        score5 = other_cards_not_special.pop(0)
                        score6 = other_cards_not_special.pop(0)
                        score7 = other_cards_not_special.pop(0)
                        score8 = other_cards_not_special.pop(0)
                    except IndexError:
                        pass
                if len(set(list_of_pair_values)) == 2:
                    list_of_pair_values = list(reversed(sorted(list_of_pair_values)))
                    score1 = 2
                    score2 = list_of_pair_values.pop(0)
                    score3 = list_of_pair_values.pop(0)
                    try:
                        score4 = other_cards_not_special.pop(0)
                        score5 = other_cards_not_special.pop(0)
                        score6 = other_cards_not_special.pop(0)
                        score7 = other_cards_not_special.pop(0)
                        score8 = other_cards_not_special.pop(0)
                    except IndexError:
                        pass
            three_of_a_kind_value = int
            other_cards_not_special = []
            three_of_a_kind_present = False
            for value_name, count in value_counter.items():
                if count == 3:
                    three_of_a_kind_present = True
                    three_of_a_kind_value = value_name
            if three_of_a_kind_present:
                for value in value_list:
                    if value != three_of_a_kind_value:
                        other_cards_not_special.append(value)
                other_cards_not_special = list(reversed(sorted(other_cards_not_special)))
                score1 = 3
                score2 = three_of_a_kind_value
                try:
                    score3 = other_cards_not_special.pop(0)
                    score4 = other_cards_not_special.pop(0)
                    score5 = other_cards_not_special.pop(0)
                    score6 = other_cards_not_special.pop(0)
                    score7 = other_cards_not_special.pop(0)
                    score8 = other_cards_not_special.pop(0)
                except IndexError:
                    pass
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)):
                score1 = 4
                score2 = max(value_list)
            if sorted(value_list) == [0, 1, 2, 3, 12]:
                score1 = 4
                score2 = 3
            if len(set(suit_list)) == 1:
                score1 = 5
                score2 = max(value_list)
            if three_of_a_kind_present and pair_present:
                score1 = 6
                score2 = three_of_a_kind_value
                score3 = pair_value
            four_of_a_kind_value = int
            other_card_value = int
            four_of_a_kind = False
            for value_name, count in value_counter.items():
                if count == 4:
                    four_of_a_kind_value = value_name
                    four_of_a_kind = True
            for value in value_list:
                if value != four_of_a_kind_value:
                    other_card_value = value
            if four_of_a_kind:
                score1 = 7
                score2 = four_of_a_kind_value
                score3 = other_card_value
            if sorted(value_list) == [0, 1, 2, 3, 12] and len(set(suit_list)) == 1:
                score1 = 8
                score2 = 3
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)) and len(set(suit_list)) == 1:
                score1 = 8
                score2 = max(value_list)
                if max(value_list) == 12:
                    score1 = 9
            list_of_all_score_possibilities.append([score1, score2, score3, score4, score5, score6, score7, score8])
        best_score = max(list_of_all_score_possibilities)
        player.score = best_score

    def score_all(self):
        for player in self.list_of_players_not_out:
            self.hand_scorer(player)

    def find_winners(self):
        if self.fold_out:
            for player in list(set(self.winners)):
                player.chips += int((self.pot / len(list(set(self.winners)))))
                print(f"{player.name} wins {int((self.pot / len(list(set(self.winners)))))} chips!")
        else:
            list_of_stakes = []
            for player in self.list_of_players_not_out:
                list_of_stakes.append(player.stake)
            list_of_stakes = list(set(list_of_stakes))
            list_of_stakes = sorted(list_of_stakes)
            for stake in list_of_stakes:
                print(stake)
            for player in self.list_of_players_not_out:
                print(player.name)
                print(player.stake)
            print(self.list_of_players_not_out)
            list_of_players_at_stake = []
            list_of_list_of_players_at_stake = []
            for i in range(len(list_of_stakes)):
                for player in self.list_of_players_not_out:
                    if player.stake >= list_of_stakes[i]:
                        list_of_players_at_stake.append(player)
                list_of_list_of_players_at_stake.append(list(set(list_of_players_at_stake)))
                list_of_players_at_stake.clear()
            print(list_of_list_of_players_at_stake)
            list_of_pot_seeds = []
            for i in list_of_stakes:
                list_of_pot_seeds.append(i)
            list_of_pot_seeds.reverse()
            for i in range(len(list_of_pot_seeds)):
                try:
                    list_of_pot_seeds[i] -= list_of_pot_seeds[i + 1]
                except IndexError:
                    pass
            list_of_pot_seeds.reverse()
            list_of_pots = []
            for i in range(len(list_of_pot_seeds)):
                print(len(list_of_list_of_players_at_stake[i]))
            for i in range(len(list_of_pot_seeds)):
                list_of_pots.append(list_of_pot_seeds[i] * len(list_of_list_of_players_at_stake[i]))
            for i in range(len(list_of_pots)):
                winners = []
                self.list_of_scores_eligible.clear()
                for player in list_of_list_of_players_at_stake[i]:
                    if player.fold:
                        pass
                    else:
                        self.list_of_scores_eligible.append(player.score)
                max_score = max(self.list_of_scores_eligible)
                for player in list_of_list_of_players_at_stake[i]:
                    if player.fold:
                        pass
                    else:
                        if player.score == max_score:
                            player.win = True
                            winners.append(player)
                prize = int(list_of_pots[i] / len(winners))
                for player in winners:
                    print(f"{player.name} wins {prize} chips!")
                    player.chips += prize
                    self.pot -= prize
            for player in self.list_of_players_not_out:
                if player.win:
                    print(
                        "\n" + player.name + ": " + str(
                            player.cards) + "\t<-WINNER WINNER WINNER WINNER WINNER WINNER "
                                            "WINNER WINNER" + "\n\t" + score_interpreter(player))
                elif player.fold:
                    print("\n" + player.name + ": " + str(player.cards) + "\n\t" + "[FOLDED]")
                else:
                    print("\n" + player.name + ": " + str(player.cards) + "\n\t" + score_interpreter(player))
                print(f"\tScoreCode: {player.score}")
                print(f"Pot: {self.pot}")
            [print(player.name, player.chips) for player in self.list_of_players_not_out]

    def clear_board(self):
        self.possible_responses.clear()
        self.cards.clear()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.pot = 0
        self.pot_dict.clear()
        self.winners.clear()
        self.list_of_scores_from_eligible_winners.clear()
        self.action_counter = 0
        self.highest_stake = 0
        self.fold_list.clear()
        self.not_fold_list.clear()
        self.fold_out = False
        self.list_of_scores_eligible.clear()
        self.round_ended = False
        for player in self.list_of_players:
            player.score.clear()
            player.cards.clear()
            player.stake = 0
            player.stake_gap = 0
            player.ready = False
            player.all_in = False
            player.fold = False
            player.list_of_special_attributes.clear()
            player.win = False

    def end_round(self):
        self.list_of_players_not_out = list(set(self.list_of_players_not_out))
        for player in self.list_of_players_not_out:
            if player.chips <= 0:
                self.list_of_players_not_out.remove(player)
                print(f"{player.name} is out of the game!")
        self.number_of_player_not_out = len(set(self.list_of_players_not_out))
        if self.number_of_player_not_out == 1:
            self.game_over = True
            self.winner = self.list_of_players_not_out[0]
            print(f"Game is over: {self.winner} wins with {self.winner.chips}!")
            quit()
        new_round = str(ask_app("Start a new round? (yes/no)"))
        if new_round == "yes":
            print("\n\n\t\t\t\t--ROUND OVER--")
            print("\n\n\t\t\t--STARTING NEW ROUND--\n")
            self.round_counter += 1
            pass
        else:
            quit()
        time.sleep(0.3)
        self.clear_board()

    def answer(self, player):
        player.stake_gap = self.highest_stake - player.stake
        if player.all_in or player.fold or self.fold_out:
            return True
        if player.chips <= 0:
            print(f"{player.name} is all in!")
            player.all_in = True
        print(f"Highest stake: {self.highest_stake}")
        print(f"Put in at least {player.stake_gap} to stay in.\nDon't Have that much? You'll have to go all-in!")
        print(f"Chips available: {player.chips}")
        self.possible_responses.clear()
        if player.stake_gap > 0:
            self.possible_responses.append("fold")
            if player.stake_gap == player.chips:
                self.possible_responses.append("all_in_exact")
            if player.stake_gap > player.chips:
                self.possible_responses.append("all_in_partial")
            if player.stake_gap < player.chips:
                self.possible_responses.append("call_exact")
                self.possible_responses.append("call_and_raise")
                self.possible_responses.append("call_and_all_in")
        if player.stake_gap == 0:
            self.possible_responses.append("check")
            self.possible_responses.append("raise")
            self.possible_responses.append("fold")
            self.possible_responses.append("all_in")
        while True:
            print(self.possible_responses)
            response = str(ask_app(f"{player}'s action\n->", self))
            if response not in self.possible_responses:
                print("Invalid response")
                continue
            if response == "all_in_partial":
                player.stake += player.chips
                self.pot += player.chips
                player.stake_gap -= player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                return True
            if response == "all_in_exact":
                print(f"{player.name} is all-in!")
                player.all_in = True
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips = 0
                player.stake_gap = 0
                return True
            if response == "fold":
                player.fold = True
                self.fold_list.append(player)
                if len(self.fold_list) == (len(self.list_of_players_not_out) - 1):
                    for player in self.list_of_players_not_out:
                        if player not in self.fold_list:
                            self.fold_out = True
                            print(f"{player} wins!")
                            self.winners.append(player)
                            for player in self.winners:
                                player.win = True
                            self.round_ended = True
                return True
            if response == "call_exact":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                return True
            if response == "check":
                player.stake_gap = 0
                return True
            if response == "raise":
                self.need_raise_info = True
                while True:
                    bet = int(
                        ask_app(f"How much would {player.name} like to raise? ({player.chips} available)\n->",
                                self))
                    if bet > player.chips or bet <= 0:
                        print("Invalid response")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} is all-in!")
                        player.all_in = True
                    self.need_raise_info = False
                    player.stake += bet
                    self.pot += bet
                    player.chips -= bet
                    self.highest_stake = player.stake
                    self.ready_list.clear()
                    player.stake_gap = 0
                    return True
            if response == "call_and_raise":
                self.need_raise_info = True
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                while True:
                    try:
                        bet = int(
                            ask_app(f"How much would {player.name} like to raise? ({player.chips} available)\n->",
                                    self))
                    except ValueError:
                        continue
                    if bet > player.chips or bet <= 0:
                        print("Invalid response")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} is all-in!")
                        player.all_in = True
                    self.need_raise_info = False
                    player.stake += bet
                    self.pot += bet
                    player.chips -= bet
                    self.highest_stake = player.stake
                    self.ready_list.clear()
                    return True
            if response == "call_and_all_in":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                player.stake += player.chips
                self.pot += player.chips
                player.stake_gap -= player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                self.highest_stake = player.stake
                self.ready_list.clear()
                return True
            if response == "all_in":
                player.stake_gap = 0
                player.stake += player.chips
                self.pot += player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                self.highest_stake = player.stake
                self.ready_list.clear()
                return True
            print("Invalid Response")

    def ask_players(self):
        self.ready_list.clear()
        starting_index = self.list_of_players_not_out.index(self.first_actor)
        for player in self.list_of_players_not_out:
            player.ready = False
        while True:
            self.acting_player = self.list_of_players_not_out[starting_index]
            player_ready = self.answer(self.list_of_players_not_out[starting_index])
            starting_index += 1
            starting_index %= len(self.list_of_players_not_out)
            if player_ready:
                self.ready_list.append("gogo")
            if len(self.ready_list) == len(self.list_of_players_not_out):
                break

    def act_one(self):
        if self.small_blind_amount > self.small_blind.chips:
            self.small_blind.stake += self.small_blind.chips
            self.highest_stake = self.small_blind.chips
            self.pot += self.small_blind.chips
            self.small_blind.chips = 0
            print(f"{self.small_blind.name} is all-in!")
            self.small_blind.all_in = True
        else:
            self.small_blind.chips -= self.small_blind_amount
            self.small_blind.stake += self.small_blind_amount
            self.highest_stake = self.small_blind_amount
            self.pot += self.small_blind_amount
        if self.big_blind_amount > self.big_blind.chips:
            self.big_blind.stake += self.big_blind.chips
            self.highest_stake = self.big_blind.chips
            self.pot