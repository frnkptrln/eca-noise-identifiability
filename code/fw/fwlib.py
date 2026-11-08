"""Small-noise limit of noisy elementary cellular automata: noise-selected cycles and orders.

Exact integer computation. For eps > 0 the chain X_{t+1} = F(X_t) XOR Z_t (Z_t i.i.d. Bernoulli(eps)
per cell) has transition probabilities eps^r (1-eps)^(n-r) with resistance r(x->y) = H(F(x), y).
By the Markov chain tree theorem, ord pi_eps(x) = W(x) - min_y W(y), where W(x) is the minimum total
resistance of a spanning in-tree rooted at x; with the cycles C of F as recurrent classes,
W(x) = min_C [gamma(C) + R(C -> x)], gamma(C) the minimum weight of an in-tree on the cycles rooted at C
with edge weights V(C, C') = R(C -> C') (minimum path resistance).

Conventions as in eca_noise.py: states 0..2^n-1, bit i = cell i on a ring, Wolfram rule numbers,
code c = 4 x_{i-1} + 2 x_i + x_{i+1}.

Main objects
------------
CycleStructure(rule, n)      cycles of F, basin labels, rotation action on cycles
bfs_from_cycle(cs, j)        0-1 BFS distances R(C_j -> x) for all x (uint8; 255 = beyond depth limit)
hier.edmonds_all_roots(provider)
                             root-free Edmonds contraction with laminar dual certificate; gamma(C)
                             for all roots at once (module hier.py)
classify(rule, n)            gamma, noise-selected cycles, k_c, k*, certificate
"""
from __future__ import annotations

import numpy as np

UNREACHED = np.uint8(255)


# ----------------------------------------------------------------------------------------------
# rules, states, codes
# ----------------------------------------------------------------------------------------------
def succ_map(rule: int, n: int) -> np.ndarray:
    x = np.arange(1 << n, dtype=np.int64)
    out = np.zeros_like(x)
    for i in range(n):
        l = (x >> ((i - 1) % n)) & 1
        c = (x >> i) & 1
        r = (x >> ((i + 1) % n)) & 1
        out |= ((rule >> (4 * l + 2 * c + r)) & 1) << i
    return out


def code_mask(n: int) -> np.ndarray:
    """(2^n,) uint8: bit c set iff code c occurs somewhere in the state."""
    x = np.arange(1 << n, dtype=np.int64)
    m = np.zeros(1 << n, dtype=np.uint8)
    for i in range(n):
        l = (x >> ((i - 1) % n)) & 1
        c = (x >> i) & 1
        r = (x >> ((i + 1) % n)) & 1
        m |= (np.uint8(1) << (4 * l + 2 * c + r).astype(np.uint8))
    return m


def rotate(x: np.ndarray, n: int, k: int = 1) -> np.ndarray:
    """Cell i -> cell i+k (mod n)."""
    k %= n
    full = (1 << n) - 1
    return ((x << k) | (x >> (n - k))) & full if k else x.copy()


def reflect_rule(rule: int) -> int:
    return sum(((rule >> c) & 1) << (4 * (c & 1) + 2 * ((c >> 1) & 1) + ((c >> 2) & 1)) for c in range(8))


def complement_rule(rule: int) -> int:
    return sum((1 - ((rule >> c) & 1)) << (7 - c) for c in range(8))


def class_rep(rule: int) -> int:
    return min({rule, reflect_rule(rule), complement_rule(rule), reflect_rule(complement_rule(rule))})


def class_reps() -> list[int]:
    return [r for r in range(256) if class_rep(r) == r]


def is_bijective(F: np.ndarray) -> bool:
    seen = np.zeros(len(F), dtype=bool)
    seen[F] = True
    return bool(seen.all())


