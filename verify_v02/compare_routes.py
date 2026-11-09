"""Compare route (a) and route (b) for the sealed sample; writes out/sample_results.csv and out/compare_routes.txt."""
import math, json
import numpy as np, pandas as pd
import eca
rows = []
lines = []
for n in (4, 5):
    A = {r['rule']: r for r in eca.read_jsonl(f'out/exact_n{n}.jsonl')}
    B = {r['rule']: r for r in eca.read_jsonl(f'out/route_b_n{n}.jsonl')}
    mism = [r for r in A if A[r]['k_c'] != B[r]['k_c']]
    lines.append(f'n={n}: exact route (a) vs route (b): {len(A)} classes, k_c mismatches {len(mism)} {mism}; exact check at eps=1/7 all true: {all(A[r]["exact_check_eps_1_7"] for r in A)}')
    for r in sorted(A):
        rows.append(dict(n=n, rule=r, k_c_a=A[r]['k_c'], k_c_b=B[r]['k_c'], k_star_a=A[r]['k_star'], k_star_b=B[r]['k_star'],
                         a_coef=A[r]['a_float'], a_exact=A[r]['a'], m_cycles=B[r]['m_cycles'], agree=A[r]['k_c'] == B[r]['k_c']))
# n = 12
S = json.load(open('SAMPLE.json'))
s12 = S['n12_fixed'] + S['n12_drawn']
G = eca.read_jsonl('out/route_a_n12_w1.jsonl') + eca.read_jsonl('out/route_a_n12_w2.jsonl')
B = {r['rule']: r for r in eca.read_jsonl('out/route_b_n12_w1.jsonl') + eca.read_jsonl('out/route_b_n12_w2.jsonl')}
maxres = max(g['max_rel_resid'] for g in G)
lines.append(f'n=12 GTH: {len(G)} solves, max componentwise relative residual |piP-pi|/pi = {maxres:.3e}')
worst = 0.0
for r in s12:
    g = sorted([x for x in G if x['rule'] == r], key=lambda x: -x['eps'])
    eps = np.array([x['eps'] for x in g]); nu = np.array([x['nu'] for x in g])
    sl = np.log(nu[:-1] / nu[1:]) / np.log(eps[:-1] / eps[1:])[:, None]   # slopes between consecutive eps
    ka = np.rint(sl[-1]).astype(int)
    dev = np.abs(sl[-3:] - ka).max()  # last three pairs (1e-6..1e-9)
    worst = max(worst, dev)
    kb = B[r]['k_c']
    ks = int(ka.max())
    a_est = min(nu[-1][c] / eps[-1] ** ks for c in range(8) if ka[c] == ks)
    rows.append(dict(n=12, rule=r, k_c_a=ka.tolist(), k_c_b=kb, k_star_a=ks, k_star_b=B[r]['k_star'], a_coef=a_est,
                     a_exact='', m_cycles=B[r]['m_cycles'], agree=ka.tolist() == kb,
                     slope_dev_1e6_1e9=float(dev), slopes_1e4_1e5=json.dumps(np.round(sl[0], 4).tolist())))
lines.append(f'n=12: route (a) GTH slopes vs route (b) on the 20 sealed classes: mismatches {[r for r in rows if r["n"]==12 and not r["agree"]]}; '
             f'max |slope - integer| over pairs (1e-6,1e-7),(1e-7,1e-8),(1e-8,1e-9) = {worst:.2e}')
df = pd.DataFrame(rows)
df.to_csv('out/sample_results.csv', index=False)
open('out/compare_routes.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
