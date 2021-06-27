import random
from copy import deepcopy
import numpy as np


class Game:
    """Class which keeps track of the rules of the game."""

    def __init__(self, deck, handsize, bet):
        """Initialize a game for a given deck, handsize and betting type."""
        self.deck = deck
        self.handsize = handsize
        self.deck.reset_deck()

        # bet: 0 is no betting, 1 is only betting by the active player and 2 is full betting
        self.bet = bet
        self.mean = np.mean(deck.ranks)

    def suit_abstraction_dict(self, hand, identity=False):
        """Function to create a suit dict for card isomorphism. Each suit is mapped to an abstraction which
        is specific for the initial hand."""
        suits = self.deck.suit
        suit_abstraction = ('first', 'second', 'third', 'fourth')
        suit_dict = {}
        check_val = set()

        hand.sort(key=lambda x: x[1])

        for card in hand:
            if card[0] not in check_val:
                suit_dict[card[0]] = suit_abstraction[len(check_val)]
                check_val.add(card[0])
        for suit in suits:
            if suit not in check_val:
                suit_dict[suit] = suit_abstraction[len(check_val)]
                check_val.add(suit)
        if identity:
            suit_dict = {'clubs': 'first', 'diamonds': 'second', 'hearts': 'third', 'spades': 'fourth'}
        return suit_dict

    @staticmethod
    def translate_suits(game_state):
        """Function which translates all the suits in a game state, based on the suit dict."""
        suit_dict = game_state[5][game_state[0]]
        hand = game_state[1][game_state[0]]
        hist = game_state[2]
        new_hand = []
        new_hist = ()
        for card in hand:
            new_card = (suit_dict[card[0]], card[1])
            new_hand.append(new_card)
        for card in hist:
            if len(card) == 2:
                new_hist += ((suit_dict[card[0]], card[1]),)
            else:
                new_hist += (card,)
        return new_hand, new_hist

    def sample_new_game(self, hands=None):
        """Function to sample an initial game state with an empty history. Optionality to provide hands instead of
        uniformly sampling a hand. Game state has form:
        (active_player, hands, history, terminal, ante, suit_dicts, betting) where,
        active_player = 0 or 1 for player 0 or 1.
        hands = a list of lists, one for each player, containing cards which are tuples of the form: (suit, rank)
        history = tuple containing all actions in order
        terminal = boolean indicating whether the state is terminal
        ante = integer representing the ante of the game
        suit_dicts = list of suit_dicts, one for each player
        betting= integer, representing the betting type"""
        if hands:
            hands = [sorted(hands[0]), sorted(hands[1])]
            suit_dicts = [self.suit_abstraction_dict(hands[0]), self.suit_abstraction_dict(hands[1])]
            return (0, hands, (), False, 1, suit_dicts, 2)
        else:
            two_hands = random.sample(self.deck.deck2, 2 * self.handsize)
            hands = [sorted(two_hands[self.handsize:]), sorted(two_hands[:self.handsize])]
            suit_dicts = [self.suit_abstraction_dict(hands[0]), self.suit_abstraction_dict(hands[1])]
            return (0, hands, (), False, 1, suit_dicts, 2)

    def get_possible_actions(self, game_state):
        """Function which uses a game state to determine the possible actions as a list from this game state."""
        actions = sorted(game_state[1][game_state[0]])

        # Logic for a game without betting.
        if self.bet == 0:
            if len(game_state[2]) % 2 == 0:
                return actions
            else:

                # Players have to play the same suit, unless they can not.
                possible = [item for item in actions if item[0] == game_state[2][-1][0]]
                if len(possible) == 0:
                    return actions
                else:
                    return possible

        # Logic for games with betting. Round size is the number of actions in a round and Divisor is used as an index
        # for when players are allowed to bet.
        if self.bet == 1:
            divisor = 4
            round_size = 4
        else:
            divisor = 3
            round_size = 6

        if len(game_state[2]) % divisor == 0:
            if game_state[6] != game_state[0]:
                return ['Bet', 'Check']
            else:
                return ['Check']

        elif len(game_state[2]) % divisor == 1:
            if game_state[2][-1] == 'Check':
                return ['Check']
            else:
                return ['Call', 'Fold']

        elif self.bet == 1 and len(game_state[2]) % round_size == 2:
            return actions
        else:
            possible = [item for item in actions if item[0] == game_state[2][-1][0]]
            if len(possible) == 0:
                return actions
            else:
                return possible

    def get_next_game_state(self, game_state, action):
        """Function which returns a new game state, based on the previous game state and the action taken."""
        terminal = False
        ante = game_state[4]
        bet_id = game_state[6]

        # Prev_index, indicates where the previous card can be found in the history for the reacting player.
        if self.bet == 0:
            round_size = 2
            prev_index = -1
        elif self.bet == 1:
            round_size = 4
            prev_index = -1
        else:
            round_size = 6
            prev_index = -3

        if len(game_state[2]) == (round_size * self.handsize) - 1 or action == 'Fold':
            terminal = True

        if action == 'Call':
            ante += 1

        if action == 'Bet':
            bet_id = game_state[0]

        next_active_player = (game_state[0] + 1) % 2

        # The same player only plays twice in a row if she wins a round as a reacting player.
        if len(game_state[2]) % round_size == round_size - 1 and ((action[0] == game_state[2][prev_index][0]) and
                                                                  (game_state[2][prev_index][1] < action[1])):
            next_active_player = game_state[0]

        history = game_state[2] + (action,)
        next_hands = deepcopy(game_state[1])

        if self.bet == 0 or len(game_state[2]) % round_size in [2, round_size - 1]:
            next_hands[game_state[0]].remove(action)
        return (next_active_player, next_hands, history, terminal, ante, game_state[5], bet_id)

