"""One-flip graph G1 of rule 94 and its closed classes, computed directly (no use of the proof).

G1 needs only: the set of periodic states, the cycle each state falls to, and all single flips of periodic
states.  Memory-lean NumPy version for one ring size per call; results are appended to
verify_ring_size/part2_94/out/g1_classes.jsonl (one line per n, existing n are skipped).

Method.  F is tabulated for all 2^n states.  G = F^(2^k) is obtained by repeated squaring (G <- G[G]).  The
image of G contains every periodic state; if F maps the image of G bijectively onto itself, every state of the
image is periodic, so the image is exactly the set of periodic states and G(x) lies on the cycle that x falls
to.  k is increased until this test holds.  Cycles are then traced with F, the flips are looked up through G,
and the strongly connected components come from scipy.

Usage (repository root):  python verify_ring_size/part2_94/g1_classes.py 6 9 12 ...
"""
import json
import os
import sys
import time
import resource
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "g1_classes.jsonl")


def bits(x, n):
    return format(int(x), "0%db" % n)


def build_F94(n):
    """F(x) = (a XOR c) OR (b AND NOT (a AND c)) with a_i = x_(i-1), c_i = x_(i+1); x_0 is the top bit."""
    N = 1 << n
    mask = np.uint32(N - 1)
    x = np.arange(N, dtype=np.uint32)
    a = x >> np.uint32(1)
    a |= (x & np.uint32(1)) << np.uint32(n - 1)
    c = x << np.uint32(1)
    c &= mask
    c |= x >> np.uint32(n - 1)
    t = a & c
    np.invert(t, out=t)
    t &= x
    del x
    a ^= c
    del c
    a |= t
    del t
    a &= mask
    return a


def run(n):
    t0 = time.process_time()
    N = 1 << n
    F = build_F94(n)
    G = F.copy()
    k = 0
    while True:
        G = G[G]
        k += 1
        if k < 4 or k % 2:
            continue
        on = np.zeros(N, bool)
        on[G] = True
        idx = np.flatnonzero(on)
        img = F[idx]
        if on[img].all():
            on2 = np.zeros(N, bool)
            on2[img] = True
            ok = int(on2.sum()) == len(idx)
            del on2
            if ok:
                break
        del on, idx, img
        if k > n + 1:
            raise RuntimeError("no stabilisation")
    del on, img
    idx = idx.astype(np.uint32)          # sorted periodic states
    S = len(idx)
    cid = np.full(S, -1, np.int64)
    minstate = []
    length = []
    Fi = np.searchsorted(idx, F[idx])    # F as a permutation of positions in idx
    for s in range(S):
        if cid[s] >= 0:
            continue
        c = len(minstate)
        cid[s] = c
        L = 1
        y = int(Fi[s])
        while y != s:
            cid[y] = c
            L += 1
            y = int(Fi[y])
        minstate.append(int(idx[s]))     # idx is sorted, so the first state met is the smallest of its cycle
        length.append(L)
    m = len(minstate)
    del F
    pairs = []
    for i in range(n):
        dst = cid[np.searchsorted(idx, G[idx ^ np.uint32(1 << i)])]
        keep = dst != cid
        pairs.append(np.unique(cid[keep] * m + dst[keep]))
    e = np.unique(np.concatenate(pairs))
    src, dst = e // m, e % m
    A = coo_matrix((np.ones(len(e), np.int8), (src, dst)), shape=(m, m)).tocsr()
    ncomp, comp = connected_components(A, directed=True, connection="strong")
    leaving = np.zeros(ncomp, bool)
    leaving[comp[src[comp[src] != comp[dst]]]] = True
    closed = np.flatnonzero(~leaving)
    members = {int(c): [] for c in closed}
    for v in np.flatnonzero(~leaving[comp]):
        members[int(comp[v])].append(bits(minstate[v], n))
    sizes = sorted(len(v) for v in members.values())
    # cycles from which a crystal phase can be reached in G1 (reverse search), if 3 | n
    rec = dict(n=n, states=N, squarings=k, periodic_states=int(S), cycles=m,
               period_hist=sorted((int(a), int(b)) for a, b in zip(*np.unique(length, return_counts=True))),
               g1_edges=int(len(e)), strong_components=int(ncomp), closed_classes=len(sizes),
               closed_class_sizes=sizes if len(sizes) <= 20 else sizes[:20],
               closed_members=[sorted(v) for v in members.values() if len(v) <= 6],
               cycles_without_out_edge=int(m - len(np.unique(src))))
    if n % 3 == 0:
        crystal = set(("011" * (n // 3))[r:] + ("011" * (n // 3))[:r] for r in range(3))
        cr = [v for v in range(m) if bits(minstate[v], n) in crystal and length[v] == 1]
        AT = A.T.tocsr()
        reach = np.zeros(m, bool)
        reach[cr] = True
        front = list(cr)
        while front:
            nxt = []
            for v in front:
                for w in AT.indices[AT.indptr[v]:AT.indptr[v + 1]]:
                    if not reach[w]:
                        reach[w] = True
                        nxt.append(int(w))
            front = nxt
        rec.update(crystal_phases_found=len(cr), cycles_reaching_crystal=int(reach.sum()),
                   cycles_not_reaching_crystal=int(m - reach.sum()),
                   closed_classes_are_exactly_the_crystal_phases=(
                       sorted(v[0] for v in members.values() if len(v) == 1) == sorted(crystal)
                       and len(sizes) == 3))
    rec["cpu_seconds"] = round(time.process_time() - t0, 2)
    rec["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 << 20), 1)
    return rec


def main():
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            done.add(json.loads(line)["n"])
    for n in [int(a) for a in sys.argv[1:]]:
        if n in done:
            print("n = %d already done" % n)
            continue
        rec = run(n)
        with open(OUT, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        print({k: v for k, v in rec.items() if k not in ("closed_members", "period_hist")}, flush=True)


if __name__ == "__main__":
    main()
