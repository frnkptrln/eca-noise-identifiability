"""Radius of the selected patterns of rules 122 (checkerboard 2-cycle), 137 (2-cycle 1000 1000 ...),
135 (checkerboard fixed point), 126 (2-cycle of n = 7 / 15), null walls, n = 4..61, by single-flip
simulation as in local_boundaries.py. Output: data/boundaries/local_radius2.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from local_boundaries import step, orbit_until, pattern, DATA


def reached_cycle(rule, n, x):
    seen = {}
    t = 0
    while x not in seen:
        seen[x] = t; x = step(rule, n, x); t += 1
    cyc = [x]; y = step(rule, n, x)
    while y != x:
        cyc.append(y); y = step(rule, n, y)
    return cyc


rows = []
for rule, word in ((122, "10"), (137, "1000"), (135, "10")):
    for n in range(4, 62):
        x0 = pattern(n, word); cyc = reached_cycle(rule, n, x0); T = set(cyc)
        res = [orbit_until(rule, n, x ^ (1 << i), T, 10 ** 4) for x in cyc for i in range(n)]
        rows.append(dict(rule=rule, n=n, word=word, period=len(cyc), pattern_periodic=int(x0 in T), all_flips_return=int(all(v is True for v in res)),
                         undecided=sum(v is None for v in res)))
d = pd.DataFrame(rows); d.to_csv(os.path.join(DATA, "local_radius2.csv"), index=False)
for rule in (122, 137, 135):
    t = d[d.rule == rule]
    print(rule, "radius >= 2 at n =", t[t.all_flips_return == 1].n.tolist(), "undecided at", t[t.undecided > 0].n.tolist(), "pattern periodic at", t[t.pattern_periodic == 1].n.tolist()[:12])
