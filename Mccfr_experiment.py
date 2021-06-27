import wandb
from Experiment_functions import full_abstraction, abstraction_func, exploit
import argparse

"""This is the program, used for the MCCFR experiments."""

# Default parameters
suits = 2
ranks = 3
hand_size = 2
bet = 0
train_iterations = 40000
intervals = 400
eval_iterations = 10000
FLAGS = None


def main():
    exploit(FLAGS.suits, FLAGS.ranks, FLAGS.hand_size, FLAGS.bet, FLAGS.train_iterations,
            FLAGS.intervals, FLAGS.eval_iterations)


if __name__ == '__main__':

    wandb.init(project='thesis', entity='daanle', group='exploit')
    config = wandb.config

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
    FLAGS, unparsed = parser.parse_known_args()
    config.update(FLAGS)

    main()
