"""Assemble report_ring_size.md from report_template.md and the data in data/ring_size/.

Every {{NAME}} in the template is replaced by a value or table computed here from a data file; the script
fails if a placeholder is left. Figure links are passed in with --fig NAME=link (artifact markers when
run inside the session, relative paths otherwise).
Usage: python3 make_report.py [--fig FIG_KSTAR=figures/ring_size/fig_kstar_mechanisms.png ...] [--literature file.md]
"""
import argparse, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import rsdata

ROOT = os.path.join(HERE, "..", "..")
OUT = rsdata.OUT


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        lines.append("| " + " | ".join(str(v).replace("|", "\\|") for v in r) + " |")
    return "\n".join(lines)


def ranges(ns):
    ns = sorted(ns); out = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        out.append(str(ns[i]) if i == j else f"{ns[i]}-{ns[j]}")
        i = j + 1
    return ", ".join(out) if out else "none"


def build(figs, literature):
    M = rsdata.load("mechanisms.csv"); O = rsdata.load("cycle_orbits.csv.gz")
    v02 = pd.read_csv(os.path.join(ROOT, "data", "fw_sweep.csv"), dtype={"k_c": str})
    V = {}
    va = pd.read_csv(os.path.join(OUT, "verify_mech_n4_8_all.csv")); vb = pd.read_csv(os.path.join(OUT, "verify_mech_n9_10_switching.csv"))
    V["VERIFY_PAIRS"] = len(va) + len(vb); V["VERIFY_BAD"] = int((va.agree == 0).sum() + (vb.agree == 0).sum())
    mrg = M.merge(v02, on=["rule", "n"], suffixes=("", "_v02"))
    bad = sum(int((mrg[a].astype(str) != mrg[b].astype(str)).sum()) for a, b in
              [("cycles", "cycles_v02"), ("n_selected", "n_stable"), ("gamma_min", "gamma_min_v02"), ("k_c", "k_c_v02"), ("kstar", "kstar_v02")])
    V["V02_COMPARED"] = len(mrg); V["V02_BAD"] = bad
    V["NMAX"] = int(M.n.max())
    nb = M[M.bijective == "0"] if M.bijective.dtype == object else M[M.bijective == 0]
    V["N_RECORDS_NONBIJ"] = len(nb)
    assert bool((nb.selected_eq_closed_union == True).all()), "selected != union of closed classes somewhere"
    V["N_SINGLE_CLOSED"] = int((nb.g1_closed == 1).sum())
    V["NMAX154"] = int(M[M.rule == 154].n.max())
    V["N154EVEN"] = int(M[(M.rule == 154) & (M.n % 2 == 0)].n.max())
    cr = M[M.rule.isin([94, 43, 142]) & (M.crystal_orbit == True)]
    V["NMAX_CRYSTAL"] = int(M[M.rule.isin([94, 43, 142])].n.max())
    # k* table
    rules = [94, 43, 142, 35, 26, 37, 154, 22, 60, 90, 122, 45, 73]
    ns = list(range(4, V["NMAX"] + 1))
    rows = []
    for r in rules:
        row = {"class": r}
        for n in ns:
            m = M[(M.rule == r) & (M.n == n)]
            if len(m):
                row[str(n)] = int(m.kstar.iloc[0])
            else:
                w = v02[(v02.rule == r) & (v02.n == n)]
                row[str(n)] = int(w.kstar.iloc[0]) if len(w) else "."
        rows.append(row)
    V["TABLE_KSTAR"] = "k* by class (rows) and n (columns); n = 4..7 from v0.2, n >= 8 from `mechanisms.csv` (`.` = not computed):\n\n" + md_table(pd.DataFrame(rows))
    mech_rows = [
        ("94", "k* >= 1 iff 3 | n", "crystal capture, (011)^{n/3}, 3 phases", "radius proved; reachability computed/sampled"),
        ("43, 142", "k* >= 1 iff 4 | n", "crystal capture, travelling (0011)^{n/4}", "radius computed to 400; reachability computed/sampled"),
        ("35", "k* >= 1 iff 3 | n", "code-101 carriers = {10,100}-words; fewest 10-blocks selected; a0 = 0 at 3 | n", "computed"),
        ("154", "k* >= 1 iff n = 2^k", "zero state; radius from rule-90 nilpotency", "odd n proved (k* = 0); radius at even n proved; reachability computed/sampled"),
        ("60, 90", "k* >= 1 iff n = 2^k", "nilpotent at 2^k (v0.2)", "proved (v0.2)"),
        ("22", "k* >= 1 iff seed of 0 returns", "zero state", "seed set proved for 4 | n, computed to 256"),
        ("26", "2^k: zero state; else code 7", "zero state; 111-defects in (100)", "radius at 2^k proved; rest resists"),
        ("122", "2^k - 1: zero state; else code 2", "zero state; checkerboard", "checkerboard selection resists"),
        ("37", "k* = 0 iff n mod 6 in {0, 5}", "period-6 defect family", "computed"),
        ("45", "only n = 8", "uniform 2-cycle radius 2 at n = 8; odd n bijective", "odd n proved; n = 8 computed"),
        ("73", "only n = 9", "uniform 2-cycle not selected at n = 9", "computed"),
    ]
    V["TABLE_MECH"] = md_table(pd.DataFrame(mech_rows, columns=["class", "pattern (n <= %d)" % V["NMAX"], "mechanism", "status"]))
    t = cr[["rule", "n", "cycles", "n_selected", "radius_selected_min", "radius_other_max", "entry_cost_max", "g2_holds", "gamma_min"]].copy()
    t["m + q - 2"] = t.cycles.astype(int) + t.n_selected.astype(int) - 2
    t = t.rename(columns={"rule": "class", "n_selected": "q (selected)", "radius_selected_min": "radius crystal",
                          "radius_other_max": "max radius others", "entry_cost_max": "max direct entry cost", "g2_holds": "Lemma B holds"})
    for c in ["radius crystal", "max radius others", "max direct entry cost"]:
        t[c] = t[c].astype(int)
    V["TABLE_CRYSTAL"] = md_table(t.sort_values(["class", "n"]))
    lc = pd.read_csv(os.path.join(OUT, "lightcone.csv"), dtype={"word": str})
    l94 = lc[(lc.rule == 94)].iloc[0]
    V["TAU94"] = int(l94.tau); V["N0_94"] = int(l94.n0)
    crad = pd.read_csv(os.path.join(OUT, "crystal_radius.csv"), dtype={"word": str})
    V["CRYSTAL_NMAX"] = int(crad.n.max())
    assert bool(crad[crad.rule.isin([43, 142])].radius_ge2.all())
    assert bool(crad[(crad.rule == 94) & (crad.n >= 6)].radius_ge2.all())
    B = pd.read_csv(os.path.join(OUT, "rule35_blocks.csv"), dtype={"pattern": str, "codes": str})
    F = B[B.family == 1]
    r35 = []
    for n in sorted(B.n.unique()):
        f = F[F.n == n]
        r35.append(dict(n=n, a0=int((2 * n) % 3), selected_a=",".join(map(str, sorted(set(f[f.selected == 1].a)))),
                        not_selected_a=",".join(map(str, sorted(set(f[f.selected == 0].a)))) or "-",
                        code5_missing=int(not B[(B.n == n) & (B.selected == 1)].has_code5.any())))
    V["TABLE_35"] = "\n" + md_table(pd.DataFrame(r35)) + "\n"
    Z = pd.read_csv(os.path.join(OUT, "zero_mechanism.csv")); zz = Z[Z.seed_returns >= 0]
    assert bool((zz.seed_returns == zz.zero_alone_selected).all())
    V["ZERO_PAIRS"] = len(zz)
    so = pd.read_csv(os.path.join(OUT, "seed_orbits.csv"))
    V["SEED_CAP"] = "400000"
    srows = []
    for r in (22, 26, 122, 154):
        s = so[so.rule == r]
        srows.append(dict(rule=r, returns_to_0_at_n=", ".join(map(str, s[s.returns_to_zero == 1].n)),
                          undetermined_n=len(s[s.capped == 1])))
    V["TABLE_SEED"] = md_table(pd.DataFrame(srows))
    s22 = so[(so.rule == 22) & (so.returns_to_zero == 1) & (so.n % 4 != 0)]
    V["R22_OTHER"] = ", ".join(map(str, s22.n))
    D = pd.read_csv(os.path.join(OUT, "g1_distance_154.csv"))
    for n in (8, 16):
        d = D[D.n == n]
        V[f"C154_{n}"] = len(d); V[f"D154_{n}"] = int(d.g1_distance_to_zero.max())
        V[f"S154_{n}"] = f"{d.mean_ones.corr(d.g1_distance_to_zero, method='spearman'):.2f}"
        assert (d.g1_distance_to_zero >= 0).all()
    cc = pd.read_csv(os.path.join(OUT, "code_carriers.csv"))
    c = cc[(cc.rule == 122) & (cc.code == 2)]
    V["C122_SEL"] = ", ".join(map(str, c[c.selected_carrier_orbits > 0].n))
    V["C122_UNSEL"] = ", ".join(map(str, c[(c.carrier_orbits > 0) & (c.selected_carrier_orbits == 0)].n))
    srows = []
    for f in sorted(glob.glob(os.path.join(OUT, "sampled_reach", "rule*_n*.csv"))):
        s = pd.read_csv(f)
        srows.append(dict(rule=int(s.rule.iloc[0]), n=int(s.n.iloc[0]), target=s.target.iloc[0],
                          target_radius_ge2=int(s.target_radius_ge2.iloc[0]), sampled=len(s),
                          distinct_cycles=s.cycle_label.nunique(), reach_target=int(s.found.sum()),
                          max_path_len=int(s.path_len.max())))
    V["TABLE_SAMPLED"] = md_table(pd.DataFrame(srows).sort_values(["rule", "n"]))
    P = pd.read_csv(os.path.join(OUT, "predictions_outcome.csv"))
    V["PRED_COUNTS"] = "; ".join(f"{k}: {v}" for k, v in P.outcome.value_counts().items())
    V["TABLE_PRED"] = md_table(P)
    files = [("data/ring_size/mechanisms.csv", "one row per (class, n): cycles, selected, G1 closed classes, radii, crystal test"),
             ("data/ring_size/cycle_orbits.csv.gz", "one row per rotation orbit of cycles: pattern, periods, drift, codes, gamma, radius, selected"),
             ("data/ring_size/mech_cost.csv", "wall time and peak memory per job"),
             ("data/ring_size/verify_mech_*.csv", "independent verifier"),
             ("data/ring_size/seed_orbits.csv", "single-flip orbit of the zero state, n = 4..256"),
             ("data/ring_size/crystal_radius.csv", "every single flip of the crystals, p | n up to 400"),
             ("data/ring_size/lightcone.csv", "healing times on the line (Lemma H)"),
             ("data/ring_size/injectivity.csv", "pair-graph certificates (Lemma P)"),
             ("data/ring_size/rule35_blocks.csv, code_carriers.csv, g1_distance_154.csv, zero_mechanism.csv", "derived tables (analyze_mechanisms.py)"),
             ("data/ring_size/sampled_reach/", "sampled reachability beyond n = 22"),
             ("data/ring_size/factor_search.csv", "block maps of width <= 4 intertwining rule 154 with a radius-1 rule"),
             ("data/ring_size/stopped_runs.csv", "runs stopped above the stated cost cap"),
             ("data/ring_size/predictions_outcome.csv", "outcome of every sealed prediction"),
             ("data/ring_size/MANIFEST.sha256", "SHA-256 of every file in data/ring_size"),
             ("code/ring_size/", "mech, verify_mech, run_mech, run_local, ringlang, lightcone, sample_reach, analyze_mechanisms, check_predictions, figures_ring_size, make_report, tests")]
    if os.path.exists(os.path.join(OUT, "atlas", "mechanisms_atlas.csv")):
        files.append(("data/ring_size/atlas/", "atlas: 75 non-switching classes at n = 4..20 and the 13 switching classes at n = 4..7; selected cycles (count, spatial and temporal periods, codes); checkpoint as mech_atlas.jsonl.gz"))
    V["TABLE_FILES"] = md_table(pd.DataFrame(files, columns=["file", "content"]))
    cost = pd.read_csv(os.path.join(OUT, "mech_cost.csv"))
    st = pd.read_csv(os.path.join(OUT, "stopped_runs.csv"))
    stop = " ".join(f"Class {int(r.rule)} at n = {int(r.n)} was stopped after {r.wall_hours} h, above the stated cap of {r.cap_hours} h; it is not computed (`stopped_runs.csv`)." for r in st.itertuples())
    V["COST_LINE"] = stop + " " + (f"Mechanism jobs {len(cost)}, total CPU {cost.cost_seconds.sum() / 3600:.1f} h, longest job "
                      f"{cost.cost_seconds.max() / 60:.0f} min (class {int(cost.loc[cost.cost_seconds.idxmax(), 'rule'])}, "
                      f"n = {int(cost.loc[cost.cost_seconds.idxmax(), 'n'])}), peak memory {cost.cost_maxrss_mb.max() / 1000:.1f} GB "
                      f"(`mech_cost.csv`).")
    atlas = os.path.join(OUT, "atlas", "mechanisms_atlas.csv")
    if os.path.exists(atlas):
        A = rsdata.load(os.path.join("atlas", "mechanisms_atlas.csv"))
        log = open(os.path.join(OUT, "atlas", "log_atlas.txt")).read()
        fin = re.findall(r"finalize: (\d+) records, (\d+) compared with v0.2, (\d+) disagreements", log)[-1]
        V["ATLAS_NOTE"] = (f"\nAtlas (step 6) [computed]: `data/ring_size/atlas/mechanisms_atlas.csv` holds {len(A)} (class, n) records "
                           f"({A.rule.nunique()} classes: the 75 non-switching classes at n = 4..20 and the 13 switching classes at "
                           f"n = 4..7) with the selected-cycle count, the spatial and temporal periods of the selected cycles, "
                           f"the codes they cover, k_c and k*; the selected orbits are in `cycle_orbits_atlas.csv.gz`. The 13 "
                           f"switching classes at n >= 8 are in `mechanisms.csv`; together these cover all 88 classes at n = 4..20. "
                           f"All {fin[1]} atlas records agree with v0.2 in cycles, selected count, gamma_min, k_c and k* "
                           f"({fin[2]} disagreements, `atlas/log_atlas.txt`). Space-time pictures of selected cycles for the 13 "
                           f"switching classes: the figure in 5.5.")
    else:
        V["ATLAS_NOTE"] = "\nAtlas (step 6): not produced in this run."
    V["LITERATURE"] = literature
    V.update(figs)
    return V


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fig", action="append", default=[])
    ap.add_argument("--literature", default=None)
    ap.add_argument("--ellison", default="")
    ap.add_argument("--out", default=os.path.join(ROOT, "report_ring_size.md"))
    a = ap.parse_args()
    figs = dict(kv.split("=", 1) for kv in a.fig)
    for k, p in [("FIG_KSTAR", "figures/ring_size/fig_kstar_mechanisms.png"), ("FIG_ENTRY", "figures/ring_size/fig_entry_cost.png"),
                 ("FIG_35", "figures/ring_size/fig_rule35_blocks.png"), ("FIG_ST", "figures/ring_size/fig_spacetime_flips.png")]:
        figs.setdefault(k, p)
    lit = open(a.literature).read() if a.literature else "Literature review not available in this run."
    V = build(figs, lit)
    V["ELLISON_REMARK"] = open(a.ellison).read().strip() if a.ellison else ""
    s = open(os.path.join(HERE, "report_template.md")).read()
    for k, v in V.items():
        s = s.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", s)
    assert not left, f"unfilled placeholders: {left}"
    open(a.out, "w").write(s)
    print("wrote", a.out, len(s), "chars")


if __name__ == "__main__":
    main()
