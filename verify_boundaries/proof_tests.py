"""Direct small-n tests of Proposition L, Lemma W and Proposition N (own code).
    python3 verify_boundaries/proof_tests.py > verify_boundaries/out/proof_tests.txt"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, vb, local_sim as ls
AFF = [0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255]
# Proposition L: G1 strongly connected (one closed class = all cycles), all cycles selected, gmin = m-1
bad = []; cnt = 0
for r in AFF:
    for n in range(3, 15):
        s = vb.Sys(r, n, 'null'); cl = s.closed_classes(); cnt += 1
        if len(cl) != 1 or len(cl[0]) != s.m: bad.append((r, n, 'G1'))
        if n <= 9 and s.m <= 300:
            V, Rr = s.resist(); g = vb.gammas(V)
            if not (g == s.m - 1).all(): bad.append((r, n, 'gamma'))
print('Proposition L, 16 affine rules, n = 3..14 (', cnt, 'records): failures', bad or 'none')
# Lemma W, direct: symmetric linear/affine M (rules 90, 150, 165, 105, 204, 51); if no nonzero u on {0,1,2} lies in V_nil
# then all 8 codes occur at cell 1 in P; and conversely report how often the hypothesis holds
def lin_rows(rule, n):
    e = rule & 1; a = ((rule >> 4) & 1) ^ e; b = ((rule >> 2) & 1) ^ e; d = ((rule >> 1) & 1) ^ e
    return a, b, d, e
res = []
for r in [90, 150, 165, 105, 204, 51]:
    a, b, d, e = lin_rows(r, 0)
    for n in range(3, 15):
        s = vb.Sys(r, n, 'null'); N = 1 << n
        # V_nil of M = states x with M^n x = 0 where M x = F(x) + F(0) (affine part removed)
        F0 = s.succ[0]; Mx = s.succ ^ F0
        y = np.arange(N)
        for _ in range(n): y = Mx[y]
        Vnil = set(np.flatnonzero(y == 0).tolist())
        hyp = not any(u in Vnil for u in range(1, 8))      # nonzero u supported on cells 0,1,2
        P = np.flatnonzero(s.per == 1)
        pats = {((x >> 0) & 1, (x >> 1) & 1, (x >> 2) & 1) for x in P.tolist()}
        res.append((r, n, hyp, len(pats) == 8))
print('Lemma W: cases with hypothesis true', sum(h for _, _, h, _ in res), '; of these with all 8 codes at cell 1:', sum(h and c for _, _, h, c in res),
      '; hypothesis false but all codes anyway:', [(r, n) for r, n, h, c in res if not h and c])
# Proposition N: orbit of e_i under 154 and 26 (null) equals the rule-90 orbit, n = 3..40, 3n steps
bad = []
for r in [154, 26]:
    for n in range(3, 41):
        F, G = ls.step_fn(r, n), ls.step_fn(90, n)
        for i in range(n):
            x = y = 1 << i
            for _ in range(3 * n):
                x, y = F(x), G(y)
                if x != y: bad.append((r, n, i)); break
print('Proposition N: orbits of e_i under 154 / 26 differ from rule 90 (n = 3..40, 3n steps):', bad or 'none')
print('all e_i die under rule 90 exactly at n =', [n for n in range(3, 41) if all((lambda G, x: [x := G(x) for _ in range(2 * n)][-1])(ls.step_fn(90, n), 1 << i) == 0 for i in range(n))])
