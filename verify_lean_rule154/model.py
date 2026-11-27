"""Literal model of the Lean definitions used by
lean/RingSize/TheoremA/StatementRotation.lean and lean/RingSize/Rule154/Statement.lean.

Written for this verification from the Lean source (Statement.lean of TheoremA, the pilot's
RingSize/Statement.lean and the two new statement files); no code of the repository is imported.

A state of the ring of n cells is a tuple x of length n with entries 0/1; cell i stands for the
element i of ZMod n, so i - 1 and i + 1 are taken mod n, and i.val = i.
"""
import heapq
import itertools


def rule_of_number(N):
    """ruleOfNumber N a b c = bit (4a + 2b + c) of N."""
    return lambda a, b, c: (N >> (4 * a + 2 * b + c)) & 1


def global_map(n, f, x):
    """globalMap n f x i = f (x (i-1)) (x i) (x (i+1))."""
    return tuple(f(x[(i - 1) % n], x[i], x[(i + 1) % n]) for i in range(n))


def rule90(n, x):
    """rule90 n x i = x (i-1) + x (i+1) in ZMod 2."""
    return tuple((x[(i - 1) % n] + x[(i + 1) % n]) % 2 for i in range(n))


def e(n, j):
    """e n j: the single 1 at cell j."""
    return tuple(1 if i == j else 0 for i in range(n))


def zero(n):
    return tuple([0] * n)


def rot(n, x):
    """rot n x i = x (i - 1)."""
    return tuple(x[(i - 1) % n] for i in range(n))


def rot_inv(n, x):
    """the other direction, x (i + 1); used only to show what the checks cannot distinguish."""
    return tuple(x[(i + 1) % n] for i in range(n))


def refl(n, x):
    """(rho x)_i = x_{-i}."""
    return tuple(x[(-i) % n] for i in range(n))


def hamming(x, y):
    return sum(a != b for a, b in zip(x, y))


def states(n):
    return list(itertools.product((0, 1), repeat=n))


def par_E(n, x):
    """parE n = {x | forall i : ZMod n, Odd i.val -> x i = 0}."""
    return all(x[i] == 0 for i in range(n) if i % 2 == 1)


def par_O(n, x):
    """parO n = {x | forall i : ZMod n, Even i.val -> x i = 0}."""
    return all(x[i] == 0 for i in range(n) if i % 2 == 0)


def iterate(g, t, x):
    for _ in range(t):
        x = g(x)
    return x


class System:
    """A map F on a finite set X with resistance r, and the objects of Part 2 of Statement.lean."""

    def __init__(self, X, F, r):
        self.X = list(X)
        self.F = F
        self.r = r
        self.Fx = {x: F(x) for x in self.X}
        self.cycles = self._cycles()
        self.m = len(self.cycles)
        self._V = None

    def orbit(self, x):
        """orbit F x = {F^[t] x | t : N}."""
        seen = []
        s = set()
        while x not in s:
            s.add(x)
            seen.append(x)
            x = self.Fx[x]
        return frozenset(seen)

    def is_periodic(self, x):
        """x in periodicPts F: F^[t] x = x for some t >= 1."""
        y = self.Fx[x]
        for _ in range(len(self.X)):
            if y == x:
                return True
            y = self.Fx[y]
        return False

    def is_cycle(self, C):
        """IsCycle F C: C = orbit F x for some periodic x."""
        C = frozenset(C)
        return any(self.is_periodic(x) and self.orbit(x) == C for x in self.X)

    def _cycles(self):
        cyc = set()
        for x in self.X:
            if self.is_periodic(x):
                cyc.add(self.orbit(x))
        return sorted(cyc, key=lambda C: (len(C), sorted(C)))

    def R(self, A, B):
        """R r A B: least pathRes of a non-empty list with head in A and last in B (Dijkstra from A)."""
        dist = {x: 0 for x in A}
        pq = [(0, x) for x in A]
        heapq.heapify(pq)
        done = set()
        while pq:
            d, x = heapq.heappop(pq)
            if x in done:
                continue
            done.add(x)
            for y in self.X:
                w = d + self.r(x, y)
                if w < dist.get(y, 10 ** 9):
                    dist[y] = w
                    heapq.heappush(pq, (w, y))
        vals = [dist[y] for y in B if y in dist]
        return min(vals) if vals else 0  # sInf of the empty set is 0

    def V(self):
        if self._V is None:
            m = self.m
            self._V = [[self.R(self.cycles[a], self.cycles[b]) for b in range(m)] for a in range(m)]
        return self._V


# ---------- Part 1 of Statement.lean: weighted graphs on nodes 0..m-1 ----------

def is_in_tree(m, c, p):
    """IsInTree c p: forall d, k >= 1, (forall j < k, p^[j] d != c) -> p^[k] d != d.
    k <= m suffices: a failure at some k gives a failure at the least period of d, which is <= m."""
    for d in range(m):
        y = d
        for k in range(1, m + 1):
            if y == c:          # p^[k-1] d = c: the hypothesis fails for this and all larger k
                break
            y = p[y]
            if y == d:
                return False
    return True


def tree_weight(V, c, p):
    return sum(V[d][p[d]] for d in range(len(V)) if d != c)


def gamma_brute(V, c):
    """gamma V c = sInf {treeWeight V c p | IsInTree c p}, over all maps p (m^m of them)."""
    m = len(V)
    best = None
    for p in itertools.product(range(m), repeat=m):
        if is_in_tree(m, c, p):
            w = tree_weight(V, c, p)
            if best is None or w < best:
                best = w
    return 0 if best is None else best


def gamma_edmonds(V, c):
    """Least weight of an in-tree rooted at c (Edmonds' algorithm on the reversed graph)."""
    import networkx as nx
    m = len(V)
    if m == 1:
        return 0
    G = nx.DiGraph()
    for a in range(m):
        for b in range(m):
            if a != b and b != c:
                # in-tree edge b -> a (b's parent is a) becomes out-arborescence edge a -> b
                G.add_edge(a, b, weight=V[b][a])
    T = nx.minimum_spanning_arborescence(G, attr="weight", default=float("inf"))
    assert all(T.in_degree(v) == 1 for v in range(m) if v != c) and T.in_degree(c) == 0
    return int(sum(d["weight"] for _, _, d in T.edges(data=True)))


def gamma_all(V, brute_max=6):
    m = len(V)
    if m <= brute_max:
        g = [gamma_brute(V, c) for c in range(m)]
        if m >= 2:
            assert g == [gamma_edmonds(V, c) for c in range(m)], "Edmonds disagrees with brute force"
        return g
    return [gamma_edmonds(V, c) for c in range(m)]


def sel(gam):
    gmin = min(gam)
    return {c for c in range(len(gam)) if gam[c] == gmin}


def G1(V):
    m = len(V)
    return {(a, b) for a in range(m) for b in range(m) if V[a][b] == 1}


def eca_system(n, N):
    f = rule_of_number(N)
    F = lambda x: global_map(n, f, x)
    Fx = {}

    def r(x, y):
        if x not in Fx:
            Fx[x] = F(x)
        return hamming(Fx[x], y)
    return System(states(n), F, r)
