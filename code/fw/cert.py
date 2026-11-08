"""Certificates for the small-noise classification of one rule on one ring.

A certificate (JSON) contains everything needed to re-derive gamma_min, the noise-selected cycles,
every k_c and k* with integer bounds that coincide:
  cycles      explicit state lists (cycle j starts at its smallest state and follows F)
  gamma       claimed stochastic potential of every cycle
  duals       laminar family [(member cycle ids, y)], y > 0: gamma(C) >= sum of y over sets not
              containing C, for every C (dual feasibility: for all C != C', the sum of y over sets
              containing C but not C' is <= V(C, C'))
  trees       {root: parent array} optimal in-trees on the cycles (parent[root] = -1): gamma(root) <=
              sum of V(j, parent[j])
  stable      the cycles with gamma = gamma_min (each has a tree)
  k_c         for every code c: (k_c, witness root C, witness trajectory s_0 in C, ..., s_k containing c);
              k_c <= gamma(C) + resistance(trajectory) - gamma_min
  kstar, cover (codes on stable cycles), uncovered (codes with k_c = k* >= 1) or covering cycles.
A trajectory is a list of chain states; its resistance is sum_t H(F(s_t), s_{t+1}).
"""
import json, os, sys
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fwlib, hier


def witness_path(F, n, sources, target_mask):
    """0-1 BFS with parents on the single-layer graph; returns a chain trajectory from a source cycle
    state to the nearest state in target_mask, and its resistance."""
    S = 1 << n
    dist = np.full(S, 1 << 30, dtype=np.int64)
    par = np.full(S, -1, dtype=np.int64)
    kind = np.zeros(S, dtype=np.int8)          # 0: reached by F-edge, 1: by a flip
    dq = deque()
    for s in sources:
        dist[s] = 0; dq.append(int(s))
    while dq:
        x = dq.popleft()
        d = dist[x]
        y = int(F[x])
        if d < dist[y]:
            dist[y] = d; par[y] = x; kind[y] = 0; dq.appendleft(y)
        for i in range(n):
            z = x ^ (1 << i)
            if d + 1 < dist[z]:
                dist[z] = d + 1; par[z] = x; kind[z] = 1; dq.append(z)
    cand = np.flatnonzero(target_mask)
    t = int(cand[np.argmin(dist[cand])])
    nodes = [t]                                 # walk back to the source (sources have no parent)
    while par[nodes[-1]] >= 0:
        nodes.append(int(par[nodes[-1]]))
    nodes = nodes[::-1]
    src = nodes[0]
    # chain trajectory: an F-edge u -> F(u) starts a new step; a flip edge changes the landing
    # state of the current step. A flip of the source itself belongs to the step from its cycle
    # predecessor, so the trajectory then starts one step earlier.
    traj = [src]
    if len(nodes) > 1 and kind[nodes[1]] == 1:
        z = src
        while int(F[z]) != src:
            z = int(F[z])
        traj = [z, src]
    for v in nodes[1:]:
        if kind[v] == 0:
            traj.append(v)
        else:
            traj[-1] = v
    res = sum(int(bin(int(F[traj[i]]) ^ traj[i + 1]).count("1")) for i in range(len(traj) - 1))
    assert res == int(dist[t]), (res, dist[t])
    return traj, res


def bijective_certificate(rule, n, F):
    """F bijective => P(x, y) = K(F(x), y) is doubly stochastic, the uniform law is stationary for every
    eps, every state is on a cycle and ord pi(x) = 0 for all x; every code occurs, so k* = 0."""
    return dict(rule=rule, n=n, bijective=True, kstar=0, k_c=[dict(code=c, k=0) for c in range(8)])


def make_certificate(res, max_trees=None):
    cs, H = res["cs"], res["H"]
    n, F = cs.n, cs.F
    cycles = []
    for j in range(cs.m):
        s0 = int(cs.cyc_min[j]); cyc = [s0]; z = int(F[s0])
        while z != s0:
            cyc.append(z); z = int(F[z])
        cycles.append(cyc)
    duals = [(mem, y) for _, mem, y in hier.laminar_sets(H)]
    gamma = [int(g) for g in res["gamma"]]
    gmin = res["gmin"]
    stable = [int(s) for s in res["stable"]]
    roots = list(stable) if max_trees is None else stable[:max_trees]
    kc = []
    for c in range(8):
        tot = res["gamma"] + res["Rcode"][:, c]
        C = int(np.argmin(tot))
        mask = ((cs.state_codes >> c) & 1).astype(bool)
        traj, r = witness_path(F, n, cs.states_of(C), mask)
        assert gamma[C] + r - gmin == int(res["k_c"][c])
        kc.append(dict(code=c, k=int(res["k_c"][c]), root=C, trajectory=traj, resistance=r))
        if C not in roots:
            roots.append(C)
    trees = {}
    for r in roots:
        par = [-1] * cs.m
        for t, h, w in hier.tree_for_root(H, r):
            par[t] = h
        trees[str(r)] = par
    kstar = int(res["kstar"])
    cover = int(res["stable_cover"])
    out = dict(rule=res["rule"], n=n, m=cs.m, cycles=cycles, gamma=gamma, gamma_min=gmin,
               stable=stable, duals=duals, trees=trees, k_c=kc, kstar=kstar,
               stable_cover_mask=cover)
    if kstar == 0:
        # a small set of stable cycles covering all codes (greedy)
        need, chosen = 255, []
        for s in sorted(stable, key=lambda s: -bin(int(cs.cyc_codes[s])).count("1")):
            if int(cs.cyc_codes[s]) & need:
                chosen.append(s); need &= ~int(cs.cyc_codes[s])
            if need == 0:
                break
        out["covering_cycles"] = chosen
    else:
        out["uncovered_codes"] = [c for c in range(8) if int(res["k_c"][c]) == kstar]
    return out


def write(cert, path):
    """Write gzip-compressed JSON atomically (path should end in .json.gz)."""
    import gzip
    tmp = path + ".tmp"
    with open(tmp, "wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as fh:     # mtime=0: byte-reproducible
            fh.write(json.dumps(cert, separators=(",", ":"), sort_keys=True).encode())
        raw.flush(); os.fsync(raw.fileno())
    os.replace(tmp, path)


def read(path):
    import gzip
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as fh:
        return json.load(fh)
