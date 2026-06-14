import os
import pandas as pd
import matplotlib
matplotlib.use("pgf")
import matplotlib.pyplot as plt
import argparse

matplotlib.rcParams.update({
    "pgf.texsystem": "lualatex",
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
    "pgf.preamble": "\n".join([
        r"\usepackage{fontspec}",
        r"\setmainfont{TeX Gyre Termes}",
        r"\setsansfont{TeX Gyre Heros}",
        r"\setmonofont{TeX Gyre Cursor}",
    ]),
    "figure.figsize": (6.2, 3.5),
})

LINE_STYLES = ["-", "--", ":", "-."]
MARKERS = ["o", "s", "^", "D"]
GRAY_COLORS = ["0.0", "0.4", "0.65"]


def load_data(prefix):
    return {
        "queue": pd.read_csv(f"{prefix}_queue.csv", header=None, names=["time", "queue"]),
        "drops": pd.read_csv(f"{prefix}_drops.csv", header=None, names=["time", "drop"]),
        "throughput": pd.read_csv(f"{prefix}_throughput.csv", header=None, names=["time", "mbps"])
    }


def smooth(df, column, window):
    return df[column].rolling(window=window).mean()


def main():
    parser = argparse.ArgumentParser(description="NS-3 AQM comparison visualizer")

    parser.add_argument("--algorithms", nargs="+", required=True,
                        help="List of algorithm prefixes (e.g. red ared gentle)")

    parser.add_argument("--window", type=int, default=30,
                        help="Smoothing window")

    args = parser.parse_args()

    data = {}

    for algo in args.algorithms:
        data[algo] = load_data(algo)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(os.path.dirname(script_dir), "image")

    # ------------------------
    # QUEUE
    # ------------------------
    fig_queue, ax_queue = plt.subplots()

    for i, (algo, d) in enumerate(data.items()):
        q = d["queue"]
        q["smooth"] = smooth(q, "queue", args.window)

        ax_queue.plot(q["time"], q["smooth"], label=algo.upper(),
                      color=GRAY_COLORS[i % len(GRAY_COLORS)],
                      linestyle=LINE_STYLES[i % len(LINE_STYLES)])

    ax_queue.set_xlabel("Time (s)")
    ax_queue.set_ylabel("Queue size (packets)")
    ax_queue.set_title("Queue Dynamics Comparison")
    ax_queue.legend()
    ax_queue.grid()
    fig_queue.savefig(os.path.join(image_dir, "queue.pgf"), bbox_inches="tight")

    # ------------------------
    # THROUGHPUT
    # ------------------------
    fig_throughput, ax_throughput = plt.subplots()

    for i, (algo, d) in enumerate(data.items()):
        t = d["throughput"]
        t["smooth"] = smooth(t, "mbps", args.window)

        ax_throughput.plot(t["time"], t["smooth"], label=algo.upper(),
                          color=GRAY_COLORS[i % len(GRAY_COLORS)],
                          linestyle=LINE_STYLES[i % len(LINE_STYLES)])

    ax_throughput.set_xlabel("Time (s)")
    ax_throughput.set_ylabel("Throughput (Mbps)")
    ax_throughput.set_title("Throughput Comparison")
    ax_throughput.legend()
    ax_throughput.grid()
    fig_throughput.savefig(os.path.join(image_dir, "throughput.pgf"), bbox_inches="tight")

    # ------------------------
    # DROPS
    # ------------------------
    fig_drops, ax_drops = plt.subplots()

    for i, (algo, d) in enumerate(data.items()):
        dr = d["drops"]

        ax_drops.scatter(dr["time"], [algo]*len(dr), s=5, label=algo.upper(),
                         color=GRAY_COLORS[i % len(GRAY_COLORS)],
                         marker=MARKERS[i % len(MARKERS)])

    ax_drops.set_xlabel("Time (s)")
    ax_drops.set_ylabel("Algorithm")
    ax_drops.set_title("Packet Drops Comparison")
    ax_drops.grid()
    fig_drops.savefig(os.path.join(image_dir, "drops.pgf"), bbox_inches="tight")


if __name__ == "__main__":
    main()
