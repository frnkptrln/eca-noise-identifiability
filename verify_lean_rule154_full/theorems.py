"""Theorem_3_9, Theorem_3_10, Theorem_3_11 (StatementMain.lean) evaluated on the literal model.

For n = 1..10 gamma is computed by Edmonds' algorithm (checked by the literal IsInTree and a lower bound, and by
enumeration of all parent maps when m <= 6).  For n = 11, 12 (not powers of two) gamma is taken from the
breadth-first G1 tree when the root is reachable from every cycle (see model.py); otherwise Edmonds.

Each conclusion is evaluated whether or not the hypothesis of the statement holds at that n, so that one sees
which hypotheses are needed.  Run: python theorems.py > out/theorems.txt
"""
import time
from model import Model, CODES, code_str, in_parM, is_pow_two, popcount


def mu(C, n):
    best = None
    for x in C:
        xe = sum((x >> i) & 1 for i in range(0, n, 2))
        xo = sum((x >> i) & 1 for i in range(1, n, 2))
        v = min(xe, xo)
        best = v if best is None else min(best, v)
    return best


def g1_dist_to(M, target):
    """Length of a shortest directed G1 path from each cycle to target (None if none)."""
    m = M.m
    dist = {target: 0}
    frontier = [target]
    while frontier:
        nxt = []
        for u in frontier:
            for d in range(m):
                if d not in dist and M.G1[d][u]:
                    dist[d] = dist[u] + 1
                    nxt.append(d)
        frontier = nxt
    return [dist.get(d) for d in range(m)]


def main():
    print("n | m | IsPowTwo | Zero_cycle | k_v (codes 000..111) | k* | |Sel| | closed classes (sizes) | gamma values"
          " | hypotheses 3.9 / 3.10 / 3.11")
    rows = []
    for n in range(1, 13):
        t0 = time.time()
        M = Model(n, fast_gamma=(n >= 11))
        m = M.m
        z = M.zero_index()
        zero_cycle = z is not None and M.cyc[z] == frozenset({0})
        others = [c for c in range(m) if c != z]
        cc = M.closed_classes()
        kvec = [M.k[v] for v in CODES]
        # Theorem_3_9 conclusions (C0 = cycle with set {0})
        a = all(all(in_parM(x, n) for x in M.cyc[c]) for c in others)
        b1 = all(M.V[z][c] >= 2 for c in others)
        b2 = all(not M.G1[z][c] for c in range(m))
        c_ = all(z in M.reach[c] for c in range(m))
        d_ = (frozenset({z}) in cc) and cc == {frozenset({z})}
        e1 = M.gamma[z] == m - 1
        e2 = all(M.gamma[c] == m for c in others)
        e3 = M.Sel == [z]
        f1 = M.k[(0, 0, 0)] == 0
        f2 = all(M.k[v] == 1 for v in CODES if v != (0, 0, 0))
        f3 = M.kstar == 1
        t39 = [a, b1, b2, c_, d_, e1, e2, e3, f1, f2, f3]
        # paper's bound in (c): path of length <= mu(C) <= n/2
        dz = g1_dist_to(M, z)
        bound_ok = all(dz[c] is not None and dz[c] <= mu(M.cyc[c], n) <= n // 2 for c in others) if c_ else None
        maxlen = max((dz[c] for c in others if dz[c] is not None), default=0)
        # Theorem_3_10 conclusions
        s1 = all(M.reach[c] == set(range(m)) for c in range(m))
        s2 = all(M.gamma[c] == m - 1 for c in range(m))
        s3 = len(M.Sel) == m
        s4 = all(M.k[v] == 0 for v in CODES)
        s5 = M.kstar == 0
        t310 = [s1, s2, s3, s4, s5]
        # Theorem_3_11 conclusions
        p = is_pow_two(n)
        t311_pow = [M.kstar == 1, M.Sel == [z], f1, f2]
        t311_other = [M.kstar == 0, s3, s4]
        hyp39 = n >= 4 and p  # n = 2^k with k >= 2
        hyp310 = n >= 3 and not p
        hyp311 = n >= 3
        cert = all(M.gamma_cert)
        print(f"{n} | {m} | {p} | {zero_cycle} | {'-'.join(map(str, kvec))} | {M.kstar} | {len(M.Sel)} | "
              f"{sorted(len(K) for K in cc)} | gamma({{0}})={M.gamma[z]}, others {sorted(set(M.gamma[c] for c in others))}"
              f" (certified: {cert}) | {hyp39} / {hyp310} / {hyp311}")
        print(f"    Theorem_3_9 conclusions (a, b1, b2, c, d, e1, e2, e3, f1, f2, f3): {t39}")
        print(f"    paper 3.9(c) bound path length <= mu(C) <= n/2: {bound_ok}; longest shortest path to {{0}}: {maxlen}")
        print(f"    Theorem_3_10 conclusions (strongly connected, gamma=m-1, all selected, all k_v=0, k*=0): {t310}")
        print(f"    Theorem_3_11 first case (k*=1, Sel={{C0}}, k000=0, k_v=1 else): {t311_pow};"
              f" second case (k*=0, all selected, all k_v=0): {t311_other}")
        if hyp39:
            assert all(t39), n
        if hyp310:
            assert all(t310), n
        if hyp311:
            assert all(t311_pow) if p else all(t311_other), n
        minV0 = min((M.V[z][c] for c in others), default=None)
        print(f"    min V({{0}}, C) over C != {{0}}: {minV0}; time {time.time() - t0:.1f} s")
        rows.append((n, m, kvec, M.kstar, len(M.Sel)))
    with open("out/model_k_values.csv", "w") as fh:
        fh.write("n,cycles,k_c,kstar,n_selected\n")
        for n, m, kvec, ks, ns in rows:
            fh.write(f"{n},{m},{'-'.join(map(str, kvec))},{ks},{ns}\n")
    print("All statements hold on their hypotheses for n = 1..12.")


if __name__ == "__main__":
    main()
