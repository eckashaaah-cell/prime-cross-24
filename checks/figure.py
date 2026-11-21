"""Rebuild the manuscript's vector figure with NumPy and Matplotlib."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def f(prime, v):
    v = np.mod(v, 1)
    length = np.log(prime)
    return length * (np.exp(length * v) / (prime - 1) - v)


def cdf(ax, values, x, label, color, style):
    sorted_values = np.sort(values.ravel())
    y = np.searchsorted(sorted_values, x, side="right") / sorted_values.size
    ax.plot(x, y, label=label, color=color, ls=style, lw=1.6)


def main():
    lp, lq = np.log(2), np.log(3)
    a = lp + lq / 2
    b = 2 + np.log(lp * lq / 2)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "pdf.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(6.45, 2.55), layout="constrained")
    left, right = axes
    t = np.linspace(0, 5.5, 3000)
    left.plot(t, f(2, t / lp) + f(3, t / lq), lw=1.45, color="#146575")
    for bound in (b, a):
        left.axhline(bound, color="#555555", lw=0.85, ls="--")
    left.set(xlabel=r"$t=\log x$", ylabel=r"$R_{24}(e^t)$", xlim=(0, 5.5),
             ylim=(1.023, 1.255), yticks=[1.04, 1.10, 1.16, 1.22])
    grid = np.linspace(b, a, 501)
    phase = (np.arange(800) + 0.5) / 800
    torus = f(2, phase[:, None]) + f(3, phase[None, :])
    cdf(right, torus, grid, "logarithmic", "#151515", "-")
    y = (np.arange(160000) + 0.5) / 160000
    for phase_pair, label, color, style in [
        ((0, 0), r"$\theta=(0,0)$", "#b14c1b", "--"),
        ((0.3, 0.7), r"$\theta=(0.3,0.7)$", "#146575", ":"),
    ]:
        v, w = phase_pair
        vals = f(2, v + np.log(y) / lp) + f(3, w + np.log(y) / lq)
        cdf(right, vals, grid, label, color, style)
    right.set(xlabel="correction", ylabel="cumulative probability", xlim=(b, a),
              ylim=(0, 1.02), xticks=[1.04, 1.10, 1.16, 1.22])
    right.legend(loc="lower right", frameon=False, fontsize=7, handlelength=2.1)
    root = Path(__file__).resolve().parents[1]
    fig.savefig(root / "figures" / "laws.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


if __name__ == "__main__":
    main()
