"""Finite-automaton certificates valid for every ring size n (ring-size study, statement G3).

A configuration on Z/nZ is a closed walk of length n in the de Bruijn graph B_w whose vertices are the
words of length w and whose edges are the words of length w+1 (overlap w-1); this holds for every
n >= 1 (the word read around the ring repeatedly is n-periodic). F^t of an (n-periodic) configuration
restricted to a window of length w+1 depends only on that window, as long as w+1 >= 2t+3.

avoid_graph(rule, codes, T): the subgraph of B_{2T+2} whose edges W (length 2T+3) satisfy: for every
t = 0..T, the codes of F^t(W) (a word of length 2T+3-2t) avoid `codes`. A ring configuration x of size
n has x, F x, ..., F^T x all avoiding `codes` iff it is a closed walk of length n in this subgraph.

Every closed walk lies in one strongly connected component (SCC), and every closed walk in an SCC of
period d has length divisible by d (d = gcd of cycle lengths, computed from BFS levels). Hence, if
every non-trivial SCC has period divisible by p, no configuration of a ring with p not dividing n
avoids `codes` for T+1 consecutive steps -- in particular no cycle of F on that ring avoids them.

For SCCs that are simple cycles the configurations are explicit: the word read along the cycle.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def eca_word(rule: int, word: np.ndarray) -> np.ndarray:
    """F applied to a batch of words (shape (B, L)) -> (B, L-2)."""
    l, c, r = word[:, :-2], word[:, 1:-1], word[:, 2:]
    return (rule >> (4 * l + 2 * c + r)) & 1


def word_codes(word: np.ndarray) -> np.ndarray:
    return 4 * word[:, :-2] + 2 * word[:, 1:-1] + word[:, 2:]


def avoid_graph(rule: int, codes, T: int):
    w = 2 * T + 2
    L = w + 1
    E = np.arange(1 << L, dtype=np.int64)
    W = ((E[:, None] >> np.arange(L - 1, -1, -1)) & 1).astype(np.int64)   # edge words, MSB first
    ok = np.ones(len(E), dtype=bool)
    cur = W
    bad = np.zeros(8, dtype=bool); bad[list(codes)] = True
    for t in range(T + 1):
        ok &= ~bad[word_codes(cur)].any(axis=1)
        if t < T:
            cur = eca_word(rule, cur)
    tail = E >> 1                       # first w letters
    head = E & ((1 << w) - 1)           # last w letters
    e = np.flatnonzero(ok)
    G = csr_matrix((np.ones(len(e), dtype=np.int8), (tail[e], head[e])), shape=(1 << w, 1 << w))
    return G, w


def scc_periods(G):
    """List of (members, period, n_edges) for every non-trivial SCC (containing at least one edge)."""
    ncomp, lab = connected_components(G, directed=True, connection="strong")
    Gc = G.tocoo()
    inside = lab[Gc.row] == lab[Gc.col]
    rows, cols = Gc.row[inside], Gc.col[inside]
    out = []
    by = {}
    for u, v in zip(rows, cols):
        by.setdefault(int(lab[u]), []).append((int(u), int(v)))
    for comp, edges in by.items():
        members = np.flatnonzero(lab == comp)
        adj = {}
        for u, v in edges:
            adj.setdefault(u, []).append(v)
        start = int(members[0])
        level = {start: 0}
        q = [start]
        while q:
            nq = []
            for u in q:
                for v in adj.get(u, []):
                    if v not in level:
                        level[v] = level[u] + 1; nq.append(v)
            q = nq
        d = 0
        for u, v in edges:
            d = math.gcd(d, level[u] + 1 - level[v])
        out.append((members, abs(d), len(edges)))
    return out


def scc_word(members, G, w):
    """For an SCC that is a simple cycle: the periodic word read along it (one letter per edge)."""
    members = set(int(v) for v in members)
    start = min(members)
    word, v = [], start
    sub = G.tocsr()
    while True:
        nb = [int(u) for u in sub.indices[sub.indptr[v]:sub.indptr[v + 1]] if int(u) in members]
        assert len(nb) == 1, "not a simple cycle"
        u = nb[0]
        word.append(u & 1)
        v = u
        if v == start:
            break
    return "".join(map(str, word))


def certificate(rule: int, codes, T: int, p: int):
    """Summary of the avoid-graph SCCs: for each SCC its period, size and (if a simple cycle) its word;
    'all_divisible' is True iff every non-trivial SCC has period divisible by p."""
    G, w = avoid_graph(rule, codes, T)
    sccs = scc_periods(G)
    items = []
    for members, d, ne in sccs:
        simple = ne == len(members)
        items.append(dict(size=len(members), edges=ne, period=d, simple_cycle=simple,
                          word=scc_word(members, G, w) if simple else ""))
    return dict(rule=rule, codes="".join(map(str, sorted(codes))), T=T, p=p, n_sccs=len(items),
                all_divisible=all(it["period"] % p == 0 for it in items), sccs=items)


def pair_graph(rule: int):
    """Pair graph of an ECA: vertices (a, b), a, b in {0,1}^2 (windows of two configurations x, y), coded
    4*a + b with a, b in 0..3 (first letter = high bit); edge (a1 a2, b1 b2) -> (a2 a3, b2 b3) iff
    f(a1 a2 a3) = f(b1 b2 b3). Closed walks of length n <-> pairs (x, y) of ring configurations of size n
    with F x = F y; x != y iff the walk visits an off-diagonal vertex (a != b)."""
    t, h = [], []
    for a in range(4):
        for b in range(4):
            for a3 in (0, 1):
                for b3 in (0, 1):
                    ca, cb = 2 * a + a3, 2 * b + b3          # 3-letter codes
                    if (rule >> ca) & 1 == (rule >> cb) & 1:
                        t.append(4 * a + b); h.append(4 * (ca & 3) + (cb & 3))
    return csr_matrix((np.ones(len(t), dtype=np.int8), (t, h)), shape=(16, 16))


def injectivity_certificate(rule: int, p: int = 2):
    """True iff every SCC of the pair graph that contains an off-diagonal vertex has period divisible by p,
    so F is injective (hence bijective) on every ring Z/nZ with p not dividing n."""
    G = pair_graph(rule)
    out = []
    for members, d, ne in scc_periods(G):
        off = [int(v) for v in members if (int(v) >> 2) != (int(v) & 3)]
        if off:
            out.append(dict(size=len(members), period=d, off_diagonal=len(off)))
    return dict(rule=rule, p=p, sccs=out, certified=all(s["period"] % p == 0 for s in out))
