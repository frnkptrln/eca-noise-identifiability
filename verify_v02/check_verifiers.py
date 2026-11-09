"""Report Section 4 claims against the work's own verifier files; extra derived facts. Writes out/check_verifiers.json."""
import json, glob, subprocess
import pandas as pd, eca
o = pd.read_csv('../data/fw_verify_orders.csv'); t = pd.read_csv('../data/fw_verify_trees.csv')
c = pd.read_csv('../data/fw_n12_checks.csv'); g = pd.read_csv('../data/fw_n12_gth.csv'); sw = pd.read_csv('../data/fw_sweep.csv')
V = dict(orders_rows=len(o), orders_n=[int(o.n.min()), int(o.n.max())], orders_max_dev_pi=float(o.max_dev_pi.max()),
         orders_max_dev_nu=float(o.max_dev_nu.max()), orders_ok=bool(o.ok.all()),
         trees_rows=len(t), trees_by_method={m: [int(len(x)), int(x.n.min()), int(x.n.max())] for m, x in t.groupby('method')},
         trees_mismatches=int(t.mismatches.sum()), trees_wmin_eq_gmin=bool((t.Wmin == t.gmin).all()),
         gth12_max_dev=float(g.max_dev_nu_last.max()),
         checks={k: [int(x.ok.sum()), int(len(x))] for k, x in c.groupby('check')})
bij = sw[(sw.n <= 14) & (sw.bijective == 1)]
C = eca.read_jsonl('out/cert_check_w1.jsonl') + eca.read_jsonl('out/cert_check_w2.jsonl')
V['sweep_certs_plus_bijective'] = sum(1 for r in C if r['file'].startswith('n')) + len(bij)
V['pairs_n4_14'] = int(len(sw[sw.n <= 14]))
first = eca.read_jsonl('logs/cert_check_firstpass_w1.jsonl') + eca.read_jsonl('logs/cert_check_firstpass_w2.jsonl')
V['firstpass_c10_only'] = sum(1 for r in first if r['fails'] == ['C10']); V['firstpass_exc'] = sum(1 for r in first if any(f.startswith('EXC') for f in r['fails']))
# unique independently recomputed pairs at n >= 15
pairs = set()
for f in glob.glob('out/route_b_switch_n*') + glob.glob('out/route_b_n17.jsonl.*') + glob.glob('out/route_b_n20.jsonl.*'):
    for r in eca.read_jsonl(f): pairs.add((r['n'], r['rule']))
V['indep_pairs_ge15'] = len(pairs)
# 106: non-selected cycles, argmin of rho on the small grid
r = [x for x in eca.read_jsonl('out/route_b_n12_w1.jsonl') + eca.read_jsonl('out/route_b_n12_w2.jsonl') if x['rule'] == 106][0]
V['r106_nonselected'] = [(r['cycle_min_state'][i], r['cycle_lengths'][i]) for i in range(r['m_cycles']) if r['cycle_orders'][i] > 0]
s = json.load(open('out/rule106_summary.json'))
V['r106_rho_min_eps'] = min(s['rho_small'], key=lambda p: p[1])[0]
# Bagnoli census details
B = []
for f in glob.glob('out/bagnoli_census_n*') + ['out/bagnoli_n17_w1.jsonl', 'out/bagnoli_n17_w2.jsonl']:
    B += eca.read_jsonl(f)
d = pd.DataFrame(B).merge(sw[['n', 'rule', 'n_stable', 'kstar']], on=['n', 'rule'])
many = d[d.n_closed > 1]
V['census_pairs'] = len(d); V['census_many_per_n'] = {int(n): int(len(x)) for n, x in many.groupby('n')}
V['census_many_range'] = [int(min(V['census_many_per_n'].values())), int(max(V['census_many_per_n'].values()))]
wrong = many[many.support_size != many.n_stable]
V['census_wrong_support'] = [dict(n=int(x.n), rule=int(x.rule), closed_sizes=x.closed_sizes, support=int(x.support_size), n_stable=int(x.n_stable)) for x in wrong.itertuples()]
V['census_verdict_wrong'] = int(((d.support_cover_mask == 255) != (d.kstar == 0)).sum())
V['census_one_class_stable_eq_closed'] = int(((d.n_closed == 1) & (d.closed_sizes.apply(lambda s: s[0] if len(s) == 1 else -1) == d.n_stable)).sum())
V['census_one_class'] = int((d.n_closed == 1).sum())
cc = {(x['n'], x['rule']): x['m_cycles'] for x in eca.read_jsonl('out/cycle_counts_n17_n20.jsonl')}
V['not_recomputed_n17'] = sorted(r for (n, r), m in cc.items() if n == 17 and (n, r) not in pairs)
V['not_recomputed_n20'] = sorted(r for (n, r), m in cc.items() if n == 20 and (n, r) not in pairs)
V['over_cap_n20'] = sorted(r for (n, r), m in cc.items() if n == 20 and m > 20000)
V['over_cap_n17'] = sorted(r for (n, r), m in cc.items() if n == 17 and m > 20000)
aff = pd.read_csv('out/affine_check.csv'); V['affine_n'] = [int(aff.n.min()), int(aff.n.max())]; V['affine_nclasses'] = int(aff.rule.nunique())
man = [l.split()[1] for l in open('../data/MANIFEST.sha256') if l.strip()]
V['manifest_n'] = len(man); V['manifest_cert_entries'] = sum(1 for p in man if p.startswith('fw_certificates'))
V['git_log'] = subprocess.run(['git', 'log', '--format=%h %ad %an <%ae> %s', '--date=short', '9ce96c6'], capture_output=True, text=True, cwd='..').stdout.strip().split('\n')
V['git_trailers'] = subprocess.run(['git', 'log', '--format=%(trailers)', 'b8ce5a5..9ce96c6'], capture_output=True, text=True, cwd='..').stdout.strip()
json.dump(V, open('out/check_verifiers.json', 'w'), indent=1, default=str)
print(json.dumps({k: V[k] for k in V if k not in ('git_log',)}, default=str)[:3000])
