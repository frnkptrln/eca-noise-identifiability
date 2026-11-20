"""Builds out/tables_94.md and out/tables_26.md from the output files of the other scripts of this folder.
The sections "Computations" of PROOF_94_converse.md and PROOF_26.md are verbatim copies of these two files.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')


def jl(name):
    with open(os.path.join(OUT, name)) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def js(name):
    with open(os.path.join(OUT, name)) as fh:
        return json.load(fh)


def table(header, rows):
    lines = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    for r in rows:
        lines.append('| ' + ' | '.join(str(v) for v in r) + ' |')
    return '\n'.join(lines)


def lemma_table(d):
    rows = [(k, v['statement'].replace('|', '\\|'), v['n'], v['cases'], v['violations'])
            for k, v in d.items() if isinstance(v, dict)]
    return table(['test', 'statement tested', 'n', 'cases', 'violations'], rows)



def crosscheck_rows(keys):
    X = js('crosscheck_data.json')
    rows = []
    for k in keys:
        v = X[k]
        rows.append((v['source'], ', '.join(str(n) for n in v['ring_sizes']), v['fields'], len(v['disagreements'])))
    return X, table(['compared with', 'ring sizes n', 'fields compared', 'disagreements'], rows)

def tables_94():
    L = js('check_lemmas_94.json')
    G = jl('g1_classes_94.jsonl')
    C = js('chains_94.json')
    t = ['### Table 1. Exhaustive tests of the lemmas (`check_lemmas_94.py` -> `out/check_lemmas_94.json`)', '',
         lemma_table(L), '',
         'All tests passed: %s. CPU time %.2f s.' % (L['all_passed'], L['cpu_s']), '',
         'Live window orbits found (test L8), by width: ' +
         '; '.join('w = %s: %s' % (w, ', '.join('{' + ', '.join(o) + '}' for o in orbs)) for w, orbs in L['L8']['live_orbits'].items()) + '.',
         '',
         'Numbers of periodic states with empty frozen set (test L9), by n: ' +
         ', '.join('%s: %s' % (n, c) for n, c in L['L9']['counts'].items()) + '.', '',
         '### Table 2. G1 and its closed classes computed directly, 3 not dividing n (`g1_classes_94.py` -> `out/g1_classes_94.jsonl`)', '']
    rows = []
    for r in G:
        rows.append((r['n'], r['cycles'], r['periodic_states'], r['g1_edges'], r['strong_components'],
                     '%d %s' % (len(r['closed_classes']), r['closed_classes']), r['block_words'],
                     r['block_words_in_one_component'],
                     '%d of %d' % (r['cycles_with_101_in_K'], r['cycles_with_101']),
                     '%d of %d' % (r['cycles_without_101_in_K'], r['cycles_without_101']),
                     '%d of %d' % (r['cycles_without_101_in_K'] - int(r['zero_state_in_K']), r['cycles_without_101'] - 1),
                     r['periods_without_101_in_K'] or '-', r['periods_without_101_outside_K'] or '-',
                     r['zero_state_in_K'], r['zero_state_in_degree'], r['codes_on_K'],
                     r['K_equals_cycles_reachable_from_block_words'], r['cpu_s'], int(r['peak_rss_mb'])))
    t += [table(['n', 'cycles', 'periodic states', 'G1 edges', 'strong components', 'closed classes (sizes)', 'block words',
                 'block words in one strong component', 'cycles with 101 in K', 'cycles without 101 in K ({0} included)',
                 'cycles of doubled words in K', 'periods of the cycles without 101 in K (period: count)', 'periods of the cycles without 101 outside K',
                 '{0} in K', 'G1 edges into {0}', 'codes on K', 'K = cycles reachable from the block words', 'CPU s', 'peak MB'], rows),
          '',
          'K denotes the closed class (unique in every row). n = 4 is listed for comparison only; the theorems need n >= 5.', '',
          '### Table 3. The chains of the proofs, executed step by step (`chains_94.py` -> `out/chains_94.json`)', '',
          'Part A: every cycle. Growth flip for the cycles without 101, freezing chain to a block word (every flip joins two '
          'periodic states), and the digraph of swaps, merges and splits on the block words with every move executed.', '']
    rows = [(a['n'], a['cycles'], a['cycles_with_101'], a['growth_flips'], a['all_chains_end_on_a_block_word'],
             a['max_freezing_flips'], a['mean_freezing_flips'], a['block_words'], a['block_word_moves_executed'],
             a['block_word_graph_strongly_connected'], a['max_flips_block_word_to_canonical'],
             a['max_flips_canonical_to_block_word']) for a in C['part_A']]
    t += [table(['n', 'cycles', 'cycles with 101', 'growth flips', 'all chains end on a block word', 'max freezing flips',
                 'mean freezing flips', 'block words', 'moves executed', 'move graph strongly connected',
                 'max flips from a block word to l^b0 s^a0', 'max flips from l^b0 s^a0 to a block word'], rows), '',
          'Part B: cycles reached from 200 random states; freezing chain, sorting and merging down to l^b0 s^a0, chain to the '
          'cycle with the code 000 (Lemma 15).', '']
    rows = [(b['n'], b['start_states'], b['all_chains_end_on_the_cycle_with_code_000'], b['max_freezing_flips'],
             b['max_sorting_and_merging_flips'], b['mean_flips']) for b in C['part_B']]
    t += [table(['n', 'start states', 'all chains end on the cycle with code 000', 'max freezing flips',
                 'max sorting and merging flips', 'mean flips'], rows), '']
    c0 = C['part_C']['code_000']
    t += ['Part C. Lemma 15, chain from l^b0 s^a0 to the cycle with a width-4 window in the state 0000, executed for n = %s '
          '(%d ring sizes): all executed: %s; flips: %s for n = 1 mod 3, %s for n = 2 mod 3.'
          % (c0['n'], c0['ring_sizes'], c0['all_chains_executed'], c0['flips_by_residue']['n = 1 mod 3'],
             c0['flips_by_residue']['n = 2 mod 3']), '',
          'Chains into {0} for n = 5, 7, 8 (a periodic state that is joined to a block word by flips between periodic states; '
          'one flip; the orbit then reaches 0):', '']
    rows = [(n, z['periodic_state'], z['period'], z['flip_cell'], z['steps_to_zero'], ' -> '.join(z.get('orbit_after_flip', [])) or '-',
             z['reversible_flips_from_a_block_word'], z['block_word']) for n, z in C['part_C']['zero_state'].items()]
    t += [table(['n', 'periodic state (cell 0 first)', 'its period', 'flipped cell', 'steps until 0', 'orbit after the flip',
                 'flips between periodic states from the block word', 'block word'], rows), '',
          'CPU time of `chains_94.py`: %.2f s.' % C['cpu_s'], '']
    X, tab = crosscheck_rows(['rule94_vs_study', 'rule94_vs_part2_94'])
    t += ['### Table 4. Comparison with data already in the repository (`crosscheck_data.py` -> `out/crosscheck_data.json`)', '', tab, '']
    return '\n'.join(t)


def tables_26():
    L = js('check_lemmas_26.json')
    G = jl('g1_26.jsonl')
    C = js('chains_26.json')
    t = ['### Table 1. Exhaustive tests of the lemmas (`check_lemmas_26.py` -> `out/check_lemmas_26.json`)', '',
         lemma_table(L), '',
         'All tests passed: %s. CPU time %.2f s.' % (L['all_passed'], L['cpu_s']), '',
         'Numbers of domain states (test M3), by n: ' + ', '.join('%s: %s' % kv for kv in L['M3']['domain_states'].items()) + '.', '',
         'Periodic states by kind (test M5), n: zero / on one parity class / domain states / orbit with 111: ' +
         '; '.join('%s: %d / %d / %d / %d' % (n, k['zero'], k['one_parity'], k['domain'], k['with_111'])
                   for n, k in L['M5']['periodic_states_by_kind'].items()) + '.', '',
         '### Table 2. G1 and its closed classes computed directly, even n (`g1_26.py` -> `out/g1_26.jsonl`)', '']
    rows = []
    for r in G:
        kk = r['cycles_by_kind']
        rows.append((r['n'], 'yes' if r['power_of_two'] else 'no', r['cycles'], r['periodic_states'], r['g1_edges'],
                     '%d %s' % (len(r['closed_classes']), r['closed_classes']), r['zero_in_the_closed_class'],
                     kk.get('one_parity', 0), kk.get('domain', 0), kk.get('with_111', 0),
                     r['one_parity_cycles_in_K'], r['domain_cycles_in_K'], r['cycles_with_111_in_K'], r['codes_on_K'],
                     r['c_of_domain_cycles'] or '-', r['c_of_cycles_with_111'] or '-',
                     r['cycles_with_111_through_a_carrier_word'], r['max_increase_of_c_along_a_G1_edge'],
                     '%d of %d' % (r['cycles_with_a_G1_path_to_zero'], r['cycles']), r['max_G1_distance_to_zero'],
                     r['cpu_s'], int(r['peak_rss_mb'])))
    t += [table(['n', '2^k', 'cycles', 'periodic states', 'G1 edges', 'closed classes (sizes)', '{0} in the closed class',
                 'cycles on one parity class (not {0})', 'domain cycles', 'cycles with 111', 'one-parity cycles in K',
                 'domain cycles in K', 'cycles with 111 in K', 'codes on K', 'c of the domain cycles', 'c of the cycles with 111',
                 'cycles with 111 through a carrier word', 'largest increase of c along a G1 edge',
                 'cycles with a G1 path to {0}', 'max G1 distance to {0}', 'CPU s', 'peak MB'], rows), '',
          'K denotes the closed class that contains {0} (the only closed class in every row). For n = 4, 8, 16, K = {0}.', '',
          '### Table 3. n = 4, 8, 16: resistances, potentials and k_c from the definitions (`g1_26.py`)', '']
    rows = []
    for r in G:
        if not r['power_of_two']:
            continue
        m = r['cycles']
        k = r.get('k_c_from_the_definition')
        how = 'Edmonds, all roots'
        if k is None:
            k = r['k_c_from_V_R_and_Theorem_3']
            how = 'V, R and Theorem 3; Edmonds for %d roots' % r['gamma_roots_computed_by_Edmonds']
        rows.append((r['n'], m, r['V_from_zero_hist'], r['T2_cycles'], r['cycles_reachable_from_T2'],
                     r['domain_cycles_reachable_from_T2'], r['cycles_with_111_reachable_from_T2'], r['gamma_zero'],
                     r['gamma_by_kind'], r['gamma_agrees_with_Theorem_3_on_the_computed_roots'],
                     r['G1_edges_equal_pairs_with_V_1'], r['R_from_zero_to_code'], k, max(k), how))
    t += [table(['n', 'm', 'V({0}, C): value: number of cycles', 'cycles with V({0}, C) = 2 (T2)', 'cycles reachable from T2 in G1',
                 'domain cycles reachable from T2', 'cycles with 111 reachable from T2', 'gamma({0})',
                 'gamma by kind of cycle (roots computed by Edmonds)', 'gamma agrees with Theorem 3',
                 'G1 edges = pairs with V = 1', 'R({0} -> D_c), c = 0..7', 'k_c, c = 0..7', 'k*', 'how gamma was obtained'], rows), '',
          '### Table 4. The chains of the proofs, executed step by step (`chains_26.py` -> `out/chains_26.json`)', '',
          'Part A: every cycle, chain of Theorem 2 down to a cycle on one parity class.', '']
    rows = [(a['n'], a['cycles'], a['all_chains_end_on_one_parity_class'], a['chains_ending_at_zero'], a['max_flips'],
             a['max_drops_of_c']) for a in C['part_A']]
    t += [table(['n', 'cycles', 'all chains end on one parity class', 'chains ending at {0}', 'max flips', 'max number of drops of c'], rows), '',
          'Part B: cycles reached from random states, n = 2^k, chain of Theorem 2 to {0}.', '']
    rows = [(b['n'], b['start_states'], b['all_chains_end_at_zero'], b['max_c_of_start_cycle'], b['max_flips'], b['max_drops_of_c'])
            for b in C['part_B']]
    t += [table(['n', 'start states', 'all chains end at {0}', 'max c of the start cycle', 'max flips', 'max number of drops of c'], rows), '',
          'Part C: chain of Theorem 4(c): 0, e_0 + e_5 (resistance 2), then single flips between periodic domain states up to '
          '10100 (100)^q, then one flip to the carrier word 11100 (100)^q.', '']
    rows = [(c['n'], c['q'], c['flips_after_e0_e5'], c['all_intermediate_states_are_periodic_domain_states'],
             c['final_state_is_the_carrier_word'], c['period_of_the_carrier_cycle'], c['c_of_last_domain_state'], c['c_of_carrier'])
            for c in C['part_C']]
    t += [table(['n', 'q', 'flips between domain states after e_0 + e_5', 'all intermediate states periodic domain states',
                 'last flip gives the carrier word, periodic, with 111', 'period of the carrier cycle', 'c of the last domain state',
                 'c of the carrier'], rows), '',
          'Part D: even n that are not powers of two. Every cycle on one parity class is joined to {0} in both directions '
          '(Lemma 9), and every domain cycle is joined to a cycle on one parity class by flips between periodic states (Theorem 5).', '']
    rows = [(d['n'], d['one_parity_cycles_joined_to_zero_both_ways'],
             d['domain_cycles_joined_to_a_one_parity_cycle_by_flips_between_periodic_states']) for d in C['part_D']]
    t += [table(['n', 'one-parity cycles joined to {0} both ways', 'domain cycles joined to a one-parity cycle'], rows), '',
          'Part E: Theorem 3(d). From e_(s1) + e_(s2) (resistance 2 from 0; s1, s2 two consecutive sources) to a given domain '
          'state by single flips; every intermediate state is asserted to be a periodic domain state.', '']
    rows = [(e['n'], e['domain_states'], 'every domain cycle' if e['every_domain_cycle'] else 'cycles reached from random states',
             e['all_intermediate_states_are_periodic_domain_states'], e['max_flips']) for e in C['part_E']]
    t += [table(['n', 'target domain states', 'which', 'all intermediate states periodic domain states', 'max flips'], rows), '',
          'Part F: Theorem 4(b). The path 0, e_0, F(e_0), F^2(e_0) + e_1, whose next state contains 111, and the orbit of a single '
          'flip of 0 (no two adjacent ones, returns to 0): executed for n = %s; all as stated: %s.'
          % (', '.join(str(f['n']) for f in C['part_F']),
             all(f['path_of_resistance_2_reaches_111'] and f['single_flip_orbit_has_no_adjacent_ones_and_dies'] for f in C['part_F'])), '',
          'CPU time of `chains_26.py`: %.2f s.' % C['cpu_s'], '']
    X, tab = crosscheck_rows(['rule26_vs_study', 'rule26_vs_part2_154'])
    t += ['### Table 5. Comparison with data already in the repository (`crosscheck_data.py` -> `out/crosscheck_data.json`)', '', tab, '',
          'k_c of the study and of this folder at the powers of two in the study: ' +
          '; '.join('n = %s: study %s, here %s' % (n, v['study'], v['here']) for n, v in X['rule26_vs_study']['k_c_compared'].items()) + '.', '']
    return '\n'.join(t)


def main():
    for name, fn in (('tables_94.md', tables_94), ('tables_26.md', tables_26)):
        with open(os.path.join(OUT, name), 'w') as fh:
            fh.write(fn())
        print('wrote out/' + name)


if __name__ == '__main__':
    main()
