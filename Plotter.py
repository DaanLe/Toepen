import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from Deck import Deck
from Game import Game
from MCCFR import MCCFR
from Abstraction_functions import simple, identity, naive, possible, advanced
from Play import Play


def exploit_plotter(suits, ranks, hand_size, bet, train_iterations, intervals, eval_iterations, runs):
    """
    train_iterations: total number of iterations
    interval: number of intevals for eval
    eval_iteration: number of iterations for each eval
    runs: total number of runs
    """
    results = []
    iterations_per_interval = int(train_iterations / intervals)
    for _ in tqdm(range(runs), leave=True):
        result = []
        deck = Deck(suits, ranks)
        game = Game(deck, hand_size, bet)
        mccfr = MCCFR(game, identity)
        result.append(mccfr.get_exploitability(eval_iterations))

        for _ in tqdm(range(intervals), leave=False):
            mccfr.train_external(iterations_per_interval)
            result.append(mccfr.get_exploitability(eval_iterations))
        results.append(result)
    results = np.array(results)
    mean = np.mean(results, axis=0)
    std = np.std(results, axis=0)
    n_plot = np.linspace(0, train_iterations, intervals+1)
    plt.fill_between(n_plot, mean + std, mean - std, alpha=0.1, color='r', label='Standard deviation')
    plt.plot(n_plot, mean, label='Mean', color='r')
    plt.legend()
    plt.title(f"Exploitability for game")
    plt.xlabel('Iterations')
    plt.ylabel('Exploitability')
    plt.savefig(f"Plots/Toepen_exploit_{suits}_{ranks}_{hand_size}_{bet}_{train_iterations}_{eval_iterations}_{runs}")
    plt.show()


def abstraction_plotter(suits, ranks, hand_size, bet, train_iterations, intervals, eval_iterations, abstraction, runs):
    """
    train_iterations: total number of iterations
    interval: number of intevals for eval
    eval_iteration: number of iterations for each eval
    runs: total number of runs
    """
    results = []
    iterations_per_interval = int(train_iterations / intervals)
    for _ in range(runs):
        result = []
        deck = Deck(suits, ranks)
        game = Game(deck, hand_size, bet)
        mccfr = MCCFR(game, identity)
        mccfr_abs = MCCFR(game, abstraction)

        play = Play(game, mccfr_abs.infoset_data, mccfr.infoset_data)
        result.append(play.play_n_rounds(eval_iterations))

        for _ in range(intervals):
            mccfr.train_external(iterations_per_interval)
            mccfr_abs.train_external(iterations_per_interval)
            play = Play(game, mccfr_abs.infoset_data, mccfr.infoset_data)
            result.append(play.play_n_rounds(eval_iterations))
        results.append(result)
    results = np.array(results)
    mean = np.mean(results, axis=0)
    std = np.std(results, axis=0)
    n_plot = np.linspace(0, train_iterations, intervals+1)
    plt.fill_between(n_plot, mean + std, mean - std, alpha=0.1, color='r', label='Standard deviation')
    plt.plot(n_plot, mean, label='Mean', color='r')
    plt.legend()
    plt.title(f"Average score versus non-abstracted strategy")
    plt.xlabel('Iterations')
    plt.ylabel('Average score')
    plt.savefig(f"Plots/abstraction/Toepen_abstraction_{suits}_{ranks}_{hand_size}_{bet}_{train_iterations}_{eval_iterations}_ " +
                f"{abstraction=}".split('=')[0] + f"{runs}")
    plt.show()


