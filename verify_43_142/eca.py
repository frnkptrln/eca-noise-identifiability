"""Independent core for the verification of proofs_43_142/PROOF_43_142.md.

Written from the rule tables and the definitions of report_ring_size.md, Section 3, and of the note v0.2,
Section 6 only. No code of proofs_43_142/ or code/ is imported or was read.

Conventions: a state of the ring Z/nZ is an integer, bit i = cell i. The code of cell i is
4 x_(i-1) + 2 x_i + x_(i+1); f(code) = bit `code` of the rule number; (F x)_i = f(code of cell i).
"""
import numpy as np


def rot_left_neighbour(x, n):
    """array whose bit i is x_(i-1)."""
    mask = (1 << n) - 1
    return ((x << 1) | (x >> (n - 1))) & mask


def rot_right_neighbour(x, n):
    """array whose bit i is x_(i+1)."""
    return (x >> 1) | ((x & 1) << (n - 1))


def global_map(rule, n, x):
    """F applied to an integer array x of states (vectorised over x)."""
    x = np.asarray(x, dtype=np.int64)
    mask = (1 << n) - 1
    L = rot_left_neighbour(x, n)
    R = rot_right_neighbour(x, n)
    nL, nx, nR = (~L) & mask, (~x) & mask, (~R) & mask
    out = np.zeros_like(x)
    for c in range(8):
        if (rule >> c) & 1:
            a, b, cc = (c >> 2) & 1, (c >> 1) & 1, c & 1
            out |= (L if a else nL) & (x if b else nx) & (R if cc else nR)
    return out


def global_map_slow(rule, n, x):
    """Cell-by-cell reference implementation for a single state (used to test global_map)."""
    bits = [(x >> i) & 1 for i in range(n)]
    y = 0
    for i in range(n):
        c = 4 * bits[(i - 1) % n] + 2 * bits[i] + bits[(i + 1) % n]
        y |= ((rule >> c) & 1) << i
    return y


def codes_present(n, x):
    """8-bit mask per state: bit c set iff code c occurs at some cell."""
    x = np.asarray(x, dtype=np.int64)
    mask = (1 << n) - 1
    L = rot_left_neighbour(x, n)
    R = rot_right_neighbour(x, n)
    nL, nx, nR = (~L) & mask, (~x) & mask, (~R) & mask
    out = np.zeros_like(x)
    for c in range(8):
        a, b, cc = (c >> 2) & 1, (c >> 1) & 1, c & 1
        hit = (L if a else nL) & (x if b else nx) & (R if cc else nR)
        out |= (hit != 0).astype(np.int64) << c
    return out


def popcount(x):
    x = np.asarray(x, dtype=np.int64)
    c = np.zeros_like(x)
    y = x.copy()
    while np.any(y):
        c += y & 1
        y >>= 1
    return c


class Dynamics:
    """Functional graph of F on all 2^n states: periodic states, cycles, attractor of every state."""

    def __init__(self, rule, n):
        self.rule, self.n = rule, n
        N = 1 << n
        self.N = N
        states = np.arange(N, dtype=np.int64)
        self.succ = global_map(rule, n, states)
        # F^(2^k) by doubling; after n+1 doublings T = 2^(n+1) > number of states >= any transient + period
        p = self.succ.copy()
        for _ in range(n + 1):
            p = p[p]
        self.FT = p                                  # F^T with T = 2^(n+1)
        periodic = np.zeros(N, dtype=bool)
        periodic[np.unique(p)] = True                # image of F^T = periodic states
        self.periodic = periodic
        # cycle label = minimum state of the cycle, via min-doubling along the orbit
        lab = states.copy()
        q = self.succ.copy()
        for _ in range(n + 1):
            lab = np.minimum(lab, lab[q])
            q = q[q]
        lab[~periodic] = -1
        self.cyc_label_of_periodic = lab
        reps = np.unique(lab[periodic])
        self.cycle_reps = reps                       # minimum state of each cycle
        self.m = len(reps)
        idx = -np.ones(N, dtype=np.int64)
        idx[reps] = np.arange(self.m)
        cyc = -np.ones(N, dtype=np.int64)
        cyc[periodic] = idx[lab[periodic]]
        self.cycle_of_periodic = cyc                 # cycle index for periodic states, -1 otherwise
        self.attractor = cyc[self.FT]                # cycle index where the orbit of each state ends
        self.cycle_states = [np.flatnonzero(cyc == k) for k in range(self.m)]
        # sanity: on each cycle F is a permutation and orbit of rep covers the cycle
        for k, st in enumerate(self.cycle_states):
            x = int(reps[k]); orbit = [x]
            y = int(self.succ[x])
            while y != x:
                orbit.append(y); y = int(self.succ[y])
            assert sorted(orbit) == list(st), (rule, n, k)

    def one_flip_graph(self):
        """G1 as a set of edges (C, C'), C != C'; built from single flips of every periodic state."""
        n = self.n
        per = np.flatnonzero(self.periodic)
        src = self.cycle_of_periodic[per]
        edges = set()
        for j in range(n):
            dst = self.attractor[per ^ (1 << j)]
            sel = dst != src
            edges.update(zip(src[sel].tolist(), dst[sel].tolist()))
        return edges

    def flip_targets(self, k):
        """dict state -> list over j of the attractor index of x + e_j, for the states of cycle k."""
        out = {}
        for x in self.cycle_states[k]:
            out[int(x)] = [int(self.attractor[int(x) ^ (1 << j)]) for j in range(self.n)]
        return out

    def resistance_from_cycle(self, k):
        """R(C_k -> x) for every state x: minimum total resistance sum_t H(F u_t, u_(t+1)) of a path from a
        state of C_k to x. Computed as a BFS in which a step is either u -> F(u) (cost 0) or a single bit
        flip (cost 1); equivalent to the resistance model (a step u -> F(u) + e_S costs |S|; a chain of
        flips can always be attached to the preceding image step, and the states of C_k are images)."""
        N, n, succ = self.N, self.n, self.succ
        INF = 1 << 30
        dist = np.full(N, INF, dtype=np.int64)
        frontier = self.cycle_states[k].copy()
        dist[frontier] = 0
        level = 0
        while frontier.size:
            # forward closure at the current level
            new = frontier
            while new.size:
                nxt = np.unique(succ[new])
                nxt = nxt[dist[nxt] > level]
                dist[nxt] = level
                new = nxt
            current = np.flatnonzero(dist == level)
            level += 1
            cand = np.unique(np.concatenate([current ^ (1 << j) for j in range(n)]))
            cand = cand[dist[cand] > level]
            dist[cand] = level
            frontier = cand
        assert np.all(dist < INF)
        return dist


