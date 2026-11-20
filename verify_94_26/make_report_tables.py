"""Builds verify_94_26/out/tables.md from the own output files (no number typed by hand)."""
import os, json
MO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
L = []
for f, title in (('test_94.json', 'Rule 94 (PROOF_94_converse.md), `test_94.py`'), ('test_26.json', 'Rule 26 (PROOF_26.md), `test_26.py`')):
    d = json.load(open(os.path.join(MO, f)))
    L.append(f'### {title}\n\n| test | statement tested | n | cases | violations |\n|---|---|---|---|---|')
    for r in d['results']:
        L.append(f"| {r['test']} | {r['statement']} | {r['n']} | {r['cases']} | {r['violations']} |")
    L.append(f"\nAll passed: {d['all_passed']}. CPU time {d['cpu_seconds']} s.\n")
m94 = json.load(open(os.path.join(MO, 'mutate_94.json')))
m26 = json.load(open(os.path.join(MO, 'mutate_26.json')))
L.append('### Mutation checks (`mutate_94.py`, `mutate_26.py`): deliberately wrong statements, violations found\n')
L.append('| rule | wrong statement injected | violations per test |\n|---|---|---|')
for rule, mm in ((94, m94), (26, m26)):
    for k, v in mm.items():
        L.append(f"| {rule} | {k} | {', '.join(f'{a}: {b}' for a, b in v)} |")
p = json.load(open(os.path.join(MO, 'potentials.json')))
L.append('\n### Potentials from the definitions (`check_potentials.py`; Theorem A not used)\n')
L.append(f"Edmonds (networkx) against brute force over all in-trees: {p['edmonds_vs_bruteforce']}\n")
L.append('| rule | n | m | gamma_min | gamma_min = m-1 | selected | closed classes (sizes) | S = union of closed classes | G1 = pairs with V = 1 | k_c, c = 0..7 | k* |\n|---|---|---|---|---|---|---|---|---|---|---|')
for r in p['rows']:
    L.append(f"| {r['rule']} | {r['n']} | {r['m']} | {r['gamma_min']} | {r['gamma_min_eq_m_minus_1']} | {r['S_size']} | {r['closed_sizes']} | {r['S_eq_union_closed']} | {r['g1_equals_V1']} | {r['k']} | {r['kstar']} |")
L.append('\nRule 26, n = 4, 8 (every root):\n')
for r in p['rows']:
    if 'thm3c_gamma' in r:
        L.append(f"* n = {r['n']}: V({{0}}, C) histogram {r['V0_hist']}; gamma by kind {r['gamma_by_kind']}; Theorem 3(c) holds for every root: {r['thm3c_gamma']}; R({{0}} -> D_c) = {r['R0']}")
q = json.load(open(os.path.join(MO, 'potentials_16.json')))
L.append(f"\nRule 26, n = 16 (`check_potentials_16.py`, {len(q['roots'])} of {q['m']} roots by Edmonds, wall {q['wall_seconds']} s): m = {q['m']}; "
         f"min V({{0}}, C) = {q['min_V_out_of_zero']}, hence gamma(C) >= {q['lower_bound_gamma_nonzero']} for every C != {{0}}; gamma({{0}}) = {q['gamma_zero']}; "
         f"V({{0}}, C) histogram {q['V0_hist']}; cycles at resistance 2: {q['T2']} (kinds {q['T2_kinds']}); reachable from them in G1: {q['reachable_from_T2']}; "
         f"the three cycles with 111: V from {{0}} = {q['c111_V_from_zero']}, reachable from T2: {q['c111_reachable_from_T2']}; "
         f"Theorem 3(c) on the computed roots: {q['thm3c_on_computed_roots']}; k_c = {q['k']} (exact by the bound: {q['k_exact']}).\n")
L.append('| root | kind | in T2 | reachable from T2 | gamma | seconds |\n|---|---|---|---|---|---|')
for x in q['roots']:
    L.append(f"| {x['root']} | {x['kind']} | {x['in_T2']} | {x['reachable_from_T2']} | {x['gamma']} | {x['seconds']} |")
rm = json.load(open(os.path.join(MO, 'remarks.json')))
L.append(f"\n### Side remarks (`check_remarks.py`)\n\n* rule 94, states without 101: walls evolve one step by rule 18: {rm['walls_rule18_one_step']}\n* rule 26, carrier words: c = (n + 4p)/3: {rm['carrier_c_formula']}\n")
c = json.load(open(os.path.join(MO, 'compare.json')))
L.append(f"### Comparison with `proofs_94_26/out/` (`compare.py`, run last)\n\nfields compared: {c['compared']}; disagreements: {len(c['disagreements'])}. Field list: `verify_94_26/out/compare.md`.\n")
open(os.path.join(MO, 'tables.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L)[:3000])
