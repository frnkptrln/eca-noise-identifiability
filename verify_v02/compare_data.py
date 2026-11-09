"""Step 2: compare own k_c, k*, cycle counts with data/fw_sweep.csv, data/fw_n12_classes.csv, data/fw_n12_all_rules.csv."""
import pandas as pd, numpy as np, json, eca
sw = pd.read_csv('../data/fw_sweep.csv')
c12 = pd.read_csv('../data/fw_n12_classes.csv')
a12 = pd.read_csv('../data/fw_n12_all_rules.csv')
mine = []
for n in range(4, 11):
    mine += eca.read_jsonl(f'out/route_b_n{n}.jsonl')
for n in (11, 12):
    mine += eca.read_jsonl(f'out/route_b_n{n}_w1.jsonl') + eca.read_jsonl(f'out/route_b_n{n}_w2.jsonl')
for n in (17, 20):
    for w in ('w1', 'w2'):
        mine += eca.read_jsonl(f'out/route_b_n{n}.jsonl.{w}')
ex = {(r['n'], r['rule']): r for n in (4, 5) for r in eca.read_jsonl(f'out/exact_n{n}.jsonl')}
lines, rows = [], []
for r in mine:
    s = sw[(sw.n == r['n']) & (sw.rule == r['rule'])]
    if len(s) != 1:
        lines.append(f"missing in fw_sweep: n={r['n']} rule={r['rule']}"); continue
    s = s.iloc[0]
    kc = '-'.join(map(str, r['k_c']))
    rows.append(dict(n=r['n'], rule=r['rule'], k_c_mine=kc, k_c_file=s.k_c, kstar_mine=r['k_star'], kstar_file=int(s.kstar),
                     cycles_mine=r['m_cycles'], cycles_file=int(s.cycles),
                     ok=(kc == s.k_c and r['k_star'] == s.kstar and r['m_cycles'] == s.cycles)))
df = pd.DataFrame(rows)
df.to_csv('out/compare_fw_sweep.csv', index=False)
lines.append(f'fw_sweep.csv: compared {len(df)} (n, class) pairs (n=4..12 all 88, n=17/20 sample); mismatches: {int((~df.ok).sum())}')
for _, x in df[~df.ok].iterrows():
    lines.append('  MISMATCH ' + x.to_json())
# n = 12 class file and all-rules file
m12 = {r['rule']: r for r in mine if r['n'] == 12}
bad = []
for _, x in c12.iterrows():
    r = m12[int(x.rule)]
    if '-'.join(map(str, r['k_c'])) != x.k_c or r['k_star'] != x.kstar or r['m_cycles'] != x.cycles:
        bad.append(int(x.rule))
lines.append(f'fw_n12_classes.csv: {len(c12)} classes, k_c/k*/cycles mismatches {bad}')
bad = []
for _, x in a12.iterrows():
    r = m12[int(x.rep)]
    if '-'.join(map(str, sorted(r['k_c']))) != '-'.join(map(str, sorted(map(int, x.k_c.split('-'))))) or r['k_star'] != x.kstar:
        bad.append(int(x.rule))
lines.append(f'fw_n12_all_rules.csv: {len(a12)} rules, k* and multiset of k_c vs representative: mismatches {bad}')
# n = 12 all 256 rules directly by route (b) (cheap) for the k_c vector itself
Nc = eca.code_counts(12)
import route_b
bad = []
for _, x in a12.iterrows():
    r = route_b.orders_route_b(int(x.rule), 12, Nc)
    if '-'.join(map(str, r['k_c'])) != x.k_c or r['k_star'] != x.kstar or r['m_cycles'] != x.cycles:
        bad.append(int(x.rule))
lines.append(f'fw_n12_all_rules.csv: all 256 rules recomputed by route (b): k_c/k*/cycles mismatches {bad}')
# GTH file (their numeric check) vs my numeric GTH at the same eps
g = pd.read_csv('../data/fw_n12_gth.csv')
G = eca.read_jsonl('out/route_a_n12_w1.jsonl') + eca.read_jsonl('out/route_a_n12_w2.jsonl')
lines.append(f'fw_n12_gth.csv rules: {g.rule.tolist()}')
for _, x in g.iterrows():
    eps = [float(e) for e in str(x.eps).split()]
    num = [float(v) for v in str(x.nu_min_at).split()]
    mineg = {gg['eps']: min(gg['nu']) for gg in G if gg['rule'] == x.rule}
    if all(e in mineg for e in eps):
        lines.append(f'  rule {x.rule}: nu_min file {num} vs mine {[float("%.6g" % mineg[e]) for e in eps]}')
    else:
        lines.append(f'  rule {x.rule}: not in my GTH sample')
open('out/compare_data.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
