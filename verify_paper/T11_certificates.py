"""T11 -- the potentials once more, without Edmonds' algorithm: explicit in-trees and an elementary lower bound.

For every cycle u let c(u) = min over u' != u of V(u, u') (the cheapest edge out of u). Every in-tree rooted at r has
one edge out of every u != r, so
        gamma(r) >= LB(r) := sum over u != r of c(u).
Let H be the graph of the cheapest edges (u -> u' with V(u, u') = c(u)). If every cycle reaches r in H, a breadth-first
in-tree of H towards r has weight exactly LB(r), so gamma(r) = LB(r); if not, no in-tree attains LB(r), so
gamma(r) >= LB(r) + 1. Every cycle reaches r in H iff r lies in a strongly connected component of H that no edge of H
leaves and that is the only such component. So one decomposition of H gives: the exact value of gamma on that
component Q, and the bound LB + 1 elsewhere. If min over Q of LB <= min over the rest of (LB + 1), this gives gamma_min
and decides for every r in Q whether it is selected; cycles outside Q are not selected if LB + 1 > gamma_min.
This uses only the matrix V. It is compared with the potentials of the C routine (minimum in-tree for every root):
equality on Q, >= LB + 1 off Q, same selected set where the certificate decides it. With the same bounds
        min_C [LB'(C) + R(C -> D_v)] - gamma_min <= k_v <= min over C in Q of [gamma(C) + R(C -> D_v)] - gamma_min
(LB' = LB on Q, LB + 1 elsewhere); where the two sides agree, k_v is certified without Edmonds.
For up to 40 roots of Q per system the breadth-first in-tree is built and its weight is summed from V.

Systems: rule 154, n = 3..N154; rule 94, n = 5..N94; rules 43, 142, n = 4..N43; rule 26, even n = 4..N26.
Output: out/T11.txt, out/T11_certificates.csv.   Usage: python3 T11_certificates.py [N154=18] [N94=21] [N43=18] [N26=20]
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def certify(rule, n, rng):
    S = vc.System(rule, n, level=2, workers=2)
    m = S.m
    V = S.V.astype(np.int64)
    g = S.gamma
    if m == 1:
        kv = S.indices()[0]
        return dict(m=1, Q=1, exact=True, s_cert=True, s_same=True, kcert=8, trees=0, gmin=0, kv=kv, ok=True)
    np.fill_diagonal(V, 10 ** 6)
    c = V.min(axis=1)
    H = V == c[:, None]
    ncomp, comp = connected_components(csr_matrix(H), directed=True, connection="strong")
    src, dst = np.nonzero(H)
    leaving = np.zeros(ncomp, dtype=bool)
    dif = comp[src] != comp[dst]
    leaving[comp[src[dif]]] = True
    sinks = np.nonzero(~leaving)[0]
    total = int(c.sum())
    LB = total - c
    inQ = np.zeros(m, dtype=bool)
    if len(sinks) == 1:
        inQ = comp == sinks[0]
    low = LB + (~inQ).astype(np.int64)                 # certified lower bound on gamma
    ok = bool((g[inQ] == LB[inQ]).all() and (g >= low).all())
    exact = bool(inQ.any())
    res = dict(m=m, Q=int(inQ.sum()), exact=exact)
    s_cert = False; s_same = True; kcert = 0; trees = 0; gmin = None
    if exact:
        gmin = int(LB[inQ].min())
        s_cert = bool(gmin <= low[~inQ].min()) if (~inQ).any() else True
        if s_cert:
            sel_cert = inQ & (LB == gmin)
            decided = inQ | (low > gmin)
            s_same = bool(((g == g.min()) == sel_cert)[decided].all()) and gmin == int(g.min())
            ok = ok and s_same
            Rc = S.Rc.astype(np.int64)
            klow = (low[:, None] + Rc).min(axis=0) - gmin
            kup = (LB[inQ][:, None] + Rc[inQ]).min(axis=0) - gmin
            kv = S.indices()[0]
            kcert = int((klow == kup).sum())
            ok = ok and all(klow[v] <= kv[v] <= kup[v] for v in range(8))
        # explicit breadth-first in-trees in H for up to 40 roots of Q
        HT = csr_matrix(H.T)
        roots = np.nonzero(inQ)[0]
        if len(roots) > 40:
            roots = rng.choice(roots, 40, replace=False)
        for r in roots:
            par = -np.ones(m, dtype=np.int64); seen = np.zeros(m, dtype=bool); seen[r] = True
            front = [int(r)]
            while front:
                nf = []
                for u in front:
                    for w in HT.indices[HT.indptr[u]:HT.indptr[u + 1]]:      # edges w -> u of H
                        if not seen[w]:
                            seen[w] = True; par[w] = u; nf.append(int(w))
                front = nf
            others = np.arange(m) != r
            wt = int(V[np.arange(m)[others], par[others]].sum()) if seen.all() else -1
            ok = ok and seen.all() and wt == LB[r] == g[r]
            trees += 1
    res.update(s_cert=s_cert, s_same=s_same, kcert=kcert, trees=trees, gmin=gmin, ok=ok)
    return res

def main():
    arg = lambda k, d: int(sys.argv[k]) if len(sys.argv) > k else d
    N154, N94, N43, N26 = arg(1, 18), arg(2, 21), arg(3, 18), arg(4, 20)
    t0 = time.process_time(); w0 = time.time()
    rng = np.random.default_rng(7)
    systems = [(154, n) for n in range(3, N154 + 1)] + [(94, n) for n in range(5, N94 + 1)] + \
              [(r, n) for r in (43, 142) for n in range(4, N43 + 1)] + [(26, n) for n in range(4, N26 + 1, 2)]
    rows = ["rule,n,m,cycles_with_gamma_certified_exactly,gamma_min_certified,selected_set_certified,agrees_with_C_routine,k_v_certified_of_8,explicit_trees_built,verdict"]
    L = []; fails = 0; nfull = 0; nS = 0
    for rule, n in systems:
        r = certify(rule, n, rng)
        if not r["ok"]: fails += 1
        nS += r["s_cert"]; nfull += (r["s_cert"] and r["kcert"] == 8)
        rows.append("%d,%d,%d,%d,%s,%d,%d,%d,%d,%s" % (rule, n, r["m"], r["Q"], "" if r["gmin"] is None else r["gmin"], r["s_cert"], r["s_same"], r["kcert"], r["trees"], "ok" if r["ok"] else "FAIL"))
        if not (r["s_cert"] and r["kcert"] == 8) or not r["ok"]:
            L.append("rule %d n=%d m=%d: gamma certified exactly for %d cycles; selected set certified: %s; k_v certified: %d of 8; agrees with the C routine: %s" % (rule, n, r["m"], r["Q"], r["s_cert"], r["kcert"], r["ok"]))
    L.insert(0, "%d systems; the certificate agrees with the C routine in %d; selected set and gamma_min certified without Edmonds in %d; in addition all eight k_v in %d. The systems where something is not certified:" % (len(systems), len(systems) - fails, nS, nfull))
    L.append("T11 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0, time.time() - w0))
    print("\n".join(L))
    open(os.path.join(HERE, "out", "T11.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(HERE, "out", "T11_certificates.csv"), "w").write("\n".join(rows) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
