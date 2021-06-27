from tqdm import tqdm
from Deck import Deck
from Game import Game
from MCCFR import MCCFR
from Abstraction_functions import simple, identity, naive, possible, advanced
from Play import Play
import wandb


def exploit(suits, ranks, hand_size, bet, train_iterations, intervals, eval_iterations):
    """
    Function to run the MCCFR experiment.
    params:
    train_iterations: total number of iterations
    interval: number of intervals for eval
    eval_iteration: number of iterations for each eval
    """
    iterations_per_interval = int(train_iterations / intervals)
    deck = Deck(suits, ranks)
    game = Game(deck, hand_size, bet)
    mccfr = MCCFR(game, identity)
    mccfr.train_external(10000)
    wandb.log({f"exploitability": mccfr.get_exploitability(eval_iterations),
               'iteration': 10000})

    for i in tqdm(range(intervals), leave=False):
        mccfr.train_external(iterations_per_interval)
        wandb.log({f"exploitability": mccfr.get_exploitability(eval_iterations),
                   'iteration': 10000 + ((i+1)*iterations_per_interval)})


def full_abstraction(suits, ranks, hand_size, bet, train_iterations, intervals, eval_iterations):
    """
    Function to run the abstraction experiment using multiple abstraction methods.
    params:
    train_iterations: total number of iterations
    interval: number of intervals for eval
    eval_iteration: number of iterations for each eval
    """

    iterations_per_interval = int(train_iterations / intervals)
    deck = Deck(suits, ranks)
    game = Game(deck, hand_size, bet)
    mccfr = MCCFR(game, identity)
    mccfr_abs_naive = MCCFR(game, naive)
    mccfr_abs_pos = MCCFR(game, possible)
    mccfr_abs_sim = MCCFR(game, simple)
    mccfr_abs_adv = MCCFR(game, advanced)



    infoset_size_normal = sum(mccfr.count_infosets())
    infoset_size_naive = sum(mccfr_abs_naive.count_infosets())
    infoset_size_pos = sum(mccfr_abs_pos.count_infosets())
    infoset_size_sim = sum(mccfr_abs_sim.count_infosets())
    infoset_size_adv = sum(mccfr_abs_adv.count_infosets())



    play_naive = Play(game, mccfr_abs_naive.infoset_data, mccfr.infoset_data)
    play_pos = Play(game, mccfr_abs_pos.infoset_data, mccfr.infoset_data)
    play_sim = Play(game, mccfr_abs_sim.infoset_data, mccfr.infoset_data)
    play_adv = Play(game, mccfr_abs_adv.infoset_data, mccfr.infoset_data)

    result_naive = play_naive.play_n_rounds(eval_iterations)
    result_pos = play_pos.play_n_rounds(eval_iterations)
    result_sim = play_sim.play_n_rounds(eval_iterations)
    result_adv = play_adv.play_n_rounds(eval_iterations)

    wandb.log({"infoset_size_adv": infoset_size_adv, 'result_adv': result_adv,
               "infoset_size_naive": infoset_size_naive, "result_naive": result_naive,
               "infoset_size_simple": infoset_size_sim, "result_simple": result_sim, 'iteration': 0})



    for i in tqdm(range(intervals), leave='False'):
        mccfr.train_external(iterations_per_interval)
        mccfr_abs_naive.train_external(iterations_per_interval)
        mccfr_abs_pos.train_external(iterations_per_interval)
        mccfr_abs_sim.train_external(iterations_per_interval)
        mccfr_abs_adv.train_external(iterations_per_interval)

        infoset_size_normal = sum(mccfr.count_infosets())
        infoset_size_naive = sum(mccfr_abs_naive.count_infosets())
        infoset_size_pos = sum(mccfr_abs_pos.count_infosets())
        infoset_size_sim = sum(mccfr_abs_sim.count_infosets())
        infoset_size_adv = sum(mccfr_abs_adv.count_infosets())

        play_naive = Play(game, mccfr_abs_naive.infoset_data, mccfr.infoset_data)
        play_pos = Play(game, mccfr_abs_pos.infoset_data, mccfr.infoset_data)
        play_sim = Play(game, mccfr_abs_sim.infoset_data, mccfr.infoset_data)
        play_adv = Play(game, mccfr_abs_adv.infoset_data, mccfr.infoset_data)

        result_naive = play_naive.play_n_rounds(eval_iterations)
        result_pos = play_pos.play_n_rounds(eval_iterations)
        result_sim = play_sim.play_n_rounds(eval_iterations)
        result_adv = play_adv.play_n_rounds(eval_iterations)
        # print(infoset_size_normal, result_adv, (i+1)*iterations_per_interval)
        wandb.log({"infoset_size_adv": infoset_size_adv, 'result_adv': result_adv,
                   "infoset_size_naive": infoset_size_naive, "result_naive": result_naive,
                   "infoset_size_simple": infoset_size_sim, "result_simple": result_sim,
                   'iteration': (i+1)*iterations_per_interval})


def abstraction_func(suits, ranks, hand_size, bet, train_iterations, intervals, eval_iterations, abstraction):
    """
    Function to run the abstraction experiment.
    params:
    train_iterations: total number of iterations
    interval: number of intervals for eval
    eval_iteration: number of iterations for each eval
    abstraction: the abstraction function
    """

    iterations_per_interval = int(train_iterations / intervals)
    deck = Deck(suits, ranks)
    game = Game(deck, hand_size, bet)
    mccfr = MCCFR(game, identity)
    mccfr_abs = MCCFR(game, abstraction)



    infoset_size_normal = sum(mccfr.count_infosets())
    infoset_size_abs = sum(mccfr_abs.count_infosets())




    play_abs = Play(game, mccfr_abs.infoset_data, mccfr.infoset_data)

    result_abs = play_abs.play_n_rounds(eval_iterations)

    wandb.log({f"infoset_size_{abstraction.__name__}": infoset_size_abs,
               f'infoset_size_non': infoset_size_normal,
               f'result_{abstraction.__name__}': result_abs,
               f'infoset_size_max': 376958,
               'iteration': 0})

    for i in tqdm(range(intervals), leave='False'):
        mccfr.train_external(iterations_per_interval)
        mccfr_abs.train_external(iterations_per_interval)

        infoset_size_normal = sum(mccfr.count_infosets())
        infoset_size_abs = sum(mccfr_abs.count_infosets())


        play_abs = Play(game, mccfr_abs.infoset_data, mccfr.infoset_data)

        result_abs = play_abs.play_n_rounds(eval_iterations)
        # print(infoset_size_normal, result_adv, (i+1)*iterations_per_interval)
        wandb.log({f"infoset_size_{abstraction.__name__}": infoset_size_abs,
                   f'result_{abstraction.__name__}': result_abs,
                   f'infoset_size_non': infoset_size_normal,
                   f'infoset_size_max': 376958,
                   'iteration': (i+1)*iterations_per_interval})