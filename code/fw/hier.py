"""Root-free Edmonds contraction for minimum in-trees, all roots at once, with a laminar dual
certificate (path-growing variant after Tarjan 1977, meldable heaps merged small-to-large).

Input: an edge provider for m nodes that yields, for node v and weight level L, the heads u with
V(v, u) == L, and rowmax[v] = max_u V(v, u). Levels are expanded lazily: a sentinel entry for node v
with key = next unexpanded level stands for all edges of v not yet in the heap; since all of them
have weight >= that level, the minimum is exact whenever an explicit edge (or tie) is selected, and
a sentinel that reaches the top of a heap is replaced by the next level of edges.

Output (class Hier): for every node or contracted set X except the top: y[X] >= 0, parent[X],
sel_tail[X], sel_head[X], sel_w[X] (selected edge, original endpoints and weight). With T = sum y and
Dsum[v] = sum of y over non-top sets containing v, gamma[v] = T - Dsum[v] is the minimum weight of an
in-tree rooted at v; the family {X: y[X] > 0} with values y is a feasible dual for every root.
"""
from __future__ import annotations
import heapq
import numpy as np


class Hier:
    pass


class MatrixProvider:
    """Complete weighted digraph from a dense integer matrix (diagonal ignored)."""

    def __init__(self, V):
        self.V = np.asarray(V, dtype=np.int64)
        self.m = len(self.V)
        off = ~np.eye(self.m, dtype=bool)
        self.rowmax = np.array([int(self.V[v][off[v]].max()) if self.m > 1 else 0 for v in range(self.m)])

    def heads_upto(self, v, L):
        u = np.flatnonzero((self.V[v] <= L)); u = u[u != v]
        return u, self.V[v][u]

    def heads_at(self, v, L):
        u = np.flatnonzero(self.V[v] == L); u = u[u != v]
        return u