# ----------------------------------------------------------------------------------------------
# cycles of the deterministic map
# ----------------------------------------------------------------------------------------------
class CycleStructure:
    """Cycles of F on {0,1}^n, numbered 0..m-1 in increasing order of their smallest state."""

    def __init__(self, rule: int, n: int, F: np.ndarray | None = None):
        self.rule, self.n = rule, n
        S = 1 << n
        self.F = succ_map(rule, n) if F is None else F
        F = self.F
        # transient depth and on-cycle flag: iterate until every orbit has entered a cycle
        G = F.copy()
        for _ in range(n):            # G = F^(2^n): lands on a cycle for every start
            G = G[G]
        on = np.zeros(S, dtype=bool)
        on[G] = True
        self.on_cycle = on
        # cycle label = smallest state on the cycle (pointer doubling)
        lab = np.arange(S, dtype=np.int64)
        P = F.copy()
        for _ in range(n):
            lab = np.minimum(lab, lab[P])
            P = P[P]
        mins = np.unique(lab[on])
        self.m = len(mins)
        idx_of_min = np.full(S, -1, dtype=np.int64)
        idx_of_min[mins] = np.arange(self.m)
        cyc_of_state = np.full(S, -1, dtype=np.int64)
        cyc_of_state[on] = idx_of_min[lab[on]]
        # basin label: the cycle reached from every state (G lands on a cycle)
        self.basin = cyc_of_state[G]
        self.cyc_of_state = cyc_of_state          # -1 off cycles
        self.cyc_min = mins
        # cycle states grouped by cycle id
        cs_states = np.flatnonzero(on)
        order = np.argsort(cyc_of_state[cs_states], kind="stable")
        self.cyc_states = cs_states[order]
        self.cyc_start = np.searchsorted(cyc_of_state[self.cyc_states], np.arange(self.m + 1))
        self.period = np.diff(self.cyc_start)
        # depth (transient length) of every state
        depth = np.zeros(S, dtype=np.int64)
        cur = np.arange(S, dtype=np.int64)
        alive = ~on
        d = 0
        while alive.any():
            d += 1
            cur = F[cur]
            newly = alive & on[cur]
            depth[newly] = d
            alive &= ~newly
        self.depth = depth
        self.max_depth = int(depth.max())
        # doubling tables for forward closure of transient parts
        self.J = max(1, int(np.ceil(np.log2(self.max_depth + 1)))) if self.max_depth > 0 else 0
        self.Fpow = []
        P = F.copy()
        for _ in range(self.J):
            self.Fpow.append(P)
            P = P[P]
        # codes on each cycle
        cm = code_mask(n)
        self.state_codes = cm
        self.cyc_codes = np.zeros(self.m, dtype=np.uint8)
        np.bitwise_or.at(self.cyc_codes, cyc_of_state[self.cyc_states], cm[self.cyc_states])
        # rotation action on cycles
        self.rot1 = cyc_of_state[rotate(self.cyc_min, n, 1)]

    def states_of(self, j: int) -> np.ndarray:
        return self.cyc_states[self.cyc_start[j]:self.cyc_start[j + 1]]

    def rot_power(self, k: int) -> np.ndarray:
        p = np.arange(self.m)
        for _ in range(k % self.n):
            p = self.rot1[p]
        return p

    def rotation_orbits(self) -> tuple[np.ndarray, np.ndarray]:
        """(rep, shift): cycle j = rot^shift[j](rep[j]); rep = smallest id in the rotation orbit."""
        rep = np.full(self.m, -1, dtype=np.int64)
        shift = np.zeros(self.m, dtype=np.int64)
        for j in range(self.m):
            if rep[j] >= 0:
                continue
            c, k = j, 0
            while rep[c] < 0:
                rep[c] = j
                shift[c] = k
                c = self.rot1[c]
                k += 1
        return rep, shift

    def closure(self, M: np.ndarray) -> np.ndarray:
        """Forward closure of a boolean state set under F (orbits including whole cycles)."""
        M = M.copy()
        for P in self.Fpow:                       # after pass j: all F^t(x), t < 2^(j+1)
            idx = np.flatnonzero(M)
            M[P[idx]] = True
        # (2^J > max_depth, so every orbit has reached its cycle); complete the cycles hit
        hit = np.zeros(self.m, dtype=bool)
        hit[self.cyc_of_state[np.flatnonzero(M & self.on_cycle)]] = True
        M |= self.on_cycle & hit[np.maximum(self.cyc_of_state, 0)] & (self.cyc_of_state >= 0)
        return M


# ----------------------------------------------------------------------------------------------
# minimum resistances from one cycle: 0-1 BFS (x -> F(x) cost 0, single bit flip cost 1)
# ----------------------------------------------------------------------------------------------
def bfs_from_cycle(cs: CycleStructure, j: int, max_depth: int | None = None,
                   stop_when_complete: bool = False) -> np.ndarray:
    """R(C_j -> x) for every state x as uint8 (UNREACHED beyond max_depth).

    The single-layer graph is equivalent to the two-layer graph (state -> pre-noise F(state) at
    cost 0, bit flips between pre-noise points at cost 1, pre-noise point -> state at cost 0) because
    a pre-noise point z is reached at the same cost as the state z whenever the sources are whole
    cycles. With stop_when_complete, stops once every cycle and every code has been reached.
    """
    n = cs.n
    S = 1 << n
    dist = np.full(S, UNREACHED, dtype=np.uint8)
    M = np.zeros(S, dtype=bool)
    M[cs.states_of(j)] = True
    dist[M] = 0
    frontier = np.flatnonzero(M)
    level = 0
    lim = n if max_depth is None else max_depth
    codes_seen = int(np.bitwise_or.reduce(cs.state_codes[frontier])) if len(frontier) else 0
    while level < lim and len(frontier):
        level += 1
        new = np.zeros(S, dtype=bool)
        for i in range(n):
            new[frontier ^ (1 << i)] = True
        new &= ~M
        new = cs.closure(new) & ~M
        frontier = np.flatnonzero(new)
        dist[frontier] = level
        M |= new
        if stop_when_complete and len(frontier):
            codes_seen |= int(np.bitwise_or.reduce(cs.state_codes[frontier]))
            if codes_seen == 255 and M[cs.cyc_min].all():
                break
    return dist


