"""Light-cone healing of single flips in a spatially periodic cycle (crystal); statement used in the
report as Lemma H.

Let X be a cycle of F whose states are p-periodic in space (all rings with p | n carry it). Simulate,
on a ring of size N >= 2*maxT + 1 with p | N (equal to the infinite line for t <= maxT), every single
flip x XOR e_j for every state x of X and every position j in 0..p-1. If each such orbit is back on X
at some time tau(x, j) <= maxT, let tau = max tau(x, j). Then on every ring Z/nZ with p | n and
n >= 2*tau + 1 a single flip of a state of X returns to X, i.e. V(X, C) >= 2 for every other cycle C.
Proof (report, Lemma H): for t <= (n-1)/2 every window [i-t, i+t] contains at most one of the flipped
sites j + kn, so the ring evolution agrees cell by cell with the single-flip evolution on the line; at
t = tau that evolution is a p-periodic state of X, and translates by multiples of n (a multiple of p)
of a p-periodic state coincide.
"""
from __future__ import annotations


def step(rule: int, x: int, n: int) -> int:
    full = (1 << n) - 1
    l = ((x << 1) | (x >> (n - 1))) & full     # bit i = x_{i-1}
    r = ((x >> 1) | (x << (n - 1))) & full     # bit i = x_{i+1}
    y = 0
    for c in range(8):
        if (rule >> c) & 1:
            y |= (l if c & 4 else ~l) & (x if c & 2 else ~x) & (r if c & 1 else ~r)
    return y & full


def from_word(word: str, N: int) -> int:
    p = len(word)
    assert N % p == 0
    return sum(int(word[i % p]) << i for i in range(N))


def heal(rule: int, word: str, maxT: int = 200):
    p = len(word)
    K = -(-(2 * maxT + 1) // p)
    N = p * K
    x0 = from_word(word, N)
    cyc = [x0]; y = step(rule, x0, N)
    while y != x0:
        cyc.append(y); y = step(rule, y, N)
        assert len(cyc) <= 4 * N, "word does not lie on a short cycle"
    S = set(cyc)
    # every state of X must be p-periodic (spatial period divides p)
    for x in cyc:
        assert ((x << p) | (x >> (N - p))) & ((1 << N) - 1) == x, "cycle state not p-periodic"
    taus = {}
    for s, x in enumerate(cyc):
        for j in range(p):
            z = x ^ (1 << j)
            t = 0
            while z not in S:
                z = step(rule, z, N); t += 1
                if t > maxT:
                    t = None; break
            taus[(s, j)] = t
    ok = all(v is not None for v in taus.values())
    tau = max(taus.values()) if ok else None
    return dict(rule=rule, word=word, p=p, cycle_length=len(cyc), N=N, healed=ok, tau=tau,
                n0=(2 * tau + 1) if ok else None)
