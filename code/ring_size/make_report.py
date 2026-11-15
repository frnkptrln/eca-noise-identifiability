"""Assemble report_ring_size.md from report_template.md and the data in data/ring_size/.

Every {{NAME}} in the template is replaced by a value, table or sentence computed here from a data file;
the script fails if a placeholder is left. Values that this study did not compute itself (class 154 at
n = 22, seed orbits settled after the study's cut-off, the sleep interval of the stopped job, the sealed
statements outside the outcome table, the computations behind the proofs of Section 5.7) are read from the
outputs of the independent verification under verify_ring_size/ through verif.py, and the report names the
file. The prose of the template is not generated. Figure links are passed in with --fig NAME=link.
Usage: python3 make_report.py [--fig FIG_KSTAR=figures/ring_size/fig_kstar_mechanisms.png ...] [--literature file.md]
"""
import argparse, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "fw"))
import numpy as np, pandas as pd
import rsdata, verif, fwlib

ROOT = os.path.join(HERE, "..", "..")
OUT = rsdata.OUT
SWITCHING = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]


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
    named = [(r, n) for r in fwlib.class_reps() for n in range(4, 9)] + [(r, n) for r in SWITCHING for n in (9, 10)]
    nbij = sum(bool(fwlib.is_bijective(fwlib.succ_map(r, n))) for r, n in named)
    V["VERIFY_NAMED"] = len(named); V["VERIFY_BIJ"] = nbij
    assert len(named) - nbij == V["VERIFY_PAIRS"], (len(named), nbij, V["VERIFY_PAIRS"])
    assert {(int(r.rule), int(r.n)) for r in pd.concat([va, vb]).itertuples()} == {(r, n) for r, n in named if not fwlib.is_bijective(fwlib.succ_map(r, n))}
    mrg = M.merge(v02, on=["rule", "n"], suffixes=("", "_v02"))
    V["V02_COMPARED"] = len(mrg); V["V02_BAD"] = len(rsdata.v02_disagreements(mrg))
    V["V02_BIJ"] = int((mrg.bijective.astype(int) == 1).sum()); V["V02_NMAX"] = int(mrg.n.max())
    V["VERIFY_NMAX"] = int(max(va.n.max(), vb.n.max()))
    bijM = M[M.bijective.astype(int) == 1]
    assert bool((bijM.gamma_min.astype(int) == bijM.cycles.astype(int) - 1).all()), "bijective records must carry gamma_min = m - 1"
    V["N_RECORDS"] = len(M); V["N_RECORDS_BIJ"] = len(bijM)
    V["NMAX"] = int(M.n.max())
    v154 = verif.v154_n22()
    assert (v154["rule"], v154["n"]) == (154, 22) and len(M[(M.rule == 154) & (M.n == 22)]) == 0
    assert v154["gamma_min"] == v154["cycles"] - 1 and v154["selected_cycles"] == v154["cycles"] and v154["g1_closed_classes"] == 1
    V["V154_KSTAR"] = int(v154["kstar"]); V["V154_CYCLES"] = int(v154["cycles"])
    V["V154_CPUMIN"] = f"{v154['cpu_seconds'] / 60:.0f}"; V["V154_GB"] = f"{v154['peak_rss_mb'] / 1000:.1f}"
    V["V154_FILE"] = verif.V154_N22
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
                if len(w):
                    row[str(n)] = int(w.kstar.iloc[0])
                elif (r, n) == (v154["rule"], v154["n"]):
                    row[str(n)] = f"{int(v154['kstar'])}†"
                else:
                    row[str(n)] = "."
        rows.append(row)
    assert not any(v == "." for row in rows for v in row.values()), "a k* cell is not computed"
    V["TABLE_KSTAR"] = ("k* by class (rows) and n (columns); n = 4..7 from v0.2, n >= 8 from `mechanisms.csv`; † = not computed in this "
                        f"study, value from the verification (`{verif.V154_N22}`):\n\n" + md_table(pd.DataFrame(rows)))
    mech_rows = [
        ("94", "k* >= 1 iff 3 | n", "crystal capture, (011)^{n/3}, 3 phases", "k* = 1 at every 3 | n, n >= 6: proved (verification, 5.7); 3 ∤ n gives k* = 0: computed"),
        ("43, 142", "k* >= 1 iff 4 | n", "crystal capture, travelling (0011)^{n/4}", "radius computed to 400; reachability computed/sampled"),
        ("35", "k* >= 1 iff 3 | n", "code-101 carriers = {10,100}-words; fewest 10-blocks selected; a0 = 0 at 3 | n", "computed"),
        ("154", "k* >= 1 iff n = 2^k", "zero state; rule 90 on one parity class, a permutation on the other states", "proved for all n >= 3 (verification, 5.7)"),
        ("60, 90", "k* >= 1 iff n = 2^k", "nilpotent at 2^k (v0.2)", "proved (v0.2)"),
        ("22", "k* >= 1 iff seed of 0 returns", "zero state", "seed set proved for 4 | n; other n: seed orbits up to 256 with open n (5.3); reachability computed/sampled"),
        ("26", "2^k: zero state; else code 7", "zero state; 111-defects in (100)", "zero-state radius proved for all n (5.3, 5.7); reachability at 2^k computed/sampled; rest resists (5.8)"),
        ("122", "2^k - 1: zero state; else code 2", "zero state; checkerboard", "checkerboard selection resists; partial results of the verification in 5.8"),
        ("37", "k* = 0 iff n mod 6 in {0, 5}", "period-6 defect family", "computed"),
        ("45", "only n = 8", "uniform 2-cycle radius 2 at n = 8; odd n bijective", "odd n proved; n = 8 computed"),
        ("73", "only n = 9", "no carrier of code 7 selected at n = 9", "computed"),
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
    za = Z[Z.zero_alone_selected == 1].merge(M[["rule", "n", "cycles"]], on=["rule", "n"])
    multi = za[za.cycles.astype(int) > 1]; single = za[za.cycles.astype(int) == 1]
    assert bool(multi.g2_holds.astype(str).eq("True").all()), "Lemma B flag false where the zero state is selected alone among several cycles"
    V["ZERO_ALONE"] = len(za); V["ZERO_ALONE_MULTI"] = len(multi); V["ZERO_ALONE_SINGLE"] = len(single)
    V["ZERO_SINGLE_WHERE"] = "; ".join(f"class {int(r)} at n = {', '.join(map(str, sorted(g.n)))}" for r, g in single.groupby("rule"))
    so = pd.read_csv(os.path.join(OUT, "seed_orbits.csv"))
    V["SEED_CAP"] = "400000"
    ss = verif.seed_status(so)
    lst = lambda v: ", ".join(map(str, sorted(int(x) for x in v))) if len(v) else "none"
    srows = []
    for r in (22, 26, 122, 154):
        s = ss[ss.rule == r]; cap = s[s.capped == 1]
        srows.append({"rule": r, "returns to 0 at n": lst(s[s.status == "returns"].n),
                      "undetermined at the cut-off of this study": len(cap),
                      "of these closed by the verification's simulation": int((cap.source == "verification (simulation)").sum()),
                      "decided by a proposition only": int(cap.source.str.startswith("Proposition").sum()),
                      "open n": lst(cap[cap.status == "open"].n)})
    V["TABLE_SEED"] = md_table(pd.DataFrame(srows))
    V["SEED_OWN_FILE"] = verif.SEED_OWN
    s22 = ss[ss.rule == 22]
    V["R22_OTHER"] = lst(s22[(s22.status == "returns") & (s22.n % 4 != 0)].n)
    new22 = s22[(s22.status == "returns") & (s22.capped == 1)]
    V["R22_NEW"] = "; ".join(f"n = {int(r.n)}, reached after {int(r.transient_own)} steps," for r in new22.itertuples())
    assert len(new22) == 1
    V["R22_OPEN"] = lst(s22[s22.status == "open"].n)
    open22 = s22[s22.status == "open"]
    V["SEED_BUDGET"] = f"{int(open22.budget.max()):.0e}".replace("e+0", "·10^").replace("e+", "·10^") if len(open22) else "-"
    near = {2 ** k - d for k in range(2, 10) for d in (0, 1, 2)}
    V["R22_EXTRA"] = lst([n for n in s22[s22.status == "returns"].n if int(n) not in near])
    k22 = sorted(set(int(r.n) for r in M[(M.rule == 22) & (M.kstar >= 1)].itertuples()) | set(int(r.n) for r in v02[(v02.rule == 22) & (v02.kstar >= 1) & (v02.n < 8)].itertuples()))
    V["K22_N"] = ranges(k22).replace("-", "..")
    assert set(k22) == set(int(n) for n in s22[(s22.status == "returns") & (s22.n <= V["NMAX"])].n)
    s122 = ss[ss.rule == 122]
    V["R122_RET"] = lst(s122[s122.status == "returns"].n)
    V["R122_OPEN"] = lst(s122[s122.status == "open"].n); V["R122_NOPEN"] = int((s122.status == "open").sum())
    V["R122_SETTLED"] = int(((s122.capped == 1) & (s122.status == "no return")).sum())
    assert all((n + 1) & n == 0 for n in s122[s122.status == "returns"].n), "a rule-122 return outside n = 2^k - 1"
    for r in (26, 154):
        c = ss[(ss.rule == r) & (ss.capped == 1)]
        assert bool((c.n % 2 == 0).all()) and not any((n & (n - 1)) == 0 for n in c.n) and bool((c.status == "no return").all())
        assert all((n & (n - 1)) == 0 for n in ss[(ss.rule == r) & (ss.status == "returns")].n)
    c26 = ss[(ss.rule == 26) & (ss.capped == 1)]
    V["R26_CAPPED"] = len(c26); V["R26_SIM"] = int((c26.source == "verification (simulation)").sum())
    k37 = sorted(int(n) for n in M[(M.rule == 37) & (M.kstar == 0)].n)
    V["K37_ZERO"] = lst(k37)
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
    # class 45 at even n >= 10 and class 73 (A2, A3): sentences generated from mechanisms.csv and cycle_orbits.csv.gz
    uni = lambda rule: O[(O.rule == rule) & O.pattern.map(lambda q: set(q) == {"0"})]
    m45 = M[(M.rule == 45) & (M.n % 2 == 0) & (M.n >= 10)]; u45 = uni(45); u45 = u45[(u45.n % 2 == 0) & (u45.n >= 10)]
    assert bool((u45.radius == 1).all()) and len(u45) == len(m45) and bool((m45.kstar == 0).all())
    part = m45[m45.n_selected.astype(int) < m45.cycles.astype(int)]
    exc = []
    for r in part.itertuples():
        us = bool(u45[u45.n == r.n].selected.iloc[0])
        exc.append(f"n = {int(r.n)} ({int(r.n_selected)} of {int(r.cycles)} cycles selected; the uniform 2-cycle is "
                   f"{'selected' if us else 'among those not selected'})")
    V["S45_EVEN"] = ("at every even n >= 10 in the computed range it has radius 1 and all cycles are selected" +
                     (" except at " + " and ".join(exc) if exc else "") + "; k* = 0 at each of these n")
    u73 = uni(73); m73 = M[M.rule == 73]
    sw73 = sorted(int(n) for n in m73[m73.kstar >= 1].n); unsel = sorted(int(n) for n in u73[~u73.selected].n)
    assert sw73 == [9] and 9 in unsel
    o9 = O[(O.rule == 73) & (O.n == 9)]; c9 = o9[o9.codes.str.contains("7")]
    assert not c9.selected.any()
    grp = o9[o9.selected].groupby(["temporal_period", "spatial_period"]).orbit_size.sum()
    sel9 = " and ".join(f"{int(v)} cycles of temporal period {int(T)} and spatial period {int(sp)}" for (T, sp), v in grp.items())
    others = []
    for n in [n for n in unsel if n != 9]:
        cn = O[(O.rule == 73) & (O.n == n) & O.codes.str.contains("7")]
        others.append(f"n = {n}, where it is again not selected (potential {int(u73[u73.n == n].gamma.iloc[0])} against the minimum "
                      f"{int(m73[m73.n == n].gamma_min.iloc[0])}) but {int(cn.selected.sum())} of the {len(cn)} orbits carrying code 7 are, so k* stays 0")
    V["S73"] = (f"The only switch for n >= 8 is n = 9: there none of the {len(c9)} orbits carrying code 7 is selected (among them the "
                f"uniform 2-cycle); the selected cycles are {sel9}, {int(m73[m73.n == 9].n_selected.iloc[0])} of "
                f"{int(m73[m73.n == 9].cycles.iloc[0])}. The uniform 2-cycle is selected at every other n in the computed range"
                + (" except " + "; ".join(others) if others else ""))
    srows = []
    for f in sorted(glob.glob(os.path.join(OUT, "sampled_reach", "rule*_n*.csv"))):
        s = pd.read_csv(f)
        srows.append(dict(rule=int(s.rule.iloc[0]), n=int(s.n.iloc[0]), target=s.target.iloc[0],
                          target_radius_ge2=int(s.target_radius_ge2.iloc[0]), sampled=len(s),
                          distinct_rotation_orbits=s.cycle_label.nunique(), reach_target=int(s.found.sum()),
                          max_path_len=int(s.path_len.max())))
        assert "path" in s.columns, f"{f}: paths not stored (re-run sample_reach.py)"
        assert bool((s[s.found == 1].path.fillna("").map(lambda t: len(t.split(";")) if t else 0) == s[s.found == 1].path_len).all())
    V["TABLE_SAMPLED"] = md_table(pd.DataFrame(srows).sort_values(["rule", "n"]).rename(columns={"distinct_rotation_orbits": "distinct rotation orbits of cycles"}))
    P = pd.read_csv(os.path.join(OUT, "predictions_outcome.csv"))
    V["PRED_COUNTS"] = "; ".join(f"{k}: {v}" for k, v in P.outcome.value_counts().items())
    V["PRED_ROWS"] = len(P)
    V["TABLE_PRED"] = md_table(P)
    R = verif.recount()
    om = R[R.study_reported_outcome == "omitted"]
    V["PRED_PARTS"] = len(R); V["PRED_COVERED"] = len(R) - len(om); V["PRED_UNCOVERED"] = len(om)
    V["PRED_UNCOVERED_COUNTS"] = "; ".join(f"{k}: {v}" for k, v in om.own_outcome.value_counts().items())
    V["TABLE_PRED_UNCOVERED"] = md_table(om[["id", "sealed_part", "own_outcome"]].rename(
        columns={"sealed_part": "sealed statement (as split by the verification)", "own_outcome": "outcome (verification)"}))
    V["RECOUNT_FILE"] = verif.RECOUNT
    files = [("data/ring_size/mechanisms.csv", "one row per (class, n): cycles, selected, G1 closed classes, radii, crystal test"),
             ("data/ring_size/cycle_orbits.csv.gz", "one row per rotation orbit of cycles: pattern, periods, drift, codes, gamma, radius, selected"),
             ("data/ring_size/mech_cost.csv", "wall time, CPU time (jobs run from 15 Nov 2026 on) and peak memory per job"),
             ("data/ring_size/verify_mech_*.csv", "independent verifier"),
             ("data/ring_size/seed_orbits.csv", "single-flip orbit of the zero state, n = 4..256"),
             ("data/ring_size/crystal_radius.csv", "every single flip of the crystals, p | n up to 400"),
             ("data/ring_size/lightcone.csv", "healing times on the line (Lemma H)"),
             ("data/ring_size/injectivity.csv", "pair-graph certificates (Lemma P)"),
             ("data/ring_size/rule35_blocks.csv, code_carriers.csv, g1_distance_154.csv, zero_mechanism.csv", "derived tables (analyze_mechanisms.py)"),
             ("data/ring_size/sampled_reach/", "sampled reachability beyond n = 22, with the one-flip path found for every sample"),
             ("data/ring_size/factor_search.csv", "block maps of width <= 4 intertwining rule 154 with a radius-1 rule"),
             ("data/ring_size/stopped_runs.csv", "jobs stopped unfinished (stopped_runs.py)"),
             ("data/ring_size/predictions_outcome.csv", "outcomes of the sealed predictions P1-P9 and of the k* table for n = 21, 22"),
             ("data/ring_size/MANIFEST.sha256", "SHA-256 of every file in data/ring_size"),
             ("code/ring_size/", "mech, verify_mech, run_mech, run_local, ringlang, lightcone, sample_reach, analyze_mechanisms, check_predictions, stopped_runs, verif, figures_ring_size, make_report, tests"),
             ("VERIFICATION_ring_size.md, verify_ring_size/", "independent verification of 14 Nov 2026: report with a header on how each finding was handled; sealed blind sample, own solver, findings, literature check, proofs for class 94 and rule 154")]
    if os.path.exists(os.path.join(OUT, "atlas", "mechanisms_atlas.csv")):
        files.append(("data/ring_size/atlas/", "atlas: 75 non-switching classes at n = 4..20 and the 13 switching classes at n = 4..7; selected cycles (count, spatial and temporal periods, codes); checkpoint as mech_atlas.jsonl.gz"))
    V["TABLE_FILES"] = md_table(pd.DataFrame(files, columns=["file", "content"]))
    cost = pd.read_csv(os.path.join(OUT, "mech_cost.csv"))
    st = pd.read_csv(os.path.join(OUT, "stopped_runs.csv"))
    assert len(st) == 1 and (int(st.rule.iloc[0]), int(st.n.iloc[0])) == (154, 22)
    r = st.iloc[0]
    stop = (f"Class {int(r.rule)} at n = {int(r.n)}: the job was stopped unfinished after at most about {float(r.awake_hours_upper):.1f} h of "
            f"computation; its wall time of {float(r.wall_hours):.1f} h is not a measure of cost, and its CPU time was not recorded "
            f"(`stopped_runs.csv`). It is not computed in this study. The verification computed the case with its own solver: k* = {V['V154_KSTAR']}, "
            f"{V['V154_CYCLES']} cycles, all selected, {V['V154_CPUMIN']} CPU-minutes, peak memory {V['V154_GB']} GB (`{verif.V154_N22}`).")
    ncpu = int(cost.cpu_seconds.notna().sum())
    V["COST_LINE"] = stop + " " + (f"Mechanism jobs {len(cost)}: sum of the wall times of the jobs {cost.wall_seconds.sum() / 3600:.1f} h, longest job "
                      f"{cost.wall_seconds.max() / 60:.0f} min wall time (class {int(cost.loc[cost.wall_seconds.idxmax(), 'rule'])}, "
                      f"n = {int(cost.loc[cost.wall_seconds.idxmax(), 'n'])}), peak memory {cost.maxrss_mb.max() / 1000:.1f} GB "
                      f"(`mech_cost.csv`). " + ("CPU time was not recorded for these jobs" if ncpu == 0 else f"CPU time is recorded for {ncpu} of these jobs")
                      + "; `run_mech.py` records it for every job run from now on, and any cost cap refers to CPU time.")
    atlas = os.path.join(OUT, "atlas", "mechanisms_atlas.csv")
    if os.path.exists(atlas):
        A = rsdata.load(os.path.join("atlas", "mechanisms_atlas.csv"))
        am = A.merge(v02, on=["rule", "n"], suffixes=("", "_v02"))
        fin = (len(A), len(am), len(rsdata.v02_disagreements(am)))
        abij = int((A.bijective.astype(int) == 1).sum())
        V["ATLAS_NOTE"] = (f"\nAtlas (step 6) [computed]: `data/ring_size/atlas/mechanisms_atlas.csv` holds {len(A)} (class, n) records "
                           f"({A.rule.nunique()} classes: the 75 non-switching classes at n = 4..20 and the 13 switching classes at "
                           f"n = 4..7) with the selected-cycle count, the spatial and temporal periods of the selected cycles, "
                           f"the codes they cover, k_c and k*; the selected orbits are in `cycle_orbits_atlas.csv.gz`. The 13 "
                           f"switching classes at n >= 8 are in `mechanisms.csv`; together these cover all 88 classes at n = 4..20. "
                           f"All {fin[1]} atlas records agree with v0.2 in cycles, selected count, gamma_min, k_c and k* "
                           f"({fin[2]} disagreements; gamma_min is not compared on the {abij} bijective records, where this study writes "
                           f"m - 1 and v0.2 a placeholder). Space-time pictures of selected cycles for the 13 "
                           f"switching classes: the figure in 5.5.")
    else:
        V["ATLAS_NOTE"] = "\nAtlas (step 6): not produced in this run."
    cs = verif.sample_comparison(); sw = verif.sweep88()
    V["VS_RECORDS"] = cs["records_common"]; V["VS_ORBITS"] = cs["orbit_rows_study"]; V["VS_MISMATCH"] = cs["n_mismatches"]
    assert cs["n_mismatches"] == len(bijM), "the only mismatches of the sealed sample were the gamma_min placeholders"
    V["SW_CASES"] = sw["cases_solved"]; V["SW_NMIN"], V["SW_NMAX"] = sw["n_range"]
    assert sw["counterexample_cases"] == []
    V["SW_UNION_FAILS"] = "; ".join(f"rule {a} at n = {b} ({c} closed classes, {d} selected)" for a, b, c, d in sw["S_proper_subset_of_union_cases"])
    g94 = [g for g in verif.g1_classes_94() if g["n"] % 3 == 0 and g["n"] >= 6]
    assert all(g["closed_classes_are_exactly_the_crystal_phases"] and g["cycles_not_reaching_crystal"] == 0 for g in g94)
    V["G94_NMAX"] = max(g["n"] for g in g94); V["G94_CYCLES"] = max(g94, key=lambda g: g["n"])["cycles"]
    V["G94_FILE"] = verif.G1_94; V["PROOF_94"] = verif.PROOF_94; V["PROOF_154"] = verif.PROOF_154
    E = verif.explore_122_26()
    e122 = sorted([e for e in E if e["rule"] == 122 and e["n"] % 2 == 0], key=lambda e: e["n"])
    V["E122_RANGE"] = f"{e122[0]['n']}..{e122[-1]['n']}"
    assert all(e["n_closed_classes"] == 1 and e["cb_in_closed_class"] == e["zero_in_closed_class"] for e in e122)
    V["E122_OUT"] = lst([e["n"] for e in e122 if not e["cb_in_closed_class"]])
    assert any(e["n"] == 26 and e["cb_in_closed_class"] for e in e122) and all(e["n"] % 8 == 2 for e in e122 if not e["cb_in_closed_class"])
    V["E122_PAIR"] = lst([e["n"] for e in e122 if e["closed_class_sizes"] == [2]])
    e26 = sorted([e for e in E if e["rule"] == 26 and e["n"] & (e["n"] - 1)], key=lambda e: e["n"])
    assert all(e["n_closed_classes"] == 1 for e in e26)
    V["E26_RANGE"] = f"{min(e['n'] for e in E if e['rule'] == 26)}..{e26[-1]['n']}"
    V["E26_K0"] = lst([e["n"] for e in e26 if 7 not in e["codes_missing_on_closed_classes"]])
    V["E26_EXC"] = lst([e["n"] for e in e26 if (7 not in e["codes_missing_on_closed_classes"]) != (e["n"] % 3 == 2)])
    assert V["E26_EXC"] == "22" and V["E122_PAIR"] == "6, 14"
    V["EXPLORE_FILE"] = verif.EXPLORE
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
