import math


def complexity_pos(suits, ranks, hand_size, betting):
    """
    Find the upper bound of the number of possible histories
    """
    com = math.comb(suits*ranks, hand_size)*math.comb((suits*ranks)-hand_size, hand_size)
    for i in range(hand_size):
        com *= (i+1)**2
    if betting == 1:
        com *= 2 ** hand_size
    elif betting == 2:
        com *= 2 ** (2*hand_size)
    return com


def complexity_info(suits, ranks, hand_size, betting):
    """
    Find the upper bound of the number of possible Information sets.
    """
    com = math.comb(suits*ranks, hand_size)
    for i in range(1, hand_size):
        com *= (suits*ranks) - (hand_size+i-1)
        com *= (i+1)
    if betting == 1:
        com *= 2 ** hand_size
    elif betting == 2:
        com *= 2 ** (2*hand_size+1)
    return com*2
