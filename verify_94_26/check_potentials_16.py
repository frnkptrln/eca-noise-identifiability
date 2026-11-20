"""Rule 26, n = 16: potentials for selected roots, and k_c exactly by bounds (Theorem A and Theorem 3 not used).
Lower bound for the roots not computed: every in-tree rooted at C != {0} contains an edge leaving {0}, of weight
>= min_C' V({0}, C') (computed), and m - 2 further edges of weight >= 1.
(All 552 roots were attempted in check_potentials.py and stopped after about 50 minutes; see the report.)
usage: python verify_94_26/check_potentials_16.py      output: verify_94_26/out/potentials_16.json"""
import os, sys, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca, potentials as P, test_26 as T26

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
t0 = time.time()
n = 16
R = eca.Ring(26, n)
V, Rc = P.VR(R)
m = R.m
z = int(R.label[0])
kind = {}
for c in range(m):
    st = R.cycle_states(c)
    kind[c] = 'zero' if st == [0] else ('domain' if T26.is_domain(st[0], n) else
                                         ('with_111' if any(T26.has111(y, n) for y in st) else 'other'))
T2 = [c for c in range(m) if V[z, c] == 2]
reach = R.reach_from(T2)
c111 = [c for c in range(m) if kind[c] == 'with_111']
rnd = random.Random(16)
others = rnd.sample([c for c in range(m) if c != z and c not in c111], 12)
roots = [z] + c111 + others
gam, log = {}, []
for r in roots:
    t = time.time()
    gam[r] = P.gamma_root(V, r)
    log.append(dict(root=r, kind=kind[r], in_T2=r in T2, reachable_from_T2=r in reach, gamma=gam[r],
                    seconds=round(time.time() - t, 1)))
    eca.log(log[-1])
min_out0 = int(min(V[z, c] for c in range(m) if c != z))
lb = (m - 2) + min_out0
gmin = gam[z]
k, exact = [], []
for code in range(8):
    ub = min(gam[r] + Rc[r, code] for r in roots) - gmin
    lb_c = min([gam[r] + Rc[r, code] for r in roots] + [lb + Rc[c, code] for c in range(m) if c not in gam]) - gmin
    k.append(int(ub))
    exact.append(bool(ub == lb_c))
res = dict(n=n, m=m, min_V_out_of_zero=min_out0, lower_bound_gamma_nonzero=int(lb), gamma_zero=gmin,
           gamma_zero_eq_m_minus_1=gmin == m - 1, gmin_is_global=bool(lb > gmin), T2=len(T2),
           reachable_from_T2=len(reach), c111=c111, c111_reachable_from_T2=[c in reach for c in c111],
           c111_V_from_zero=[int(V[z, c]) for c in c111], T2_kinds=sorted({kind[c] for c in T2}),
           V0_hist={int(v): int(np.sum(V[z] == v)) for v in sorted(set(V[z].tolist()))}, R0=[int(v) for v in Rc[z]],
           thm3c_on_computed_roots=all((gam[r] == m) == (r in reach) and gam[r] >= m for r in roots if r != z),
           k=k, k_exact=exact, roots=log, wall_seconds=round(time.time() - t0, 1))
json.dump(res, open(os.path.join(OUT, 'potentials_16.json'), 'w'), indent=1, default=str)
eca.log({kk: res[kk] for kk in res if kk != 'roots'})
