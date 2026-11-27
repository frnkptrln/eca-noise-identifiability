"""Literal Python model of the Lean definitions used by lean/RingSize/Rule154/StatementMain.lean.

Written for this verification only; it uses no code from the repository.

Conventions copied from the Lean files:
  * RingSize/Statement.lean: a state is a map ZMod n -> ZMod 2.  Here a state is an int whose bit i is the value
    of the cell i (i = i.val in {0, ..., n-1}).  e n j = 1 << j.
  * TheoremA/Statement.lean:
      ruleOfNumber N a b c = testBit N (4a + 2b + c);  globalMap: (F x)_i = f(x_{i-1}, x_i, x_{i+1}).
      resistance x y = hammingDist (F x) y.
      pathRes over a list = sum of the resistances of its steps; R A B = sInf of pathRes over all non-empty
      lists from A to B (a list of length 1 counts; sInf of the empty set is 0).
      IsCycle C: C is the orbit of a periodic point (F^t x = x for some t >= 1).
      VE = Vc = R between the state sets of two cycles.  G1 a b <-> V a b = 1.  Reach = ReflTransGen G1.
      IsInTree c p: for all d, k > 0: (for all j < k, p^[j] d != c) -> p^[k] d != d.
      treeWeight c p = sum over d != c of V d (p d).  gamma c = sInf of the weights of in-trees rooted at c.
      gammaMin = sInf of the range of gamma.  Sel = {c | gamma c = gammaMin}.
      IsClosedClass K: K non-empty, any a, b in K satisfy Reach a b, and every G1 edge out of K ends in K.
      Contains x v: some cell i with (x_{i-1}, x_i, x_{i+1}) = v.  D v = states that contain v.
      kIndex v = sInf {gamma C + R C (D v)} - gammaMin  (natural subtraction).  kStar = max over the 8 codes.
      numCycles = number of cycles.
  * Rule154/Statement.lean: parE = states that are 0 on every cell i with i.val odd; parO = 0 on every cell with
    i.val even.  StatementMain.lean: parM = complement of parE u parO.  IsPowTwo n <-> exists k, n = 2^k.

R is computed exactly by a 0-1 breadth-first search on a two-layer graph: from a state x (layer 0) one goes to
F x in layer 1 at cost 0; in layer 1 one may flip one cell at cost 1; from layer 1 one returns to layer 0 at cost
0.  A list x_0, ..., x_T of resistance sum_s H(F x_s, x_{s+1}) is exactly such a walk, and the cheapest walk
between two layer-0 states realises the cheapest list.  `R_direct` (Dijkstra on the complete graph of steps) is
kept to check this on small rings.
"""
from collections import deque
from itertools import product
import heapq

CODES = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]  # order 4a + 2b + c


def code_str(v):
    return "".join(map(str, v))


def rule_of_number(N):
    return lambda a, b, c: (N >> (4 * a + 2 * b + c)) & 1


def bit(x, i, n):
    return (x >> (i % n)) & 1


def global_map(n, N):
    f = rule_of_number(N)
    F = []
    for x in range(1 << n):
        y = 0
        for i in range(n):
            if f(bit(x, i - 1, n), bit(x, i, n), bit(x, i + 1, n)):
                y |= 1 << i
        F.append(y)
    return F


def F154(n):
    return global_map(n, 154)


def e(n, j):
    return 1 << (j % n)


def in_parE(x, n):
    return all(bit(x, i, n) == 0 for i in range(n) if i % 2 == 1)


def in_parO(x, n):
    return all(bit(x, i, n) == 0 for i in range(n) if i % 2 == 0)


def in_parM(x, n):
    return not (in_parE(x, n) or in_parO(x, n))


def is_pow_two(n):
    return n >= 1 and (n & (n - 1)) == 0


def one(n):
    return (1 << n) - 1


def oneE(n):
    return sum(1 << i for i in range(0, n, 2))


def oneO(n):
    return sum(1 << i for i in range(1, n, 2))


def contains(x, v, n):
    return any((bit(x, i - 1, n), bit(x, i, n), bit(x, i + 1, n)) == v for i in range(n))


def popcount(x):
    return bin(x).count("1")


def periodic_points(F):
    """x with F^t x = x for some t >= 1 (Mathlib periodicPts)."""
    N = len(F)
    per = []
    for x in range(N):
        y = F[x]
        for _ in range(N):
            if y == x:
                per.append(x)
                break
            y = F[y]
    return per


def cycles(F):
    """Cycles as frozensets: orbits of periodic points (IsCycle).  Sorted by least element."""
    per = periodic_points(F)
    seen, out = set(), []
    for x in per:
        if x in seen:
            continue
        orb, y = {x}, F[x]
        while y != x:
            orb.add(y)
            y = F[y]
        seen |= orb
        out.append(frozenset(orb))
    out.sort(key=min)
    return out


def dist_from(F, n, A):
    """dist[y] = R(A -> {y}) for every state y (0-1 BFS on the two-layer graph)."""
    N = 1 << n
    INF = 10 ** 9
    d0 = [INF] * N
    d1 = [INF] * N
    dq = deque()
    for x in A:
        d0[x] = 0
        dq.appendleft((0, x))
    while dq:
        layer, z = dq.popleft()
        d = d0[z] if layer == 0 else d1[z]
        if layer == 0:
            w = F[z]
            if d < d1[w]:
                d1[w] = d
                dq.appendleft((1, w))
        else:
            if d < d0[z]:
                d0[z] = d
                dq.appendleft((0, z))
            for j in range(n):
                w = z ^ (1 << j)
                if d + 1 < d1[w]:
                    d1[w] = d + 1
                    dq.append((1, w))
    return d0


