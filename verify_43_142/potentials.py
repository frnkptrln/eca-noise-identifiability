"""Stochastic potentials, selected set and k_c for rules 43 and 142 from the definitions, without Theorem A.

V(C, C') = R(C -> C') from a BFS on the full state graph (report_ring_size.md Section 3; note v0.2 Section 6);
gamma(C) = minimum weight in-tree on the cycles rooted at C with weights V; S = argmin gamma;
k_c = min_C [gamma(C) + R(C -> D_c)] - min gamma, D_c = states containing code c; k* = max_c k_c.
Compared with Corollaries 1-4 and Proposition 3 of PROOF_43_142.md, and with G1 / r(C).

Usage: python potentials.py NMIN NMAX   -> out/potentials.jsonl (one line per (rule, n))
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import networkx as nx
from eca import Dynamics, codes_present, walls, potentials, brute_force_potentials, sccs


def nx_potentials(V):
    m = V.shape[0]
    out = []
    for r in range(m):
        G = nx.DiGraph([(c, a, {"weight": int(V[a, c])}) for a in range(m) for c in range(m) if a != c and a != r])
        if m == 1:
            out.append(0); continue
        T = nx.minimum_spanning_arborescence(G)
        out.append(int(sum(d["weight"] for _, _, d in T.edges(data=True))))
    return np.array(out)


def analyse(rule, n):
    t0 = time.time()
    dyn = Dynamics(rule, n)
    m = dyn.m
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    cp = codes_present(n, xs)
    wst = walls(n, xs)
    V = np.zeros((m, m), dtype=np.int64)
    RD = np.zeros((m, 8), dtype=np.int64)
    for k in range(m):
        dist = dyn.resistance_from_cycle(k)
        for k2 in range(m):
            V[k, k2] = dist[dyn.cycle_states[k2]].min()
        for c in range(8):
            sel = ((cp >> c) & 1) == 1
            RD[k, c] = dist[sel].min()
    assert np.all(np.diag(V) == 0) and np.all(V[~np.eye(m, dtype=bool)] >= 1)
    if m <= 40:
        gam = potentials(V)
        gam_nx = nx_potentials(V)
        assert np.array_equal(gam, gam_nx), (rule, n)
        method = "own Edmonds = networkx"
        if m <= 7:
            assert np.array_equal(gam, brute_force_potentials(V)), (rule, n)
            method += " = brute force"
    else:
        gam = nx_potentials(V)
        method = "networkx"
    gmin = int(gam.min())
    S = sorted(np.flatnonzero(gam == gmin).tolist())
    kc = [int((gam + RD[:, c]).min() - gmin) for c in range(8)]
    kstar = max(kc)
    # G1 from V == 1 versus G1 from single flips (Section 1 of the proof)
    e_flip = dyn.one_flip_graph()
    e_V = {(a, b) for a in range(m) for b in range(m) if a != b and V[a, b] == 1}
    _, closed = sccs(m, e_flip)
    cw = [int(wst[s[0]]) for s in dyn.cycle_states]
    radius = [int(min(V[k, k2] for k2 in range(m) if k2 != k)) if m > 1 else None for k in range(m)]
    rec = dict(rule=rule, n=n, m=m, n_periodic=int(dyn.periodic.sum()), gamma_min=gmin,
               selected=S, selected_walls=sorted(set(cw[k] for k in S)), n_selected=len(S),
               selected_states=sorted(int(x) for k in S for x in dyn.cycle_states[k]),
               k=kc, kstar=kstar, closed_classes=closed, G1_flip_equals_V1=(e_flip == e_V),
               potential_method=method)
    # comparison with the document
    chk = {}
    chk["gamma_min = m - 1"] = gmin == m - 1
    chk["S = union of closed classes (single class)"] = len(closed) == 1 and S == closed[0]
    if n % 4 == 0:
        x0 = sum(1 << i for i in range(n) if i % 4 in (2, 3))
        kX = int(dyn.cycle_of_periodic[x0])
        chk["Cor 1: S = {X}"] = S == [kX]
        chk["Cor 2: k = (1,0,1,0,0,1,0,1), k* = 1"] = kc == [1, 0, 1, 0, 0, 1, 0, 1] and kstar == 1
        chk["Prop 3: V(C,X) = |w-n/2|/2"] = all(int(V[k, kX]) == abs(cw[k] - n // 2) // 2 for k in range(m))
        chk["Prop 3: max V(C,X) = n/4 exactly at w in {0,n}"] = (
            int(V[:, kX].max()) == n // 4 and
            sorted(k for k in range(m) if V[k, kX] == n // 4) == sorted(k for k in range(m) if cw[k] in (0, n)))
        chk["Thm 1: r(X) >= 2"] = radius[kX] >= 2
        rec["radius_X"] = radius[kX]
        rec["V_to_X_max"] = int(V[:, kX].max())
    else:
        half = n / 2
        wm = max(v for v in range(0, n + 1, 2) if v < half)
        wp = min(v for v in range(0, n + 1, 2) if v > half)
        K = sorted(k for k in range(m) if cw[k] in (wm, wp))
        chk["Cor 3: S = K"] = S == K
        chk["Cor 3: k = 0 for all c, k* = 0"] = kc == [0] * 8
        rec["K_size"] = len(K)
    chk["G1 (flips) = {V = 1}"] = e_flip == e_V
    rec["checks"] = chk
    rec["seconds"] = round(time.time() - t0, 2)
    return rec


if __name__ == "__main__":
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    path = "out/potentials.jsonl"
    with open(path, "a") as fh:
        for n in range(nmin, nmax + 1):
            for rule in (43, 142):
                r = analyse(rule, n)
                fh.write(json.dumps(r) + "\n"); fh.flush()
                bad = [k for k, v in r["checks"].items() if not v]
                print(rule, n, "m", r["m"], "gmin", r["gamma_min"], "|S|", r["n_selected"], "k", r["k"],
                      "k*", r["kstar"], "FAIL" if bad else "ok", bad, f"{r['seconds']}s", flush=True)
