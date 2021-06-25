
def identity(hand, hist, pos, mean):
    return hand, hist


def simple(hand, hist, pos, mean):
    """Use only the hand"""
    new_hist = ()
    return hand, new_hist


def naive(hand, hist, pos, mean):
    """Least possible states"""
    return [], ()


def possible(hand, hist, pos, mean):
    """For non-betting actions only use possible cards"""
    if 'Bet' in pos or 'Call' in pos:
        new_hand = hand
    else:
        new_hand = pos
    return new_hand, hist


def remove_bets(hist):
    new_hist = ()
    for action in hist:
        if action not in ['Call', 'Check', 'Bet']:
            new_hist += (action,)
    return new_hist


def change_hist(hand, hist):
    new_hist = ()
    for action in hist:
        print('kaas')
    return new_hist


def advanced(hand, hist, pos, mean):
    # react = True
    # if len(hist) % 2 == 0:
    #     react = False

    if len(hand) == 0:
        hand_str = 0
    else:
        hand_str = sum(map(lambda x: x[1], hand)) / len(hand)

    new_hist = remove_bets(hist) + (hist.count('Call'),)
    # if ('Bet' or 'Call') in pos:
    suits = set()
    for card in hand:
        suits.add(card[0])
    high_cards = len([x for x in hand if x[1] > mean])
    new_hand = [hand_str, len(suits), high_cards]
    # else:
    #     new_hand = hand

    return new_hand, new_hist


def adv_hist(hand, hist, pos, mean):

    new_hist = remove_bets(hist) + (hist.count('Call'),)

    return hand, new_hist


def adv_hand(hand, hist, pos, mean):

    if len(hand) == 0:
        hand_str = 0
    else:
        hand_str = sum(map(lambda x: x[1], hand)) / len(hand)

    # if ('Bet' or 'Call') in pos:
    suits = set()
    for card in hand:
        suits.add(card[0])
    high_cards = len([x for x in hand if x[1] > mean])
    new_hand = [hand_str, len(suits), high_cards]
    # else:
    #     new_hand = hand

    return new_hand, hist


def simple_hand(hand, hist, pos, mean):
    return [], hist
