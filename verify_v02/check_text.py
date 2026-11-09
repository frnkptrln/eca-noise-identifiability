"""Step 7: recompute the numbers of report.md / numbers_v02.tex from data files and own outputs.
Writes out/check_text.txt (one line per claim: OK/DIFF, claim, value)."""
import re, math, json
import numpy as np, pandas as pd
import eca
L = []
def claim(ok, text):
    L.append(('OK   ' if ok else 'DIFF ') + text)
sw = pd.read_csv('../data/fw_sweep.csv')
K = sw.pivot(index='rule', columns='n', values='kstar')
# per-n counts of k* = 0
cnt = {n: int((K[n] == 0).sum()) for n in K.columns}
rep_cnt = {4: 16, 5: 26, 6: 22, 7: 30, 8: 24, 9: 27, 10: 30, 11: 32, 12: 28, 13: 30, 14: 30, 15: 27, 16: 25, 17: 32, 18: 29, 19: 30, 20: 30}
claim(cnt == rep_cnt, f'report s7 per-n counts of k*=0: {cnt}')
ge8 = K[[n for n in K.columns if n >= 8]]
allz = int((ge8 == 0).all(axis=1).sum()); allf = int((ge8 >= 1).all(axis=1).sum())
vary = sorted(int(r) for r in ge8.index[((ge8 == 0).any(axis=1)) & ((ge8 >= 1).any(axis=1))])
claim((allz, allf, len(vary)) == (20, 55, 13), f'n>=8: all k*=0 {allz}, all k*>=1 {allf}, switching {len(vary)} {vary}')
claim(vary == [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154], 'SweepVaryRules macro list equals switching set (n>=8)')
all_n = sorted(int(r) for r in K.index[((K == 0).any(axis=1)) & ((K >= 1).any(axis=1))])
claim(len(all_n) == 13, f'abstract "for n=4..20 ... 13 classes change side with the ring size": classes changing side over n=4..20 = {len(all_n)}: {all_n}')
# predictions 5(c)-(e)
s12 = (K[12] == 0)
diff47 = sorted(int(r) for r in K.index if any((K.loc[r, n] == 0) != s12[r] for n in range(4, 8)))
claim(len(diff47) == 27, f'5(d) classes differing at some n=4..7 from their n=12 status: {len(diff47)}')
keep = len([r for r in K.index if all((K.loc[r, n] == 0) == s12[r] for n in range(8, 21))])
claim(keep == 75, f'5(c) classes keeping their n=12 classification for every n>=8: {keep}')
fall_rows = ge8[(ge8 >= 1).all(axis=1)]
const = int((fall_rows.nunique(axis=1) == 1).sum())
claim((len(fall_rows), const) == (55, 53), f'5(e) k*>=1 for all n>=8: {len(fall_rows)}, constant value: {const}; non-constant: {sorted(int(r) for r in fall_rows.index[fall_rows.nunique(axis=1) > 1])}')
# switching table patterns
rep = open('../report.md').read()
sec7 = rep[rep.index('## 7. Ring sizes'):rep.index('## 8. Literature')]
def ranges(ns):
    ns = sorted(ns); out = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1: j += 1
        out.append(f'{ns[i]}' if i == j else f'{ns[i]}-{ns[j]}'); i = j + 1
    return ', '.join(out)
bad = []
for r in vary:
    z = [n for n in range(8, 21) if K.loc[r, n] == 0]; f = [n for n in range(8, 21) if K.loc[r, n] >= 1]
    row = re.search(rf'^\| {r} \| ([^|]*) \| ([^|]*) \|', sec7, re.M)
    if not row or row.group(1).strip() != ranges(z) or row.group(2).strip() != ranges(f): bad.append(r)
claim(not bad, f'switching table n-ranges vs fw_sweep.csv: mismatches {bad}')
# pattern labels
def pat(r):
    z = {n for n in range(8, 21) if K.loc[r, n] == 0}
    pats = []
    for dd in range(2, 9):
        if z == {n for n in range(8, 21) if n % dd}: pats.append(f'k*>=1 iff {dd}|n')
        if z == {n for n in range(8, 21) if n % dd == 0}: pats.append(f'k*=0 iff {dd}|n')
    if z == {n for n in range(8, 21) if n & (n - 1)}: pats.append('k*>=1 iff n power of 2')
    return pats
claim(True, 'own pattern labels (n=8..20): ' + '; '.join(f'{r}: {pat(r) or "none"}' for r in vary))
# full k* table in the report
tab = sec7[sec7.index('Full k* table'):]
bad = []
for r in K.index:
    m = re.search(rf'^\| {r} \|(.*)\|$', tab, re.M)
    vals = [int(v) for v in m.group(1).split('|')]
    if vals != [int(K.loc[r, n]) for n in range(4, 21)]: bad.append(r)
claim(not bad, f'report full k* table (88 x 17) vs fw_sweep.csv: mismatching rows {bad}')
# own sample vs that table (n = 17, 20)
for n in (17, 20):
    for w in ('w1', 'w2'):
        for rr in eca.read_jsonl(f'out/route_b_n{n}.jsonl.{w}'):
            claim(rr['k_star'] == K.loc[rr['rule'], n], f'own route (b) n={n} class {rr["rule"]}: k*={rr["k_star"]} vs table {K.loc[rr["rule"], n]}')