def R_direct(F, n, A, B):
    """R(A -> B) by Dijkstra on the complete graph of steps x -> y with weight H(F x, y)."""
    N = 1 << n
    dist = {x: 0 for x in A}
    pq = [(0, x) for x in A]
    heapq.heapify(pq)
    done = set()
    while pq:
        d, x = heapq.heappop(pq)
        if x in done:
            continue
        done.add(x)
        if x in B:
            return d
        for y in range(N):
            w = d + popcount(F[x] ^ y)
            if w < dist.get(y, 10 ** 9):
                dist[y] = w
                heapq.heappush(pq, (w, y))
    return 0  # sInf of the empty set


class Model:
    """All quantities of Section 2 for rule N on n cells, computed from the definitions."""

    def __init__(self, n, N=154, need_gamma=True, fast_gamma=False):
        """fast_gamma: for a root that every cycle reaches in G1, take the breadth-first G1 tree (weight m - 1,
        equal to the lower bound, so optimal) instead of running Edmonds' algorithm."""
        self.n, self.N = n, N
        self.fast_gamma = fast_gamma
        self.F = global_map(n, N)
        self.cyc = cycles(self.F)
        self.m = len(self.cyc)
        self.idx = {}
        for k, C in enumerate(self.cyc):
            for x in C:
                self.idx[x] = k
        self.dist = [dist_from(self.F, n, C) for C in self.cyc]
        self.V = [[min(self.dist[a][x] for x in self.cyc[b]) for b in range(self.m)] for a in range(self.m)]
        self.G1 = [[self.V[a][b] == 1 for b in range(self.m)] for a in range(self.m)]
        self.reach = self._reach()
        if need_gamma:
            self.gamma, self.gamma_cert = self._gammas()
            self.gmin = min(self.gamma)
            self.Sel = [c for c in range(self.m) if self.gamma[c] == self.gmin]
            self.k = {}
            for v in CODES:
                Dv = [x for x in range(1 << n) if contains(x, v, n)]
                RD = [min((self.dist[c][x] for x in Dv), default=0) for c in range(self.m)]
                self.k[v] = min(self.gamma[c] + RD[c] for c in range(self.m)) - self.gmin
                assert self.k[v] >= 0
            self.kstar = max(self.k.values())

    def _reach(self):
        m = self.m
        R = []
        for a in range(m):
            seen = {a}
            st = [a]
            while st:
                u = st.pop()
                for w in range(m):
                    if self.G1[u][w] and w not in seen:
                        seen.add(w)
                        st.append(w)
            R.append(seen)
        return R

    def closed_classes(self):
        """All K with IsClosedClass K.  Such a K is closed under G1 edges, so it contains Reach(a) for each of
        its elements a, and mutual reachability forces K = Reach(a).  So the candidates are the sets Reach(a);
        each is tested against the three clauses of the definition."""
        out = set()
        for a in range(self.m):
            K = frozenset(self.reach[a])
            ok = all(b in self.reach[c] for c in K for b in K) and all(
                w in K for c in K for w in range(self.m) if self.G1[c][w])
            if ok:
                out.add(K)
        return out

    def is_in_tree(self, c, p):
        m = self.m
        for d in range(m):
            y = d
            hit_root = (y == c)
            for k in range(1, m + 2):
                if hit_root:
                    break
                y = p[y]
                if y == d:
                    return False
                if y == c:
                    hit_root = True
        return True

    def tree_weight(self, c, p):
        return sum(self.V[d][p[d]] for d in range(self.m) if d != c)

    def _gammas(self):
        """gamma(c) for every c.  An optimal tree is found by Edmonds' algorithm (networkx); the tree is
        checked with the literal IsInTree, and its weight is compared with the lower bound
        sum_{d != c} min_{e != d} V(d, e), valid for every in-tree.  'cert' is True when the two agree,
        i.e. the value is proved optimal without relying on Edmonds.  For m <= 6 all parent maps are also
        enumerated."""
        import networkx as nx
        m = self.m
        g, cert = [], []
        minout = [min((self.V[d][e2] for e2 in range(m) if e2 != d), default=0) for d in range(m)]
        for c in range(m):
            if m == 1:
                g.append(0)
                cert.append(True)
                continue
            if self.fast_gamma and all(c in self.reach[d] for d in range(m)):
                # a breadth-first in-tree of G1 edges towards c: weight m - 1 = the lower bound
                p = list(range(m))
                seen, frontier = {c}, [c]
                while frontier:
                    nxt = []
                    for u in frontier:
                        for d in range(m):
                            if d not in seen and self.G1[d][u]:
                                p[d] = u
                                seen.add(d)
                                nxt.append(d)
                    frontier = nxt
                assert self.is_in_tree(c, p)
                w = self.tree_weight(c, p)
                lb = sum(minout[d] for d in range(m) if d != c)
                assert w == lb == m - 1
                g.append(w)
                cert.append(True)
                continue
            G = nx.DiGraph()
            G.add_nodes_from(range(m))
            for d in range(m):
                if d == c:
                    continue
                for q in range(m):
                    if q != d:
                        G.add_edge(q, d, weight=self.V[d][q])  # arborescence edge q -> d = in-tree edge d -> q
            A = nx.minimum_spanning_arborescence(G, attr="weight")
            p = list(range(m))
            for q, d in A.edges():
                p[d] = q
            assert self.is_in_tree(c, p)
            w = self.tree_weight(c, p)
            lb = sum(minout[d] for d in range(m) if d != c)
            g.append(w)
            cert.append(w == lb)
        if m <= 6:
            for c in range(m):
                best = min(self.tree_weight(c, p) for p in product(range(m), repeat=m) if self.is_in_tree(c, list(p)))
                assert best == g[c], (self.n, c, best, g[c])
        return g, cert

    def zero_index(self):
        return self.idx.get(0)
