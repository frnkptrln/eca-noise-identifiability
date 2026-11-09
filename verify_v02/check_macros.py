"""Every macro of note/numbers_v02.tex against a value recomputed from own outputs (or from data/ where the macro
counts a property of the work's own files, marked 'file'). Writes out/check_macros.txt."""
import re, json, math, glob
import pandas as pd, eca
mac = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^}]*)\}', open('../note/numbers_v02.tex').read()))
sw = pd.read_csv('../data/fw_sweep.csv'); K = sw.pivot(index='rule', columns='n', values='kstar')
mine12 = {r['rule']: r for r in eca.read_jsonl('out/route_b_n12_w1.jsonl') + eca.read_jsonl('out/route_b_n12_w2.jsonl')}
cs = pd.read_csv('../data/class_summary.csv')
typ = {r: ('B' if cs[cs.rule == r].limit_type.iloc[0].startswith('B') else ('UR' if cs[cs.rule == r].rising.iloc[0] == 1 else 'UF')) for r in mine12}
U = [r for r in mine12 if typ[r] != 'B']
agree = [r for r in mine12 if (typ[r] == 'UR') == (mine12[r]['k_star'] == 0)]
s106 = json.load(open('out/rule106_summary.json'))
ge8 = K[[n for n in K.columns if n >= 8]]
vary = sorted(int(r) for r in ge8.index[((ge8 == 0).any(axis=1)) & ((ge8 >= 1).any(axis=1))])
C = eca.read_jsonl('out/cert_check_w1.jsonl') + eca.read_jsonl('out/cert_check_w2.jsonl')
vo = pd.read_csv('../data/fw_verify_orders.csv'); vt = pd.read_csv('../data/fw_verify_trees.csv')
pred = pd.read_csv('../data/fw_n12_vs_v01.csv') if 'k_from_ratio' in open('../data/fw_n12_vs_v01.csv').readline() else None
want = {
 'NumClasses': len(mine12), 'NumUclasses': len(U), 'NumUrisingVtwo': sum(mine12[r]['k_star'] == 0 for r in U),
 'NumUfallingVtwo': sum(mine12[r]['k_star'] >= 1 for r in U), 'NumAgreeVone': len(agree),
 'FlipRules': ', '.join(str(r) for r in sorted(mine12) if r not in agree),
 'NumBkOne': sum(mine12[r]['k_star'] == 1 for r in mine12 if typ[r] == 'B'), 'NumBkTwo': sum(mine12[r]['k_star'] == 2 for r in mine12 if typ[r] == 'B'),
 'NumBkThree': sum(mine12[r]['k_star'] == 3 for r in mine12 if typ[r] == 'B'),
 'RuleOneOhSixStable': sum(v == 0 for v in mine12[106]['cycle_orders']), 'RuleOneOhSixCycles': mine12[106]['m_cycles'],
 'RuleOneOhSixNuLimit': f"{s106['a_limit']:.4f}", 'RuleOneOhSixEpsStar': 'v0.1 value 0.0095 (own fit %.5f)' % s106['eps_star_fit'],
 'RuleOneOhSixRhoStar': f"{s106['rho_star_fit']:.3f}", 'RuleOneOhSixCrossExp': str(round(s106['log10_crossing'])),
 'SweepNmin': int(K.columns.min()), 'SweepNmax': int(K.columns.max()), 'SweepVaryCount': len(vary),
 'SweepAllZero': int((ge8 == 0).all(axis=1).sum()), 'SweepAllFall': int((ge8 >= 1).all(axis=1).sum()),
 'VerifyNmax': f'file: {int(vo.n.max())}', 'VerifyRows': f'file: {len(vo)}', 'VerifyTreesRows': f'file: {len(vt)}',
 'CertsNtwelve': sum(r['ok'] for r in C if r['file'].startswith('rule_')), 'CertsSweep': sum(r['ok'] for r in C if r['file'].startswith('n')),
 'SweepVaryRules': ', '.join(map(str, vary)),
}
# KpredOK: number of classes whose sealed predicted k equals k* (PREDICTIONS.md table: | rule | type | ratio | k_cont | k_pred |)
pt = re.findall(r'^\| (\d+) \| (?:B|U[^|]*) \| [-\d.]+ \| [-\d.]+ \| (\d+) \|', open('../PREDICTIONS.md').read(), re.M)
want['KpredOK'] = f"{sum(int(k) == mine12[int(r)]['k_star'] for r, k in pt)} of {len(pt)} (PREDICTIONS.md table vs own k*)"
L = []
for k, v in mac.items():
    w = want.get(k, 'NOT RECOMPUTED')
    ok = (str(w) == v) or (isinstance(w, str) and (w.endswith(': ' + v) or w.startswith(v + ' ') or ('own fit' in w and abs(float(v) - s106['eps_star_fit']) < 5e-4)))
    L.append(f"{'OK  ' if ok else 'DIFF'} \\{k} = {v}  | own: {w}")
open('out/check_macros.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
