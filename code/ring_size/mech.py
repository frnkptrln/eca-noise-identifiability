"""Mechanism analysis of the noise-selected cycles (ring-size study).

For one rule on one ring: the v0.2 solver (code/fw/fwlib.classify) gives the cycles, the inter-cycle
resistances V(C, C') (one 0-1 BFS per rotation orbit) and the potentials gamma. This module adds,
per cycle: temporal period T, spatial period s (smallest s | n with rot^s x = x; the same for every
state of a cycle because F commutes with rotations), drift d (F x = rot^d x on the cycle, -1 if F is
not a rotation there), codes, radius r(C) = min_{C' != C} V(C, C'); and per (rule, n): the one-flip
graph G1 (edges of weight 1) with its strongly connected components and closed classes, and the
crystal-capture test of PREDICTIONS_ring_size.md (criterion G2).

Exact integer computation. Conventions as in fwlib: bit i = cell i, code c = 4 x_{i-1} + 2 x_i + x_{i+1}.
"""
from __future__ import annotations
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fw"))
import numpy as np
import fwlib  # noqa: E402
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def codes_str(mask: int) -> str:
    return "".join(str(c) for c in range(8) if (int(mask) >> c) & 1)


def rot1(x: int, n: int, k: int) -> int:
    k %= n
    full = (1 << n) - 1
    return ((x << k) | (x >> (n - k))) & full if k else x


def spatial_period(x: int, n: int) -> int:
    for s in range(1, n + 1):
        if n % s == 0 and rot1(x, n, s) == x:
            return s
    raise AssertionError


def drift(cs, j: int) -> int:
    st = [int(z) for z in cs.states_of(j)]
    for d in range(cs.n):
        if all(rot1(z, cs.n, d) == int(cs.F[z]) for z in st):
            return d
    return -1


def bits(x: int, n: int) -> str:
    """Cells 0..n-1, left to right."""
    return "".join(str((int(x) >> i) & 1) for i in range(n))


class Rows:
    """V(C_j, .) for every cycle j from the representative rows of fwlib.EdgeStore."""

    def __init__(self, es):
        self.es, self.n = es, es.cs.n

    def row(self, j: int) -> np.ndarray:
        k = int(self.es.shift[j]); r = int(self.es.rep[j])
        return self.es.vrows[r][self.es.rot[(-k) % self.n]].astype(np.int64)


def one_flip_graph(es):
    """Edges j -> i with V(C_j, C_i) = 1, i != j, as CSR (built from representative rows)."""
    m = es.m
    tails, heads = [], []
    for r in es.reps:
        r = int(r)
        h = np.flatnonzero(es.vrows[r] == 1); h = h[h != r]
        for j in np.flatnonzero(es.rep == r):
            hj = es.rot[int(es.shift[j])][h]
            tails.append(np.full(len(hj), j, dtype=np.int64)); heads.append(hj.astype(np.int64))
    t = np.concatenate(tails) if tails else np.zeros(0, np.int64)
    h = np.concatenate(heads) if heads else np.zeros(0, np.int64)
    return csr_matrix((np.ones(len(t), dtype=np.int8), (t, h)), shape=(m, m))


def closed_classes(G):
    ncomp, lab = connected_components(G, directed=True, connection="strong")
    Gc = G.tocoo()
    leaving = np.zeros(ncomp, dtype=bool)
    s = lab[Gc.row] != lab[Gc.col]
    leaving[lab[Gc.row[s]]] = True
    return ncomp, lab, [c for c in range(ncomp) if not leaving[c]]


def reaches(G_rev, target: int) -> np.ndarray:
    """Nodes that reach `target`, by BFS on the reversed graph G_rev (CSR)."""
    m = G_rev.shape[0]
    seen = np.zeros(m, dtype=bool); seen[target] = True
    frontier = np.array([target])
    ip, ix = G_rev.indptr, G_rev.indices
    while len(frontier):
        nxt = np.unique(np.concatenate([ix[ip[v]:ip[v + 1]] for v in frontier]))
        nxt = nxt[~seen[nxt]]
        seen[nxt] = True
        frontier = nxt
    return seen