# ---- n = 12, against v0.1 files and own results
cs = pd.read_csv('../data/class_summary.csv'); es = pd.read_csv('../data/epsilon_star.csv')
mine12 = {r['rule']: r for r in eca.read_jsonl('out/route_b_n12_w1.jsonl') + eca.read_jsonl('out/route_b_n12_w2.jsonl')}
def v01type(r):
    x = cs[cs.rule == r].iloc[0]
    if x.limit_type.startswith('B'): return 'B'
    return 'U-rising' if x.rising == 1 else 'U-falling'
types = {r: v01type(r) for r in mine12}
dist = {t: dict(pd.Series([mine12[r]['k_star'] for r in mine12 if types[r] == t]).value_counts().sort_index()) for t in ('B', 'U-falling', 'U-rising')}
claim(dist['B'] == {1: 29, 2: 5, 3: 8} and dist['U-falling'] == {0: 1, 1: 17, 2: 1} and dist['U-rising'] == {0: 27},
      f'report s5 k* distribution by v0.1 type (own k*): { {t: {int(k): int(v) for k, v in d.items()} for t, d in dist.items()} }')
U = [r for r in mine12 if types[r] != 'B']
claim((len(U), sum(mine12[r]['k_star'] == 0 for r in U)) == (46, 28), f'46 U classes: {len(U)}, k*=0: {sum(mine12[r]["k_star"] == 0 for r in U)}')
agree = [r for r in mine12 if (types[r] == 'U-rising') == (mine12[r]['k_star'] == 0)]
claim(len(agree) == 87 and [r for r in mine12 if r not in agree] == [106], f'agree with v0.1 trend: {len(agree)}, exceptions {[r for r in mine12 if r not in agree]}')
lam = lambda e: (1 - 2 * e) * math.log((1 - e) / e)
s5 = rep[rep.index('| class | v0.1 |'):rep.index('## 6.')]
bad = {}
Nc = eca.code_counts(12)
import route_b
for r in sorted(mine12):
    m = re.search(rf'^\| {r} \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|', s5, re.M)
    g = [x.strip() for x in m.groups()]
    me = mine12[r]
    exp_ratio = 2 ** me['k_star'] * lam(0.002) / lam(0.001)
    v01ratio = float(es[es.rule == r].rho_ratio_0002_over_0001.iloc[0])
    res, h, V = route_b.orders_route_b(r, 12, Nc, return_states=True)
    F, cid, cycles = route_b.cycle_structure(r, 12)
    hc = np.array(res['cycle_orders']) if 'cycle_orders' in res else None
    sel = int((hc == 0).sum())
    if me['k_star'] >= 1:
        cover = ','.join(format(c, '03b') for c in range(8) if me['k_c'][c] == me['k_star'])
    else:
        # covering cycles named by smallest state/period: they must be noise-selected and cover all codes
        ok_cov = True; mask = 0
        if g[7] == 'all':
            ok_cov = sel == len(cycles); mask = 255
        else:
            for item in g[7].split(';'):
                s, p = item.split('/p'); s = int(s); p = int(p)
                i = cid[s]
                if i < 0 or cycles[i].min() != s or len(cycles[i]) != p or hc[i] != 0: ok_cov = False
                else:
                    for c in range(8):
                        if np.any(Nc[c, cycles[i]] > 0): mask |= 1 << c
        cover = g[7] if (ok_cov and mask == 255) else 'INVALID'
    want = [types[r], f'{v01ratio:.3f}', f'{exp_ratio:.3f}', str(me['k_star']), '-'.join(map(str, me['k_c'])), str(me['m_cycles']), str(sel), cover,
            'yes' if r in agree else '**no**']
    if g != want:
        bad[r] = (g, want)
claim(not bad, f'report s5 table, 88 rows x 9 columns recomputed (v0.1 files + own orders): mismatching rows {bad}')
# weak cases: noise-selected cycles of 7, 19, 23, 232
for r in (7, 19, 23, 232):
    me = mine12[r]
    selc = [(me['cycle_min_state'][i], me['cycle_lengths'][i]) for i in range(me['m_cycles']) if me['cycle_orders'][i] == 0]
    claim(True, f'class {r}: noise-selected cycles (min state, period) {selc}')
# rule 106
s = json.load(open('out/rule106_summary.json'))
claim(abs(s['a_limit'] - 0.0472) < 5e-5, f'106 limit of min nu: own {s["a_limit"]:.6f} (report 0.0472)')
claim(True, f'106 linear coefficient b/a: own (secant 1e-8..1e-9) {s["b_over_a"]:.1f}; secant from 1e-4: {(s["nu_min_small"][0][1] - s["a_limit"]) / (s["a_limit"] * 1e-4):.1f} (report "about 4102")')
claim(round(s['log10_crossing']) == -57, f'106 crossing level 10^{s["log10_crossing"]:.2f} (report about 10^-57)')
claim(abs(s['rho_star_fit'] - 6.189) < 1e-3, f'106 local maximum: eps*={s["eps_star_fit"]:.5f}, rho*={s["rho_star_fit"]:.5f} (v0.1: 0.0095, 6.189)')
rs = [round(v, 5) for _, v in s['nu_min_small']]
claim(rs == [0.06653, 0.04909, 0.04736, 0.04719, 0.04717, 0.04717], f'106 min nu at 1e-4..1e-9 (5 digits): {rs}')
open('out/check_text.txt', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
