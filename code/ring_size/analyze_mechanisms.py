"""Derived tables for the ring-size report (reads data/ring_size/mechanisms.csv, cycle_orbits.csv.gz).

  rule35_blocks.csv     class 35: every cycle orbit parsed into blocks 1 0^k; family = words over {10, 100};
                        a = number of 10-blocks, a0 = 2n mod 3; selection status
  code_carriers.csv     for (rule, code) pairs of interest: number of cycle orbits carrying the code and how
                        many of them are selected, per n
  g1_distance_154.csv   class 154 at n = 8, 16: one-flip-graph distance of every cycle to the zero state and
                        the mean number of ones over the cycle
  zero_mechanism.csv    rules with F(0) = 0 among the switching classes: per n, seed returns to 0 (from
                        seed_orbits.csv), selected set == {0}, k*
Usage: python3 analyze_mechanisms.py
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "fw"))
import numpy as np, pandas as pd
import rsdata, fwlib, mech
from scipy.sparse.csgraph import dijkstra

OUT = rsdata.OUT


def blocks(pattern):
    n = len(pattern)
    if "1" not in pattern or "0" not in pattern:
        return None
    i = next(k for k in range(n) if pattern[k] == "1" and pattern[k - 1] == "0")
    s = pattern[i:] + pattern[:i]
    b = re.findall("10+", s)
    return [len(x) for x in b] if "".join(b) == s else None


def main():
    M = rsdata.load("mechanisms.csv"); O = rsdata.load("cycle_orbits.csv.gz")
    rows = []
    for r in O[O.rule == 35].itertuples():
        bl = blocks(r.pattern)
        fam = bl is not None and set(bl) <= {2, 3}
        rows.append(dict(n=r.n, pattern=r.pattern, codes=r.codes, selected=int(r.selected), family=int(fam),
                         a=bl.count(2) if fam else -1, a0=(2 * r.n) % 3, has_code5=int("5" in r.codes),
                         spatial_period=r.spatial_period, temporal_period=r.temporal_period, drift=r.drift))
    B = pd.DataFrame(rows).sort_values(["n", "pattern"])
    B.to_csv(os.path.join(OUT, "rule35_blocks.csv"), index=False)
    # claims checked here and printed (the report quotes this output via the CSV)
    ok1 = bool((B[B.has_code5 == 1].family == 1).all())
    ok2 = bool(((B.family == 1) & (B.has_code5 == 0)).eq((B.family == 1) & (B.a == 0)).all())
    fam = B[B.family == 1]
    ok3 = bool((fam.selected == (fam.a == fam.a0)).all())
    ok4 = bool((B[B.family == 0].selected == 1).all())
    ok5 = bool(((fam.a - fam.a0) % 3 == 0).all())
    print(f"rule35: code5 => family {ok1}; family & no code5 <=> a = 0 {ok2}; family selected <=> a = a0 {ok3}; "
          f"non-family all selected {ok4}; a = a0 mod 3 {ok5}; n = {B.n.min()}..{B.n.max()}")
    pairs = [(35, 5), (122, 2), (26, 7), (37, 2), (37, 5), (73, 7), (94, 0), (94, 1), (94, 2), (94, 4), (94, 7)]
    rows = []
    for rule, code in pairs:
        for n in sorted(O[O.rule == rule].n.unique()):
            t = O[(O.rule == rule) & (O.n == n)]
            c = t[t.codes.str.contains(str(code))]
            k = int(M[(M.rule == rule) & (M.n == n)].kstar.iloc[0])
            rows.append(dict(rule=rule, code=code, n=n, kstar=k, carrier_orbits=len(c),
                             selected_carrier_orbits=int(c.selected.sum()),
                             carrier_patterns=";".join(c.pattern.tolist()[:6])))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "code_carriers.csv"), index=False)
    rows = []
    for n in (8, 16):
        res = fwlib.classify(154, n); cs, es = res["cs"], res["es"]
        G1 = mech.one_flip_graph(es)
        z = int(cs.cyc_of_state[0])
        dist = dijkstra(G1.T.astype(float), indices=z, unweighted=True)
        for j in range(cs.m):
            st = cs.states_of(j)
            rows.append(dict(n=n, cycle_min=int(cs.cyc_min[j]), pattern=mech.bits(int(cs.cyc_min[j]), n),
                             period=int(cs.period[j]), mean_ones=float(np.mean([bin(int(s)).count("1") for s in st])),
                             g1_distance_to_zero=int(dist[j]) if np.isfinite(dist[j]) else -1,
                             selected=int(j in set(res["stable"].tolist()))))
    D = pd.DataFrame(rows)
    D.to_csv(os.path.join(OUT, "g1_distance_154.csv"), index=False)
    for n in (8, 16):
        d = D[D.n == n]
        print(f"rule154 n={n}: cycles {len(d)}, unreachable {int((d.g1_distance_to_zero < 0).sum())}, "
              f"max distance {d.g1_distance_to_zero.max()}, Spearman(mean ones, distance) "
              f"{d.mean_ones.corr(d.g1_distance_to_zero, method='spearman'):.3f}")
    so = pd.read_csv(os.path.join(OUT, "seed_orbits.csv"))
    rows = []
    for rule in (22, 26, 122, 154, 60, 90):
        for r in M[M.rule == rule].itertuples():
            s = so[(so.rule == rule) & (so.n == r.n)]
            ret = int(s.returns_to_zero.iloc[0]) if len(s) and str(s.returns_to_zero.iloc[0]) != "nan" else -1
            zero_alone = int(r.n_selected == 1 and str(r.selected_cover) == "0")
            rows.append(dict(rule=rule, n=r.n, seed_returns=ret, zero_alone_selected=zero_alone, kstar=r.kstar,
                             g2_holds=r.g2_holds))
    Z = pd.DataFrame(rows)
    Z.to_csv(os.path.join(OUT, "zero_mechanism.csv"), index=False)
    zz = Z[Z.seed_returns >= 0]
    print("zero mechanism: seed returns <=> zero alone selected:",
          bool((zz.seed_returns == zz.zero_alone_selected).all()), "over", len(zz), "(rule, n) pairs",
          "rules", sorted(zz.rule.unique()))


if __name__ == "__main__":
    main()
