"""Deterministic checks of expectation (a) (PREDICTIONS_boundaries.md):
(1) for every reflection-symmetric rule with f(000) = f(101) = 0, the null row of n cells evolves as the
    mirror-symmetric subspace of the ring of N = 2n + 2 cells (ring cells -1 and n held at 0 by the dynamics):
    lift(x) = ring state with ring cell j = x_j (0 <= j < n), ring cell N-2-j = x_j, cells n and N-1 = 0;
    checked F_ring(lift x) = lift(F_null x) for all x, n = 1..10; and that it fails for every other rule;
(2) rule 94: a fixed point whose code set is exactly {3, 5, 6} exists iff 3 | (n + 1), n = 1..20, from the
    stored cycle lists (data/boundaries/null_details) for n >= 4 and by enumeration below;
(3) rule 90 null nilpotent iff n + 1 is a power of two, n = 1..20 (F^n(x) = 0 for all x).
Output: data/boundaries/check_mirror.txt"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fwlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries", "check_mirror.txt")


def lift(x, n):
    N = 2 * n + 2
    y = np.zeros_like(x)
    for j in range(n):
        b = (x >> j) & 1
        y |= b << j
        y |= b << (N - 2 - j)
    return y


lines = []
qual = [r for r in range(256) if fwlib.reflect_rule(r) == r and not (r & 1) and not ((r >> 5) & 1)]
works = []
for r in range(256):
    ok = True
    for n in range(1, 11):
        x = np.arange(1 << n, dtype=np.int64)
        Fn = fwlib.succ_map(r, n, "null"); Fr = fwlib.succ_map(r, 2 * n + 2)
        if not np.array_equal(Fr[lift(x, n)], lift(Fn, n)):
            ok = False; break
    if ok:
        works.append(r)
lines.append(f"(1) rules with the mirror embedding for all n = 1..10: {len(works)}; reflection-symmetric with "
             f"f(000)=f(101)=0: {len(qual)}; sets equal: {set(works) == set(qual)}; includes 22, 90, 94, 150: "
             f"{all(r in works for r in (22, 90, 94, 150))}; rules: {works}")
fp = []
for n in range(1, 21):
    F = fwlib.succ_map(94, n, "null"); cm = fwlib.code_mask(n, "null")
    fixed = np.flatnonzero(F == np.arange(1 << n))
    has = any(int(cm[x]) == (1 << 3) | (1 << 5) | (1 << 6) for x in fixed)
    fp.append((n, has, (n + 1) % 3 == 0))
lines.append("(2) rule 94, fixed point with codes exactly {3,5,6} exists: " +
             ", ".join(f"n={n}:{int(h)}" for n, h, _ in fp) + f"; equals [3 | n+1] for n = 1..20: {all(h == p for _, h, p in fp)}")
nil = []
for n in range(1, 21):
    F = fwlib.succ_map(90, n, "null"); G = F.copy()
    for _ in range(n - 1):
        G = F[G]
    nil.append((n, bool((G == 0).all())))
lines.append("(3) rule 90 null nilpotent at n = " + str([n for n, v in nil if v]) +
             f"; equals [n+1 power of 2] for n = 1..20: {all(v == (((n + 1) & n) == 0) for n, v in nil)}")
open(OUT, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
