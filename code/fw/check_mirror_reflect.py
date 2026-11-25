"""Reflecting walls: (1) for every reflection-symmetric rule the row of n cells evolves as the mirror-symmetric
subspace of the ring of 2n cells (ring cell j = x_j, ring cell 2n-1-j = x_j), checked n = 1..10 for all 256
rules (holds exactly for the 64 symmetric rules); (2) rule 90 nilpotent iff n is a power of two, n = 1..16;
(3) rule 94: fixed points with code set within {3, 5, 6} and their radius, n = 4..16.
Output: data/boundaries/check_mirror_reflect.txt"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fwlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries", "check_mirror_reflect.txt")
lines = []
works = []
for r in range(256):
    ok = True
    for n in range(1, 11):
        x = np.arange(1 << n, dtype=np.int64)
        lift = lambda v: sum((((v >> j) & 1) << j) | (((v >> j) & 1) << (2 * n - 1 - j)) for j in range(n))
        Fn = fwlib.succ_map(r, n, "reflect"); Fr = fwlib.succ_map(r, 2 * n)
        if not np.array_equal(Fr[lift(x)], lift(Fn)):
            ok = False; break
    works.append(r) if ok else None
sym = [r for r in range(256) if fwlib.reflect_rule(r) == r]
lines.append(f"(1) mirror embedding (reflect, ring 2n) holds for {len(works)} rules; equals the reflection-symmetric rules: {set(works) == set(sym)}")
nil = []
for n in range(1, 17):
    F = fwlib.succ_map(90, n, "reflect"); G = F.copy()
    for _ in range(n):
        G = F[G]
    nil.append(n) if (G == 0).all() else None
lines.append(f"(2) rule 90 reflect nilpotent at n = {nil}")
from local_boundaries import orbit_until
for n in range(4, 17):
    F = fwlib.succ_map(94, n, "reflect"); cm = fwlib.code_mask(n, "reflect")
    fixed = [int(x) for x in np.flatnonzero(F == np.arange(1 << n)) if (int(cm[x]) & ~0b01101000) == 0]
    res = cs = None
    out = []
    for x in fixed:
        returns = []
        for i in range(n):
            y = x ^ (1 << i); seen = set()
            while y not in seen and y != x:
                seen.add(y); y = int(F[y])
            returns.append(y == x)
        out.append(("".join(str((x >> i) & 1) for i in range(n)), all(returns)))
    lines.append(f"(3) n={n}: rule 94 reflect fixed points with codes in {{3,5,6}}: {out}")
open(OUT, "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
