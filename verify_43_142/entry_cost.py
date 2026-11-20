"""Proposition 3 for 4 | n up to n = 20: V(C, X) = |w(C) - n/2| / 2, by a backward computation.

h(x) = R(x -> X) = minimum total resistance of a path from state x to a state of X. h = 0 on X and
h(x) = min_y [H(F x, y) + h(y)] = g(F x) otherwise, g = Hamming distance transform of h. Iterated to the
fixed point from h = inf off X. V(C, X) = min over x in C of h(x). Also the G1 distance is compared.

Usage: python entry_cost.py NMAX  -> out/entry_cost.json
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eca import Dynamics, walls


def entry_costs(rule, n):
    dyn = Dynamics(rule, n)
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    x0 = sum(1 << i for i in range(n) if i % 4 in (2, 3))
    kX = int(dyn.cycle_of_periodic[x0])
    inX = np.zeros(N, dtype=bool); inX[dyn.cycle_states[kX]] = True
    INF = 10 ** 6
    h = np.where(inX, 0, INF).astype(np.int64)
    it = 0
    while True:
        it += 1
        g = h.copy()
        for j in range(n):
            g = np.minimum(g, g[xs ^ (1 << j)] + 1)
        hn = np.where(inX, 0, np.minimum(h, g[dyn.succ]))
        if np.array_equal(hn, h):
            break
        h = hn
    w = walls(n, xs)
    bad = []
    vmax = 0
    for k, st in enumerate(dyn.cycle_states):
        v = int(h[st].min())
        wc = int(w[st[0]])
        vmax = max(vmax, v)
        if v != abs(wc - n // 2) // 2:
            bad.append((k, wc, v))
    return dict(rule=rule, n=n, m=dyn.m, iterations=it, V_to_X_max=vmax, failures=bad)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    out = []
    for n in range(4, nmax + 1, 4):
        for rule in (43, 142):
            t = time.time()
            r = entry_costs(rule, n); r["seconds"] = round(time.time() - t, 1)
            out.append(r); print(r, flush=True)
    json.dump(out, open("out/entry_cost.json", "w"), indent=1)
