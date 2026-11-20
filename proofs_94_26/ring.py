"""Small-n tools for elementary cellular automata on a ring (own code, NumPy/SciPy only).

Conventions (as in report_ring_size.md, Section 3, and verify_ring_size/part2_94/PROOF_94.md):
  * a state is an integer, bit i = cell i, cells 0..n-1, indices mod n;
  * (F x)_i = f(x_(i-1), x_i, x_(i+1)), f(a,b,c) = bit (4a+2b+c) of the rule number;
  * a word such as '01101' lists cell 0 first;
  * cycles are the periodic orbits of F; G1 has an edge C -> C' (C != C') iff for some state x of C and
    some cell j the orbit of x + e_j ends on C'; a closed class is a strongly connected component of G1
    that no edge leaves.
Nothing is imported from code/ or verify_ring_size/.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


# ---------------------------------------------------------------- single states
def w2s(word):
    return sum(1 << i for i, ch in enumerate(word) if ch == '1')


def s2w(s, n):
    return ''.join('1' if (s >> i) & 1 else '0' for i in range(n))


def step(rule, s, n):
    """one application of F (bit operations on a Python integer; any n)."""
    mask = (1 << n) - 1
    left = ((s << 1) | (s >> (n - 1))) & mask      # bit i = x_(i-1)
    right = ((s >> 1) | (s << (n - 1))) & mask     # bit i = x_(i+1)
    out = 0
    for code in range(8):
        if (rule >> code) & 1:
            a, b, c = (code >> 2) & 1, (code >> 1) & 1, code & 1
            out |= (left if a else ~left) & (s if b else ~s) & (right if c else ~right)
    return out & mask


def step_slow(rule, s, n):
    """cell-by-cell reference implementation of F (used by the tests to check step and F_table)."""
    out = 0
    for i in range(n):
        code = 4 * ((s >> ((i - 1) % n)) & 1) + 2 * ((s >> i) & 1) + ((s >> ((i + 1) % n)) & 1)
        if (rule >> code) & 1:
            out |= 1 << i
    return out


def codes_of(s, n):
    return {4 * ((s >> ((i - 1) % n)) & 1) + 2 * ((s >> i) & 1) + ((s >> ((i + 1) % n)) & 1)
            for i in range(n)}


def rot(s, k, n):
    """state whose cell i is the cell i-k of s (shift to the right by k)."""
    k %= n
    return ((s << k) | (s >> (n - k))) & ((1 << n) - 1)


def limit_cycle(rule, s, n):
    """(transient length, list of the states of the cycle reached from s, starting at the entry state)."""
    seen = {}
    t = 0
    while s not in seen:
        seen[s] = t
        s = step(rule, s, n)
        t += 1
    t0 = seen[s]
    cyc = [s]
    u = step(rule, s, n)
    while u != s:
        cyc.append(u)
        u = step(rule, u, n)
    return t0, cyc


# ---------------------------------------------------------------- all states of a ring
def F_table(rule, n):
    N = 1 << n
    x = np.arange(N, dtype=np.uint32)
    mask = np.uint32(N - 1)
    left = ((x << np.uint32(1)) | (x >> np.uint32(n - 1))) & mask     # bit i = x_(i-1)
    right = ((x >> np.uint32(1)) | (x << np.uint32(n - 1))) & mask    # bit i = x_(i+1)
    out = np.zeros(N, dtype=np.uint32)
    for code in range(8):
        if (rule >> code) & 1:
            a, b, c = (code >> 2) & 1, (code >> 1) & 1, code & 1
            out |= (left if a else ~left) & (x if b else ~x) & (right if c else ~right)
    return out & mask


def analyse(rule, n):
    """F table, periodic mask, list of cycles (lists of states), and for every state the index of the
    cycle its orbit ends on."""
    F = F_table(rule, n)
    N = 1 << n
    G = F.copy()
    for _ in range(n + 1):          # G = F^(2^(n+1)); 2^(n+1) > number of states, so G(x) is periodic
        G = G[G]
    per = np.zeros(N, dtype=bool)
    per[G] = True                   # image of a power of F beyond every transient = the periodic states
    cid = np.full(N, -1, dtype=np.int32)
    cycles = []
    for s in np.nonzero(per)[0]:
        if cid[s] >= 0:
            continue
        cyc = [int(s)]
        t = int(F[s])
        while t != s:
            cyc.append(t)
            t = int(F[t])
        cid[cyc] = len(cycles)
        cycles.append(cyc)
    att = cid[G]
    return F, per, cycles, att


def g1(rule, n, res=None):
    """One-flip graph on the cycles: sparse adjacency, strong components, closed classes."""
    F, per, cycles, att = res if res is not None else analyse(rule, n)
    m = len(cycles)
    ps = np.nonzero(per)[0].astype(np.uint32)
    src = att[ps]
    rows, cols = [], []
    for j in range(n):
        dst = att[ps ^ np.uint32(1 << j)]
        ok = dst != src
        rows.append(src[ok])
        cols.append(dst[ok])
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    A = csr_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(m, m))
    A.sum_duplicates()
    A.data[:] = 1
    ncomp, lab = connected_components(A, directed=True, connection='strong')
    coo = A.tocoo()
    leaving = np.zeros(ncomp, dtype=bool)
    d = lab[coo.row] != lab[coo.col]
    leaving[lab[coo.row[d]]] = True
    closed = [int(c) for c in range(ncomp) if not leaving[c]]
    return dict(F=F, per=per, cycles=cycles, att=att, A=A, lab=lab, ncomp=int(ncomp), closed=closed, m=m,
                n_edges=int(A.nnz))


def reach_from(A, sources):
    """boolean mask of the nodes reachable from the given nodes along edges of the sparse matrix A."""
    m = A.shape[0]
    seen = np.zeros(m, dtype=bool)
    stack = [int(v) for v in sources]
    seen[stack] = True
    indptr, indices = A.indptr, A.indices
    while stack:
        v = stack.pop()
        for u in indices[indptr[v]:indptr[v + 1]]:
            if not seen[u]:
                seen[u] = True
                stack.append(int(u))
    return seen


# ---------------------------------------------------------------- rule 94: frozen set, block words, windows
def occ94(s, n):
    """centres of the occurrences of 101."""
    return [i for i in range(n)
            if ((s >> ((i - 1) % n)) & 1, (s >> i) & 1, (s >> ((i + 1) % n)) & 1) == (1, 0, 1)]


def frozen94(s, n):
    w = set()
    for i in occ94(s, n):
        w |= {(i - 1) % n, i, (i + 1) % n}
    return w


def is_block_word(s, n):
    """cyclic word over the blocks 01 and 011: zeros isolated, runs of ones of length 1 or 2, a zero exists."""
    if s == (1 << n) - 1:
        return False
    for i in range(n):
        a, b, c = [(s >> ((i + k) % n)) & 1 for k in range(3)]
        if a == 0 and b == 0:
            return False
        if a == 1 and b == 1 and c == 1:
            return False
    return True


def block_words(n):
    """all block words of the ring, as (state, number of short blocks, number of long blocks)."""
    out = []
    for s in range(1 << n):
        if is_block_word(s, n):
            zeros = n - bin(s).count('1')
            b = n - 2 * zeros            # a + b = zeros, 2a + 3b = n
            out.append((s, zeros - b, b))
    return out


def windows94(s, n):
    """maximal runs of cells outside the frozen set, as lists of cells in ring order.
    Empty list if the state is fully frozen; None if the frozen set is empty."""
    W = frozen94(s, n)
    if not W:
        return None
    out = []
    for i in range(n):
        if i not in W and (i - 1) % n in W:
            run = [i]
            while (run[-1] + 1) % n not in W:
                run.append((run[-1] + 1) % n)
            out.append(run)
    return out


def phi(rule, u, w):
    """window map: w cells (bit i = window cell i+1) with both neighbours of the window held at 1."""
    out = 0
    for i in range(w):
        a = (u >> (i - 1)) & 1 if i > 0 else 1
        b = (u >> i) & 1
        c = (u >> (i + 1)) & 1 if i < w - 1 else 1
        if (rule >> (4 * a + 2 * b + c)) & 1:
            out |= 1 << i
    return out


def phi_table(rule, w):
    N = 1 << w
    x = np.arange(N, dtype=np.int64)
    left = ((x << 1) | 1) & (N - 1)
    right = (x >> 1) | (1 << (w - 1))
    out = np.zeros(N, dtype=np.int64)
    for code in range(8):
        if (rule >> code) & 1:
            a, b, c = (code >> 2) & 1, (code >> 1) & 1, code & 1
            out |= (left if a else ~left) & (x if b else ~x) & (right if c else ~right)
    return out & (N - 1)


def window_unfrozen(u, w):
    """no occurrence of 101 centred at a window cell in the padded word 1 u 1."""
    p = [1] + [(u >> i) & 1 for i in range(w)] + [1]
    return not any(p[i - 1] == 1 and p[i] == 0 and p[i + 1] == 1 for i in range(1, w + 1))


def live_window_orbits(w):
    """orbits of the phi-periodic states of the width-w window of rule 94 all of whose states are
    unfrozen ('live' states); lists of ints."""
    P = phi_table(94, w)
    G = P.copy()
    for _ in range(w + 1):
        G = G[G]
    per = np.zeros(1 << w, dtype=bool)
    per[G] = True
    seen, out = set(), []
    for s in np.nonzero(per)[0]:
        s = int(s)
        if s in seen:
            continue
        cyc = [s]
        t = int(P[s])
        while t != s:
            cyc.append(t)
            t = int(P[t])
        seen |= set(cyc)
        if all(window_unfrozen(u, w) for u in cyc):
            out.append(cyc)
    return out


def AB_window(w):
    """the two states A_w, B_w of Lemma 8 (w = 2 mod 3): restrictions to the window cells 1..w of the
    words A = (111100)^inf and B = (100111)^inf (cell 0 first)."""
    A = sum(1 << (i - 1) for i in range(1, w + 1) if i % 6 in (0, 1, 2, 3))
    B = sum(1 << (i - 1) for i in range(1, w + 1) if i % 6 in (0, 3, 4, 5))
    return A, B
