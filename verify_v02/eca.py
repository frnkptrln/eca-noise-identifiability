"""Own implementation from the definitions in the verification brief (no code from code/fw/).

Ring of n cells, state x in 0..2^n-1, bit i = cell i, indices mod n.
Code c = 4*x_{i-1} + 2*x_i + x_{i+1}; new cell i = bit c of the Wolfram rule number.
"""
import json, os
import numpy as np


def reflect(rule):
    out = 0
    for c in range(8):
        a, b, d = (c >> 2) & 1, (c >> 1) & 1, c & 1
        c2 = 4 * d + 2 * b + a
        if (rule >> c) & 1:
            out |= 1 << c2
    return out


def complement(rule):
    # f'(x) = 1 - f(1 - x): bit c of f' = 1 - bit (7-c) of f
    out = 0
    for c in range(8):
        if not ((rule >> (7 - c)) & 1):
            out |= 1 << c
    return out


def orbit(rule):
    return sorted({rule, reflect(rule), complement(rule), reflect(complement(rule))})


def class_reps():
    return sorted({min(orbit(r)) for r in range(256)})


def neighbours(s, n):
    """Return (L, C, R) arrays: bit i of L = x_{i-1}, of C = x_i, of R = x_{i+1}."""
    mask = (1 << n) - 1
    s = s.astype(np.uint32)
    L = ((s << 1) | (s >> (n - 1))) & mask
    R = ((s >> 1) | ((s & 1) << (n - 1))) & mask
    return L.astype(np.uint32), s, R.astype(np.uint32)


def code_masks(n, states=None):
    """masks[c][x] = bitmask of positions i whose code is c."""
    if states is None:
        states = np.arange(1 << n, dtype=np.uint32)
    mask = np.uint32((1 << n) - 1)
    L, C, R = neighbours(states, n)
    nL, nC, nR = (~L) & mask, (~C) & mask, (~R) & mask
    out = []
    for c in range(8):
        a = L if (c >> 2) & 1 else nL
        b = C if (c >> 1) & 1 else nC
        d = R if c & 1 else nR
        out.append((a & b & d).astype(np.uint32))
    return out


def popcount(a):
    a = a.astype(np.uint64)
    cnt = np.zeros(a.shape, dtype=np.int64)
    while np.any(a):
        cnt += (a & np.uint64(1)).astype(np.int64)
        a = a >> np.uint64(1)
    return cnt


def step_map(rule, n):
    """F as an array of length 2^n."""
    cm = code_masks(n)
    F = np.zeros(1 << n, dtype=np.uint32)
    for c in range(8):
        if (rule >> c) & 1:
            F |= cm[c]
    return F


def code_counts(n):
    """N[c, x] = number of positions of x with code c (int16)."""
    cm = code_masks(n)
    return np.stack([popcount(m) for m in cm]).astype(np.int16)


def cycles_of(F):
    """Return (cycle_id per state for cycle states, -1 otherwise; list of cycles as arrays)."""
    N = len(F)
    # iterate F^N on all states via repeated squaring: images after >= N steps lie on cycles
    G = F.copy()
    k = 1
    while k < N:
        G = G[G]
        k *= 2
    on = np.zeros(N, dtype=bool)
    on[G] = True  # every cycle state is an image of F^(2^m) since F permutes cycle states
    cid = -np.ones(N, dtype=np.int64)
    cycles = []
    for z in np.nonzero(on)[0]:
        if cid[z] >= 0:
            continue
        cyc = [z]
        cid[z] = len(cycles)
        y = F[z]
        while y != z:
            cid[y] = len(cycles)
            cyc.append(y)
            y = F[y]
        cycles.append(np.array(cyc, dtype=np.int64))
    return cid, cycles


def append_jsonl(path, rec):
    """Append-only checkpoint with fsync."""
    with open(path, 'a') as fh:
        fh.write(json.dumps(rec, sort_keys=True) + '\n')
        fh.flush()
        os.fsync(fh.fileno())


def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return [json.loads(l) for l in fh if l.strip()]
