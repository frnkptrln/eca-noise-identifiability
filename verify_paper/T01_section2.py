"""T01 -- Section 2 of the paper on ALL 256 elementary rules, n = 3..NMAX (default 12), every cycle, every state.

From the definitions (vp_core): V, R(C -> D_v), gamma for every root (minimum spanning in-tree for every root),
gamma_min, the selected set S, k_v, k*, the one-flip graph G1 = {V = 1} and its closed classes. Checked:

 L2.2 (lem:kzero)   k_v = 0 iff v is contained in a state of a selected cycle; k* = 0 iff the selected cycles jointly
                    contain all eight codes; k_v <= 1 whenever some flip of some state of a selected cycle contains v.
 L2.3 (lem:edge)    V(C, C') >= 1 for C != C'; V(C, C') = 1 iff some x in C and cell j have the orbit of x + e_j end
                    on C'; if x and x + e_j are periodic on different cycles, both edges are in G1.
 L2.4 (lem:sym)     V(sigma C, sigma C') = V(C, C'), gamma(sigma C) = gamma(C); S and G1 invariant under rotation.
 L2.5 (lem:reroot)  for random in-trees T rooted at B and random N != B: T - (out-edge of N) + (B -> N) is an in-tree
                    rooted at N; if V(B, N) = 1 its weight is at most that of T.
 L2.6 (lem:closure) C in S and V(C, C') = 1 imply C' in S.
 L2.7 (lem:inclosed) every selected cycle lies in a closed class of G1.
 T2.8 (thm:A)       S is a union of closed classes; if there is exactly one closed class K then S = K and
                    gamma_min = m - 1.
Output: out/T01.txt, out/T01_sweep.csv (one row per rule and n).
Usage: python3 T01_section2.py [NMAX]
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def is_in_tree(par, root, m):
    """par[u] = head of the out-edge of u (par[root] = -1). True iff every node reaches root."""
    if par[root] != -1 or (np.delete(par, root) < 0).any():
        return False
    ok = np.zeros(m, dtype=bool)
    ok[root] = True
    for u in range(m):
        path = []
        x = u
        steps = 0
        while not ok[x] and steps <= m:
            path.append(x)
            x = par[x]
            steps += 1
        if not ok[x]:
            return False
        ok[path] = True
    return True

def check(rule, n, rng):
    S = vc.System(rule, n, level=2)
    m = S.m
    V = S.V.astype(np.int64)
    g = S.gamma
    kv, kstar, gmin, sel = S.indices()
    res = {}
    cc = S.cycle_codes()
    # L2.2
    selcodes = int(np.bitwise_or.reduce(cc[sel]))
    a = all((kv[v] == 0) == bool((selcodes >> v) & 1) for v in range(8))
    b = (kstar == 0) == (selcodes == 255)
    c = True
    for ci in np.nonzero(sel)[0]:
        xs = S.states_of(ci)
        fm = 0
        for j in range(n):
            fm |= int(np.bitwise_or.reduce(S.codes[xs ^ np.uint32(1 << j)]))
        c = c and all(kv[v] <= 1 for v in range(8) if (fm >> v) & 1)
    res["L2.2"] = a and b and c
    # L2.3
    px = S.cyc_states
    A1 = np.zeros((m, m), dtype=bool)
    both = True
    for j in range(n):
        y = px ^ np.uint32(1 << j)
        A1[S.lab[px], S.lab[y]] = True
        pp = (S.per[y] == 1) & (S.lab[y] != S.lab[px])
        both = both and (V[S.lab[px][pp], S.lab[y][pp]] == 1).all() and (V[S.lab[y][pp], S.lab[px][pp]] == 1).all()
    off = ~np.eye(m, dtype=bool)
    res["L2.3"] = bool((np.diag(V) == 0).all() and (V[off] >= 1).all() and ((V == 1)[off] == A1[off]).all() and both)
    # L2.4
    perm = np.array([S.lab[vc.rot(int(S.states_of(ci)[0]), n)] for ci in range(m)])
    res["L2.4"] = bool((V[np.ix_(perm, perm)] == V).all() and (g[perm] == g).all() and (sel[perm] == sel).all())
    # L2.5
    ok5 = True
    ntree = 0
    if m >= 2:
        for trial in range(20):
            order = rng.permutation(m)
            par = -np.ones(m, dtype=np.int64)
            for i in range(1, m):
                par[order[i]] = order[rng.integers(0, i)]
            B = int(order[0])
            N = int(order[rng.integers(1, m)])
            w0 = int(sum(V[u, par[u]] for u in range(m) if u != B))
            par2 = par.copy()
            par2[N] = -1
            par2[B] = N
            ok5 = ok5 and is_in_tree(par, B, m) and is_in_tree(par2, N, m)
            if V[B, N] == 1:
                w1 = int(sum(V[u, par2[u]] for u in range(m) if u != N))
                ok5 = ok5 and (w1 <= w0)
            ntree += 1
    res["L2.5"] = ok5
    # L2.6
    res["L2.6"] = bool(sel[np.nonzero((V == 1) & sel[:, None])[1]].all())
    # L2.7, T2.8
    classes, comp = S.closed_classes()
    inclosed = np.zeros(m, dtype=bool)
    for K in classes:
        inclosed[K] = True
    res["L2.7"] = bool(inclosed[sel].all())
    union = all(sel[K].all() or not sel[K].any() for K in classes) and res["L2.7"]
    if len(classes) == 1:
        K = np.zeros(m, dtype=bool)
        K[classes[0]] = True
        union = union and (K == sel).all() and gmin == m - 1
    res["T2.8"] = bool(union)
    return res, m, len(classes), int(sel.sum()), gmin, kstar, ntree

def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    t0 = time.process_time(); w0 = time.time()
    rng = np.random.default_rng(1)
    keys = ["L2.2", "L2.3", "L2.4", "L2.5", "L2.6", "L2.7", "T2.8"]
    rows = ["rule,n,m,closed_classes,selected,gamma_min,kstar," + ",".join(keys)]
    fail = {k: 0 for k in keys}
    lines = []
    for n in range(3, nmax + 1):
        cyc = unique = trees = 0
        for rule in range(256):
            res, m, ncl, nsel, gmin, kstar, ntree = check(rule, n, rng)
            cyc += m; unique += (ncl == 1); trees += ntree
            for k in keys:
                if not res[k]:
                    fail[k] += 1
                    lines.append("FAIL %s rule %d n %d" % (k, rule, n))
            rows.append("%d,%d,%d,%d,%d,%d,%d," % (rule, n, m, ncl, nsel, gmin, kstar) + ",".join(str(int(res[k])) for k in keys))
        lines.append("n = %2d: 256 rules, %d cycles in total, %d rules with a unique closed class, %d random in-trees re-rooted" % (n, cyc, unique, trees))
    for k in keys:
        lines.append("%s failures: %d" % (k, fail[k]))
    lines.append("T01 %s   n = 3..%d, all 256 rules; CPU %.1f s (Python) wall %.1f s" % ("PASS" if sum(fail.values()) == 0 else "FAIL", nmax, time.process_time() - t0, time.time() - w0))
    txt = "\n".join(lines)
    print(txt)
    open(os.path.join(HERE, "out", "T01.txt"), "w").write(txt + "\n")
    open(os.path.join(HERE, "out", "T01_sweep.csv"), "w").write("\n".join(rows) + "\n")
    return sum(fail.values())

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
