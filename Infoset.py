import numpy as np


class Infoset:
    def __init__(self, info_key):
        """Info_key is a tuple containing:
        (active_player:int, activehand:frozenset, history:tuple(1st played... last played), bet)"""
        self.info_key = info_key
        # self.possible_actions = self.get_possible_actions()
        self.num_actions = info_key[3]
        self.cumulative_regrets = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.average_strategy = np.repeat(1 / self.num_actions, self.num_actions)

    # def get_possible_actions(self):
    #
    #     actions = sorted(list(self.info_key[1]))
    #     if self.info_key[3] == 0:
    #         if len(self.info_key[2]) % 2 == 0:
    #             return actions
    #         else:
    #             possible = [item for item in actions if item[0] == self.info_key[2][-1][0]]
    #             if len(possible) == 0:
    #                 return actions
    #             else:
    #                 return possible
    #
    #     # divisor = 1
    #     # round_size = 1
    #     if self.info_key[3] == 1:
    #         divisor = 4
    #         round_size = 4
    #     if self.info_key[3] == 2:
    #         divisor = 3
    #         round_size = 6
    #
    #     if len(self.info_key[2]) % divisor == 0:
    #         return ['Bet', 'Check']
    #
    #     elif len(self.info_key[2]) % divisor == 1:
    #         if self.info_key[2][-1] == 'Check':
    #             return ['Check']
    #         else:
    #             return ['Call', 'Fold']
    #
    #     elif len(self.info_key[2]) % round_size == 2:
    #         return actions
    #     else:
    #         possible = [item for item in actions if item[0] == self.info_key[2][-1][0]]
    #         if len(possible) == 0:
    #             return actions
    #         else:
    #             return possible

    def normalize(self, strategy):
        if sum(strategy) > 0:
            strategy /= sum(strategy)
        else:
            strategy = np.repeat(1 / self.num_actions, self.num_actions)
        return strategy

    def get_regret_strategy(self):
        strategy = np.maximum(0, self.cumulative_regrets)
        strategy = self.normalize(strategy)
        return strategy

    def update_strategy_sum(self, reach_probability):
        strategy = np.maximum(0, self.cumulative_regrets)
        strategy = self.normalize(strategy)
        self.strategy_sum += reach_probability * strategy

    def heuristic_update(self, index, value=1):
        self.strategy_sum[index] = value

    def get_average_strategy(self):
        """Return average strategy"""

        self.average_strategy = self.normalize(self.strategy_sum.copy())
        #         strategy = np.maximum(0, self.cumulative_regrets)
        #         strategy = self.normalize(strategy)
        #         self.average_strategy = strategy

        return self.average_strategy
