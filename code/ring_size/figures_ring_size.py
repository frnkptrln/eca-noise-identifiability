"""Figures of the ring-size report (figures/ring_size/). Reads only data files.

make_all(outdir, style=None): style is an optional callable applied before plotting (the session used a
figure-style helper; without it matplotlib defaults are used).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import rsdata
from lightcone import step, from_word

DATA = os.path.join(HERE, "..", "..", "data")
GROUPS = [("crystal capture", [94, 43, 142]), ("defect family", [35, 26, 37]),
          ("zero state", [154, 22, 60, 90, 122]), ("other", [45, 73])]


def kstar_table():
    v = pd.read_csv(os.path.join(DATA, "fw_sweep.csv"))
    M = rsdata.load("mechanisms.csv")
    rules = [r for _, g in GROUPS for r in g]
    ns = list(range(4, int(M.n.max()) + 1))
    K = np.full((len(rules), len(ns)), np.nan)
    mark = np.zeros_like(K, dtype=int)     # 1 crystal orbit alone (p > 1), 2 zero state alone
    for i, r in enumerate(rules):
        for j, n in enumerate(ns):
            m = M[(M.rule == r) & (M.n == n)]
            if len(m):
                K[i, j] = m.kstar.iloc[0]
                sp1 = int(m.n_selected.iloc[0]) == 1 and str(m.selected_spatial_periods.iloc[0]) == "1"
                if sp1:
                    mark[i, j] = 2          # one uniform-state cycle (zero state, or 0 <-> 1) selected alone
                elif m.crystal_orbit.iloc[0] == True and int(m.crystal_p.iloc[0]) > 1:   # NaN for bijective rows
                    mark[i, j] = 1
            else:
                w = v[(v.rule == r) & (v.n == n)]
                if len(w):
                    K[i, j] = w.kstar.iloc[0]
    return rules, ns, K, mark


def fig_kstar(outdir):
    rules, ns, K, mark = kstar_table()
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    cmap = ListedColormap(["#f0f0f0", "#6baed6", "#08519c"])
    ax.imshow(K, cmap=cmap, vmin=-0.5, vmax=2.5, aspect="auto")
    for i in range(len(rules)):
        for j in range(len(ns)):
            if mark[i, j] == 1:
                ax.plot(j, i, marker="D", ms=4, mfc="white", mec="black", mew=0.6, ls="")
            elif mark[i, j] == 2:
                ax.plot(j, i, marker="o", ms=4, mfc="white", mec="black", mew=0.6, ls="")
    ax.set_xticks(range(len(ns))); ax.set_xticklabels(ns)
    ax.set_yticks(range(len(rules))); ax.set_yticklabels([f"class {r}" for r in rules])
    y = -0.5
    for name, g in GROUPS:
        ax.axhline(y, color="white", lw=2)
        ax.text(len(ns) - 0.3, y + len(g) / 2, name, va="center", ha="left", fontsize=7)
        y += len(g)
    ax.set_xlabel("ring size n")
    ax.set_title("Which classes switch with n, and what the noise selects", loc="left")
    from matplotlib.patches import Patch
    hs = [Patch(color=c, label=f"k* = {k}") for k, c in zip((0, 1, 2), ["#f0f0f0", "#6baed6", "#08519c"])]
    hs += [plt.Line2D([], [], marker="D", ms=4, mfc="white", mec="black", ls="", label="crystal orbit (p > 1) selected alone"),
           plt.Line2D([], [], marker="o", ms=4, mfc="white", mec="black", ls="", label="uniform-state cycle selected alone")]
    ax.legend(handles=hs, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=5, frameon=False, fontsize=6)
    fig.tight_layout()
    p = os.path.join(outdir, "fig_kstar_mechanisms.png"); fig.savefig(p, dpi=200); plt.close(fig)
    return p


def fig_entry_cost(outdir):
    M = rsdata.load("mechanisms.csv")
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    styles = {94: ("#1b9e77", "o"), 43: ("#d95f02", "s"), 142: ("#7570b3", "^"), 154: ("#444444", "D"), 22: ("#999999", "v")}
    for r, (c, mk) in styles.items():
        d = M[(M.rule == r) & (M.crystal_orbit == True)].sort_values("n")
        ax.plot(d.n, d.entry_cost_max, color=c, marker=mk, ms=4, lw=1, label=f"class {r}: entry cost")
    d = M[(M.crystal_orbit == True) & M.rule.isin(list(styles))]
    ax.scatter(d.n, d.radius_selected_min, color="black", marker="_", s=60, zorder=3, label="radius of the selected cycle (all)")
    ax.set_xlabel("ring size n"); ax.set_ylabel("resistance (flips)")
    ax.set_title("Leaving the selected cycle costs 2; direct entry grows", loc="left")
    ax.legend(frameon=False, fontsize=6, loc="upper left")
    ax.margins(0.06)
    fig.tight_layout()
    p = os.path.join(outdir, "fig_entry_cost.png"); fig.savefig(p, dpi=200); plt.close(fig)
    return p


def fig_rule35(outdir):
    B = pd.read_csv(os.path.join(DATA, "ring_size", "rule35_blocks.csv"), dtype={"pattern": str, "codes": str})
    F = B[B.family == 1]
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    s = F[F.selected == 1]; u = F[F.selected == 0]
    ax.scatter(s.n, s.a, color="#08519c", s=18, label="selected")
    ax.scatter(u.n, u.a, facecolor="none", edgecolor="#08519c", s=18, label="not selected")
    ns = np.arange(F.n.min(), F.n.max() + 1)
    ax.plot(ns, (2 * ns) % 3, color="#999999", lw=0.8, ls="--", label="a0 = 2n mod 3")
    ax.set_xlabel("ring size n"); ax.set_ylabel("number a of 10-blocks")
    ax.set_title("Class 35: only the fewest 10-blocks are selected", loc="left")
    ax.legend(frameon=False, fontsize=6, loc="upper left"); ax.margins(0.06)
    fig.tight_layout()
    p = os.path.join(outdir, "fig_rule35_blocks.png"); fig.savefig(p, dpi=200); plt.close(fig)
    return p


def cycle_states(rule, x, n):
    cyc = [x]; y = step(rule, x, n)
    while y != x:
        cyc.append(y); y = step(rule, y, n)
    return cyc


def rot(x, n, k):
    k %= n
    return ((x << k) | (x >> (n - k))) & ((1 << n) - 1) if k else x


def selected_states(O, rule, n):
    """All states of all noise-selected cycles (rotations included)."""
    S = set()
    for x in O[(O.rule == rule) & (O.n == n) & O.selected].orbit_rep_min_state:
        for s in cycle_states(rule, int(x), n):
            S.update(rot(s, n, k) for k in range(n))
    return S


def spacetime_after_flip(rule, x, n, j, tmax, S=None):
    """Rows: x, x XOR e_j, then the orbit until it is on a cycle in S (default: the cycle of x).
    By Lemma 1 (closure) a single flip of a noise-selected cycle always ends on a noise-selected cycle."""
    rows = [x]; z = x ^ (1 << j); rows.append(z)
    if S is None:
        S = set(cycle_states(rule, x, n))
    for _ in range(tmax):
        if z in S and len(rows) > 2:
            break
        z = step(rule, z, n); rows.append(z)
    A = np.array([[(r >> i) & 1 for i in range(n)] for r in rows])
    return A, (rows[-1] in S)


def fig_spacetime(outdir):
    O = rsdata.load("cycle_orbits.csv.gz"); M = rsdata.load("mechanisms.csv")
    picks = [(94, 12), (43, 16), (142, 16), (35, 12), (26, 16), (37, 14), (154, 16), (22, 16), (60, 16),
             (90, 16), (122, 15), (45, 8), (73, 9)]
    fig, axes = plt.subplots(1, len(picks), figsize=(11, 3.4))
    pics = []
    for ax, (r, n) in zip(axes, picks):
        o = O[(O.rule == r) & (O.n == n) & O.selected].sort_values("orbit_rep_min_state").iloc[0]
        x = int(o.orbit_rep_min_state)
        S = selected_states(O, r, n)
        # flip the cell whose orbit takes longest to reach a selected cycle (the most informative picture)
        best = None
        for j in range(n):
            A, back = spacetime_after_flip(r, x, n, j, 3 * n, S)
            if best is None or len(A) > len(best[0]):
                best = (A, back, j)
        A, back, j = best
        assert back, (r, n)            # Lemma 1: must end on a noise-selected cycle
        pics.append((ax, A, j, r, n))
    tmax = max(len(A) for _, A, *_ in pics)
    for ax, A, j, r, n in pics:
        ax.imshow(A, cmap=ListedColormap(["white", "#222222"]), aspect="auto", interpolation="nearest",
                  extent=(-0.5, A.shape[1] - 0.5, A.shape[0] - 0.5, -0.5))
        ax.set_ylim(tmax - 0.5, -0.5)
        ax.axhline(A.shape[0] - 0.5, color="#999999", lw=0.6)
        ax.plot([j], [1], marker="o", ms=3, color="#e6550d")
        ax.set_title(f"{r}, n={n}", fontsize=7)
        ax.set_xticks([]); ax.set_yticks([])
    axes[0].set_ylabel("time (grey line: on a selected cycle again)", fontsize=7)
    axes[0].set_yticks([0, tmax - 1]); axes[0].set_yticklabels(["0", str(tmax - 1)], fontsize=6)
    fig.suptitle("A noise-selected cycle, one flip (orange), and the orbit until it is on a noise-selected cycle again; ring sizes with k* >= 1",
                 x=0.01, ha="left", fontsize=8)
    fig.tight_layout()
    p = os.path.join(outdir, "fig_spacetime_flips.png"); fig.savefig(p, dpi=200); plt.close(fig)
    return p


def make_all(outdir, style=None):
    os.makedirs(outdir, exist_ok=True)
    if style:
        style()
    return [fig_kstar(outdir), fig_entry_cost(outdir), fig_rule35(outdir), fig_spacetime(outdir)]


if __name__ == "__main__":
    print(make_all(os.path.join(HERE, "..", "..", "figures", "ring_size")))
