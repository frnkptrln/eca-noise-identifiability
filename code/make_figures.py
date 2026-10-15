"""Figures for the note, generated from the CSVs in data/ (no numbers are typed by hand)."""
import os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "note", "figures")
os.makedirs(FIG, exist_ok=True)

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
GRAY, INK, INK2 = "#c9c8c2", "#0b0b0b", "#52514e"
SEQ = ["#c6dbf2", "#8fb8e6", "#5a94d9", "#2a78d6", "#1b56a0", "#0f3a70"]   # one hue, light -> dark

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.edgecolor": INK2, "axes.linewidth": 0.6,
    "xtick.color": INK2, "ytick.color": INK2, "axes.labelcolor": INK, "text.color": INK,
    "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.5, "axes.spines.top": False,
    "axes.spines.right": False, "legend.frameon": False, "figure.dpi": 150, "savefig.dpi": 300,
    "pdf.fonttype": 42,
})


def load():
    st = pd.read_csv(os.path.join(DATA, "stationary_rates.csv"))
    z = pd.read_csv(os.path.join(DATA, "zero_noise_per_rule.csv"))
    es = pd.read_csv(os.path.join(DATA, "epsilon_star.csv")) if os.path.exists(os.path.join(DATA, "epsilon_star.csv")) else None
    fh = pd.read_csv(os.path.join(DATA, "finite_horizon_per_rule.csv"))
    r2 = pd.read_csv(os.path.join(DATA, "radius2_boundary.csv"))
    return st, z, es, fh, r2


def fig_rates(st, z, es):
    reps = sorted(z.rep.unique())
    st = st[st.rule.isin(reps) & (st.resolved == 1)]
    ltype = z.set_index("rule").limit_type
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), sharey=True)
    panels = [("B_proved", "(a) a code missing from every cycle"),
              ("undetermined", "(b) every code on some cycle")]
    highlights = {"B_proved": [(0, BLUE, "rule 0"), (26, ORANGE, "rule 26"), (18, AQUA, "rule 18")],
                  "undetermined": [(30, BLUE, "rule 30"), (204, ORANGE, "rule 204"), (232, AQUA, "rule 232")]}
    for ax, (lt, title) in zip(axes, panels):
        for rule in reps:
            if ltype[rule] != lt:
                continue
            g = st[st.rule == rule].sort_values("eps")
            ax.plot(g.eps, g.rho, color=GRAY, lw=0.6, zorder=1)
        for rule, col, lab in highlights[lt]:
            g = st[st.rule == rule].sort_values("eps")
            ax.plot(g.eps, g.rho, color=col, lw=1.6, label=lab, zorder=3)
            if es is not None:
                e = es[es.rule == rule]
                if len(e) and e.interior_max.iloc[0] == 1 and e.eps_star.notna().iloc[0]:
                    ax.plot(e.eps_star, e.rho_star, "o", color=col, ms=5, zorder=4, mec="white", mew=0.8)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(0.0009, 0.5); ax.set_xlabel("noise level $\\varepsilon$")
        ax.set_title(title, loc="left")
        ax.legend(loc="lower right")
    axes[0].set_ylabel("identifiability rate $\\rho(f;\\varepsilon)$ [nats/step]")
    axes[0].set_ylim(3e-8, 30)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_rates.pdf")); plt.close(fig)


def fig_zero_noise(z, es):
    reps = z[z.rule == z.rep].copy().sort_values("frac_full_identification").reset_index(drop=True)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), gridspec_kw={"width_ratios": [1.6, 1]})
    ax = axes[0]
    col = reps.limit_type.map({"B_proved": BLUE, "undetermined": ORANGE})
    ax.bar(np.arange(len(reps)), reps.frac_full_identification, color=col, width=0.8)
    ax.set_xlabel("88 rule classes, sorted"); ax.set_ylabel("fraction of initial states\nidentified at $\\varepsilon=0$")
    ax.set_ylim(0, 1); ax.set_xticks([])
    ax.set_title("(a) identification at $\\varepsilon=0$", loc="left")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=BLUE, label="a code missing from every cycle"), Patch(color=ORANGE, label="every code on some cycle")], loc="upper left", fontsize=7)
    ax = axes[1]
    cs_path = os.path.join(DATA, "class_summary.csv")
    if es is not None and os.path.exists(cs_path):
        cs = pd.read_csv(cs_path)
        m = cs.merge(z[["rule", "frac_full_identification"]], on="rule")
        mi = m[(m.interior_max == 1) & (m.rising == 0)]        # the classes that fall towards eps -> 0
        ax.scatter(mi.frac_full_identification, mi.eps_star, s=14, color=mi.limit_type.map({"B_proved": BLUE, "undetermined": ORANGE}), zorder=3)
        ax.set_xlabel("fraction identified at $\\varepsilon=0$"); ax.set_ylabel("$\\varepsilon^*$ (interior maximum)")
        ax.set_title("(b) $\\varepsilon^*$ vs. zero-noise coverage", loc="left")
        ax.set_xlim(0, 1); ax.set_ylim(0, 0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_zero_noise.pdf")); plt.close(fig)


def fig_finite(fh, z):
    reps = sorted(z.rep.unique())
    fh = fh[fh.rule.isin(reps)]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for ax, (col, title) in zip(axes, [("frac_m_above_ln100", "(a) all initial states"),
                                       ("frac_m_zero_class_gt1", "(b) initial states not identified at $\\varepsilon=0$")]):
        for k, T in enumerate([8, 16, 32, 64]):
            g = fh[fh["T"] == T].groupby("eps")[col].mean()
            ax.plot(g.index, g.values, "-o", color=SEQ[k + 2], ms=4, lw=1.4, label=f"$T={T}$")
        ax.set_xscale("log"); ax.set_xlabel("noise level $\\varepsilon$"); ax.set_title(title, loc="left")
        ax.set_ylim(0, 1.02)
    axes[0].set_ylabel("fraction of initial states with\n$m_T \\geq \\ln 100$ (mean over classes)")
    axes[1].legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_finite.pdf")); plt.close(fig)


def fig_boundary(r2):
    gens = [("majority5", "majority of 5"), ("rule110_defect10101", "rule 110 with a radius-2 defect"), ("parity5", "parity of 5")]
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.7), sharey=True)
    for ax, (g, title) in zip(axes, gens):
        d = r2[r2.generator == g].sort_values("eps")
        ax.plot(d.eps, d.apparent_rate, "-", color=BLUE, lw=1.6, label="apparent rate (within $R$)")
        ax.plot(d.eps, d.misfit_rate, "-", color=ORANGE, lw=1.6, label="misfit rate (vs. best $g\\in R$)")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("$\\varepsilon$"); ax.set_title(title, loc="left")
        ax.set_ylim(1e-4, 100)
        if (d.apparent_rate < 1e-9).all():
            ax.text(0.03, 0.08, "apparent rate $= 0$ at every $\\varepsilon$\n(no rule in $R$ preferred)", transform=ax.transAxes, color=BLUE, fontsize=8)
    axes[0].set_ylabel("rate [nats/step]"); axes[0].legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_boundary.pdf")); plt.close(fig)


if __name__ == "__main__":
    st, z, es, fh, r2 = load()
    fig_rates(st, z, es); fig_zero_noise(z, es); fig_finite(fh, z); fig_boundary(r2)
    print("figures written to", FIG)
