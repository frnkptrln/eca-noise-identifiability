"""Collect every number used in VERIFICATION_v02.md from the files in verify_v02/out (and data/ where a claim is quoted).
Writes out/facts.json."""
import json, glob, re, math
import numpy as np, pandas as pd
import eca
F = {}
S = json.load(open('SAMPLE.json'))
F['seed'] = S['seed']; F['seed_big'] = S['seed_big']; F['cap'] = S['cap_cycles']
F['n12_drawn'] = S['n12_drawn']; F['n17'] = S['n17']; F['n20'] = S['n20']
F['m17_max'] = S['n17_maxcycle_m']; F['m20_max'] = S['n20_maxcycle_m']
# route (a) exact
for n in (4, 5):
    R = eca.read_jsonl(f'out/exact_n{n}.jsonl')
    F[f'exact_n{n}_classes'] = len(R); F[f'exact_n{n}_check_ok'] = sum(r['exact_check_eps_1_7'] for r in R)
    F[f'exact_n{n}_kstar_hist'] = {int(k): int(v) for k, v in pd.Series([r['k_star'] for r in R]).value_counts().sort_index().items()}
    F[f'exact_n{n}_sec'] = round(sum(r['sec'] for r in R), 1)
    B = {r['rule']: r for r in eca.read_jsonl(f'out/route_b_n{n}.jsonl')}
    F[f'ab_n{n}_mismatch'] = [r['rule'] for r in R if r['k_c'] != B[r['rule']]['k_c']]
G = eca.read_jsonl('out/route_a_n12_w1.jsonl') + eca.read_jsonl('out/route_a_n12_w2.jsonl')
F['gth12_solves'] = len(G); F['gth12_maxres'] = max(g['max_rel_resid'] for g in G); F['gth12_sec_max'] = max(g['sec'] for g in G)
sr = pd.read_csv('out/sample_results.csv'); s12 = sr[sr.n == 12]
F['ab_n12_mismatch'] = s12[~s12.agree].rule.tolist(); F['ab_n12_slope_dev'] = float(s12.slope_dev_1e6_1e9.max())
F['ab_n12_kstar'] = {int(r.rule): int(r.k_star_b) for r in s12.itertuples()}
big = pd.read_csv('out/sample_results_n17_n20.csv')
F['big'] = [dict(n=int(r.n), rule=int(r.rule), m=int(r.m_cycles), k_c=r.k_c_b, kstar=int(r.k_star_b), sel=int(r.n_cycles_order0),
                 sec=float(r.sec), rss=float(r.maxrss_MB), consistent=bool(r.consistent)) for r in big.itertuples()]
# validation of the reduction
val = 0; valbad = 0
for n in range(4, 11):
    for r in eca.read_jsonl(f'out/route_b_n{n}.jsonl'): val += 1; valbad += (not r['full_tropical_equal_all_states'])
for n in (11, 12):
    for r in eca.read_jsonl(f'out/route_b_n{n}_w1.jsonl') + eca.read_jsonl(f'out/route_b_n{n}_w2.jsonl'): val += 1; valbad += (not r['full_tropical_equal_all_states'])
F['reduction_validated_pairs'] = val; F['reduction_validated_bad'] = valbad
F['compare_data'] = open('out/compare_data.txt').read().strip().split('\n')
cs = pd.read_csv('out/compare_fw_sweep.csv'); F['fw_sweep_pairs'] = len(cs); F['fw_sweep_bad'] = int((~cs.ok).sum())
# certificates
C = eca.read_jsonl('out/cert_check_w1.jsonl') + eca.read_jsonl('out/cert_check_w2.jsonl')
c12 = [r for r in C if r['file'].startswith('rule_')]; csw = [r for r in C if r['file'].startswith('n')]
F['cert12'] = len(c12); F['cert12_ok'] = sum(r['ok'] for r in c12); F['cert12_stubs'] = sum(bool(r.get('stub')) for r in c12)
F['cert12_stub_rules'] = sorted(r['rule'] for r in c12 if r.get('stub'))
F['certsw'] = len(csw); F['certsw_ok'] = sum(r['ok'] for r in csw); F['cert_max_m'] = max(r['m'] or 0 for r in C)
F['cert_nrange'] = [min(r['n'] for r in csw), max(r['n'] for r in csw)]
F['cert_sec'] = round(sum(r['sec'] for r in C), 1)
first = eca.read_jsonl('../verify_v02/logs/cert_check_firstpass_w1.jsonl') + eca.read_jsonl('../verify_v02/logs/cert_check_firstpass_w2.jsonl')
F['cert_firstpass_fail'] = sum(not r['ok'] for r in first)
T = eca.read_jsonl('out/tamper_test.jsonl'); F['tamper_n'] = sum(r['tamper'] != 'none' for r in T); F['tamper_accepted'] = sum(r['ok'] for r in T if r['tamper'] != 'none')
F['tamper_kinds'] = sorted({r['tamper'] for r in T if r['tamper'] != 'none'})
sw = pd.read_csv('out/compare_switching_n15_n20.csv'); F['switch_runs'] = len(sw); F['switch_bad'] = int((~sw.ok).sum())
F['switch_sec_max'] = float(sw.sec.max()); F['switch_rss_max'] = float(sw.maxrss_MB.max()); F['switch_cpu'] = round(float(sw.sec.sum()))
# 106
F['r106'] = json.load(open('out/rule106_summary.json'))
r106b = [r for r in eca.read_jsonl('out/route_b_n12_w1.jsonl') + eca.read_jsonl('out/route_b_n12_w2.jsonl') if r['rule'] == 106][0]
F['r106_cycles'] = r106b['m_cycles']; F['r106_selected'] = sum(v == 0 for v in r106b['cycle_orders'])
# affine
aff = pd.read_csv('out/affine_check.csv'); F['affine_rows'] = len(aff); F['affine_classes'] = sorted(aff.rule.unique().tolist())
F['affine_compare'] = open('out/compare_affine.txt').read().strip().split('\n')
F['affine_n3'] = open('out/affine_n3.txt').read().strip().split('\n')
for r in (60, 90):
    x = aff[aff.rule == r]
    F[f'aff{r}_nonuniform'] = x[x.uniform_marginals == 0].n.tolist(); F[f'aff{r}_nilpotent'] = x[x.L_nilpotent == 1].n.tolist()
# text checks
F['check_text'] = open('out/check_text.txt').read().strip().split('\n')
F['check_cost'] = open('out/check_cost.txt').read().strip().split('\n')
F['manifest'] = open('out/manifest_check.txt').read().strip().split('\n')
# Bagnoli
F['bag17'] = open('out/bagnoli_n17_summary.txt').read().strip().split('\n')
F['bag_census'] = open('out/bagnoli_census_summary.txt').read().strip().split('\n')
bc = pd.read_csv('out/bagnoli_n17_compare.csv'); F['bag17_dSmax'] = float(bc.dS.max())
json.dump(F, open('out/facts.json', 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('facts:', len(F))
