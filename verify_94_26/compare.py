"""Comparison of the own results (verify_94_26/out/) with the outputs of the session (proofs_94_26/out/), n <= 20.
Run only after all own tests (test_94.py, test_26.py, check_potentials*.py) had been written and run. Reads, changes nothing.
usage: python verify_94_26/compare.py      output: verify_94_26/out/compare.json, verify_94_26/out/compare.md"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SO = os.path.join(ROOT, 'proofs_94_26', 'out')
MO = os.path.join(HERE, 'out')


def jl(path):
    return {r['n']: r for r in (json.loads(l) for l in open(path))}


def ab(s):
    a, b = s.split(' of ')
    return int(a), int(b)


def norm(d):
    return {str(k): v for k, v in d.items()} if isinstance(d, dict) else d


rows = []


def cmp(rule, n, field, mine, theirs):
    rows.append(dict(rule=rule, n=n, field=field, mine=mine, theirs=theirs, agree=norm(mine) == norm(theirs)))


t94 = json.load(open(os.path.join(MO, 'test_94.json')))
my94 = {r['n']: r for r in next(x for x in t94['results'] if x['test'] == 'T2')['extra']}
s94 = jl(os.path.join(SO, 'g1_classes_94.jsonl'))
for n, m in sorted(my94.items()):
    s = s94.get(n)
    if s is None:
        continue
    for mf, sf in (('cycles', 'cycles'), ('periodic_states', 'periodic_states'), ('g1_edges', 'g1_edges'),
                   ('sccs', 'strong_components'), ('closed_sizes', 'closed_classes'), ('block_words', 'block_words'),
                   ('block_words_one_scc', 'block_words_in_one_component'),
                   ('K_eq_reach_from_block_words', 'K_equals_cycles_reachable_from_block_words'),
                   ('zero_in_K', 'zero_state_in_K'), ('edges_into_zero', 'zero_state_in_degree'),
                   ('codes_on_K', 'codes_on_K'), ('periods_no101_in_K', 'periods_without_101_in_K'),
                   ('periods_no101_outside_K', 'periods_without_101_outside_K')):
        cmp(94, n, sf, m[mf], s[sf])
    a, b = ab(m['cycles_with_101_in_K'])
    cmp(94, n, 'cycles_with_101_in_K / cycles_with_101', [a, b], [s['cycles_with_101_in_K'], s['cycles_with_101']])
    a, b = ab(m['dw_cycles_in_K'])
    cmp(94, n, 'cycles_without_101_in_K (= doubled-word cycles in K + [0 in K])', a + int(m['zero_in_K']), s['cycles_without_101_in_K'])
c94 = json.load(open(os.path.join(SO, 'check_lemmas_94.json')))
myL9 = next(x for x in t94['results'] if x['test'] == 'L9n')['extra']
cmp(94, '3..20', 'periodic states with empty frozen set (L9 counts)', myL9, c94['L9']['counts'])
myL8 = next(x for x in t94['results'] if x['test'] == 'L8')['extra']
theirs_L8 = {str(w): sorted(''.join(map(str, s)) if not isinstance(s, str) else s for orb in v for s in (orb if isinstance(orb, list) else [orb]))
             for w, v in c94['L8'].get('live_orbits', {}).items()}
cmp(94, 'w=1..22', 'live window states (L8)', {str(k): v for k, v in myL8.items()}, theirs_L8)

t26 = json.load(open(os.path.join(MO, 'test_26.json')))
my26 = {r['n']: r for r in next(x for x in t26['results'] if x['test'] == 'T5')['extra']}
s26 = jl(os.path.join(SO, 'g1_26.jsonl'))
for n, m in sorted(my26.items()):
    s = s26.get(n)
    if s is None:
        continue
    for mf, sf in (('cycles', 'cycles'), ('periodic_states', 'periodic_states'), ('g1_edges', 'g1_edges'),
                   ('closed_sizes', 'closed_classes'), ('zero_in_K', 'zero_in_the_closed_class'),
                   ('domain_in_K', 'domain_cycles_in_K'), ('c111_in_K', 'cycles_with_111_in_K'),
                   ('codes_on_K', 'codes_on_K'), ('c_domain', 'c_of_domain_cycles'), ('c_111', 'c_of_cycles_with_111'),
                   ('cycles_111_through_carrier', 'cycles_with_111_through_a_carrier_word')):
        cmp(26, n, sf, m[mf], s[sf])
    a, b = ab(m['one_parity_in_K'])
    cmp(26, n, 'one_parity_cycles_in_K (without {0})', f'{a - int(m["zero_in_K"])} of {b - 1}', s['one_parity_cycles_in_K'])
    if s.get('max_increase_of_c_along_a_G1_edge') is not None:
        cmp(26, n, 'max_increase_of_c_along_a_G1_edge', m['max_c_increase_along_edge'], s['max_increase_of_c_along_a_G1_edge'])
    kinds = {k: v for k, v in dict(domain=m['domain_cycles'], with_111=m['cycles_with_111'], zero=1,
                                    one_parity=m['one_parity_cycles_not_zero']).items() if v}
    theirs_k = {k: v for k, v in s['cycles_by_kind'].items() if v}
    cmp(26, n, 'cycles_by_kind', kinds, theirs_k)
c26 = json.load(open(os.path.join(SO, 'check_lemmas_26.json')))
myM3 = next(x for x in t26['results'] if x['test'] == 'M3c')['extra']['domain_state_counts']
cmp(26, '4..18', 'domain states (M3 counts)', myM3, c26['M3']['domain_states'])
for n, kd in c26['M5']['periodic_states_by_kind'].items():
    mk = dict(my26[int(n)]['periodic_by_kind'])
    mk['with_111'] = mk.pop('orbit_111')
    cmp(26, int(n), 'periodic states by kind', mk, kd)
# potentials (Table 3 of PROOF_26)
pot = json.load(open(os.path.join(MO, 'potentials.json')))
p16 = json.load(open(os.path.join(MO, 'potentials_16.json')))
for r in pot['rows']:
    if r['rule'] == 26 and r['n'] in (4, 8):
        s = s26[r['n']]
        cmp(26, r['n'], 'k_c_from_the_definition', r['k'], s['k_c_from_the_definition'])
        cmp(26, r['n'], 'V_from_zero_hist', r['V0_hist'], s['V_from_zero_hist'])
        cmp(26, r['n'], 'gamma_by_kind', r['gamma_by_kind'], s['gamma_by_kind'])
        cmp(26, r['n'], 'R_from_zero_to_code', r['R0'], s['R_from_zero_to_code'])
s = s26[16]
cmp(26, 16, 'k_c_from_the_definition', p16['k'], s['k_c_from_the_definition'])
cmp(26, 16, 'V_from_zero_hist', p16['V0_hist'], s['V_from_zero_hist'])
cmp(26, 16, 'R_from_zero_to_code', p16['R0'], s['R_from_zero_to_code'])
cmp(26, 16, 'T2_cycles', p16['T2'], s['T2_cycles'])
cmp(26, 16, 'cycles_reachable_from_T2', p16['reachable_from_T2'], s['cycles_reachable_from_T2'])
cmp(26, 16, 'gamma of {0}', p16['gamma_zero'], s['gamma_zero'])
mine_g = {'zero': sorted({x['gamma'] for x in p16['roots'] if x['kind'] == 'zero'}),
          'domain': sorted({x['gamma'] for x in p16['roots'] if x['kind'] == 'domain'}),
          'with_111': sorted({x['gamma'] for x in p16['roots'] if x['kind'] == 'with_111'})}
cmp(26, 16, 'gamma by kind (own: 16 of 552 roots)', mine_g, s['gamma_by_kind'])

dis = [r for r in rows if not r['agree']]
json.dump(dict(compared=len(rows), disagreements=dis, rows=rows), open(os.path.join(MO, 'compare.json'), 'w'), indent=1, default=str)
with open(os.path.join(MO, 'compare.md'), 'w') as fh:
    fh.write(f'# Own results vs proofs_94_26/out (n <= 20)\n\nfields compared: {len(rows)}; disagreements: {len(dis)}\n\n')
    fh.write('| rule | n | field | own | session | agree |\n|---|---|---|---|---|---|\n')
    for r in rows:
        fh.write(f"| {r['rule']} | {r['n']} | {r['field']} | {r['mine']} | {r['theirs']} | {r['agree']} |\n")
print('compared', len(rows), 'disagreements', len(dis))
for r in dis:
    print(r)
