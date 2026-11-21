"""Rule 26: tools shared by the scripts of PROOF_26.md (own code).

Left-moving frame: u_t(j) = x_t(j - t), i.e. u_t = rot(x_t, t). In this frame one step is
    U(u)(j) = f(u(j-2), u(j-1), u(j)) = u(j) + u(j-2) * [1 + u(j-1) * (1 + u(j))]   (mod 2):
a cell changes only if the cell two to its left is 1 ("attack"); the attack toggles the cell, except that
it has no effect when the cell in between is 1 and the target is 0.
"""
import numpy as np

import ring
from ring import step, rot

R = 26


def ones(s, n):
    return [i for i in range(n) if (s >> i) & 1]


def c_changes(s, n):
    """number of parity changes in the cyclic sequence of the ones of s (even n). 0 iff s lies on one parity class."""
    o = ones(s, n)
    if len(o) < 2:
        return 0
    return sum(1 for a, b in zip(o, o[1:] + o[:1]) if (a - b) % 2)


def c_changes_all(n):
    """c for all 2^n states (vectorised)."""
    N = 1 << n
    x = np.arange(N, dtype=np.uint32)
    last = np.full(N, -1, dtype=np.int8)
    first = np.full(N, -1, dtype=np.int8)
    cnt = np.zeros(N, dtype=np.int16)
    for i in range(n):
        bit = ((x >> np.uint32(i)) & np.uint32(1)).astype(bool)
        p = i % 2
        cnt += (bit & (last >= 0) & (last != p))
        first[bit & (first < 0)] = p
        last[bit] = p
    cnt += ((first >= 0) & (last != first))
    return cnt


def groups(s, n):
    """the maximal same-parity runs of the cyclic sequence of ones: list of lists of cells, each starting
    with its first one ('source'); None if all ones have the same parity (or there is none)."""
    o = ones(s, n)
    starts = [k for k in range(len(o)) if (o[k] - o[k - 1]) % 2]
    if not starts:
        return None
    out = []
    for a, b in zip(starts, starts[1:] + [starts[0] + len(o)]):
        out.append([o[k % len(o)] for k in range(a, b)])
    return out


def singleton_groups(s, n):
    g = groups(s, n)
    return [] if g is None else [grp[0] for grp in g if len(grp) == 1]


def is_domain_state(s, n):
    """ones on both parity classes and every source at distance >= 3 from the next source."""
    g = groups(s, n)
    if g is None:
        return False
    src = [grp[0] for grp in g]
    return all((b - a) % n >= 3 for a, b in zip(src, src[1:] + src[:1]))


def has_ancestor_pattern(s, n):
    """some pattern 1 0^(2r) 1 1, r >= 0: adjacent ones at (j, j+1) whose preceding one (cyclically; it may be the cell j+1 itself when there are
    only two ones) is at odd distance 2r+1 from j. Returns the list of (j, r)."""
    o = ones(s, n)
    out = []
    if len(o) < 2:
        return out
    for k, j in enumerate(o):
        if o[(k + 1) % len(o)] == (j + 1) % n and ((j - o[k - 1]) % n) % 2 == 1:
            out.append((j, ((j - o[k - 1]) % n - 1) // 2))
    return out


def has111(s, n):
    m = (1 << n) - 1
    return (s & rot(s, 1, n) & rot(s, n - 1, n) & m) != 0


def carrier_words(n):
    """all cyclic words over the blocks 11100 and 100 with at least one block 11100 (states, all rotations)."""
    out = set()

    def rec(word):
        if len(word) == n:
            if '11100' in word:
                s = ring.w2s(word)
                for k in range(n):
                    out.add(rot(s, k, n))
            return
        for b in ('11100', '100'):
            if len(word) + len(b) <= n:
                rec(word + b)
    rec('')
    return out
