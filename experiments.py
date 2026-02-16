import random
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

from tournament import Tournament


# ============================
# ===== CONFIGURABLE PARAMS ==
# ============================

ROUNDS = 10000
NUM_SEEDS = 100
NOISE_START = 0.0
NOISE_END = 0.5
NOISE_STEP = 0.05
NUM_PROCESSES = mp.cpu_count()

# ============================


# Formal strategy names for publication
DISPLAY_NAMES = {
    "Clara": "Always Cooperate (AC)",
    "Victor": "Always Defect (AD)",
    "Miles": "Tit-for-Tat (TFT)",
    "Elena": "Tit-for-Tat (Defect-First)",
    "Isabella": "Generous Tit-for-Tat (GTFT)",
    "Nathan": "Two-Tits-for-Tat (2TFT)",
    "Gabriel": "Grim Trigger (GT)",
    "Iris": "Random Strategy (RS)",
    "Lucas": "Win-Stay Lose-Shift (WSLS)",
    "Samuel": "Majority Strategy (MS)",
    "Emily": "Profitability-Adaptive Strategy (PAS)",
}


def run_single_experiment(args):
    noise, seed = args

    tournament = Tournament(
        rounds=ROUNDS,
        noise=noise,
        seed=seed,
    )

    results, _ = tournament.run_round_robin()

    num_strategies = len(tournament.strategies)
    total_rounds_per_strategy = num_strategies * ROUNDS

    averages = {
        name: score / total_rounds_per_strategy
        for name, score in results.items()
    }

    return noise, averages


def run_experiments_parallel():
    noise_values = np.arange(NOISE_START, NOISE_END + NOISE_STEP, NOISE_STEP)

    tasks = []
    for noise in noise_values:
        for _ in range(NUM_SEEDS):
            seed = random.randint(0, 10_000_000)
            tasks.append((noise, seed))

    print("Running parallel experiments...")
    print(f"Rounds per match: {ROUNDS}")
    print(f"Seeds per noise level: {NUM_SEEDS}")
    print(f"Noise values: {noise_values}")
    print(f"Using {NUM_PROCESSES} processes")
    print("-" * 60)

    with mp.Pool(NUM_PROCESSES) as pool:
        results = pool.map(run_single_experiment, tasks)

    temp_tournament = Tournament(rounds=ROUNDS, noise=0.0, seed=1)
    strategy_names = list(temp_tournament.strategies.keys())

    all_results = {
        name: {noise: [] for noise in noise_values}
        for name in strategy_names
    }

    for noise, averages in results:
        for name, avg in averages.items():
            all_results[name][noise].append(avg)

    return all_results, noise_values, strategy_names


def summarize_results(all_results, noise_values, strategy_names):
    summary = {}

    print("\n===== STATISTICAL SUMMARY =====")

    for name in strategy_names:
        formal_name = DISPLAY_NAMES[name]
        summary[name] = {}

        print(f"\nStrategy: {formal_name}")

        for noise in noise_values:
            data = np.array(all_results[name][noise])

            mean = np.mean(data)
            std = np.std(data)
            stderr = std / np.sqrt(len(data))

            # 95% confidence interval
            ci95 = 1.96 * stderr

            summary[name][noise] = {
                "mean": mean,
                "std": std,
                "stderr": stderr,
                "ci95": ci95,
            }

            print(
                f"Noise={noise:.2f} | "
                f"Mean={mean:.4f} | "
                f"Std={std:.4f} | "
                f"95% CI=±{ci95:.4f}"
            )

    return summary


def plot_all_strategies(summary, noise_values, strategy_names):
    plt.figure(figsize=(12, 8))

    for name in strategy_names:
        means = [summary[name][noise]["mean"] for noise in noise_values]
        plt.plot(
            noise_values,
            means,
            label=DISPLAY_NAMES[name],
            linewidth=2,
        )

    plt.xlabel("Noise Level")
    plt.ylabel("Average Payoff per Round")
    plt.title("Strategy Performance vs Noise")
    plt.legend(fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_pas_vs_all(summary, noise_values, strategy_names):
    plt.figure(figsize=(12, 8))

    # Plot all strategies faintly
    for name in strategy_names:
        means = [summary[name][noise]["mean"] for noise in noise_values]

        if name == "Emily":
            continue  # skip PAS for now

        plt.plot(
            noise_values,
            means,
            color="gray",
            alpha=0.4,
            linewidth=1.5,
        )

    # Plot PAS prominently
    pas_name = "Emily"
    pas_means = [summary[pas_name][noise]["mean"] for noise in noise_values]
    pas_ci = [summary[pas_name][noise]["ci95"] for noise in noise_values]

    plt.plot(
        noise_values,
        pas_means,
        color="blue",
        linewidth=3,
        label="Profitability-Adaptive Strategy (PAS)",
    )

    # Confidence band
    upper = np.array(pas_means) + np.array(pas_ci)
    lower = np.array(pas_means) - np.array(pas_ci)

    plt.fill_between(
        noise_values,
        lower,
        upper,
        color="blue",
        alpha=0.2,
    )

    plt.xlabel("Noise Level")
    plt.ylabel("Average Payoff per Round")
    plt.title("PAS Performance Relative to Other Strategies Across Noise Levels")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    all_results, noise_vals, names = run_experiments_parallel()
    summary_stats = summarize_results(all_results, noise_vals, names)
    plot_all_strategies(summary_stats, noise_vals, names)
    plot_pas_vs_all(summary_stats, noise_vals, names)
