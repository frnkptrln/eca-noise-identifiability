"""Outcomes of the sealed predictions P1-P9 and of the k* table for n = 21, 22 in PREDICTIONS_ring_size.md.
Writes data/ring_size/predictions_outcome.csv (id, part, outcome, evidence).

Scope: 50 rows. They do not cover every sealed statement: the general expectations G1-G3, the column
"proof for all n expected?" of the class table and some sub-claims of P3, P4, P8, P9 are outside this table
(29 of the 92 single statements counted by the verification; listed in the report from
verify_ring_size/phase2/out/predictions_recount.csv).
Outcomes are decided from the data files, with three exceptions that are stated in the evidence column:
the row "4 does not divide n: no cycle with spatial period 4" is a triviality (holds (trivially)); the k* of
class 154 at n = 22 was not computed by this study and is taken from the verification
(verify_ring_size/phase2/out/v154_n22.json); the k* values of class 154 at n = 24, 28, 32 are not computed
(not tested), and the evidence column names the proof that now implies them.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pandas as pd
import rsdata, verif

OUT = rsdata.OUT


def main():
    M = rsdata.load("mechanisms.csv"); O = rsdata.load("cycle_orbits.csv.gz")
    so = pd.read_csv(os.path.join(OUT, "seed_orbits.csv"))
    cr = pd.read_csv(os.path.join(OUT, "crystal_radius.csv"), dtype={"word": str})
    rows = []

    def add(pid, part, ok, ev, outcome=None):
        rows.append(dict(id=pid, part=part, outcome=outcome or ("holds" if ok else "fails"), evidence=ev))

    def m(rule, cond):
        return M[(M.rule == rule) & cond(M)]
    ns = sorted(M.n.unique()); rng = f"n = {min(ns)}..{max(ns)}"
    # P1
    d = m(94, lambda M: M.n % 3 == 0)
    sel = O[(O.rule == 94) & (O.n % 3 == 0) & O.selected]
    add("P1", "3|n: selected set = the 3 shifts of (011)^{n/3}",
        bool((d.n_selected == 3).all() and (d.crystal_p == 3).all() and sel.pattern.map(lambda p: set(p[i:i+3] for i in range(0, len(p), 3)) <= {"011", "101", "110"}).all()),
        f"mechanisms.csv, cycle_orbits.csv.gz, {rng}")
    add("P1", "3|n: radius of the crystal 2, every other cycle radius 1",
        bool((d.radius_selected_min == 2).all() and (d.radius_other_max == 1).all()), "mechanisms.csv")
    add("P1", "3|n: one-flip graph has a single closed class, the crystal orbit", bool((d.g1_closed == 1).all()),
        f"mechanisms.csv: g1_closed = {sorted(int(v) for v in d.g1_closed.unique())} (one closed class per phase)")
    o = O[(O.rule == 94) & (O.n % 3 != 0)]
    bad = o[o.codes.map(lambda c: set(c) <= set("356"))]
    add("P1", "3 does not divide n: no cycle avoids all of codes 0,1,2,4,7", len(bad) == 0,
        f"cycle_orbits.csv.gz: {len(bad)} counterexample orbits")
    # P2
    for r in (43, 142):
        d = m(r, lambda M: M.n % 4 == 0)
        add("P2", f"class {r}, 4|n: selected = one travelling cycle (0011)^{{n/4}}, T = 4, radius 2, others radius 1, single closed class",
            bool((d.n_selected == 1).all() and (d.crystal_p == 4).all() and (d.selected_temporal_periods == "4").all()
                 and (d.radius_selected_min == 2).all() and (d.radius_other_max == 1).all() and (d.g1_closed == 1).all()),
            "mechanisms.csv")
    add("P2", "4 does not divide n: no cycle with spatial period 4", True, "trivial: the spatial period divides n",
        outcome="holds (trivially)")
    # P3
    ok = True
    for n in [n for n in ns if n % 3 == 0]:
        t = O[(O.rule == 35) & (O.n == n)]
        ok &= set(t[t.codes.str.contains("5")].orbit_rep_min_state) == set(t[~t.selected].orbit_rep_min_state)
    add("P3", "3|n: cycles containing code 5 = cycles not selected", bool(ok), "cycle_orbits.csv.gz")
    car = O[(O.rule == 35) & (O.n % 3 == 0) & O.codes.str.contains("5")]
    add("P3", "they have spatial period 3 or consist of 3-periodic segments", bool((car.spatial_period == 3).all()),
        f"cycle_orbits.csv.gz: {int((car.spatial_period == 3).sum())} of {len(car)} carrier orbits have spatial period 3 "
        f"({int((car.spatial_period == car.n).sum())} have spatial period n); rule35_blocks.csv: they are travelling words "
        "over the blocks 10 and 100")
    # P4
    c = pd.read_csv(os.path.join(OUT, "code_carriers.csv"), dtype={"carrier_patterns": str})
    c = c[(c.rule == 122) & (c.code == 2)]
    sp4 = O[(O.rule == 122) & O.selected & (O.spatial_period == 4) & O.codes.str.contains("2")]
    add("P4", "4|n: a selected cycle with spatial period 4 carries code 2", len(sp4) > 0,
        "cycle_orbits.csv.gz: the only carrier of code 2 is the checkerboard (spatial period 2)")
    d = m(122, lambda M: M.n.isin([9, 10, 11, 13, 17, 18, 19]))
    add("P4", "missing code is 2 at n in {9,10,11,13,17,18,19}", bool((d.k_c.str.split("-").str[2] != "0").all()), "mechanisms.csv")
    d14 = m(122, lambda M: M.n == 14).iloc[0]; d15 = m(122, lambda M: M.n == 15).iloc[0]
    add("P4", "n = 15: zero state alone with radius >= 2", bool(d15.n_selected == 1 and d15.radius_selected_min >= 2), "mechanisms.csv")
    add("P4", "n = 14: uniform states selected with radius >= 2", bool(d14.radius_selected_min >= 2),
        f"mechanisms.csv: selected = zero state and checkerboard, radius {int(d14.radius_selected_min)}")
    # P5
    d = m(154, lambda M: (M.n % 2 == 0) & ~M.n.isin([8, 16]))
    add("P5", "154, even n not a power of 2: every cycle radius 1, one-flip graph strongly connected",
        bool((d.g1_sccs == 1).all() and (d.radius_selected_max == 1).all()), f"mechanisms.csv, n = {sorted(d.n.tolist())}")
    d = m(154, lambda M: M.n.isin([8, 16]))
    add("P5", "154, n = 8, 16: zero radius 2, others radius 1, {0} the single closed class",
        bool((d.radius_selected_min == 2).all() and (d.radius_other_max == 1).all() and (d.g1_closed == 1).all()
             and (d.n_selected == 1).all()), "mechanisms.csv")
    # P6
    Z = pd.read_csv(os.path.join(OUT, "zero_mechanism.csv"))
    z = Z[(Z.rule == 22) & (Z.seed_returns >= 0)]
    add("P6", "22: k* = 1 exactly where the single-flip orbit of 0 returns to 0", bool((z.seed_returns == (z.kstar >= 1)).all()),
        f"zero_mechanism.csv, n = {z.n.min()}..{z.n.max()}")
    d = m(26, lambda M: M.n == 16).iloc[0]
    add("P6", "26, n = 16: zero state alone, k* = 2", bool(d.n_selected == 1 and d.kstar == 2), "mechanisms.csv")
    d = m(26, lambda M: (M.kstar >= 1) & (M.n != 16))          # sealed: "at the other n with k* = 1 the missing code is 7"
    bad = d[d.selected_cover != "0123456"]
    add("P6", "26, other n with k* >= 1: missing code 7", len(bad) == 0,
        "mechanisms.csv: " + ("; ".join(f"fails at n = {int(r.n)} (codes covered by the selected set: {r.selected_cover}; number of selected cycles: {int(r.n_selected)})"
                                         for r in bad.itertuples()) + "; " if len(bad) else "")
        + "holds at n = " + ", ".join(str(int(v)) for v in d[d.selected_cover == "0123456"].n))
    # P7
    d = m(45, lambda M: M.n == 8).iloc[0]
    add("P7", "45, n = 8: uniform 2-cycle selected alone", bool(d.n_selected == 1 and d.selected_cover == "07"), "mechanisms.csv")
    inj = pd.read_csv(os.path.join(OUT, "injectivity.csv"))
    add("P7", "45, odd n: bijective", bool(inj[inj.rule == 45].certified_bijective_odd_n.iloc[0] == 1), "injectivity.csv (proved)")
    o = O[(O.rule == 45) & (O.n % 2 == 0) & (O.n >= 10) & O.pattern.map(lambda p: set(p) == {"0"})]
    add("P7", "45, even n >= 10: the uniform 2-cycle has radius 1", bool((o.radius == 1).all()), f"cycle_orbits.csv.gz, {len(o)} n")
    # P8
    d = M[M.rule == 37]
    add("P8", "37: k* = 0 iff n mod 6 in {0, 5}", bool(((d.n % 6).isin([0, 5]) == (d.kstar == 0)).all()), f"mechanisms.csv, {rng}")
    d = M[M.rule == 73]
    add("P8", "73: the only switch for n >= 8 is n = 9", bool(((d.n == 9) == (d.kstar >= 1)).all()), f"mechanisms.csv, {rng}")
    # k* at 21, 22
    pred = {35: (1, 0), 94: (1, 0), 43: (0, 0), 142: (0, 0), 122: (1, 1), 60: (0, 0), 90: (0, 0), 154: (0, 0),
            45: (0, 0), 73: (0, 0), 37: (1, 1)}
    for r, (k21, k22) in pred.items():
        for n, k in ((21, k21), (22, k22)):
            d = m(r, lambda M: M.n == n)
            if len(d):
                add("k*(21,22)", f"class {r}, n = {n}: k* = {k}", int(d.kstar.iloc[0]) == k, f"mechanisms.csv (computed {int(d.kstar.iloc[0])})")
            elif (r, n) == (154, 22):
                v = verif.v154_n22()
                assert (v["rule"], v["n"]) == (154, 22)
                add("k*(21,22)", f"class {r}, n = {n}: k* = {k}", int(v["kstar"]) == k,
                    f"not computed in this study (job stopped unfinished, stopped_runs.csv); computed by the verification: "
                    f"k* = {int(v['kstar'])} ({verif.V154_N22})")
            else:
                add("k*(21,22)", f"class {r}, n = {n}: k* = {k}", False, "not computed", outcome="not tested")
    for n in (21, 22):
        d = m(22, lambda M: M.n == n); s = so[(so.rule == 22) & (so.n == n)]
        add("k*(21,22)", f"class 22, n = {n}: k* = 1 iff seed returns", int(d.kstar.iloc[0] >= 1) == int(s.returns_to_zero.iloc[0]),
            "mechanisms.csv, seed_orbits.csv")
    # P9
    sr = pd.read_csv(os.path.join(OUT, "sampled_reach", "rule154_n32.csv"))
    add("P9", "154, n = 32: zero radius >= 2", bool(sr.target_radius_ge2.iloc[0] == 1), "sampled_reach/rule154_n32.csv; proved (Proposition R154)")
    add("P9", "154, n = 32: sampled cycles reach 0 by one-flip steps", bool(sr.found.all()),
        f"sampled_reach/rule154_n32.csv: {int(sr.found.sum())}/{len(sr)} (observed); proved for every cycle and every n = 2^k "
        f"by the verification ({verif.PROOF_154}, Theorem 1)", outcome="holds (observed, sampled)" if sr.found.all() else None)
    add("P9", "154: k* = 1 at n = 32, k* = 0 at n = 24, 28", False,
        f"not computed (no enumeration at these sizes); implied by Theorems 1 and 2 of {verif.PROOF_154} (proved by the verification)",
        outcome="not tested")
    P = pd.DataFrame(rows)
    P.to_csv(os.path.join(OUT, "predictions_outcome.csv"), index=False)
    print(P.outcome.value_counts().to_dict())
    print(P[P.outcome != "holds"][["id", "part", "outcome"]].to_string(index=False))


if __name__ == "__main__":
    main()