def edmonds_all_roots(prov, L0: int = 1) -> Hier:
    m = prov.m
    H = Hier(); H.m = m
    if m == 1:
        H.nsup = 1; H.top = 0; H.y = np.zeros(1, np.int64); H.parent = np.full(1, -1, np.int64)
        H.sel_tail = H.sel_head = H.sel_w = np.full(1, -1, np.int64)
        H.T = 0; H.Dsum = np.zeros(1, np.int64); H.gamma = np.zeros(1, np.int64); H.expanded = 0
        return H
    cap = 2 * m
    uf = list(range(cap))                     # union-find over node/set ids (root = current set)

    def find(x):
        r = x
        while uf[r] != r:
            r = uf[r]
        while uf[x] != r:
            uf[x], x = r, uf[x]
        return r

    y = [0] * cap; parent = [-1] * cap
    sel_tail = [-1] * cap; sel_head = [-1] * cap; sel_w = [-1] * cap
    heaps = [None] * cap; off = [0] * cap
    expanded = 0
    # heap entries: (key, kind, head, tail, aux)
    #   kind 0: edge tail -> head; aux = iterator id (>0) whose next head is pushed when this pops
    #   kind 1: sentinel for the unexpanded levels of tail; aux = next level
    iters = [None]                            # iterator id -> [sorted heads array, position]

    def new_iter(heads):
        heads = np.sort(np.asarray(heads, dtype=np.int64))
        if len(heads) == 0:
            return None
        iters.append([heads, 0])
        return len(iters) - 1

    for v in range(m):
        h = []
        for lev in range(0, L0 + 1):          # level 0 included (zero-resistance edges)
            it = new_iter(prov.heads_at(v, lev))
            if it is not None:
                h.append((lev, 0, int(iters[it][0][0]), v, it))
        if prov.rowmax[v] > L0:
            h.append((L0 + 1, 1, -1, v, L0 + 1))
        heapq.heapify(h)
        heaps[v] = h
    in_path = [False] * cap
    nxt = m
    path = [0]; in_path[0] = True
    alive = m                                 # number of current sets
    pop, push = heapq.heappop, heapq.heappush
    while True:
        X = path[-1]
        if alive == 1:
            top = X
            break
        h = heaps[X]
        # extract the minimum valid entry
        while True:
            assert h, "set without outgoing edges while others remain"
            ent = pop(h)
            key, kind, u, v, aux = ent
            if kind == 1:                     # sentinel: expand level aux of v's edges
                expanded += 1
                lev = aux
                it = new_iter(prov.heads_at(v, lev))
                if it is not None:
                    push(h, (key, 0, int(iters[it][0][0]), v, it))
                if prov.rowmax[v] > lev:
                    push(h, (key + 1, 1, -1, v, lev + 1))
                continue
            if aux:                           # advance the iterator this edge came from
                st = iters[aux]
                st[1] += 1
                if st[1] < len(st[0]):
                    push(h, (key, 0, int(st[0][st[1]]), v, aux))
                else:
                    iters[aux] = None
            if find(u) == X:                  # internal edge: dead forever
                continue
            break
        key, kind, u, v, aux = ent
        r = key - off[X]
        assert r >= 0
        y[X] = r
        off[X] += r
        sel_tail[X] = v; sel_head[X] = u
        Z = find(u)
        if not in_path[Z]:
            path.append(Z); in_path[Z] = True
            continue
        # contract the path segment from Z to X into a new set Q
        Q = nxt; nxt += 1
        seg = []
        while True:
            W = path.pop(); in_path[W] = False; seg.append(W)
            if W == Z:
                break
        # merge heaps small-to-large, converting offsets
        seg.sort(key=lambda W: -len(heaps[W]))
        big = seg[0]
        hq = heaps[big]; oq = off[big]
        push = heapq.heappush
        for W in seg[1:]:                       # push the smaller heaps' entries: O(small log big)
            d = oq - off[W]
            for e in heaps[W]:
                push(hq, (e[0] + d, e[1], e[2], e[3], e[4]))
            heaps[W] = None
        heaps[big] = None
        heaps[Q] = hq; off[Q] = oq
        for W in seg:
            uf[W] = Q; parent[W] = Q
        alive -= len(seg) - 1
        path.append(Q); in_path[Q] = True
    H.nsup = nxt; H.top = top
    H.y = np.array(y[:nxt], dtype=np.int64); H.y[top] = 0
    H.parent = np.array(parent[:nxt], dtype=np.int64)
    H.sel_tail = np.array(sel_tail[:nxt], dtype=np.int64)
    H.sel_head = np.array(sel_head[:nxt], dtype=np.int64)
    # weights of selected edges (exact V)
    H.sel_w = np.array([prov_weight(prov, int(H.sel_tail[X]), int(H.sel_head[X])) if X != top else -1
                        for X in range(nxt)], dtype=np.int64)
    H.T = int(H.y.sum())
    # Dsum: sum of y over non-top sets containing each node (sets have larger ids than children)
    acc = np.zeros(nxt, dtype=np.int64)
    for X in range(nxt - 1, -1, -1):
        p = H.parent[X]
        acc[X] = (acc[p] if p >= 0 else 0) + H.y[X]
    H.Dsum = acc[:m]
    H.gamma = H.T - H.Dsum
    H.expanded = expanded
    return H


def prov_weight(prov, t, h):
    return int(prov.weight(t, h)) if hasattr(prov, "weight") else int(prov.V[t, h])


def children_lists(H):
    ch = [[] for _ in range(H.nsup)]
    for X in range(H.nsup):
        if H.parent[X] >= 0:
            ch[H.parent[X]].append(X)
    return ch


def tree_for_root(H, r):
    """Optimal in-tree rooted at r as (tail, head, weight) edges (top-down sink propagation)."""
    if H.m == 1:
        return []
    ch = children_lists(H)

    def child_containing(X, v):
        z = v
        while H.parent[z] != X:
            z = H.parent[z]
        return z
    edges = []
    stack = [(H.top, r)]
    while stack:
        X, s = stack.pop()
        if X < H.m:
            continue
        c = child_containing(X, s)
        for Y in ch[X]:
            if Y == c:
                stack.append((Y, s))
            else:
                t = int(H.sel_tail[Y])
                edges.append((t, int(H.sel_head[Y]), int(H.sel_w[Y])))
                stack.append((Y, t))
    return edges


def laminar_sets(H):
    """(set id, sorted member nodes, y) for every non-top set with y > 0 (singletons included)."""
    ch = children_lists(H)
    members = [None] * H.nsup
    for X in range(H.nsup):
        members[X] = [X] if X < H.m else sorted(v for Y in ch[X] for v in members[Y])
    return [(X, members[X], int(H.y[X])) for X in range(H.nsup) if X != H.top and H.y[X] > 0]
