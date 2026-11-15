"""Step 3: Lemma Z for all rules with F(0) = 0 and Lemma P (pair graph) for all 256 rules, n = 3..15, against brute force.
Also rebuilds the pair-graph certificate (components, periods) for all 256 rules and compares with the study's
data/ring_size/injectivity.csv.  Writes out/lemmaZP.json and out/pairgraph_all256.csv."""
import csv
import json
import os
import sys
import time
from math import gcd

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P
from p2lib import K

OUT = os.path.join(P.HERE, "out")
NMIN, NMAX = 3, 15
t0 = time.process_time()

# ---------------------------------------------------------------- Lemma Z
z = {"cases": 0, "counterexamples": [], "radius_ge2": 0, "radius_ge2_single_cycle_map": 0, "seed_returns": 0}
for rule in range(0, 256, 2):                       # F(0) = 0 iff f(000) = 0 iff the rule number is even
    for n in range(NMIN, NMAX + 1):
        c = P.Case(rule, n)
        assert c.F[0] == 0
        zc = int(c.cyc[0])
        ret = all(int(c.attr[1 << i]) == zc for i in range(1))          # orbit of e_0 ends on the cycle {0}
        ret_all = all(int(c.attr[1 << i]) == zc for i in range(n))      # every single flip of 0 (definition of r(0) >= 2)
        r2 = not bool(c.has_out[zc])                                    # no one-flip edge out of {0}
        z["cases"] += 1
        z["radius_ge2"] += r2
        z["radius_ge2_single_cycle_map"] += (r2 and c.m == 1)
        z["seed_returns"] += ret
        if not (r2 == ret == ret_all):
            z["counterexamples"].append([rule, n])

# ---------------------------------------------------------------- Lemma P
def f(rule, a, b, c):
    return (rule >> (4 * a + 2 * b + c)) & 1


VERT = [(a, b, a2, b2) for a in (0, 1) for b in (0, 1) for a2 in (0, 1) for b2 in (0, 1)]
IDX = {v: i for i, v in enumerate(VERT)}
OFF = [v[:2] != v[2:] for v in VERT]


def pair_graph(rule):
    A = np.zeros((16, 16), dtype=object)
    adj = [[] for _ in range(16)]
    for (a, b, a2, b2) in VERT:
        for c in (0, 1):
            for c2 in (0, 1):
                if f(rule, a, b, c) == f(rule, a2, b2, c2):
                    i, j = IDX[(a, b, a2, b2)], IDX[(b, c, b2, c2)]
                    A[i, j] = 1
                    adj[i].append(j)
    return A, adj


def sccs(adj):
    """Strongly connected components by forward/backward reachability (16 vertices)."""
    n = len(adj)
    reach = [set() for _ in range(n)]
    for s in range(n):
        st = [s]
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in reach[s]:
                    reach[s].add(v)
                    st.append(v)
    comp, seen = [], set()
    for s in range(n):
        if s in seen:
            continue
        cset = {t for t in range(n) if (t == s) or (t in reach[s] and s in reach[t])}
        seen |= cset
        comp.append(sorted(cset))
    return comp


def period(cset, adj):
    """gcd of the lengths of the closed walks inside the component (0 if it contains no edge)."""
    s = cset[0]
    lev = {s: 0}
    st = [s]
    g = 0
    inside = set(cset)
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in inside:
                continue
            if v not in lev:
                lev[v] = lev[u] + 1
                st.append(v)
            g = gcd(g, lev[u] + 1 - lev[v])
    return abs(g)


def matpow_trace(A, n):
    R = np.eye(16, dtype=object)
    B = A.copy()
    e = n
    while e:
        if e & 1:
            R = R.dot(B)
        B = B.dot(B)
        e >>= 1
    return int(sum(R[i, i] for i in range(16)))


rows = []
p = {"cases": 0, "trace_identity_failures": [], "criterion_counterexamples": [], "certified_rules": [],
     "bijective_all_odd_n_but_not_certified": [], "injective_iff_trace_failures": []}
for rule in range(256):
    A, adj = pair_graph(rule)
    comps = sccs(adj)
    offper = []
    for cset in comps:
        if any(OFF[v] for v in cset):
            per = period(cset, adj)
            if per > 0:                       # components without an edge carry no closed walk
                offper.append(per)
    certified = all(q % 2 == 0 for q in offper)
    bij_odd = True
    for n in range(NMIN, NMAX + 1):
        F, cm = K.build_F(rule, n)
        cnt = np.bincount(F, minlength=1 << n).astype(np.int64)
        pairs = int((cnt * cnt).sum())                      # number of (x, y) with F x = F y
        bij = bool(cnt.max() == 1)
        tr = matpow_trace(A, n)
        p["cases"] += 1
        if tr != pairs:
            p["trace_identity_failures"].append([rule, n])
        if (tr == (1 << n)) != bij:
            p["injective_iff_trace_failures"].append([rule, n])
        if n % 2 == 1:
            bij_odd &= bij
            if certified and not bij:
                p["criterion_counterexamples"].append([rule, n])
    if certified:
        p["certified_rules"].append(rule)
    elif bij_odd:
        p["bijective_all_odd_n_but_not_certified"].append(rule)
    rows.append({"rule": rule, "certified_bijective_odd_n": int(certified),
                 "offdiag_scc_periods": ";".join(map(str, sorted(offper, reverse=True))),
                 "n_components": len(comps), "bijective_at_all_odd_n_3_15": int(bij_odd)})
with open(os.path.join(OUT, "pairgraph_all256.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0]))
    w.writeheader()
    w.writerows(rows)

# comparison with the study's certificate file
study = list(csv.DictReader(open(os.path.join(P.REPO, "data", "ring_size", "injectivity.csv"))))
cmpr = {"rows": len(study), "certified_equal": 0, "periods_equal": 0, "differences": []}
for r in study:
    own = rows[int(r["rule"])]
    a = int(r["certified_bijective_odd_n"]) == own["certified_bijective_odd_n"]
    b = sorted(r["offdiag_scc_periods"].split(";")) == sorted(own["offdiag_scc_periods"].split(";"))
    cmpr["certified_equal"] += a
    cmpr["periods_equal"] += b
    if not (a and b):
        cmpr["differences"].append({"rule": int(r["rule"]), "study": [r["certified_bijective_odd_n"], r["offdiag_scc_periods"]],
                                    "own": [own["certified_bijective_odd_n"], own["offdiag_scc_periods"]]})
res = {"n_range": [NMIN, NMAX], "lemmaZ": z, "lemmaP": p, "injectivity_csv": cmpr,
       "rule154": rows[154], "rule45": rows[45], "cpu_seconds": round(time.process_time() - t0, 2)}
json.dump(res, open(os.path.join(OUT, "lemmaZP.json"), "w"), indent=1)
print(json.dumps(res)[:3000])
