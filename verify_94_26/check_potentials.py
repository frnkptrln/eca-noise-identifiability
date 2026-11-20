"""gamma for every root (Chu-Liu/Edmonds on the matrix V from vbfs), S, gamma_min and k_c from the definitions,
compared with Corollary 1 (rule 94, 3 not dividing n), Theorem V94 / P94 Corollary 2 (3 | n), Theorems 3, 4 and
Corollary 5 (rule 26). Theorem A is NOT used here.

usage: python verify_94_26/check_potentials.py
output: verify_94_26/out/potentials.json
"""
import os, sys, json, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca
import potentials as P
import test_26 as T26

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
rows = []
t0 = time.time()


def brute_gamma(V, root):
    m = V.shape[0]
    others = [c for c in range(m) if c != root]
    best = None
    for par in itertools.product(range(m), repeat=len(others)):
        pmap = dict(zip(others, par))
        if any(pmap[c] == c for c in others):
            continue
        ok = True
        for c in others:
            seen = set()
            u = c
            while u != root:
                if u in seen:
                    ok = False
                    break
                seen.add(u)
                u = pmap[u]
            if not ok:
                break
        if ok:
            w = sum(int(V[c, pmap[c]]) for c in others)
            best = w if best is None else min(best, w)
    return best


# Edmonds (networkx) against brute force on small cases
bf = []
for rule, n in ((26, 6), (94, 4), (154, 5), (26, 5), (90, 5), (30, 5)):
    R = eca.Ring(rule, n)
    if R.m > 7:
        continue
    V, Rc = P.VR(R)
    agree = all(P.gamma_root(V, r) == brute_gamma(V, r) for r in range(R.m))
    bf.append(dict(rule=rule, n=n, m=R.m, agree=agree))
eca.log('Edmonds vs brute force:', bf)


def analyse(rule, n):
    R = eca.Ring(rule, n)
    V, Rc = P.VR(R)
    gam = P.potentials(V)
    g = np.array([gam[c] for c in range(R.m)])
    gmin = int(g.min())
    S = set(np.nonzero(g == gmin)[0].tolist())
    k = P.k_vector(gam, Rc)
    ncomp, comp, closed = R.closed_classes()
    A, e = R.g1()
    g1_ok = set(map(tuple, e.tolist())) == {(a, b) for a in range(R.m) for b in range(R.m) if a != b and V[a, b] == 1}
    row = dict(rule=rule, n=n, m=R.m, gamma_min=gmin, gamma_min_eq_m_minus_1=gmin == R.m - 1, S_size=len(S),
               closed_sizes=[len(c) for c in closed], S_eq_union_closed=S == set().union(*[set(c.tolist()) for c in closed]),
               k=k, kstar=max(k), g1_equals_V1=g1_ok, gamma_hist={int(v): int(np.sum(g == v)) for v in sorted(set(g.tolist()))})
    z = int(R.label[0])
    if rule == 26 and n in (4, 8, 16, 32):
        T2 = [c for c in range(R.m) if V[z, c] == 2]
        reach = R.reach_from(T2) if T2 else set()
        row['V0_hist'] = {int(v): int(np.sum(V[z] == v)) for v in sorted(set(V[z].tolist()))}
        row['T2'] = len(T2)
        row['zero_out_V_ge_2'] = bool(all(V[z, c] >= 2 for c in range(R.m) if c != z))
        row['thm3c_gamma'] = bool(gam[z] == R.m - 1 and all((gam[c] == R.m) == (c in reach) and gam[c] >= R.m
                                                            for c in range(R.m) if c != z))
        kinds = {}
        for c in range(R.m):
            st = R.cycle_states(c)
            kd = 'zero' if st == [0] else ('domain' if T26.is_domain(st[0], n) else ('with_111' if any(T26.has111(y, n) for y in st) else 'other'))
            kinds.setdefault(kd, set()).add(int(gam[c]))
        row['gamma_by_kind'] = {kk: sorted(v) for kk, v in kinds.items()}
        row['R0'] = [int(v) for v in Rc[z]]
    rows.append(row)
    json.dump(dict(edmonds_vs_bruteforce=bf, rows=rows, wall_seconds=round(time.time() - t0, 1)),
              open(os.path.join(OUT, 'potentials.json'), 'w'), indent=1, default=str)
    eca.log(rule, n, 'm', R.m, 'gmin', gmin, 'S', len(S), 'closed', row['closed_sizes'], 'k', k,
            {kk: row[kk] for kk in ('thm3c_gamma', 'V0_hist', 'gamma_by_kind') if kk in row}, f'{time.time() - t0:.0f}s')
    return row


for n in (5, 6, 7, 8, 9, 10, 11, 12):          # n = 13, 14 not run (Edmonds cost, see report)
    analyse(94, n)
for n in (4, 6, 8, 10, 12, 14, 16):
    analyse(26, n)

json.dump(dict(edmonds_vs_bruteforce=bf, rows=rows, wall_seconds=round(time.time() - t0, 1)),
          open(os.path.join(OUT, 'potentials.json'), 'w'), indent=1, default=str)
eca.log('done', round(time.time() - t0, 1), 's')
