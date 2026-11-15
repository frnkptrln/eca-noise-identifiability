"""Small-n tools for elementary CA on rings (pure NumPy, written from the definitions).

Conventions as in verify_ring_size/SAMPLE.md section 2: a state is the bit string x_0 ... x_(n-1) read as a
binary numeral (x_0 most significant); f(a,b,c) = bit (4a+2b+c) of the rule number;
(F x)_i = f(x_(i-1), x_i, x_(i+1)) with indices mod n.
"""
import numpy as np


def bits(x, n):
    return format(int(x), "0%db" % n)


def build_F(rule, n):
    N = 1 << n
    x = np.arange(N, dtype=np.uint32)
    mask = np.uint32(N - 1)
    # a_i = x_(i-1): string rotated right; c_i = x_(i+1): string rotated left
    a = (x >> np.uint32(1)) | ((x & np.uint32(1)) << np.uint32(n - 1))
    c = ((x << np.uint32(1)) & mask) | (x >> np.uint32(n - 1))
    F = np.zeros(N, np.uint32)
    for code in range(8):
        if (rule >> code) & 1:
            A = a if code & 4 else ~a
            B = x if code & 2 else ~x
            Cc = c if code & 1 else ~c
            F |= A & B & Cc
    return F & mask


def step_str(s, rule=94):
    n = len(s)
    return "".join(str((rule >> (4 * int(s[i - 1]) + 2 * int(s[i]) + int(s[(i + 1) % n]))) & 1) for i in range(n))


def analyse(rule, n):
    """Returns dict with F, G (= F^K, K >= 2^n so G maps every state onto its cycle), cyc_state (bool),
    label (state -> index of the cycle its orbit ends on), cycles (list of arrays of states in time order),
    minstate (per cycle)."""
    F = build_F(rule, n)
    N = 1 << n
    G = F.copy()
    for _ in range(n + 1):          # G = F^(2^(n+1)); transients are shorter than 2^n
        G = G[G]
    on = np.zeros(N, bool)
    on[G] = True
    cid = np.full(N, -1, np.int64)
    cycles = []
    for s in np.flatnonzero(on):
        if cid[s] >= 0:
            continue
        k = len(cycles)
        orb = [int(s)]
        cid[s] = k
        y = int(F[s])
        while y != s:
            cid[y] = k
            orb.append(y)
            y = int(F[y])
        cycles.append(np.array(orb, np.int64))
    label = cid[G]
    minstate = np.array([c.min() for c in cycles], np.int64)
    return dict(n=n, F=F, G=G, on=on, cid=cid, label=label, cycles=cycles, minstate=minstate)


def g1(A):
    """Edge set of the one-flip graph: (C, C') with C != C' and some state of C with one cell flipped falling to C'."""
    n = A["n"]
    st = np.flatnonzero(A["on"])
    src = A["cid"][st]
    E = set()
    for i in range(n):
        dst = A["label"][st ^ (1 << i)]
        keep = dst != src
        E.update(zip(src[keep].tolist(), dst[keep].tolist()))
    return E


def closed_classes(m, E):
    """Strongly connected components of the digraph ([0,m), E) that have no leaving edge (iterative Tarjan)."""
    adj = [[] for _ in range(m)]
    for u, v in E:
        adj[u].append(v)
    index = [-1] * m
    low = [0] * m
    onst = [False] * m
    comp = [-1] * m
    stack = []
    idx = 0
    nc = 0
    for r in range(m):
        if index[r] != -1:
            continue
        work = [(r, 0)]
        index[r] = low[r] = idx
        idx += 1
        stack.append(r)
        onst[r] = True
        while work:
            v, pi = work[-1]
            if pi < len(adj[v]):
                work[-1] = (v, pi + 1)
                w = adj[v][pi]
                if index[w] == -1:
                    index[w] = low[w] = idx
                    idx += 1
                    stack.append(w)
                    onst[w] = True
                    work.append((w, 0))
                elif onst[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    u = work[-1][0]
                    low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    while True:
                        w = stack.pop()
                        onst[w] = False
                        comp[w] = nc
                        if w == v:
                            break
                    nc += 1
    leaving = [False] * nc
    for u, v in E:
        if comp[u] != comp[v]:
            leaving[comp[u]] = True
    classes = {}
    for v in range(m):
        if not leaving[comp[v]]:
            classes.setdefault(comp[v], []).append(v)
    return list(classes.values()), comp


def canon_rot(s):
    return min(s[k:] + s[:k] for k in range(len(s)))
