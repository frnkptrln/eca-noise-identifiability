"""Tools for elementary cellular automata on rings (NumPy and plain Python integers; written from the definitions
for proofs_43_142/).

Conventions: a state x of the ring Z/nZ is stored as an integer with cell i at bit i (the convention of
data/ring_size/sampled_reach/); f(a, b, c) = bit (4a + 2b + c) of the rule number;
(F x)_i = f(x_(i-1), x_i, x_(i+1)), indices mod n. The wall word of x is d = delta(x), d_i = x_i XOR x_(i+1)
("a wall between the cells i and i+1"). The wall count w(x) is the number of ones of delta(x).
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


# ----------------------------------------------------------------------------- single states (any n)
def rot_up(x, n, k=1):
    """y_i = x_(i-k): the pattern moves k cells to the right (towards larger indices)."""
    k %= n
    return ((x << k) | (x >> (n - k))) & ((1 << n) - 1) if k else x


def rot_down(x, n, k=1):
    """y_i = x_(i+k): the pattern moves k cells to the left."""
    return rot_up(x, n, n - (k % n))


def step(rule, x, n):
    """One step of the rule on a single state (Python integer, any n >= 3)."""
    mask = (1 << n) - 1
    a = rot_up(x, n)      # a_i = x_(i-1)
    c = rot_down(x, n)    # c_i = x_(i+1)
    y = 0
    for code in range(8):
        if (rule >> code) & 1:
            A = a if code & 4 else ~a
            B = x if code & 2 else ~x
            C = c if code & 1 else ~c
            y |= A & B & C
    return y & mask


def delta(x, n):
    """Wall word: d_i = x_i XOR x_(i+1)."""
    return x ^ rot_down(x, n)


def comp(x, n):
    return x ^ ((1 << n) - 1)


def popcount(x):
    return bin(x).count("1")


def wall_count(x, n):
    return popcount(delta(x, n))


def from_string(s):
    """'0011' -> state with cell i = s[i]."""
    return sum(1 << i for i, ch in enumerate(s) if ch == "1")


def to_string(x, n):
    return "".join("1" if (x >> i) & 1 else "0" for i in range(n))


def codes_of(x, n):
    """Set of neighbourhood codes 4 x_(i-1) + 2 x_i + x_(i+1) occurring in x."""
    mask = (1 << n) - 1
    a = rot_up(x, n)      # a_i = x_(i-1)
    c = rot_down(x, n)    # c_i = x_(i+1)
    out = set()
    for code in range(8):
        A = a if code & 4 else ~a
        B = x if code & 2 else ~x
        C = c if code & 1 else ~c
        if A & B & C & mask:
            out.add(code)
    return out


def count_pattern(d, n, pat):
    """Number of cells i with (d_i, ..., d_(i+len-1)) = pat (string), cyclically."""
    L = len(pat)
    return sum(all(((d >> ((i + k) % n)) & 1) == int(pat[k]) for k in range(L)) for i in range(n))


def positions(d, n, pat):
    """Set of cells i with (d_i, ..., d_(i+len-1)) = pat, cyclically."""
    L = len(pat)
    return {i for i in range(n) if all(((d >> ((i + k) % n)) & 1) == int(pat[k]) for k in range(L))}


def limit_cycle(rule, x, n, cap=10 ** 7):
    """The cycle the orbit of x ends on, as a list of states in time order, and the transient length (Brent)."""
    power = lam = 1
    t = x
    h = step(rule, x, n)
    steps = 0
    while t != h:
        if power == lam:
            t = h
            power *= 2
            lam = 0
        h = step(rule, h, n)
        lam += 1
        steps += 1
        if steps > cap:
            raise RuntimeError("no cycle found within cap")
    t = h = x
    for _ in range(lam):
        h = step(rule, h, n)
    mu = 0
    while t != h:
        t = step(rule, t, n)
        h = step(rule, h, n)
        mu += 1
    cyc = [t]
    y = step(rule, t, n)
    while y != t:
        cyc.append(y)
        y = step(rule, y, n)
    return cyc, mu


# ----------------------------------------------------------------------------- all states (small n)
def _rot_up_arr(x, n):
    return ((x << np.uint32(1)) | (x >> np.uint32(n - 1))) & np.uint32((1 << n) - 1)


def _rot_down_arr(x, n):
    return (x >> np.uint32(1)) | ((x & np.uint32(1)) << np.uint32(n - 1))


def build_F(rule, n):
    """Table of F on all 2^n states (uint32)."""
    N = 1 << n
    x = np.arange(N, dtype=np.uint32)
    mask = np.uint32(N - 1)
    a = _rot_up_arr(x, n)
    c = _rot_down_arr(x, n)
    F = np.zeros(N, np.uint32)
    for code in range(8):
        if (rule >> code) & 1:
            A = a if code & 4 else ~a
            B = x if code & 2 else ~x
            C = c if code & 1 else ~c
            F |= A & B & C
    return F & mask


def delta_arr(n):
    x = np.arange(1 << n, dtype=np.uint32)
    return x ^ _rot_down_arr(x, n)


def popcount_arr(v):
    v = v.astype(np.uint64)
    out = np.zeros(v.shape, np.int64)
    while True:
        nz = v != 0
        if not nz.any():
            break
        out += (v & np.uint64(1)).astype(np.int64)
        v = v >> np.uint64(1)
    return out


def periodic_mask(F, n):
    """Boolean array: state lies on a cycle. Also returns G = F^(2^(n+1)) (maps every state onto its cycle)."""
    G = F.copy()
    for _ in range(n + 1):
        G = G[G]
    on = np.zeros(len(F), bool)
    on[G] = True
    return on, G


def analyse(rule, n):
    """F, G, on (periodic states), cid (cycle index of a periodic state, -1 otherwise), label (index of the cycle
    the orbit of a state ends on), cycles (list of lists of states in time order)."""
    F = build_F(rule, n)
    on, G = periodic_mask(F, n)
    cid = np.full(len(F), -1, np.int64)
    cycles = []
    st = np.flatnonzero(on)
    nxt = dict(zip(st.tolist(), F[st].tolist()))      # F restricted to the periodic states
    for s in st.tolist():
        if cid[s] >= 0:
            continue
        k = len(cycles)
        orb = [s]
        cid[s] = k
        y = nxt[s]
        while y != s:
            cid[y] = k
            orb.append(y)
            y = nxt[y]
        cycles.append(orb)
    label = cid[G]
    return dict(rule=rule, n=n, F=F, G=G, on=on, cid=cid, label=label, cycles=cycles)


def g1_edges(A):
    """Edge set of the one-flip graph G1 as an array of pairs (C, C'), C != C'."""
    n = A["n"]
    st = np.flatnonzero(A["on"])
    src = A["cid"][st]
    m = len(A["cycles"])
    keys = []
    for i in range(n):
        dst = A["label"][st ^ (1 << i)]
        keep = dst != src
        keys.append(np.unique(src[keep] * m + dst[keep]))
    keys = np.unique(np.concatenate(keys)) if keys else np.zeros(0, np.int64)
    return np.stack([keys // m, keys % m], axis=1)


def closed_classes(m, E):
    """Strongly connected components of ([0, m), E) without leaving edge. Returns (number of components,
    component label per node, list of closed classes as sorted lists of nodes)."""
    if len(E):
        M = csr_matrix((np.ones(len(E), np.int8), (E[:, 0], E[:, 1])), shape=(m, m))
    else:
        M = csr_matrix((m, m), dtype=np.int8)
    nc, comp_ = connected_components(M, directed=True, connection="strong")
    leaving = np.zeros(nc, bool)
    if len(E):
        cu, cv = comp_[E[:, 0]], comp_[E[:, 1]]
        leaving[cu[cu != cv]] = True
    closed = [np.flatnonzero(comp_ == k).tolist() for k in np.flatnonzero(~leaving)]
    return nc, comp_, closed


def reaches(m, E, targets):
    """Boolean array: node has a directed path (length >= 0) into the set targets."""
    radj = [[] for _ in range(m)]
    for u, v in E.tolist():
        radj[v].append(u)
    seen = np.zeros(m, bool)
    stack = list(targets)
    for t in stack:
        seen[t] = True
    while stack:
        v = stack.pop()
        for u in radj[v]:
            if not seen[u]:
                seen[u] = True
                stack.append(u)
    return seen
