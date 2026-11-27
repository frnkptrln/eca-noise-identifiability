"""All 256 rules for n = 1..6: check the statements of Statement.lean on the literal model and compare
m, k*, k_v, gamma_min and |S| with data/fw_sweep.csv of the repository (n = 4..6; data only, no code).
Run from this directory: python sweep.py [path to fw_sweep.csv]"""
import csv
import sys
import time
import random
from collections import defaultdict
from instance import Instance
from lean_defs import CODES

DATA = sys.argv[1] if len(sys.argv) > 1 else '../data/fw_sweep.csv'
data = {(int(r['n']), int(r['rule'])): r for r in csv.DictReader(open(DATA))}
rows, fails, cmp_stats = [], [], defaultdict(lambda: [0, 0])
t0 = time.time()
for n in range(1, 7):
    for N in range(256):
        I = Instance(N, n, crosscheck_R=(n <= 4), brute_cc_max=12)
        ch = I.check_statements(rng=random.Random(N * 10 + n), trees_per_root=20 if I.m <= 16 else 5)
        for k, v in ch.items():
            if not v:
                fails.append((n, N, k))
        kv = '-'.join(str(I.k[v]) for v in CODES)
        rows.append(dict(n=n, rule=N, m=I.m, gamma_min=I.gammaMin, n_sel=len(I.Sel), n_closed=len(I.cc),
                         k_v=kv, kstar=I.kstar, checks=len(ch),
                         failed=';'.join(k for k, v in ch.items() if not v)))
        d = data.get((n, N))
        if d:
            comps = [('cycles', I.m, int(d['cycles'])), ('kstar', I.kstar, int(d['kstar'])),
                     ('k_v (order 4a+2b+c)', kv, d['k_c'])]
            if d['bijective'] != '1':
                comps += [('gamma_min (non-bijective rows)', I.gammaMin, int(d['gamma_min'])),
                          ('n_stable = |S| (non-bijective rows)', len(I.Sel), int(d['n_stable']))]
            for name, mine, theirs in comps:
                cmp_stats[name][0] += 1
                cmp_stats[name][1] += (mine == theirs)
                if mine != theirs:
                    fails.append((n, N, f'data mismatch {name}: model {mine}, data {theirs}'))
    print(f'n={n} done, {time.time() - t0:.0f} s', flush=True)

with open('out/sweep_n1_6.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
with open('out/sweep_summary.txt', 'w') as fh:
    fh.write(f'instances: {len(rows)} (256 rules x n = 1..6), wall time {time.time() - t0:.0f} s\n')
    fh.write('comparison with data/fw_sweep.csv (rows present there):\n')
    for k, (tot, ok) in cmp_stats.items():
        fh.write(f'  {k}: {ok} of {tot} agree\n')
    fh.write(f'failures ({len(fails)}):\n')
    for f in fails:
        fh.write(f'  n={f[0]} rule={f[1]}: {f[2]}\n')
print(open('out/sweep_summary.txt').read()[:4000])
