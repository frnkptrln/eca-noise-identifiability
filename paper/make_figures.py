#!/usr/bin/env python3
"""Space-time figures of ring_size_paper.tex.

Every panel is the orbit of one state under one elementary rule on a ring, simulated here from the definition
(F x)_i = f(x_{i-1}, x_i, x_{i+1}), f(a, b, c) = bit 4a + 2b + c of the rule number.  Nothing is read from a data
file.  Every number printed in a panel title is computed in this script, and the statements of the titles are
asserted before the figure is written.

Usage: python make_figures.py            (writes figures/*.pdf next to this file)
       FIG_PREVIEW_DIR=dir python make_figures.py   (also writes PNG copies to dir, for inspection)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
PREVIEW = os.environ.get("FIG_PREVIEW_DIR")       # optional: also write PNG copies there

BASE, SMALL, TICK = 8, 7, 6          # three font sizes: labels and titles, annotations, ticks
FLIP = "#D55E00"                      # the flipped cell (the only colour besides black and white)

plt.rcParams.update({
    "font.size": BASE, "axes.titlesize": BASE, "axes.labelsize": BASE,
    "xtick.labelsize": TICK, "ytick.labelsize": TICK, "font.family": "DejaVu Sans",
    "axes.linewidth": 0.5, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2, "ytick.major.size": 2, "pdf.fonttype": 42,
})


def step(rule, x):
    """One step of the elementary rule on the ring."""
    a, c = np.roll(x, 1), np.roll(x, -1)          # a_i = x_{i-1}, c_i = x_{i+1}
    return (rule >> (4 * a + 2 * x + c)) & 1


def orbit(rule, x, steps):
    rows = [x.copy()]
    for _ in range(steps):
        rows.append(step(rule, rows[-1]))
    return np.array(rows)


def cycle_of(rule, x):
    """(transient, period) of the orbit of x."""
    seen, t = {}, 0
    while x.tobytes() not in seen:
        seen[x.tobytes()] = t
        x, t = step(rule, x), t + 1
    return seen[x.tobytes()], t - seen[x.tobytes()]


def draw(ax, rows, flipped, title, mark_row=None, mark_text=None, ylabel=True):
    T, n = rows.shape
    ax.imshow(rows, cmap=ListedColormap(["white", "black"]), vmin=0, vmax=1, interpolation="nearest",
              aspect="equal", extent=(-0.5, n - 0.5, T - 0.5, -0.5))
    for k in range(n + 1):                         # thin cell grid, so that white cells are visible as cells
        ax.plot([k - 0.5, k - 0.5], [-0.5, T - 0.5], color="0.8", lw=0.25, zorder=2)
    for k in range(T + 1):
        ax.plot([-0.5, n - 0.5], [k - 0.5, k - 0.5], color="0.8", lw=0.25, zorder=2)
    ax.add_patch(Rectangle((flipped - 0.5, -0.5), 1, 1, fill=False, ec=FLIP, lw=1.4, zorder=4))
    if mark_row is not None:
        ax.annotate(mark_text, xy=(n - 0.5, mark_row), xytext=(n + 0.6, mark_row), fontsize=SMALL, va="center",
                    ha="left", arrowprops=dict(arrowstyle="-", lw=0.6, color="0.3", shrinkA=0, shrinkB=0),
                    annotation_clip=False)
    ax.set_title(title, loc="left", pad=4)
    ax.set_xlabel("cell")
    if ylabel:
        ax.set_ylabel("time step")
    ax.set_xticks(range(0, n, 4))
    ax.set_yticks(range(0, T, 4))
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(T - 0.5, -0.5)
    for s in ax.spines.values():
        s.set_zorder(5)


def check_layout(fig):
    """No text overlaps another text, and all text lies inside the figure."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    boxes = [(t.get_text(), t.get_window_extent(r)) for t in fig.findobj(matplotlib.text.Text)
             if t.get_text().strip() and t.get_visible()]
    for i, (a, ba) in enumerate(boxes):
        assert fig.bbox.x0 <= ba.x0 and ba.x1 <= fig.bbox.x1 and fig.bbox.y0 <= ba.y0 and ba.y1 <= fig.bbox.y1, a
        for b, bb in boxes[i + 1:]:
            assert not ba.overlaps(bb), (a, b)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), metadata={"CreationDate": None})   # no time stamp in the file
    if PREVIEW:                                    # raster copy for inspection, not used by the paper
        os.makedirs(PREVIEW, exist_ok=True)
        fig.savefig(os.path.join(PREVIEW, name + ".png"), dpi=200)


