from Deck import Deck
from Game import Game
from MCCFR import MCCFR
from Infoset import Infoset
from Play import Play
from Heuristic import Heuristic
from Abstraction_functions import simple, identity, naive, possible, advanced, adv_hand, adv_hist, simple_hand
import wandb
from Lisa import full_abstraction, abstraction_func
import argparse


# Default constants
suits = 3
ranks = 3
hand_size = 3
bet = 2
train_iterations = 100000
intervals = 1000
eval_iterations = 20000
abstraction = "sim_hand"
FLAGS = None

def main():
    abstraction_functions = {
        "adv": advanced,
        "sim": simple,
        "naive": naive,
        "hand": adv_hand,
        "hist": adv_hist,
        "sim_hand": simple_hand
    }
    abstraction_func(FLAGS.suits, FLAGS.ranks, FLAGS.hand_size, FLAGS.bet, FLAGS.train_iterations,
                     FLAGS.intervals, FLAGS.eval_iterations, abstraction_functions[FLAGS.abstraction])


if __name__ == '__main__':

    wandb.init(project='thesis', entity='daanle', group='abstraction')
    config = wandb.config

    # config.suits = suits
    # config.ranks = ranks
    # config.hand_size = hand_size
    # config.bet = bet
    # config.train_iterations = train_iterations
    # config.intervals = intervals
    # config.eval_iterations = eval_iterations

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--suits', type=int, default=suits,
                        help='Number of suits')
    parser.add_argument('--ranks', type=int, default=ranks,
                        help='Number of ranks')
    parser.add_argument('--hand_size', type=int, default=hand_size,
                        help='Number of cards in a hand')
    parser.add_argument('--bet', type=int, default=bet,
                        help='Betting variable, 0 for no betting, 1 for betting start and 2 for full betting')
    parser.add_argument('--train_iterations', type=int, default=train_iterations,
                        help='Number of total train iterations')
    parser.add_argument('--intervals', type=int, default=intervals,
                        help='Frequency of evaluation')
    parser.add_argument('--eval_iterations', type=int, default=eval_iterations,
                        help='Number of iterations for evaluation')
    parser.add_argument('--abstraction', type=str, default=abstraction,
                        help='Abstraction type')
    FLAGS, unparsed = parser.parse_known_args()
    config.update(FLAGS)


    main()