def analyze(rule: int, n: int, res: dict | None = None, list_all: bool = False):
    """(summary record, orbit records) for (rule, n). Orbit records: every selected rotation orbit of
    cycles, and every orbit if list_all."""
    if res is None:
        res = fwlib.classify(rule, n)
    cs, es, gamma = res["cs"], res["es"], res["gamma"]
    m = cs.m
    sel = np.zeros(m, dtype=bool); sel[res["stable"]] = True
    rows = Rows(es)
    rad = np.full(m, -1, dtype=np.int64)
    if m > 1:
        for r in es.reps:
            r = int(r)
            v = es.vrows[r].astype(np.int64).copy(); v[r] = 10 ** 6
            rad[es.rep == r] = int(v.min())
        G1 = one_flip_graph(es)
        ncomp, lab, closed = closed_classes(G1)
    else:
        G1 = csr_matrix((1, 1), dtype=np.int8); ncomp, lab, closed = 1, np.zeros(1, int), [0]
    closed_union = np.isin(lab, closed)
    S = np.flatnonzero(sel)
    S_reps = np.unique(es.rep[S])
    # BUG-R1: with a single cycle (m = 1) nothing competes; not called a crystal orbit (verifier convention)
    one_orbit = m > 1 and len(S_reps) == 1 and np.array_equal(S, np.flatnonzero(es.rep == S_reps[0]))
    cover = int(np.bitwise_or.reduce(cs.cyc_codes[S]))
    sp = {int(r): spatial_period(int(cs.cyc_min[int(r)]), n) for r in es.reps}
    rec = dict(rule=rule, n=n, cycles=m, cycle_orbits=len(es.reps), n_selected=int(sel.sum()),
               selected_orbits=len(S_reps), gamma_min=int(res["gmin"]), kstar=int(res["kstar"]),
               k_c="-".join(str(int(v)) for v in res["k_c"]), selected_cover=codes_str(cover),
               g1_sccs=int(ncomp), g1_closed=len(closed),
               selected_eq_closed_union=bool(np.array_equal(sel, closed_union)),
               radius_selected_min=int(rad[S].min()), radius_selected_max=int(rad[S].max()),
               radius_other_min=int(rad[~sel].min()) if (~sel).any() else -1,
               radius_other_max=int(rad[~sel].max()) if (~sel).any() else -1,
               selected_spatial_periods=";".join(str(v) for v in sorted({sp[int(r)] for r in S_reps})),
               selected_temporal_periods=";".join(str(v) for v in sorted({int(cs.period[int(r)]) for r in S_reps})),
               crystal_orbit=bool(one_orbit), crystal_p=-1, entry_cost_max=-1, g2_holds=False,
               gamma_formula_ok=False)
    if one_orbit and m > 1:
        A = S; A1 = int(A[0])
        rec["crystal_p"] = sp[int(S_reps[0])]
        ec = 0
        for j in np.flatnonzero(~sel):
            ec = max(ec, int(rows.row(int(j))[A].min()))
        rec["entry_cost_max"] = ec
        Gc = G1.tocoo()
        keep = ~sel[Gc.row]
        t = [Gc.row[keep]]; h = [Gc.col[keep]]
        for a in A:
            ra = rows.row(int(a)); hh = np.flatnonzero(ra == 2); hh = hh[hh != a]
            t.append(np.full(len(hh), int(a))); h.append(hh)
        t = np.concatenate(t); h = np.concatenate(h)
        G2rev = csr_matrix((np.ones(len(t), np.int8), (h, t)), shape=(m, m))
        ok = bool(reaches(G2rev, A1).all()) and int(rad[A].min()) >= 2
        rec["g2_holds"] = ok
        rec["gamma_formula_ok"] = bool(ok and int(res["gmin"]) == m + len(A) - 2)
    orbit_recs = []
    for r in es.reps:
        r = int(r)
        if not (sel[r] or list_all):
            continue
        orbit_recs.append(dict(rule=rule, n=n, orbit_rep_min_state=int(cs.cyc_min[r]),
                               pattern=bits(int(cs.cyc_min[r]), n),
                               orbit_size=int((es.rep == r).sum()), temporal_period=int(cs.period[r]),
                               spatial_period=sp[r], drift=drift(cs, r),
                               codes=codes_str(int(cs.cyc_codes[r])), gamma=int(gamma[r]),
                               radius=int(rad[r]), selected=bool(sel[r])))
    return rec, orbit_recs