def vrow_and_codes(cs: CycleStructure, dist: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """V(C, C') for all C' (uint8, UNREACHED if beyond depth) and R(C -> D_c) for the 8 codes."""
    d = dist[cs.cyc_states]
    vrow = np.minimum.reduceat(d, cs.cyc_start[:-1]).astype(np.uint8)
    rc = np.full(8, UNREACHED, dtype=np.uint8)
    for c in range(8):
        sel = (cs.state_codes >> c) & 1
        v = dist[sel.astype(bool)]
        rc[c] = v.min() if len(v) else UNREACHED
    return vrow, rc


# ----------------------------------------------------------------------------------------------
# classification of one rule on one ring
# ----------------------------------------------------------------------------------------------
class EdgeStore:
    """Edge provider for hier.edmonds_all_roots. Per rotation representative: BFS once (stopping when
    every cycle and every code is reached), keep the full V row and R(C -> D_c). Edges of cycle
    j = rot^k(rep) are the rep's row rotated: V(rot^k C_rep, C_i) = V(C_rep, rot^-k C_i)."""

    def __init__(self, cs, keep_dists=False):
        self.cs = cs
        self.m = cs.m
        rep, shift = cs.rotation_orbits()
        self.rep, self.shift = rep, shift
        self.reps = np.unique(rep)
        self.rot = [cs.rot_power(k) for k in range(cs.n)]
        self.vrows, self.rc, self.dists = {}, {}, {}
        self._cache = {}
        for r in self.reps:
            dist = bfs_from_cycle(cs, int(r), stop_when_complete=not keep_dists)
            vrow, rc = vrow_and_codes(cs, dist)
            assert (vrow != UNREACHED).all() and (rc != UNREACHED).all()
            self.vrows[int(r)] = vrow
            self.rc[int(r)] = rc
            if keep_dists:
                self.dists[int(r)] = dist
        self.Rcode = np.array([self.rc[int(rep[j])] for j in range(cs.m)], dtype=np.int64).reshape(cs.m, 8)
        rmax = {}
        for r in self.reps:
            row = self.vrows[int(r)].astype(np.int64).copy(); row[int(r)] = -1
            rmax[int(r)] = int(row.max())
        self.rowmax = np.array([rmax[int(rep[j])] for j in range(cs.m)], dtype=np.int64)

    def weight(self, j, i):
        k = int(self.shift[j]); r = int(self.rep[j])
        return int(self.vrows[r][self.rot[(-k) % self.cs.n][i]])

    def _level(self, r, L):
        """Heads (in the representative's frame) with V(C_rep, .) == L, cached per (rep, level)."""
        key = (r, L)
        c = self._cache.get(key)
        if c is None:
            c = np.flatnonzero(self.vrows[r] == L).astype(np.int32)   # int32: halves cache memory
            self._cache[key] = c
        return c

    def heads_upto(self, j, L):
        r = int(self.rep[j]); k = int(self.shift[j])
        hs, ws = [], []
        for lev in range(1, L + 1):
            h = self._level(r, lev)
            hs.append(h); ws.append(np.full(len(h), lev, dtype=np.int64))
        hr = np.concatenate(hs) if hs else np.zeros(0, np.int64)
        w = np.concatenate(ws) if ws else np.zeros(0, np.int64)
        hj = self.rot[k][hr]
        keep = hj != j
        return hj[keep], w[keep]

    def heads_at(self, j, L):
        r = int(self.rep[j]); k = int(self.shift[j])
        hj = self.rot[k][self._level(r, L)]
        return hj[hj != j]


def classify(rule: int, n: int, L0: int = 1, keep_dists: bool = False, F: np.ndarray | None = None) -> dict:
    """gamma for every cycle, noise-selected cycles, k_c and k* for one rule on one ring (exact)."""
    import hier
    F = succ_map(rule, n) if F is None else F
    cs = CycleStructure(rule, n, F)
    es = EdgeStore(cs, keep_dists)
    H = hier.edmonds_all_roots(es, L0)
    gamma = H.gamma
    gmin = int(gamma.min())
    stable = np.flatnonzero(gamma == gmin)
    Rcode = es.Rcode
    k_c = (gamma[:, None] + Rcode).min(axis=0) - gmin        # (8,)
    kstar = int(k_c.max())
    cover = int(np.bitwise_or.reduce(cs.cyc_codes[stable]))
    return dict(rule=rule, n=n, m=cs.m, cs=cs, es=es, H=H, gamma=gamma, gmin=gmin, stable=stable,
                Rcode=Rcode, k_c=k_c, kstar=kstar, stable_cover=cover, dists=es.dists,
                rep=es.rep, shift=es.shift, expanded=H.expanded)
