"""T03 -- Theorems 3.9, 3.10, 3.11 (rule 154) from the definitions of Section 2, n = 3..NMAX (default 18).

For every n: all cycles, the full matrix V(C, C'), R(C -> D_v) for the eight codes, gamma(C) for EVERY root by a
minimum spanning in-tree (not by Theorem 2.8), gamma_min, the selected set, k_v, k*, G1 and its closed classes.

 n = 2^k (Theorem 3.9):  (a) the cycles are {0} and cycles inside M; (b) V({0}, C) >= 2 for every other cycle;
     (c) every cycle C != {0} has a G1 path to {0} of length <= mu(C) <= n/2; (d) {0} is the only closed class;
     (e) gamma({0}) = m - 1, gamma(C) = m otherwise, S = {{0}}; (f) k_000 = 0, k_v = 1 for the seven others, k* = 1.
 other n (Theorem 3.10): G1 strongly connected, gamma(C) = m - 1 for every cycle, all cycles selected, k_v = 0 for all
     eight codes; the states named in the proof are periodic and carry the codes named.
 Theorem 3.11 is the conjunction. The prediction of Theorem 2.8 (S = unique closed class, gamma_min = m - 1) is
 compared with the potentials.
 For m <= MPY (default 320) every gamma(C) is recomputed with the per-root Chu-Liu/Edmonds in Python (the Python
 routine is too slow beyond that; for larger m the potentials rest on the C routine, which T00 validates).
Output: out/T03.txt, out/T03_rule154.csv.   Usage: python3 T03_rule154_theorems.py [NMAX] [MPY]
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def popcount(a):
    a = a.astype(np.uint64)
    c = np.zeros(a.shape, dtype=np.int64)
    while a.any():
        c += (a & np.uint64(1)).astype(np.int64)
        a >>= np.uint64(1)
    return c

def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    MPY = int(sys.argv[2]) if len(sys.argv) > 2 else 320
    t0 = time.process_time(); w0 = time.time()
    L = []
    rows = ["n,power_of_two,m,closed_classes,selected,gamma_min,gamma_max,k000,k001,k010,k011,k100,k101,k110,k111,kstar,roots_rechecked_per_root,verdict"]
    fails = 0
    for n in range(3, NMAX + 1):
        w1 = time.time()
        S = vc.System(154, n, level=2, workers=2)
        m = S.m
        V = S.V
        g = S.gamma
        kv, kstar, gmin, sel = S.indices()
        classes, comp = S.closed_classes()
        zero = int(S.lab[0])
        ok = bool(S.per[0])
        ev = sum(1 << i for i in range(0, n, 2)); od = sum(1 << i for i in range(1, n, 2))
        pow2 = n & (n - 1) == 0
        notes = []
        # per-root recheck
        roots = range(m) if m <= MPY else []
        nre = 0
        for r in roots:
            nre += 1
            if vc.in_tree_root_py(V, r) != g[r]:
                ok = False; notes.append("per-root mismatch at root %d" % r)
        if pow2:
            px = S.cyc_states
            inM = ((px & np.uint32(od)) != 0) & ((px & np.uint32(ev)) != 0)
            a = bool((inM | (px == 0)).all()) and S.cyc_start[zero + 1] - S.cyc_start[zero] == 1
            row0 = V[zero].astype(np.int64)
            b = bool((np.delete(row0, zero) >= 2).all())
            # mu(C)
            mu_state = np.minimum(popcount(px & np.uint32(ev)), popcount(px & np.uint32(od)))
            mu = np.full(m, 10 ** 9, dtype=np.int64)
            np.minimum.at(mu, S.lab[px], mu_state)
            dist = S.g1_dist_to([zero])
            others = np.arange(m) != zero
            c = bool((dist[others] >= 1).all() and (dist[others] <= mu[others]).all() and (mu[others] <= n // 2).all())
            d = len(classes) == 1 and list(classes[0]) == [zero]
            e = g[zero] == m - 1 and bool((g[others] == m).all()) and sel.sum() == 1 and sel[zero]
            f = kv == [0, 1, 1, 1, 1, 1, 1, 1] and kstar == 1
            ok = ok and a and b and c and d and e and f
            notes.append("(a)%s (b)%s [min V({0},C) = %d] (c)%s [max G1 distance to {0} = %d, max mu = %d] (d)%s (e)%s (f)%s" % (
                a, b, int(np.delete(row0, zero).min()), c, int(dist[others].max()), int(mu[others].max()), d, e, f))
        else:
            ncomp, _ = connected_components(csr_matrix(S.g1()), directed=True, connection="strong")
            a = ncomp == 1
            b = bool((g == m - 1).all()) and bool(sel.all())
            c = kv == [0] * 8 and kstar == 0
            if n >= 5:
                s1 = vc.from_word("0" * (n - 2) + "11"); s2 = vc.from_word("0" * (n - 4) + "1011")
                want1 = {1, 3, 4, 6}; want2 = {2, 5}
            else:
                s1 = vc.from_word("001"); s2 = vc.from_word("011")
                want1 = {1, 2, 4}; want2 = {3, 5, 6}
            has = lambda x: {v for v in range(8) if (int(S.codes[x]) >> v) & 1}
            d = bool(S.per[s1] and S.per[s2] and want1 <= has(s1) and want2 <= has(s2) and S.per[(1 << n) - 1] and S.per[0])
            ok = ok and a and b and c and d
            notes.append("G1 strongly connected %s; gamma = m-1 for all and all selected %s; k_v = 0 for all %s; named states periodic with the named codes %s" % (a, b, c, d))
        # Theorem 2.8 against the potentials
        if len(classes) == 1:
            K = np.zeros(m, dtype=bool); K[classes[0]] = True
            t28 = bool((K == sel).all()) and gmin == m - 1
            ok = ok and t28
            notes.append("Theorem 2.8 agrees with the in-trees: %s" % t28)
        if not ok:
            fails += 1
        rows.append("%d,%d,%d,%d,%d,%d,%d,%s,%d,%d,%s" % (n, pow2, m, len(classes), int(sel.sum()), gmin, int(g.max()), ",".join(map(str, kv)), kstar, nre, "ok" if ok else "FAIL"))
        L.append("n=%2d m=%5d %s  k*=%d  %s  [%d roots rechecked per root; wall %.1f s]" % (n, m, "ok  " if ok else "FAIL", kstar, "; ".join(notes), nre, time.time() - w1))
        print(L[-1], flush=True)
    L.append("T03 %s   n = 3..%d   CPU %.1f s (Python; the C program runs with 2 threads in addition) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", NMAX, time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T03.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(HERE, "out", "T03_rule154.csv"), "w").write("\n".join(rows) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
