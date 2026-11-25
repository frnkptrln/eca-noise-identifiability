"""Own verification library (imports nothing from code/fw or reader_checks).
Bit i of a state = cell i; code at cell i = 4 x[i-1] + 2 x[i] + x[i+1].
Boundaries: ring, null (cells -1, n are 0), one (cells -1, n are 1), reflect (cell -1 = cell 0, cell n = cell n-1)."""
import numpy as np
from numba import njit
BND = {'ring': 0, 'null': 1, 'one': 2, 'reflect': 3}

@njit(cache=True)
def _cell(x, j, n, bnd):
    if 0 <= j < n: return (x >> j) & 1
    if bnd == 0: return (x >> ((j + n) % n)) & 1
    if bnd == 1: return 0
    if bnd == 2: return 1
    if j < 0: return x & 1
    return (x >> (n - 1)) & 1

@njit(cache=True)
def _build(rule, n, bnd):
    N = 1 << n
    succ = np.empty(N, np.int64); mask = np.empty(N, np.int64)
    for x in range(N):
        y = 0; mk = 0
        for i in range(n):
            c = 4 * _cell(x, i - 1, n, bnd) + 2 * _cell(x, i, n, bnd) + _cell(x, i + 1, n, bnd)
            mk |= 1 << c
            if (rule >> c) & 1: y |= 1 << i
        succ[x] = y; mask[x] = mk
    return succ, mask

@njit(cache=True)
def _cycles(succ):
    N = succ.shape[0]
    mark = -np.ones(N, np.int64); cyc = -np.ones(N, np.int64); per = np.zeros(N, np.uint8)
    m = 0
    for s in range(N):
        if mark[s] != -1: continue
        x = s
        while mark[x] == -1:
            mark[x] = s; x = succ[x]
        if mark[x] == s and cyc[x] == -1:
            cid = m; m += 1; z = x
            while True:
                cyc[z] = cid; per[z] = 1; z = succ[z]
                if z == x: break
        else:
            cid = cyc[x]
        x = s
        while cyc[x] == -1:
            cyc[x] = cid; x = succ[x]
    return m, cyc, per

@njit(cache=True)
def _g1(n, cyc, per):
    N = cyc.shape[0]; k = 0
    out = np.empty((int(per.sum()) * n + 1, 2), np.int64)
    for x in range(N):
        if per[x]:
            for i in range(n):
                a = cyc[x]; b = cyc[x ^ (1 << i)]
                if a != b:
                    out[k, 0] = a; out[k, 1] = b; k += 1
    return out[:k]

@njit(cache=True)
def _resist(n, m, succ, mask, cyc, per):
    """0-1 BFS from each cycle: edges y -> succ[y] (cost 0) and y -> y ^ e_i (cost 1)."""
    N = succ.shape[0]
    V = np.full((m, m), 32767, np.int64); R = np.full((m, 8), 32767, np.int64)
    dist = np.empty(N, np.int64)
    cap = 2 * N * (n + 1) + 8
    dq = np.empty(cap, np.int64)
    cnt = np.zeros(m + 1, np.int64)
    for x in range(N):
        if per[x]: cnt[cyc[x] + 1] += 1
    for c in range(m): cnt[c + 1] += cnt[c]
    lst = np.empty(cnt[m], np.int64); pos = cnt[:m].copy()
    for x in range(N):
        if per[x]:
            lst[pos[cyc[x]]] = x; pos[cyc[x]] += 1
    for c in range(m):
        dist[:] = 1 << 30
        head = cap // 2; tail = cap // 2
        for k in range(cnt[c], cnt[c + 1]):
            x = lst[k]; dist[x] = 0; dq[tail] = x; tail += 1
        while head < tail:
            y = dq[head]; head += 1; d = dist[y]
            z = succ[y]
            if dist[z] > d:
                dist[z] = d; head -= 1; dq[head] = z
            for i in range(n):
                w = y ^ (1 << i)
                if dist[w] > d + 1:
                    dist[w] = d + 1; dq[tail] = w; tail += 1
        for x in range(N):
            dx = dist[x]
            if per[x] and dx < V[c, cyc[x]]: V[c, cyc[x]] = dx
            mk = mask[x]
            for q in range(8):
                if (mk >> q) & 1 and dx < R[c, q]: R[c, q] = dx
    return V, R

def refl_rule(r):
    return sum(((r >> c) & 1) << (((c & 1) << 2) | (c & 2) | (c >> 2)) for c in range(8))
