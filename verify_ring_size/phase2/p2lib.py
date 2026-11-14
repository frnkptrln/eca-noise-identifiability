"""Shared helpers for phase 2.  Uses the verification's own sealed solver (../core.c, ../eca_core.py)."""
import ctypes as C
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)            # verify_ring_size/
REPO = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

import eca_core as K  # noqa: E402

_SRC = os.path.join(HERE, "p2core.c")
_LIB = os.path.join(HERE, "build", "p2core.dylib")
os.makedirs(os.path.dirname(_LIB), exist_ok=True)
if (not os.path.exists(_LIB)) or os.path.getmtime(_LIB) < os.path.getmtime(_SRC):
    tmp = _LIB + ".%d.tmp" % os.getpid()
    subprocess.check_call(["/usr/bin/clang", "-O2", "-shared", "-fPIC", "-o", tmp, _SRC])
    os.replace(tmp, _LIB)
_lib = C.CDLL(_LIB)
u32p, u8p = C.POINTER(C.c_uint32), C.POINTER(C.c_uint8)
_lib.dist_to_set.argtypes = [C.c_int, u32p, u8p, u8p]
_lib.dist_to_set.restype = None


def bits(x, n):
    return format(int(x), "0%db" % n)


def codes_str(mask):
    return "".join(str(c) for c in range(8) if (int(mask) >> c) & 1)


def dist_to_set(n, F, target):
    target = np.ascontiguousarray(target, np.uint8)
    d = np.empty(1 << n, np.uint8)
    _lib.dist_to_set(n, F.ctypes.data_as(u32p), target.ctypes.data_as(u8p), d.ctypes.data_as(u8p))
    return d


def cycle_states(F, s0):
    out = [int(s0)]
    z = int(F[s0])
    while z != s0:
        out.append(z)
        z = int(F[z])
    return out


class Case:
    """Cycles, rotation orbits, one-flip graph G1 and its closed classes for one (rule, n)."""

    def __init__(self, rule, n):
        self.rule, self.n = rule, n
        self.F, self.cm = K.build_F(rule, n)
        (self.m, self.cyc, self.attr, self.minstate, self.length, self.ccodes) = K.find_cycles(n, self.F, self.cm)
        m = self.m
        (self.no, self.rot1, self.orb, self.reps, self.osz, self.omin) = K.rotation_orbits(n, m, self.cyc, self.minstate)
        self.bijective = int(self.length.sum()) == (1 << n)
        self.src, self.dst = K.g1_edges(n, self.F, self.attr, m, self.minstate, self.length)
        G = csr_matrix((np.ones(len(self.src), np.int8), (self.src, self.dst)), shape=(m, m))
        self.ncomp, self.lab = connected_components(G, directed=True, connection="strong")
        leaving = np.zeros(self.ncomp, bool)
        cross = self.lab[self.src] != self.lab[self.dst]
        leaving[self.lab[self.src[cross]]] = True
        self.closed_comp = ~leaving
        self.in_closed = self.closed_comp[self.lab]
        self.has_out = np.bincount(self.src, minlength=m) > 0

    def row(self, c):
        """V(c, .) for all cycles (forward search from cycle c)."""
        d = K.bfs_from_cycle(self.n, self.F, self.minstate[c])
        return d[self.minstate], d

    def radius(self):
        """Exact radius r(C) = min_{C' != C} V(C, C') for every cycle (0 if there is only one cycle)."""
        r = np.where(self.has_out, 1, 0).astype(np.int64)
        if self.m == 1:
            return r
        for c in np.nonzero(~self.has_out)[0]:
            row, _ = self.row(c)
            row = row.astype(np.int64)
            row[c] = 10 ** 6
            r[c] = row.min()
        return r

    def full_V(self):
        V, kd = K.compute_V(self.n, self.F, self.cyc, self.cm, self.m, self.minstate, self.rot1, self.reps, use_rot=True)
        return V, kd

    def orbit_members(self, o):
        return np.nonzero(self.orb == o)[0]

    def reach_to(self, src, dst, targets):
        """Boolean array: nodes that reach one of `targets` along edges (src -> dst)."""
        m = self.m
        can = np.zeros(m, bool)
        can[list(targets)] = True
        order = np.argsort(dst, kind="stable")
        s_sorted, d_sorted = src[order], dst[order]
        starts = np.searchsorted(d_sorted, np.arange(m + 1))
        stack = list(targets)
        while stack:
            v = stack.pop()
            for u in s_sorted[starts[v]:starts[v + 1]]:
                if not can[u]:
                    can[u] = True
                    stack.append(int(u))
        return can

    def lemmaB(self, o, radius):
        """Hypotheses of Lemma B for rotation orbit o (members A_1..A_q, all of radius >= 2)."""
        A = self.orbit_members(o)
        q = len(A)
        inA = np.zeros(self.m, bool)
        inA[A] = True
        keep = ~inA[self.src]
        s1, d1 = self.src[keep], self.dst[keep]
        s2, d2 = [], []
        for a in A:
            row, _ = self.row(a)
            t = np.nonzero(row == 2)[0]
            s2.append(np.full(len(t), a, np.int32))
            d2.append(t.astype(np.int32))
        s2 = np.concatenate(s2) if s2 else np.zeros(0, np.int32)
        d2 = np.concatenate(d2) if d2 else np.zeros(0, np.int32)
        g2 = bool(self.reach_to(np.r_[s1, s2], np.r_[d1, d2], [int(A[0])]).all())
        g1_into_A = bool(self.reach_to(s1, d1, [int(a) for a in A]).all())   # weaker: weight-1 edges only
        target = np.zeros(1 << self.n, np.uint8)
        for a in A:
            target[cycle_states(self.F, self.minstate[a])] = 1
        dts = dist_to_set(self.n, self.F, target)
        entry = dts[self.minstate].astype(np.int64)
        entry_max = int(entry[~inA].max()) if q < self.m else 0
        return {"q": int(q), "g2_holds": g2, "g1_reach_A": g1_into_A, "entry_cost_max": entry_max}


def solve_full(rule, n):
    """Case plus dense V, gamma for all roots (sealed Edmonds), selected set, k_c."""
    c = Case(rule, n)
    V, kd = c.full_V()
    c.V = V.copy()
    c.kd = kd
    c.gamma = K.edmonds_all_roots(V)
    c.gmin = int(c.gamma.min())
    c.sel = c.gamma == c.gmin
    c.kc = (c.gamma[c.reps][:, None] + kd.astype(np.int64)).min(axis=0) - c.gmin
    c.kstar = int(c.kc.max())
    c.joint = int(np.bitwise_or.reduce(c.ccodes[c.sel]))
    return c


def class_reps():
    """Smallest rule number of each class under reflection and complementation (derived here)."""
    def refl(r):
        return sum(((r >> (4 * a + 2 * b + c)) & 1) << (4 * c + 2 * b + a) for a in (0, 1) for b in (0, 1) for c in (0, 1))

    def comp(r):
        return sum((1 - ((r >> (7 - k)) & 1)) << k for k in range(8))
    reps = sorted({min(r, refl(r), comp(r), refl(comp(r))) for r in range(256)})
    return reps, refl, comp
