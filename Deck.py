import itertools
import random


class Deck:
    """Class to determine the deck"""

    def __init__(self, suits, ranks):
        """Initialize a deck for a given number of ranks and suits."""

        self.suit = ('clubs', 'diamonds', 'hearts', 'spades')
        self.ranks = (10, 9, 8, 7, 6, 5, 4, 3)
        self.suit = self.suit[:suits]
        self.ranks = self.ranks[:ranks]
        self.deck1 = list(itertools.product(self.suit, self.ranks))
        self.deck2 = self.deck1.copy()
        random.shuffle(self.deck1)

    def remove_hand_deck(self, hand):
        # Remove a given hand from the deck
        self.deck1 = [x for x in self.deck1 if x not in hand]

    def reset_deck(self):
        self.deck1 = self.deck2.copy()
