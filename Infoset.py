import numpy as np


class Infoset:
    """Class to represent an information set. Contains functions to update the regret and strategy."""
    def __init__(self, info_key):
        """Initialize an infoset for a given an info_key. The key must contain the number of possible actions."""
        self.info_key = info_key
        self.num_actions = info_key[3]
        self.cumulative_regrets = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.average_strategy = np.repeat(1 / self.num_actions, self.num_actions)

    def normalize(self, strategy):
        """Normalize a strategy to a valid probability distribution."""
        if sum(strategy) > 0:
            strategy /= sum(strategy)
        else:
            strategy = np.repeat(1 / self.num_actions, self.num_actions)
        return strategy

    def regret_matching(self):
        """Use regret matching to find the new strategy at an iteration."""
        strategy = np.maximum(0, self.cumulative_regrets)
        strategy = self.normalize(strategy)
        return strategy

    def update_strategy_sum(self, reach_probability):
        """Update the sum of weighted strategies."""
        strategy = np.maximum(0, self.cumulative_regrets)
        strategy = self.normalize(strategy)
        self.strategy_sum += reach_probability * strategy

    def heuristic_update(self, index, value=1):
        """Update the strategy for a given action at index to the given value."""
        self.strategy_sum[index] = value

    def get_average_strategy(self):
        """Return the average strategy from the sum of weighted strategies."""

        self.average_strategy = self.normalize(self.strategy_sum.copy())

        return self.average_strategy
