"""Own tools for the verification of proofs_94_26 (written from the rule tables and the definitions only).

Conventions: a state of the ring Z/nZ is an integer whose bit i is the cell i.
(F x)_i = f(x_(i-1), x_i, x_(i+1)), f(a, b, c) = bit (4a + 2b + c) of the rule number.
"""
import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def rule_f(rule):
    return {(a, b, c): (rule >> (4 * a + 2 * b + c)) & 1 for a in (0, 1) for b in (0, 1) for c in (0, 1)}


def step_all(rule, n, x=None):
    """F applied to every state (or to the array x of states)."""
    mask = (1 << n) - 1
    if x is None:
        x = np.arange(1 << n, dtype=np.int64)
    x = np.asarray(x, dtype=np.int64)
    a = ((x << 1) | (x >> (n - 1))) & mask      # bit i = x_(i-1)
    c = ((x >> 1) | (x << (n - 1))) & mask      # bit i = x_(i+1)
    out = np.zeros_like(x)
    for code in range(8):
        if (rule >> code) & 1:
            p, q, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
            t = (a if p else ~a) & (x if q else ~x) & (c if r else ~c)
            out |= t
    return out & mask


def step_list(rule, cells):
    """F on a list of 0/1 (any n >= 3), for simulations on large rings."""
    n = len(cells)
    return [(rule >> (4 * cells[i - 1] + 2 * cells[i] + cells[(i + 1) % n])) & 1 for i in range(n)]


def to_cells(x, n):
    return [(x >> i) & 1 for i in range(n)]


def from_cells(cells):
    return sum(b << i for i, b in enumerate(cells))


def word(x, n):
    """cells 0..n-1 as a string, cell 0 first"""
    return ''.join(str((x >> i) & 1) for i in range(n))


def from_word(s):
    return sum(int(ch) << i for i, ch in enumerate(s))


def rot(x, n, k=1):
    """sigma^k: (sigma x)_i = x_(i-1), i.e. move every one k cells to the right (towards larger index)."""
    k %= n
    mask = (1 << n) - 1
    return ((x << k) | (x >> (n - k))) & mask if k else x


class Ring:
    """All states of one (rule, n): F, periodic states, cycles, attractor labels, G1."""

    def __init__(self, rule, n):
        self.rule, self.n = rule, n
        N = 1 << n
        self.N = N
        F = step_all(rule, n)
        self.F = F
        K = n + 1  # 2^K > N >= any transient length and any period
        G = F.copy()
        for _ in range(K):
            G = G[G]
        per = np.zeros(N, dtype=bool)
        per[G] = True
        self.periodic = per
        L = np.arange(N, dtype=np.int64)
        P = F.copy()
        for _ in range(K):
            L = np.minimum(L, L[P])
            P = P[P]
        rep = L[G]                  # min state of the cycle every state falls to
        reps = np.unique(rep[per])
        self.reps = reps
        self.m = len(reps)
        idx = np.full(N, -1, dtype=np.int64)
        idx[reps] = np.arange(self.m)
        self.label = idx[rep]       # cycle id that every state falls to
        self.pstates = np.nonzero(per)[0]
        self.pcyc = self.label[self.pstates]
        self._g1 = None

    def cycle_states(self, cid):
        x0 = int(self.reps[cid])
        out = [x0]
        x = int(self.F[x0])
        while x != x0:
            out.append(x)
            x = int(self.F[x])
        return out

    def g1(self):
        """edge set of G1 as a sparse 0/1 matrix and an array of edges (src, dst), src != dst"""
        if self._g1 is None:
            src, dst = [], []
            for j in range(self.n):
                t = self.label[self.pstates ^ (1 << j)]
                keep = t != self.pcyc
                src.append(self.pcyc[keep])
                dst.append(t[keep])
            src = np.concatenate(src)
            dst = np.concatenate(dst)
            e = np.unique(np.stack([src, dst], 1), axis=0) if len(src) else np.zeros((0, 2), dtype=np.int64)
            A = csr_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(self.m, self.m))
            self._g1 = (A, e)
        return self._g1

    def closed_classes(self):
        A, e = self.g1()
        ncomp, comp = connected_components(A, directed=True, connection='strong')
        leaves = np.zeros(ncomp, dtype=bool)
        if len(e):
            cross = comp[e[:, 0]] != comp[e[:, 1]]
            leaves[comp[e[cross, 0]]] = True
        closed = [np.nonzero(comp == k)[0] for k in range(ncomp) if not leaves[k]]
        return ncomp, comp, closed

    def reach_from(self, start_ids):
        """set of cycle ids reachable in G1 from the given ids (including them)"""
        A, e = self.g1()
        adj = [[] for _ in range(self.m)]
        for s, d in e:
            adj[s].append(d)
        seen = set(int(s) for s in start_ids)
        stack = list(seen)
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(int(v))
                    stack.append(int(v))
        return seen

    def codes_of_states(self, states):
        """set of codes (4a+2b+c) present in the given states"""
        n = self.n
        mask = (1 << n) - 1
        x = np.asarray(states, dtype=np.int64)
        a = ((x << 1) | (x >> (n - 1))) & mask
        c = ((x >> 1) | (x << (n - 1))) & mask
        found = set()
        for code in range(8):
            p, q, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
            t = (a if p else ~a) & (x if q else ~x) & (c if r else ~c) & mask
            if np.any(t != 0):
                found.add(code)
        return found

    def codes_of_cycles(self, cids):
        cids = set(int(c) for c in cids)
        sel = np.isin(self.pcyc, list(cids))
        return self.codes_of_states(self.pstates[sel])


def has_code(x, n, code):
    cells = to_cells(x, n)
    p, q, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
    return any(cells[i - 1] == p and cells[i] == q and cells[(i + 1) % n] == r for i in range(n))


def periodic_points_linear(h, apply):
    """periodic points of a map on GF(2)^h given as apply(v) on integers (by enumeration)"""
    N = 1 << h
    T = np.array([apply(v) for v in range(N)], dtype=np.int64)
    G = T.copy()
    for _ in range(h + 1):
        G = G[G]
    per = np.zeros(N, dtype=bool)
    per[G] = True
    return set(np.nonzero(per)[0].tolist())


def log(*a):
    print(*a, flush=True)
    sys.stdout.flush()
