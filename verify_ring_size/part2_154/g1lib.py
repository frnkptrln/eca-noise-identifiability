"""One-flip graph G1 of an elementary cellular automaton on a ring, from the definitions (numpy + scipy only).

Conventions as in ../SAMPLE.md section 2 (x_0 = most significant bit).  Written for this folder; it does not
use the solver of the parent folder or any code of the study.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def build_F(n, rule, chunk=1 << 22):
    N = 1 << n
    F = np.empty(N, dtype=np.int32 if n < 31 else np.int64)
    for lo in range(0, N, chunk):                       # in chunks, to keep the peak memory low
        x = np.arange(lo, min(N, lo + chunk), dtype=np.int64)
        c = ((x << 1) | (x >> (n - 1))) & (N - 1)       # c_i = x_(i+1)
        a = (x >> 1) | ((x & 1) << (n - 1))             # a_i = x_(i-1)
        y = np.zeros(len(x), dtype=np.int64)
        for code in range(8):
            if (rule >> code) & 1:
                pa = a if code & 4 else ~a
                pb = x if code & 2 else ~x
                pc = c if code & 1 else ~c
                y |= pa & pb & pc
        F[lo:lo + len(x)] = y & (N - 1)
    return F


def codes_mask(n, states):
    """bit mask (bit c set iff code c occurs) for each state of the integer array."""
    N = 1 << n
    x = np.asarray(states, dtype=np.int64)
    c = ((x << 1) | (x >> (n - 1))) & (N - 1)
    a = (x >> 1) | ((x & 1) << (n - 1))
    out = np.zeros(len(x), dtype=np.int64)
    for code in range(8):
        pa = a if code & 4 else ~a
        pb = x if code & 2 else ~x
        pc = c if code & 1 else ~c
        out |= (((pa & pb & pc) & (N - 1)) != 0).astype(np.int64) << code
    return out


class G1:
    def __init__(self, n, rule):
        self.n, self.rule = n, rule
        N = 1 << n
        F = build_F(n, rule)
        P, t = F.copy(), 1
        while t < N:
            P, t = P[P], 2 * t
        periodic = np.zeros(N, bool)
        periodic[P] = True
        per = np.nonzero(periodic)[0]
        cid = np.full(N, -1, np.int32)
        cycles = []
        Fl = F
        for s in per.tolist():
            if cid[s] >= 0:
                continue
            members, t = [], s
            while cid[t] < 0:
                cid[t] = len(cycles)
                members.append(t)
                t = int(Fl[t])
            cycles.append(members)
        self.F, self.per, self.cid, self.cycles = F, per, cid, cycles
        self.m = m = len(cycles)
        self.att = att = cid[P]
        pc = cid[per].astype(np.int64)
        keys = []
        for i in range(n):
            tgt = att[per ^ (1 << i)].astype(np.int64)
            keep = tgt != pc
            keys.append(pc[keep] * m + tgt[keep])
        keys = np.unique(np.concatenate(keys)) if keys else np.zeros(0, np.int64)
        self.src, self.dst = keys // m, keys % m
        self.A = csr_matrix((np.ones(len(keys), np.int8), (self.src, self.dst)), shape=(m, m))
        self.ncomp, self.lab = connected_components(self.A, directed=True, connection="strong")
        leaving = np.zeros(self.ncomp, bool)
        cross = self.lab[self.src] != self.lab[self.dst]
        leaving[self.lab[self.src[cross]]] = True
        self.closed_labels = np.nonzero(~leaving)[0]
        self.in_closed = ~leaving[self.lab]
        cm = codes_mask(n, per)
        self.cycle_codes = np.zeros(m, np.int64)
        np.bitwise_or.at(self.cycle_codes, pc, cm)

    def rep(self, c):
        return format(min(self.cycles[c]), "0%db" % self.n)

    def out_nbrs(self, c):
        return self.dst[self.src == c]

    def reachable_from(self, c):
        seen = np.zeros(self.m, bool)
        seen[c] = True
        stack = [c]
        indptr, indices = self.A.indptr, self.A.indices
        while stack:
            u = stack.pop()
            for v in indices[indptr[u]:indptr[u + 1]]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(int(v))
        return seen