def fig_crystal_43(n=24):
    """Rule 43, 4 | n: one flip of the crystal (0011)^(n/4); the orbit is back on the crystal cycle X after one
    step (left cell) or after n/2 - 1 steps (right cell)."""
    assert n % 4 == 0
    x0 = np.array([0, 0, 1, 1] * (n // 4))
    X = {np.roll(x0, s).tobytes() for s in range(4)}
    assert step(43, x0).tobytes() in X and len({orbit(43, x0, 3)[t].tobytes() for t in range(4)}) == 4

    def tau(j):
        y = x0.copy(); y[j] ^= 1
        t = 0
        while True:
            y, t = step(43, y), t + 1
            if y.tobytes() in X:
                return t
    left = [j for j in range(n) if x0[j - 1] != x0[j] == x0[(j + 1) % n]]
    right = [j for j in range(n) if x0[j - 1] == x0[j] != x0[(j + 1) % n]]
    assert sorted(left + right) == list(range(n))
    assert all(tau(j) == 1 for j in left) and all(tau(j) == n // 2 - 1 for j in right)
    jl = [j for j in left if n // 2 - 2 <= j][0]
    jr = [j for j in right if n // 2 - 2 <= j][0]
    T = n // 2 + 2
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.35), constrained_layout=True)
    for ax, j, name, yl in ((axes[0], jl, "left", True), (axes[1], jr, "right", False)):
        y = x0.copy(); y[j] ^= 1
        t = tau(j)
        draw(ax, orbit(43, y, T), j, f"flip of a {name} cell: back on $X$ after {t} step{'s' if t > 1 else ''}",
             mark_row=t, mark_text="on $X$", ylabel=yl)
    check_layout(fig)
    save(fig, "fig_crystal_43")
    plt.close(fig)
    return {"n": n, "tau_left": 1, "tau_right": n // 2 - 1}


def fig_zero_154(n_a=16, n_b=12):
    """Rule 154: one flip of the zero state.  n = 16: the orbit is back at the zero state after n/2 steps.
    n = 12: the orbit never returns to the zero state."""
    out = {}
    T = 13
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.9), constrained_layout=True)
    for ax, n, yl in ((axes[0], n_a, True), (axes[1], n_b, False)):
        j = n // 2
        y = np.zeros(n, dtype=int); y[j] = 1
        rows = orbit(154, y, T)
        transient, period = cycle_of(154, y)
        zero_at = [t for t in range(len(rows)) if not rows[t].any()]
        if zero_at:
            t0 = zero_at[0]
            assert t0 == n // 2 and (n & (n - 1)) == 0
            title = f"$n={n}$: zero state after {t0} steps"
            draw(ax, rows, j, title, mark_row=t0, mark_text="zero\nstate", ylabel=yl)
        else:
            # the orbit ends on a cycle that is not the zero state: no state of the cycle is zero
            z = y.copy()
            for _ in range(transient):
                z = step(154, z)
            cyc = orbit(154, z, period - 1)
            assert all(r.any() for r in cyc) and (n & (n - 1)) != 0
            title = f"$n={n}$: never the zero state"
            draw(ax, rows, j, title, ylabel=yl)
        out[n] = {"transient": transient, "period": period}
    check_layout(fig)
    save(fig, "fig_zero_154")
    plt.close(fig)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("fig_crystal_43:", fig_crystal_43())
    print("fig_zero_154:", fig_zero_154())