def full_abstraction_plotter(suits, ranks, hand_size, bet, train_iterations, intervals, eval_iterations, runs):
    """
    train_iterations: total number of iterations
    interval: number of intevals for eval
    eval_iteration: number of iterations for each eval
    runs: total number of runs
    """
    results_naive = []
    results_pos = []
    results_sim = []
    results_adv = []

    infoset_sizes_normal =[]
    infoset_sizes_naive = []
    infoset_sizes_pos = []
    infoset_sizes_sim = []
    infoset_sizes_adv = []


    iterations_per_interval = int(train_iterations / intervals)
    for _ in range(runs):
        deck = Deck(suits, ranks)
        game = Game(deck, hand_size, bet)
        mccfr = MCCFR(game, identity)
        mccfr_abs_naive = MCCFR(game, naive)
        mccfr_abs_pos = MCCFR(game, possible)
        mccfr_abs_sim = MCCFR(game, simple)
        mccfr_abs_adv = MCCFR(game, advanced)

        result_naive = []
        result_pos = []
        result_sim = []
        result_adv = []

        infoset_size_normal = []
        infoset_size_naive = []
        infoset_size_pos = []
        infoset_size_sim = []
        infoset_size_adv = []

        infoset_size_normal.append(sum(mccfr.count_infosets()))
        infoset_size_naive.append(sum(mccfr_abs_naive.count_infosets()))
        infoset_size_pos.append(sum(mccfr_abs_pos.count_infosets()))
        infoset_size_sim.append(sum(mccfr_abs_sim.count_infosets()))
        infoset_size_adv.append(sum(mccfr_abs_adv.count_infosets()))

        play_naive = Play(game, mccfr_abs_naive.infoset_data, mccfr.infoset_data)
        play_pos = Play(game, mccfr_abs_pos.infoset_data, mccfr.infoset_data)
        play_sim = Play(game, mccfr_abs_sim.infoset_data, mccfr.infoset_data)
        play_adv = Play(game, mccfr_abs_adv.infoset_data, mccfr.infoset_data)

        result_naive.append(play_naive.play_n_rounds(eval_iterations))
        result_pos.append(play_pos.play_n_rounds(eval_iterations))
        result_sim.append(play_sim.play_n_rounds(eval_iterations))
        result_adv.append(play_adv.play_n_rounds(eval_iterations))




        for _ in tqdm(range(intervals), leave='False'):
            mccfr.train_external(iterations_per_interval)
            mccfr_abs_naive.train_external(iterations_per_interval)
            mccfr_abs_pos.train_external(iterations_per_interval)
            mccfr_abs_sim.train_external(iterations_per_interval)
            mccfr_abs_adv.train_external(iterations_per_interval)

            infoset_size_normal.append(sum(mccfr.count_infosets()))
            infoset_size_naive.append(sum(mccfr_abs_naive.count_infosets()))
            infoset_size_pos.append(sum(mccfr_abs_pos.count_infosets()))
            infoset_size_sim.append(sum(mccfr_abs_sim.count_infosets()))
            infoset_size_adv.append(sum(mccfr_abs_adv.count_infosets()))

            play_naive = Play(game, mccfr_abs_naive.infoset_data, mccfr.infoset_data)
            play_pos = Play(game, mccfr_abs_pos.infoset_data, mccfr.infoset_data)
            play_sim = Play(game, mccfr_abs_sim.infoset_data, mccfr.infoset_data)
            play_adv = Play(game, mccfr_abs_adv.infoset_data, mccfr.infoset_data)

            result_naive.append(play_naive.play_n_rounds(eval_iterations))
            result_pos.append(play_pos.play_n_rounds(eval_iterations))
            result_sim.append(play_sim.play_n_rounds(eval_iterations))
            result_adv.append(play_adv.play_n_rounds(eval_iterations))



        results_naive.append(result_naive)
        results_pos.append(result_pos)
        results_sim.append(result_sim)
        results_adv.append(result_adv)

        infoset_sizes_normal.append(infoset_size_normal)
        infoset_sizes_naive.append(infoset_size_naive)
        infoset_sizes_pos.append(infoset_size_pos)
        infoset_sizes_sim.append(infoset_size_sim)
        infoset_sizes_adv.append(infoset_size_adv)

    mccfr.evaluate()
    infoset_max = sum(mccfr.count_infosets())


    results_naive = np.array(results_naive)
    results_pos = np.array(results_pos)
    results_sim = np.array(results_sim)
    results_adv = np.array(results_adv)

    n_plot = np.linspace(0, train_iterations, intervals+1)
    plt.figure(figsize=(8, 6))

    mean_naive = np.mean(results_naive, axis=0)
    std_naive = np.std(results_naive, axis=0)
    plt.fill_between(n_plot, mean_naive + std_naive, mean_naive - std_naive, alpha=0.1, color='r')
    plt.plot(n_plot, mean_naive, label='Naive', color='r')

    mean_pos = np.mean(results_pos, axis=0)
    std_pos = np.std(results_pos, axis=0)
    plt.fill_between(n_plot, mean_pos + std_pos, mean_pos - std_pos, alpha=0.1, color='b')
    plt.plot(n_plot, mean_pos, label='Possible', color='b')

    mean_sim = np.mean(results_sim, axis=0)
    std_sim = np.std(results_sim, axis=0)
    plt.fill_between(n_plot, mean_sim + std_sim, mean_sim - std_sim, alpha=0.1, color='g')
    plt.plot(n_plot, mean_sim, label='Simple', color='g')

    mean_adv = np.mean(results_adv, axis=0)
    std_adv = np.std(results_adv, axis=0)
    plt.fill_between(n_plot, mean_adv + std_adv, mean_adv - std_adv, alpha=0.1, color='y')
    plt.plot(n_plot, mean_adv, label='Advanced', color='y')

    plt.legend()
    plt.title(f"Average score versus non-abstracted strategy")
    plt.xlabel('Iterations')
    plt.ylabel('Average score')
    plt.savefig(f"Plots/abstraction/Toepen_abstraction_{suits}_{ranks}_{hand_size}_{bet}_{train_iterations}_{eval_iterations}_{runs}")
    plt.show()

    results_normal = np.array(infoset_sizes_normal)
    results_naive = np.array(infoset_sizes_naive)
    results_pos = np.array(infoset_sizes_pos)
    results_sim = np.array(infoset_sizes_sim)
    results_adv = np.array(infoset_sizes_adv)

    n_plot = np.linspace(0, train_iterations, intervals + 1)
    plt.figure(figsize=(8, 6))

    # plt.plot(n_plot, np.repeat(376958, intervals + 1), '--', label='Total Infosets', color='m')
    plt.plot(n_plot, np.repeat(infoset_max, intervals + 1), '--', label='Total Infosets', color='m')

    mean_normal = np.mean(results_normal, axis=0)
    plt.plot(n_plot, mean_normal, label='Identity', color='c')

    mean_naive = np.mean(results_naive, axis=0)
    plt.plot(n_plot, mean_naive, label='Naive', color='r')

    mean_pos = np.mean(results_pos, axis=0)
    plt.plot(n_plot, mean_pos, label='Possible', color='b')

    mean_sim = np.mean(results_sim, axis=0)
    plt.plot(n_plot, mean_sim, label='Simple', color='g')

    mean_adv = np.mean(results_adv, axis=0)
    plt.plot(n_plot, mean_adv, label='Advanced', color='y')

    plt.legend()
    plt.title(f"Average number of information sets reached")
    plt.xlabel('Iterations')
    plt.ylabel('Information sets')
    plt.savefig(f"Plots/abstraction/Toepen_abstraction_infosize_{suits}_{ranks}_{hand_size}_{bet}_{hand_size}_{train_iterations}_{eval_iterations}_{runs}")
    plt.show()