def walls(n, x):
    """number of walls w(x) = number of i with x_i != x_(i+1)."""
    x = np.asarray(x, dtype=np.int64)
    return popcount(x ^ rot_right_neighbour(x, n))


# ---------- minimum in-trees (Chu-Liu / Edmonds), written for this verification ----------

def min_arborescence_weight(nodes, w, root):
    """Minimum weight of a spanning out-arborescence rooted at `root` on the complete digraph with
    weights w[(u, v)] (edge u -> v). Recursive Chu-Liu/Edmonds contraction. Returns an integer."""
    nodes = list(nodes)
    if len(nodes) == 1:
        return 0
    # cheapest incoming edge for every non-root node
    inc = {}
    for v in nodes:
        if v == root:
            continue
        best = None
        for u in nodes:
            if u != v and (u, v) in w:
                if best is None or w[(u, v)] < best[1]:
                    best = (u, w[(u, v)])
        if best is None:
            raise ValueError("no arborescence")
        inc[v] = best
    # find a cycle among the chosen edges
    visited = {}
    cycle = None
    for v in nodes:
        if v == root:
            continue
        path = []
        u = v
        while u != root and u not in visited and u not in path:
            path.append(u)
            u = inc[u][0]
        if u in path:
            cycle = path[path.index(u):]
            break
        for p in path:
            visited[p] = True
    if cycle is None:
        return sum(b[1] for b in inc.values())
    cyc = set(cycle)
    cyc_w = sum(inc[v][1] for v in cycle)
    c = ("c", len(nodes), tuple(sorted(map(str, cycle))))
    new_nodes = [v for v in nodes if v not in cyc] + [c]
    nw = {}
    for (u, v), x in w.items():
        if u in cyc and v in cyc:
            continue
        if u not in nodes or v not in nodes:
            continue
        uu = c if u in cyc else u
        if v in cyc:
            val = x - inc[v][1]
            vv = c
        else:
            val = x
            vv = v
        if uu == vv:
            continue
        if (uu, vv) not in nw or val < nw[(uu, vv)]:
            nw[(uu, vv)] = val
    return cyc_w + min_arborescence_weight(new_nodes, nw, root)


def potentials(V):
    """gamma(C) for every cycle: minimum weight of an in-tree rooted at C (every other cycle has one
    out-edge, edges point towards C) with weights V[C, C']. An in-tree towards C is an out-arborescence
    from C in the reversed graph."""
    m = V.shape[0]
    w = {(b, a): int(V[a, b]) for a in range(m) for b in range(m) if a != b}   # reversed edges
    return np.array([min_arborescence_weight(range(m), w, r) for r in range(m)], dtype=np.int64)


def brute_force_potentials(V):
    """Exhaustive minimum in-trees for small m (functional graphs without cycles), for testing."""
    import itertools
    m = V.shape[0]
    res = []
    for r in range(m):
        others = [k for k in range(m) if k != r]
        best = None
        for choice in itertools.product(range(m), repeat=len(others)):
            par = dict(zip(others, choice))
            if any(par[k] == k for k in others):
                continue
            ok = True
            for k in others:
                seen = set(); u = k
                while u != r:
                    if u in seen:
                        ok = False; break
                    seen.add(u); u = par[u]
                if not ok:
                    break
            if ok:
                s = sum(int(V[k, par[k]]) for k in others)
                best = s if best is None or s < best else best
        res.append(best)
    return np.array(res)


def sccs(m, edges):
    """strongly connected components (Tarjan, iterative) and the closed ones."""
    adj = [[] for _ in range(m)]
    for a, b in edges:
        adj[a].append(b)
    index = [None] * m; low = [0] * m; onst = [False] * m; st = []; comps = []; cnt = 0
    for s in range(m):
        if index[s] is not None:
            continue
        work = [(s, 0)]
        index[s] = low[s] = cnt; cnt += 1; st.append(s); onst[s] = True
        while work:
            v, i = work[-1]
            if i < len(adj[v]):
                work[-1] = (v, i + 1)
                u = adj[v][i]
                if index[u] is None:
                    index[u] = low[u] = cnt; cnt += 1; st.append(u); onst[u] = True
                    work.append((u, 0))
                elif onst[u]:
                    low[v] = min(low[v], index[u])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        u = st.pop(); onst[u] = False; comp.append(u)
                        if u == v:
                            break
                    comps.append(sorted(comp))
    cid = {}
    for k, c in enumerate(comps):
        for v in c:
            cid[v] = k
    closed = [c for k, c in enumerate(comps) if not any(cid[b] != k for a in c for b in adj[a])]
    return comps, closed