def comp_rule(r):
    return sum((1 - ((r >> (7 - c)) & 1)) << c for c in range(8))

class Sys:
    def __init__(self, rule, n, bnd='null'):
        self.rule, self.n, self.bnd = rule, n, bnd
        self.succ, self.mask = _build(rule, n, BND[bnd])
        self.m, self.cyc, self.per = _cycles(self.succ)
        self.bijective = bool(self.per.all())
        cm = np.zeros(self.m, np.int64)
        np.bitwise_or.at(cm, self.cyc[self.per == 1], self.mask[self.per == 1])
        self.cycle_mask = cm                       # codes carried by the states of each cycle
        self.union_mask = int(np.bitwise_or.reduce(cm))
    def g1(self):
        e = _g1(self.n, self.cyc, self.per)
        return np.unique(e, axis=0) if len(e) else e
    def closed_classes(self):
        import scipy.sparse as sp
        from scipy.sparse.csgraph import connected_components
        e = self.g1(); m = self.m
        A = sp.csr_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(m, m))
        nc, lab = connected_components(A, directed=True, connection='strong')
        leaves = np.ones(nc, bool)
        if len(e):
            cross = lab[e[:, 0]] != lab[e[:, 1]]
            leaves[np.unique(lab[e[cross, 0]])] = False
        return [np.flatnonzero(lab == c) for c in np.flatnonzero(leaves)]
    def resist(self):
        V, R = _resist(self.n, self.m, self.succ, self.mask, self.cyc, self.per)
        np.fill_diagonal(V, 0)
        return V, R

def gammas(V):
    """Root-free Edmonds contraction. A[u,v] = cost of u having out-edge to v (in-tree).
    Returns gamma[r] = min weight of an in-tree rooted at r, for every r."""
    m = V.shape[0]
    if m == 1: return np.zeros(1, np.int64)
    INF = 1 << 40
    A = V.astype(np.int64).copy(); np.fill_diagonal(A, INF)
    groups = [[i] for i in range(m)]          # members of current supernodes
    contain = np.zeros(m, np.int64); Y = 0    # sum of y over sets containing node; total
    while len(groups) > 1:
        k = len(groups)
        y = A.min(axis=1); par = A.argmin(axis=1)
        A = A - y[:, None]; np.fill_diagonal(A, INF)
        Y += int(y.sum())
        for g, yy in zip(groups, y): contain[g] += int(yy)
        # cycles of the functional graph u -> par[u]
        state = np.zeros(k, np.int8); lab = -np.ones(k, np.int64); ncyc = 0
        for s in range(k):
            if state[s]: continue
            path = []; u = s
            while state[u] == 0:
                state[u] = 1; path.append(u); u = par[u]
            if state[u] == 1:  # cycle closes in this path
                i = path.index(u)
                for w in path[i:]: lab[w] = ncyc
                ncyc += 1
            for w in path: state[w] = 2
        # new labels: each cycle -> one node, others singletons
        new = -np.ones(k, np.int64); nxt = ncyc
        for u in range(k):
            if lab[u] >= 0: new[u] = lab[u]
            else: new[u] = nxt; nxt += 1
        K = nxt
        order = np.argsort(new, kind='stable'); starts = np.searchsorted(new[order], np.arange(K))
        B = np.minimum.reduceat(A[order], starts, axis=0)
        B = np.minimum.reduceat(B[:, order], starts, axis=1)
        np.fill_diagonal(B, INF)
        ng = [[] for _ in range(K)]
        for u in range(k): ng[new[u]].extend(groups[u])
        groups, A = ng, B
    return Y - contain

def solve(rule, n, bnd='null', cap=None):
    """Full exact solution: m, gamma, selected set, k_c, k*. cap: skip potentials if m > cap."""
    s = Sys(rule, n, bnd)
    out = dict(rule=rule, n=n, bnd=bnd, m=s.m, bij=s.bijective, union=s.union_mask)
    if s.bijective:
        out.update(kstar=0 if s.union_mask == 255 else None, exact=False); return s, out
    if cap is not None and s.m > cap:
        out.update(exact=False); return s, out
    V, R = s.resist()
    g = gammas(V); gmin = g.min()
    sel = np.flatnonzero(g == gmin)
    kc = (g[:, None] + R).min(axis=0) - gmin
    cover = int(np.bitwise_or.reduce(s.cycle_mask[sel]))
    out.update(exact=True, gmin=int(gmin), nsel=len(sel), sel=sel, kc=kc, kstar=int(kc.max()), cover=cover, gamma=g, V=V, R=R)
    return s, out
