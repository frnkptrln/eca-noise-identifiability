"""T00 -- validation of the engine vp_core.py.

(a) C routines against the pure numpy/Python reference: map F and code masks, periodic states and cycles, the matrix
    V(C, C') and R(C -> D_v), for all 256 rules at n = 3..7 and for rules 154, 43, 142, 94, 26 at n = 8..10.
(b) Minimum spanning in-tree for every root: the C routine (root-free Edmonds contraction) against
    - enumeration of ALL spanning in-trees (m <= 6, random weight matrices, many ties),
    - a per-root Chu-Liu/Edmonds in Python (random matrices up to m = 60; and the V matrices of (a)).
Output: out/T00.txt
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc

def main():
    t0 = time.process_time()
    out = []
    fails = 0
    # (a)
    ncmp = 0
    cases = [(r, n) for n in range(3, 8) for r in range(256)] + [(r, n) for r in (154, 43, 142, 94, 26) for n in (8, 9, 10)]
    vmats = []
    for rule, n in cases:
        S = vc.System(rule, n, level=2)
        F, codes = vc.eca_map_py(rule, n)
        per, cycles, lab = vc.cycles_py(F)
        ok = (F == S.F).all() and (codes == S.codes).all() and (per == (S.per == 1)).all() and len(cycles) == S.m
        # match cycle numbering through one state of each cycle
        perm = np.array([S.lab[orb[0]] for orb in cycles])
        ok = ok and (perm[lab] == S.lab).all()
        V, Rc = vc.search_py(n, F, cycles, lab, codes)
        Vc = S.V[np.ix_(perm, perm)].astype(np.int64)
        ok = ok and (V == Vc).all() and (Rc == S.Rc[perm].astype(np.int64)).all()
        ncmp += 1
        if not ok:
            fails += 1
            out.append("FAIL (a) rule %d n %d" % (rule, n))
        if S.m <= 40:
            vmats.append((rule, n, S.V.copy(), S.gamma.copy()))
    out.append("(a) C against numpy reference: %d (rule, n) cases compared, failures: %d" % (ncmp, fails))
    # (b) brute force
    rng = np.random.default_rng(20261120)
    nb = fb = 0
    for trial in range(400):
        m = int(rng.integers(2, 7))
        hi = int(rng.choice([2, 3, 4, 9]))
        W = rng.integers(1, hi + 1, size=(m, m)).astype(np.uint8)
        g = vc.in_tree_all_roots(W)
        for r in range(m):
            b = vc.in_tree_brute(W.tolist(), r)
            p = vc.in_tree_root_py(W, r)
            nb += 1
            if not (b == g[r] == p):
                fb += 1
                out.append("FAIL (b) brute m=%d r=%d brute=%s C=%s py=%s" % (m, r, b, g[r], p))
    out.append("(b1) all roots (C) = per root (Python) = enumeration of all in-trees: %d roots in 400 random matrices, m = 2..6, failures: %d" % (nb, fb))
    npr = fpr = 0
    for trial in range(60):
        m = int(rng.integers(7, 61))
        hi = int(rng.choice([2, 3, 5, 20]))
        W = rng.integers(1, hi + 1, size=(m, m)).astype(np.uint8)
        g = vc.in_tree_all_roots(W)
        for r in range(m):
            npr += 1
            if vc.in_tree_root_py(W, r) != g[r]:
                fpr += 1
    out.append("(b2) all roots (C) = per root (Python): %d roots in 60 random matrices, m = 7..60, failures: %d" % (npr, fpr))
    nv = fv = 0
    for rule, n, V, g in vmats:
        if V.shape[0] < 2:
            continue
        for r in range(V.shape[0]):
            nv += 1
            if vc.in_tree_root_py(V, r) != g[r]:
                fv += 1
                out.append("FAIL (b3) rule %d n %d root %d" % (rule, n, r))
    out.append("(b3) all roots (C) = per root (Python) on the V matrices of (a) with 2 <= m <= 40: %d roots in %d systems, failures: %d" % (nv, len(vmats), fv))
    fails += fb + fpr + fv
    out.append("T00 %s   CPU %.1f s (Python process; the C program adds a few seconds)" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0))
    txt = "\n".join(out)
    print(txt)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "T00.txt"), "w").write(txt + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
