"""Literal Python model of the definitions in lean/RingSize/TheoremA/Statement.lean.

Written independently of the code in the repository (no import from it). Each function names
the Lean definition it models. Conventions of Lean/Mathlib that matter here are reproduced:
  * sInf of an empty set of natural numbers is 0 (Nat.sInf_empty);
  * natural-number subtraction truncates at 0;
  * Finset.sup over an empty set in N is 0.
States are tuples of bits (x_0, ..., x_{n-1}); cell indices are taken mod n (ZMod n).
"""
from itertools import product
import heapq


def sInf_nat(values):
    """Mathlib `sInf : Set ℕ → ℕ`: the least element, and 0 for the empty set."""
    values = list(values)
    return min(values) if values else 0


def nat_sub(a, b):
    """Subtraction in ℕ (truncated)."""
    return max(a - b, 0)


# ---------------------------------------------------------------- Part 3: ECA
def rule_of_number(N):
    """ruleOfNumber N a b c = if N.testBit (4a + 2b + c) then 1 else 0."""
    return lambda a, b, c: (N >> (4 * a + 2 * b + c)) & 1


def states(n):
    return list(product((0, 1), repeat=n))


def global_map(n, f):
    """globalMap n f x i = f (x (i-1)) (x i) (x (i+1)), indices in ZMod n."""
    def F(x):
        return tuple(f(x[(i - 1) % n], x[i], x[(i + 1) % n]) for i in range(n))
    return F


def hamming(x, y):
    return sum(a != b for a, b in zip(x, y))


def resistance(n, f):
    """resistance n f x y = hammingDist (globalMap n f x) y."""
    F = global_map(n, f)
    return lambda x, y: hamming(F(x), y)


def contains(n, x, v):
    """Contains n x v: ∃ i, (x (i-1), x i, x (i+1)) = v."""
    return any((x[(i - 1) % n], x[i], x[(i + 1) % n]) == v for i in range(n))


def D(n, v):
    return {x for x in states(n) if contains(n, x, v)}


def e(n, j):
    return tuple(1 if i == j else 0 for i in range(n))


def flip(n, x, j):
    """flip n x j = x + e n j (addition in ZMod 2)."""
    return tuple((a + b) % 2 for a, b in zip(x, e(n, j)))


CODES = list(product((0, 1), repeat=3))   # Code = ZMod 2 × ZMod 2 × ZMod 2


# ------------------------------------------------------------ Part 2: dynamics
def iterate(F, t, x):
    for _ in range(t):
        x = F(x)
    return x


def periodic_pts(X, F):
    """Function.periodicPts F = {x | ∃ t > 0, F^[t] x = x}. For |X| states a period is at most |X|."""
    out = set()
    for x in X:
        y = x
        for _ in range(len(X)):
            y = F(y)
            if y == x:
                out.add(x)
                break
    return out


def orbit(F, x, size):
    """orbit F x = {F^[t] x | t : ℕ}; size bounds the length of the orbit."""
    o, y = set(), x
    for _ in range(size + 1):
        o.add(y)
        y = F(y)
    return frozenset(o)


def cycles(X, F):
    """Cyc F: the sets C with ∃ x ∈ periodicPts F, C = orbit F x (as a set of sets, so no duplicates)."""
    return sorted({orbit(F, x, len(X)) for x in periodic_pts(X, F)}, key=lambda C: sorted(C))


def ends_on(F, x, C, size):
    """EndsOn F x C: ∃ t, F^[t] x ∈ C. Bounded by size steps, which suffices on a finite set."""
    y = x
    for _ in range(size + 1):
        if y in C:
            return True
        y = F(y)
    return False


def R_dijkstra(X, r, A, B):
    """R r A B = sInf {pathRes r l | l ≠ [], head l ∈ A, getLast l ∈ B}.
    Paths may have length 0 (a single state). Computed by multi-source Dijkstra on the complete
    digraph with weights r x y; sInf ∅ = 0 when A or B is empty."""
    if not A or not B:
        return 0
    dist = {x: float('inf') for x in X}
    pq = []
    for a in A:
        dist[a] = 0
        heapq.heappush(pq, (0, a))
    while pq:
        d, x = heapq.heappop(pq)
        if d > dist[x]:
            continue
        for y in X:
            nd = d + r(x, y)
            if nd < dist[y]:
                dist[y] = nd
                heapq.heappush(pq, (nd, y))
    return min(dist[b] for b in B)


