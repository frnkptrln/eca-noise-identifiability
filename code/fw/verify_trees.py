"""Verifier (a'): exact check of the reduction to cycles.

By the Markov chain tree theorem, pi_eps(x) is proportional to the sum over spanning in-trees rooted
at x of the product of transition probabilities eps^r (1-eps)^(n-r), r(u->v) = H(F(u), v); all terms
are positive, so ord pi_eps(x) = W(x) - min_y W(y) with W(x) the minimum total resistance of an
in-tree rooted at x on the FULL state graph (2^n nodes, complete). This file computes W(x) directly:
  method 'nx'  : networkx Edmonds, one call per root on the reversed graph (independent code), n <= 6
  method 'hier': the all-roots contraction of hier.py applied to the full state graph, n <= 8
and compares W(x) - min W with the cycle formula ord pi(x) = min_C[gamma(C) + R(C->x)] - min gamma
from fwlib/orders. Output: data/fw_verify_trees.csv (one row per n, rule, method)."""
import os, sys, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, orders, hier
from verify_stationary import succ_def, popcount

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")


def resistance_matrix(rule, n):
    F = succ_def(rule, n)
    S = 1 << n
    return popcount(F[:, None] ^ np.arange(S)[None, :])       # R[u, v] = H(F(u), v)


def W_nx(R):
    import networkx as nx
    S = len(R)
    out = np.zeros(S, dtype=np.int64)
    for r in range(S):
        G = nx.DiGraph()
        for u in range(S):
            for v in range(S):
                if u != v and u != r:
                    G.add_edge(v, u, weight=int(R[u, v]))    # reversed edge of u -> v
        A = nx.minimum_spanning_arborescence(G, attr="weight", preserve_attrs=True)
        assert [x for x in A.nodes if A.in_degree(x) == 0] == [r]
        out[r] = int(sum(d["weight"] for _, _, d in A.edges(data=True)))
    return out


def W_hier(R):
    V = R.copy()
    np.fill_diagonal(V, 0)
    H = hier.edmonds_all_roots(hier.MatrixProvider(V), L0=int(V.max()))
    return H.gamma


def job(args):
    n, rule, methods = args
    R = resistance_matrix(rule, n)
    res = fwlib.classify(rule, n, keep_dists=True)
    pred = orders.state_orders(res)
    rows = []
    for meth in methods:
        W = W_nx(R) if meth == "nx" else W_hier(R)
        obs = W - W.min()
        rows.append(dict(n=n, rule=rule, method=meth, states=1 << n,
                         mismatches=int((obs != pred).sum()), max_ord=int(obs.max()),
                         Wmin=int(W.min()), gmin=int(res["gmin"])))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nx-nmax", type=int, default=5, help="networkx for all 256 rules up to this n")
    ap.add_argument("--nx-reps-n", type=int, default=6, help="networkx for the 88 class representatives at this n")
    ap.add_argument("--hier-nmax", type=int, default=8)
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    reps = set(fwlib.class_reps())
    jobs = []
    for n in range(3, max(a.nx_nmax, a.nx_reps_n, a.hier_nmax) + 1):
        for rule in range(256):
            meths = []
            if n <= a.nx_nmax or (n == a.nx_reps_n and rule in reps):
                meths.append("nx")
            if n <= a.hier_nmax:
                meths.append("hier")
            if meths:
                jobs.append((n, rule, tuple(meths)))
    from multiprocessing import Pool
    t0 = time.time(); rows = []
    with Pool(a.workers) as pool:
        for i, r in enumerate(pool.imap_unordered(job, jobs)):
            rows.extend(r)
            if (i + 1) % 256 == 0:
                print(f"{i+1}/{len(jobs)} at {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows).sort_values(["n", "rule", "method"]).reset_index(drop=True)
    df.to_csv(os.path.join(OUT, "fw_verify_trees.csv"), index=False)
    print(f"wall {time.time()-t0:.0f}s rows", len(df), "total mismatching states", int(df.mismatches.sum()),
          "Wmin==gmin everywhere", bool((df.Wmin == df.gmin).all()),
          "nx rows", int((df.method == "nx").sum()), "hier rows", int((df.method == "hier").sum()))


if __name__ == "__main__":
    main()
