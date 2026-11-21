"""V, R(C -> D_c) by the C solver vbfs; gamma by Chu-Liu/Edmonds (networkx); k_c from the definition
k_c = min_C [gamma(C) + R(C -> D_c)] - min gamma (conventions of PROOF_154.md, Section 1)."""
import os, sys, subprocess, tempfile, heapq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import networkx as nx
import eca

HERE = os.path.dirname(os.path.abspath(__file__))
VBFS = os.path.join(HERE, 'vbfs')


def code_masks(n):
    mask = (1 << n) - 1
    x = np.arange(1 << n, dtype=np.int64)
    a = ((x << 1) | (x >> (n - 1))) & mask
    c = ((x >> 1) | (x << (n - 1))) & mask
    out = np.zeros(1 << n, dtype=np.uint8)
    for code in range(8):
        p, q, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
        t = (a if p else ~a) & (x if q else ~x) & (c if r else ~c) & mask
        out |= ((t != 0).astype(np.uint8) << code)
    return out


def VR(R):
    n, m = R.n, R.m
    lab = np.full(1 << n, -1, dtype=np.int32)
    lab[R.pstates] = R.pcyc
    with tempfile.TemporaryDirectory() as td:
        fi, fo = os.path.join(td, 'in.bin'), os.path.join(td, 'out.bin')
        with open(fi, 'wb') as fh:
            np.array([n, m], dtype=np.int32).tofile(fh)
            R.F.astype(np.uint32).tofile(fh)
            lab.tofile(fh)
            code_masks(n).tofile(fh)
            R.reps.astype(np.int32).tofile(fh)
        subprocess.run([VBFS, fi, fo], check=True)
        raw = np.fromfile(fo, dtype=np.int32)
    V = raw[:m * m].reshape(m, m)
    Rc = raw[m * m:].reshape(m, 8)
    return V, Rc


def VR_python(R):
    """slow independent version: Dijkstra with explicit multi-flip steps x -> y, cost H(Fx, y) (n <= 8)"""
    n, m = R.n, R.m
    N = 1 << n
    cm = code_masks(n)
    V = np.zeros((m, m), dtype=np.int64)
    Rc = np.zeros((m, 8), dtype=np.int64)
    pc = [bin(i).count('1') for i in range(N)]
    for s in range(m):
        dist = [10 ** 9] * N
        src = int(R.reps[s])
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, x = heapq.heappop(pq)
            if d > dist[x]:
                continue
            fx = int(R.F[x])
            for y in range(N):
                nd = d + pc[fx ^ y]
                if nd < dist[y]:
                    dist[y] = nd
                    heapq.heappush(pq, (nd, y))
        for c in range(m):
            V[s, c] = min(dist[y] for y in R.pstates[R.pcyc == c])
        for code in range(8):
            ys = [y for y in range(N) if (cm[y] >> code) & 1]
            Rc[s, code] = min(dist[y] for y in ys) if ys else 10 ** 9
    return V, Rc


def spt_weight(V, root):
    """weight of a shortest-path in-tree towards root (Dijkstra on the reversed complete graph): an upper bound"""
    m = V.shape[0]
    dist = np.full(m, np.inf)
    dist[root] = 0
    done = np.zeros(m, dtype=bool)
    par = np.full(m, -1)
    for _ in range(m):
        u = int(np.argmin(np.where(done, np.inf, dist)))
        done[u] = True
        cand = V[:, u] + dist[u]          # edges a -> u
        better = (~done) & (cand < dist)
        dist[better] = cand[better]
        par[better] = u
    return int(sum(V[a, par[a]] for a in range(m) if a != root))


def gamma_root(V, root, prune=True):
    """minimum weight of a spanning in-tree rooted at root (edges C -> C' of weight V(C, C')).
    prune: every edge weighs >= 1, so a tree containing an edge of weight w weighs >= (m - 2) + w; with UB the weight
    of a feasible tree, edges with w > UB - (m - 2) are in no optimal tree and are dropped (the SPT survives)."""
    m = V.shape[0]
    if m == 1:
        return 0
    wmax = spt_weight(V, root) - (m - 2) if prune else 1 << 30
    G = nx.DiGraph()
    G.add_nodes_from(range(m))
    a_idx, b_idx = np.nonzero(V <= wmax)
    for a, b in zip(a_idx.tolist(), b_idx.tolist()):
        if a != b and a != root:
            G.add_edge(b, a, weight=int(V[a, b]))   # reversed edge of a -> b
    T = nx.minimum_spanning_arborescence(G, attr='weight', preserve_attrs=True)
    return int(sum(d['weight'] for _, _, d in T.edges(data=True)))


def potentials(V, roots=None):
    m = V.shape[0]
    roots = range(m) if roots is None else roots
    return {int(r): gamma_root(V, r) for r in roots}


def k_vector(gam, Rc):
    """needs gamma for every cycle"""
    g = np.array([gam[c] for c in range(len(gam))])
    gmin = g.min()
    return [int(min(g[c] + Rc[c, code] for c in range(len(g))) - gmin) for code in range(8)]
