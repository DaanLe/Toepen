import numpy as np
from tqdm import tqdm
import random
from copy import deepcopy
import itertools
from Infoset import Infoset


class MCCFR:
    """Class to run the MCCFR algorithm."""

    def __init__(self, game, abstraction_function):
        """Initialize a game, a dictionary containing the strategy profile and an abstraction function."""
        self.game = game
        self.infoset_dict = {}
        self.abstraction_function = abstraction_function
        self.infoset_data = (self.infoset_dict, self.abstraction_function)

    def get_infoset(self, info_key):
        """Create an infoset if needed and return."""
        if info_key not in self.infoset_dict:
            self.infoset_dict[info_key] = Infoset(info_key)
        return self.infoset_dict[info_key]

    def comb(self, n, k):
        """Function which returns the number of combinations."""
        m = 0
        if k == 0:
            m = 1
        if k == 1:
            m = n
        if k >= 2:
            num, dem, op1, op2 = 1, 1, k, n
            while (op1 >= 1):
                num *= op2
                dem *= op1
                op1 -= 1
                op2 -= 1
            m = num // dem
        return m

    def get_info_key(self, game_state):
        """Function which generates an info_key, given a game_state. First the suits are abstracted using the
        suit dict, after which the abstraction function is used for further abstraction."""

        possible_action = self.game.get_possible_actions(game_state)
        possible_action_len = len(possible_action)
        new_hand, new_hist = self.game.translate_suits(game_state)
        abs_hand, abs_hist = self.abstraction_function(new_hand, new_hist, possible_action, self.game.mean)
        key = (game_state[0], frozenset(abs_hand), abs_hist, possible_action_len)
        return key

    def chance_cfr(self, game_state, reach_probs):
        """Recursive function for chance sampled MCCFR."""

        # Base case
        if game_state[3]:
            return game_state[4]

        possible_actions = self.game.get_possible_actions(game_state)
        counterfactual_values = np.zeros(len(possible_actions))
        payoff = -1

        # If only 1 possible action, no strategy required.
        if len(possible_actions) == 1:
            next_game_state = self.game.get_next_game_state(game_state, possible_actions[0])
            if game_state[0] == next_game_state[0]:
                payoff = 1
            node_value = payoff * self.chance_cfr(next_game_state, reach_probs)

        else:
            player = game_state[0]
            opponent = (player + 1) % 2
            info_key = self.get_info_key(game_state)
            infoset = self.get_infoset(info_key)

            strategy = infoset.regret_matching()
            infoset.update_strategy_sum(reach_probs[player])
            for ix, action in enumerate(possible_actions):
                action_prob = strategy[ix]

                # Compute new reach probabilities after this action
                new_reach_probs = reach_probs.copy()
                new_reach_probs[player] *= action_prob

                # recursively call MCCFR
                next_game_state = self.game.get_next_game_state(game_state, action)
                if game_state[0] == next_game_state[0]:
                    payoff = 1
                counterfactual_values[ix] = payoff * self.chance_cfr(next_game_state, new_reach_probs)

            # Value of the current game state is counterfactual values weighted by the strategy
            node_value = counterfactual_values.dot(strategy)

            for ix, action in enumerate(possible_actions):
                infoset.cumulative_regrets[ix] += reach_probs[opponent] * (counterfactual_values[ix] - node_value)
        return node_value

    def external_cfr(self, game_state, reach_probs, update_player):
        """Recursive function for external sampled MCCFR."""

        # Base case
        if game_state[3]:
            return game_state[4]

        possible_actions = self.game.get_possible_actions(game_state)
        counterfactual_values = np.zeros(len(possible_actions))
        payoff = -1

        # If only 1 possible action, no strategy required.
        if len(possible_actions) == 1:
            next_game_state = self.game.get_next_game_state(game_state, possible_actions[0])
            if game_state[0] == next_game_state[0]:
                payoff = 1
            node_value = payoff * self.external_cfr(next_game_state, reach_probs, update_player)

        else:
            player = game_state[0]
            opponent = (player + 1) % 2
            info_key = self.get_info_key(game_state)
            infoset = self.get_infoset(info_key)

            # External gets sampled
            if player != update_player:
                strategy = infoset.regret_matching()
                action = random.choices(possible_actions, strategy)[0]
                action_index = list(possible_actions).index(action)
                action_prob = strategy[action_index]

                # compute new reach probabilities after this action
                new_reach_probs = reach_probs.copy()
                new_reach_probs[player] *= action_prob

                next_game_state = self.game.get_next_game_state(game_state, action)
                if game_state[0] == next_game_state[0]:
                    payoff = 1
                node_value = payoff * self.external_cfr(next_game_state, new_reach_probs, update_player)

            else:
                strategy = infoset.regret_matching()
                infoset.update_strategy_sum(reach_probs[player])
                for ix, action in enumerate(possible_actions):
                    action_prob = strategy[ix]

                    # compute new reach probabilities after this action
                    new_reach_probs = reach_probs.copy()
                    new_reach_probs[player] *= action_prob

                    # recursively call MCCFR
                    next_game_state = self.game.get_next_game_state(game_state, action)
                    if game_state[0] == next_game_state[0]:
                        payoff = 1
                    counterfactual_values[ix] = payoff * self.external_cfr(next_game_state, new_reach_probs,
                                                                           update_player)

                # Value of the current game state is counterfactual values weighted by the strategy
                node_value = counterfactual_values.dot(strategy)

                for ix, action in enumerate(possible_actions):
                    infoset.cumulative_regrets[ix] += reach_probs[opponent] * (counterfactual_values[ix] - node_value)
        return node_value

    def train_chance(self, num_iterations):
        """Train chance mccfr by calling the recursive function, iteration number of times."""
        util = 0
        for _ in range(num_iterations):
            game_state = self.game.sample_new_game()
            reach_probs = np.ones(2)
            util += self.chance_cfr(game_state, reach_probs)
        return util / num_iterations

    def train_external(self, num_iterations):
        """Train external mccfr by calling the recursive function, iteration number of times."""
        util = 0
        for _ in tqdm(range(num_iterations)):
            for i in range(2):
                game_state = self.game.sample_new_game()
                reach_probs = np.ones(2)
                util += self.external_cfr(game_state, reach_probs, i)
        return util / (num_iterations * 2)

    def count_infosets(self):
        """Function which counts the number of information sets in the dict"""
        p1_count = len([x for x, _ in self.infoset_dict.items() if x[0] == 0])
        p2_count = len(self.infoset_dict.items()) - p1_count
        return p1_count, p2_count

    def evaluate_helper(self, game_state, reach_prob):
        """Function which recursively finds the expected utility."""

        # Base case
        if game_state[3]:
            return game_state[4]

        possible_actions = self.game.get_possible_actions(game_state)
        payoff = -1
        partial_values = np.zeros(len(possible_actions))

        # If only 1 possible action, no strategy required.
        if len(possible_actions) == 1:
            next_game_state = self.game.get_next_game_state(game_state, possible_actions[0])
            if game_state[0] == next_game_state[0]:
                payoff = 1
            node_value = payoff * self.evaluate_helper(next_game_state, reach_prob)

        else:
            info_key = self.get_info_key(game_state)
            infoset = self.get_infoset(info_key)

            strategy = infoset.get_average_strategy()
            for ix, action in enumerate(possible_actions):
                action_prob = strategy[ix]

                # compute new reach probabilities after this action
                new_reach_prob = reach_prob
                new_reach_prob *= action_prob

                # recursively call evaluate function
                next_game_state = self.game.get_next_game_state(game_state, action)
                if game_state[0] == next_game_state[0]:
                    payoff = 1
                partial_values[ix] = payoff * self.evaluate_helper(next_game_state, new_reach_prob)

            # Value of the current game state is counterfactual values weighted by the strategy
            node_value = partial_values.dot(strategy)
        return node_value

    def evaluate(self):
        """Evaluates the current infodict by multiplying the probabilities of the
        terminal notes with the utilities of those notes"""
        hand_prob = (self.comb(len(self.game.deck.deck2), self.game.handsize) *
                     self.comb(len(self.game.deck.deck2) - self.game.handsize, self.game.handsize))
        util = 0
        for dealt_cards in itertools.combinations(self.game.deck.deck2, self.game.handsize * 2):
            for hand1 in itertools.combinations(dealt_cards, self.game.handsize):
                hand2 = list(card for card in dealt_cards if card not in hand1)
                hands = [sorted(list(hand1)), sorted(hand2)]
                game_state = self.game.sample_new_game(hands=hands)

                reach_prob = 1
                util += self.evaluate_helper(game_state, reach_prob)
        return util / hand_prob

    def get_exploitability(self, num_iterations):
        """Use MCCFR to update just one player and evaluate after. Doing this for both players approximates the
        exploitability."""
        info_dict_copy = deepcopy(self.infoset_dict)
        for _ in range(num_iterations):
            game_state = self.game.sample_new_game()
            reach_probs = np.ones(2)
            self.external_cfr(game_state, reach_probs, 0)
        b_1 = self.evaluate()
        self.infoset_dict = deepcopy(info_dict_copy)
        for _ in range(num_iterations):
            game_state = self.game.sample_new_game()
            reach_probs = np.ones(2)
            self.external_cfr(game_state, reach_probs, 1)
        b_2 = self.evaluate()
        self.infoset_dict = deepcopy(info_dict_copy)
        return b_1 - b_2