def all_pairs_floyd(X, r):
    """Second, independent method: Floyd–Warshall over states, distance 0 on the diagonal (length-0 path)."""
    idx = {x: i for i, x in enumerate(X)}
    m = len(X)
    d = [[0 if i == j else r(X[i], X[j]) for j in range(m)] for i in range(m)]
    for k in range(m):
        dk = d[k]
        for i in range(m):
            dik = d[i][k]
            di = d[i]
            for j in range(m):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return idx, d


# ---------------------------------------------------------- Part 1: graphs
def is_in_tree(nodes, c, p):
    """IsInTree c p: ∀ d k, 0 < k → (∀ j < k, p^[j] d ≠ c) → p^[k] d ≠ d.
    p is a dict node -> node. Checking k ≤ |nodes| is exact: if p^[k] d = d with the avoidance
    condition for some k, the least such k is the length of a circuit, at most |nodes|, and the
    avoidance condition for it is implied."""
    m = len(nodes)
    for d in nodes:
        y = d
        for k in range(1, m + 1):
            if y == c:          # p^[k-1] d = c: the hypothesis fails for this k and all larger k
                break
            y = p[y]
            if y == d:
                return False
    return True


def tree_weight(nodes, V, c, p):
    """treeWeight V c p = Σ_{d ≠ c} V d (p d)."""
    return sum(V[d][p[d]] for d in nodes if d != c)


def gamma_bruteforce(nodes, V, c):
    """gamma V c = sInf {treeWeight V c p | IsInTree c p}, enumerating all parent maps.
    p c does not enter IsInTree or treeWeight, so p c = c is fixed and the other values range over all nodes."""
    others = [d for d in nodes if d != c]
    best = []
    for vals in product(nodes, repeat=len(others)):
        p = dict(zip(others, vals))
        p[c] = c
        if is_in_tree(nodes, c, p):
            best.append(tree_weight(nodes, V, c, p))
    return sInf_nat(best)


def gamma_edmonds(nodes, V, c):
    """Independent method: minimum spanning arborescence (Chu–Liu/Edmonds, networkx).
    An in-tree towards c is an arborescence out of c in the reversed graph."""
    import networkx as nx
    if len(nodes) == 1:
        return 0
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    for a in nodes:
        for b in nodes:
            if a != b and a != c:          # edge a -> b of the in-tree; reversed: b -> a
                G.add_edge(b, a, weight=V[a][b])
    T = nx.minimum_spanning_arborescence(G, attr='weight', preserve_attrs=True)
    assert [u for u in T.nodes if T.in_degree(u) == 0] == [c]
    return int(sum(dd['weight'] for _, _, dd in T.edges(data=True)))


def reach_matrix(nodes, G1):
    """Reach = ReflTransGen G1 (transitive closure, reflexive)."""
    reach = {a: {a} for a in nodes}
    changed = True
    while changed:
        changed = False
        for a in nodes:
            new = set(reach[a])
            for b in reach[a]:
                new |= {c for c in nodes if G1(b, c)}
            if new != reach[a]:
                reach[a] = new
                changed = True
    return reach


def is_closed_class(nodes, G1, reach, K):
    """IsClosedClass V K: K nonempty ∧ ∀ a b ∈ K, Reach a b ∧ ∀ a ∈ K, ∀ b, G1 a b → b ∈ K."""
    if not K:
        return False
    if any(b not in reach[a] for a in K for b in K):
        return False
    return all(b in K for a in K for b in nodes if G1(a, b))


def closed_classes_by_subsets(nodes, G1, reach):
    """All K with IsClosedClass, by enumeration of all subsets (literal; use for small node sets)."""
    out = []
    m = len(nodes)
    for mask in range(1, 1 << m):
        K = frozenset(nodes[i] for i in range(m) if mask >> i & 1)
        if is_closed_class(nodes, G1, reach, K):
            out.append(K)
    return out


def closed_classes_by_scc(nodes, G1, reach):
    """Paper, 2.4: strongly connected components of G1 that no edge of G1 leaves."""
    comps = {frozenset(b for b in nodes if b in reach[a] and a in reach[b]) for a in nodes}
    return [K for K in comps if all(b in K for a in K for b in nodes if G1(a, b))]
