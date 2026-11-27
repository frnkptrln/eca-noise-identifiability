"""Theorem_3_9 (a)-(f) at n = 16 (and n = 4, 8 as a control), without the full matrix V.

G1 is computed from the criterion of Lemma 2.3 (proved in Lean, statement checked in VERIFICATION_lean_theorem_a.md):
for C != C', V(C, C') = 1 iff the orbit of some flip of some state of C ends on C'.  gamma is then pinned by bounds
valid for every in-tree:
  lower bound: sum over d != root of min_{e != d} V(d, e); here min_{e} V(d, e) = 1 for d != {0} that have a G1
               out-edge, and >= 2 for {0} when {0} has no G1 out-edge (V >= 1 off the diagonal, = 1 iff G1);
  upper bound for root {0}: a breadth-first in-tree of G1 edges (weight m - 1);
  upper bound for root C != {0}: a breadth-first in-tree of G1 edges among the cycles != {0} (weight m - 2) plus the
               edge {0} -> C* with C* the cycle of e_2 + e_3, of weight <= 2 (the path [0, e_2 + e_3]).
k_v then follows from (1): k_v = min(gamma({0}) + R({0} -> D_v), min_{C != {0}} gamma(C) + R(C -> D_v)) - gamma_min,
with R(C -> D_v) = 0 iff a state of C contains v, R({0} -> D_v) >= 1 for v != 000, and R({0} -> D_v) <= 1
when e_j or F(e_j) contains v for some cell j.
Run: python n16.py > out/n16.txt
"""
import time
from model import global_map, in_parM, contains, CODES, code_str


def run(n):
    t0 = time.time()
    F = global_map(n, 154)
    N = 1 << n
    P = set(range(N))
    while True:
        Q = {F[x] for x in P}
        if Q == P:
            break
        P = Q
    idx, cyc = {}, []
    for x in sorted(P):
        if x in idx:
            continue
        orb, y = [x], F[x]
        while y != x:
            orb.append(y)
            y = F[y]
        for y in orb:
            idx[y] = len(cyc)
        cyc.append(orb)
    m = len(cyc)
    z = idx[0]
    memo = {}

    def ends(x):
        path = []
        while x not in idx and x not in memo:
            path.append(x)
            x = F[x]
        c = idx[x] if x in idx else memo[x]
        for y in path:
            memo[y] = c
        return c

    out = [set() for _ in range(m)]
    for c in range(m):
        for x in cyc[c]:
            for j in range(n):
                d = ends(x ^ (1 << j))
                if d != c:
                    out[c].add(d)
    inn = [set() for _ in range(m)]
    for c in range(m):
        for d in out[c]:
            inn[d].add(c)
    a = all(all(in_parM(x, n) for x in cyc[c]) for c in range(m) if c != z)
    b = len(out[z]) == 0

    def back_bfs(root, allowed):
        seen, fr = {root}, [root]
        while fr:
            nx_ = []
            for u in fr:
                for d in inn[u]:
                    if d in allowed and d not in seen:
                        seen.add(d)
                        nx_.append(d)
            fr = nx_
        return seen

    allc = set(range(m))
    c_ = back_bfs(z, allc) == allc
    nonzero = allc - {z}
    r0 = next(iter(nonzero))
    # G1 restricted to the cycles != {0} strongly connected: every node reaches r0 and r0 reaches every node
    def fwd_bfs(root, allowed):
        seen, fr = {root}, [root]
        while fr:
            nx_ = []
            for u in fr:
                for d in out[u]:
                    if d in allowed and d not in seen:
                        seen.add(d)
                        nx_.append(d)
            fr = nx_
        return seen
    sc = back_bfs(r0, nonzero) == nonzero and fwd_bfs(r0, nonzero) == nonzero
    # (d): {0} closed (b) and every cycle reaches {0} (c) => {{0}} is the only closed class
    d_ = b and c_
    # (e): gamma({0}) = m - 1 (BFS tree, = lower bound); gamma(C) = m for C != {0}:
    #      lower bound (m - 2) + 2 needs b; upper bound needs sc and V({0}, C*) <= 2 with C* != {0}
    cstar = idx.get((1 << 2) | (1 << 3))
    e_ = c_ and b and sc and cstar is not None and cstar != z
    # (f)
    has = {v: any(contains(x, v, n) for c in nonzero for x in cyc[c]) for v in CODES}
    k = {}
    for v in CODES:
        if v == (0, 0, 0):
            k[v] = 0  # 0 contains 000, R = 0, gamma({0}) = gamma_min
        else:
            # gamma({0}) + R({0} -> D_v) >= m - 1 + 1; a nonzero cycle containing v gives m + 0
            # or R({0} -> D_v) <= 1: a path [0, e_j, F e_j, ...] of resistance 1 meets D_v
            via_flip = any(contains(y, v, n) for j in range(n) for y in ((1 << j), F[1 << j]))
            k[v] = 1 if (has[v] or via_flip) else None
    f_ = all(k[v] == (0 if v == (0, 0, 0) else 1) for v in CODES)
    print(f"n={n}: m={m}; (a)={a} (b) no G1 edge leaves {{0}}={b} (c)={c_} (d)={d_} "
          f"G1 on cycles != {{0}} strongly connected={sc} (e)={e_} (f)={f_}; k_v={[k[v] for v in CODES]};"
          f" time {time.time() - t0:.1f} s")
    return all([a, b, c_, d_, e_, f_])


if __name__ == "__main__":
    ok = all(run(n) for n in (4, 8, 16))
    print("ALL OK" if ok else "FAILED")
