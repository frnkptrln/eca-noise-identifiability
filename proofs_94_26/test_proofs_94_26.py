"""Tests of proofs_94_26/ (run: python -m pytest proofs_94_26/test_proofs_94_26.py -q).

Fast tests recompute small cases directly; the other tests check the output files in out/ and that the two
documents carry the tables of out/ verbatim. Nothing is imported from code/ or verify_ring_size/.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ring  # noqa: E402
import r26  # noqa: E402
import make_tables  # noqa: E402
from ring import step, w2s, s2w  # noqa: E402

OUT = os.path.join(HERE, 'out')
TAGS = ('[proved]', '[proved, given Theorem A]', '[computed for n', '[attempted (gap:')


def js(name):
    with open(os.path.join(OUT, name)) as fh:
        return json.load(fh)


def jl(name):
    with open(os.path.join(OUT, name)) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def doc(name):
    with open(os.path.join(HERE, name)) as fh:
        return fh.read()


# ------------------------------------------------------------------ tools
def test_step_and_table_agree_with_the_cell_by_cell_rule():
    random.seed(1)
    for rule in (94, 26, 90, 154):
        for n in (3, 4, 7, 12, 33):
            for _ in range(100):
                s = random.getrandbits(n)
                assert step(rule, s, n) == ring.step_slow(rule, s, n)
        F = ring.F_table(rule, 9)
        assert all(int(F[s]) == ring.step_slow(rule, s, 9) for s in range(1 << 9))


def test_rule_tables():
    assert [c for c in range(8) if (94 >> c) & 1] == [1, 2, 3, 4, 6]
    assert [c for c in range(8) if (26 >> c) & 1] == [1, 3, 4]


# ------------------------------------------------------------------ rule 94, direct small cases
def test_live_window_orbits_small_widths():
    for w in range(1, 13):
        got = {frozenset(o) for o in ring.live_window_orbits(w)}
        want = set()
        if w % 3 == 2:
            want.add(frozenset(ring.AB_window(w)))
        if w == 4:
            want.add(frozenset(w2s(u) for u in ('0000', '1001', '1111')))
        assert got == want, w


def test_rule94_closed_class_n10_and_n11():
    for n, m, size in ((10, 73, 67), (11, 78, 77)):
        r = ring.g1(94, n)
        assert r['m'] == m and len(r['closed']) == 1
        K = r['lab'] == r['closed'][0]
        assert int(K.sum()) == size
        for i, cyc in enumerate(r['cycles']):
            if ring.frozen94(cyc[0], n):
                assert K[i]                       # Theorem 2(b)
            else:
                assert ring.frozen94(cyc[-1], n) == set()
        codes = set()
        for i, cyc in enumerate(r['cycles']):
            if K[i]:
                for s in cyc:
                    codes |= ring.codes_of(s, n)
        assert codes == set(range(8))             # Theorem 2(d)


def test_split_and_merge_examples():
    n = 10
    x = w2s('0101101101')                         # s l l s
    y1 = x ^ (1 << 2)
    y0 = step(94, y1, n)
    assert step(94, y0, n) == y1 and y0 != y1     # 2-cycle of Lemma 13
    z = y0 ^ (1 << 6)
    for _ in range(5):
        z = step(94, z, n)
    assert s2w(z, n) == '0101010101'
    back = step(94, z ^ (1 << 3), n)              # merge (Lemma 12) on the first three short blocks
    assert s2w(back, n) == '0110110101'


def test_code_000_window():
    for n in (7, 10, 11, 13, 40):
        tail = n - 7
        b = tail % 2
        word = '0100001' + '011' * b + '01' * ((tail - 3 * b) // 2)
        assert len(word) == n
        z = w2s(word)
        t, cyc = ring.limit_cycle(94, z, n)
        assert t == 0 and len(cyc) == 3 and 0 in ring.codes_of(z, n)
        assert ring.frozen94(z, n) == set(range(n)) - {2, 3, 4, 5}


def test_zero_state_chains_n5_n7_n8():
    assert step(94, w2s('11111'), 5) == 0 and ring.limit_cycle(94, w2s('01111'), 5)[0] == 0
    assert step(94, w2s('1111111'), 7) == 0 and ring.limit_cycle(94, w2s('0111111'), 7)[0] == 0
    y = w2s('01111010')
    assert ring.limit_cycle(94, y, 8)[0] == 0
    v = y ^ (1 << 5)
    orbit = [s2w(v, 8)]
    while v:
        v = step(94, v, 8)
        orbit.append(s2w(v, 8))
    assert orbit == ['01111110', '11000011', '01100110', '11111111', '00000000']


# ------------------------------------------------------------------ rule 26, direct small cases
def test_c_does_not_increase_n10():
    n = 10
    F = ring.F_table(26, n)
    c = r26.c_changes_all(n)
    assert int((c[F] > c).sum()) == 0
    assert all(int(c[s]) == r26.c_changes(s, n) for s in range(0, 1 << n, 7))


def test_domain_states_are_permuted_n8():
    n = 8
    dom = [s for s in range(1 << n) if r26.is_domain_state(s, n)]
    assert len(dom) == 64
    img = {step(26, s, n) for s in dom}
    assert img == set(dom)


def test_ancestor_pattern_gives_111():
    n = 12
    for s in range(1 << n):
        for (j, r) in r26.has_ancestor_pattern(s, n):
            v = s
            for _ in range(r):
                v = ring.rot(step(26, v, n), 1, n)
            assert all((v >> ((j + k) % n)) & 1 for k in (-1, 0, 1))


def test_carrier_words_shift():
    for n in (8, 13, 16, 21):
        ws = r26.carrier_words(n)
        assert ws
        for s in ws:
            assert step(26, step(26, s, n), n) == ring.rot(s, 1, n)


def test_every_cycle_reaches_zero_n8():
    import chains_26
    F, per, cycles, att = ring.analyse(26, 8)
    assert len(cycles) == 10
    for cyc in cycles:
        x, flips, drops = chains_26.reduce_chain(cyc[0], 8)
        assert x == 0


def test_k_odd_chain_n32():
    n, q = 32, 9
    x = w2s('10100' + '100' * q)
    y = w2s('11100' + '100' * q)
    assert r26.is_domain_state(x, n) and ring.limit_cycle(26, x, n)[0] == 0
    assert y == x ^ (1 << 1) and ring.limit_cycle(26, y, n)[0] == 0 and r26.has111(y, n)


# ------------------------------------------------------------------ output files
def test_lemma_tests_passed():
    for name in ('check_lemmas_94.json', 'check_lemmas_26.json'):
        d = js(name)
        assert d['all_passed']
        for k, v in d.items():
            if isinstance(v, dict):
                assert v['violations'] == 0 and v['cases'] > 0, (name, k)


def test_g1_rule94_records():
    recs = {r['n']: r for r in jl('g1_classes_94.jsonl')}
    assert sorted(recs) == [4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23]
    for n, r in recs.items():
        if n < 5:
            continue
        assert len(r['closed_classes']) == 1
        assert r['block_words_in_one_component'] and r['block_words_all_in_K']
        assert r['cycles_with_101_in_K'] == r['cycles_with_101'] and r['cycles_outside_K_with_101'] == 0
        assert r['codes_on_K'] == list(range(8))
        assert r['K_equals_cycles_reachable_from_block_words']
        assert r['zero_state_in_K'] == (n in (5, 7, 8))                       # Proposition 3 (n = 16: computed)
        if n >= 10 and n % 8:
            assert r['zero_state_in_degree'] == 0
        if n % 2 == 1 and n >= 11:
            assert r['closed_classes'] == [r['cycles'] - 1] and r['cycles_without_101'] == 1
    assert recs[4]['codes_on_K'] == [2, 5]


def test_chains_rule94():
    d = js('chains_94.json')
    assert [a['n'] for a in d['part_A']] == [5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23]
    assert all(a['all_chains_end_on_a_block_word'] and a['block_word_graph_strongly_connected'] for a in d['part_A'])
    assert all(b['all_chains_end_on_the_cycle_with_code_000'] for b in d['part_B'])
    assert d['part_C']['code_000']['all_chains_executed']
    assert sorted(d['part_C']['zero_state']) == ['5', '7', '8']


def test_g1_rule26_records():
    recs = {r['n']: r for r in jl('g1_26.jsonl')}
    assert sorted(recs) == list(range(4, 23, 2))
    for n, r in recs.items():
        assert len(r['closed_classes']) == 1 and r['zero_in_the_closed_class']
        assert r['cycles_with_a_G1_path_to_zero'] == r['cycles']
        if r['g1_edges']:
            assert r['max_increase_of_c_along_a_G1_edge'] <= 2
        if r['power_of_two']:
            assert r['closed_classes'] == [1]                                 # Theorem 3(b)
            assert r['gamma_zero'] == r['cycles'] - 1
            assert r['gamma_agrees_with_Theorem_3_on_the_computed_roots'] and r['G1_edges_equal_pairs_with_V_1']
            if n >= 8:
                dn, dt = r['domain_cycles_reachable_from_T2'].split(' of ')
                assert dn == dt                                               # Theorem 3(d)
        else:
            a, b = r['one_parity_cycles_in_K'].split(' of ')
            assert a == b
            a, b = r['domain_cycles_in_K'].split(' of ')
            assert a == b
            assert r['cycles_outside_K_all_carry_111']                        # Theorem 5
            assert set(range(7)) <= set(r['codes_on_K'])
    assert recs[4]['k_c_from_the_definition'] == [0, 1, 1, 2, 1, 1, 2, 2]
    assert recs[8]['k_c_from_the_definition'] == [0, 1, 1, 1, 1, 1, 1, 1]     # Theorem 4(a), (c)
    assert recs[16]['k_c_from_the_definition'] == [0, 1, 1, 1, 1, 1, 1, 2]
    assert recs[16]['gamma_roots_computed_by_Edmonds'] == 552 and recs[16]['gamma_by_kind'] == {'domain': [552], 'with_111': [553], 'zero': [551]}
    assert recs[16]['cycles_with_111_reachable_from_T2'].startswith('0 of')
    assert recs[8]['cycles_with_111_reachable_from_T2'] == '1 of 1'


def test_chains_rule26():
    d = js('chains_26.json')
    for a in d['part_A']:
        assert a['all_chains_end_on_one_parity_class']
        if a['n'] in (4, 8, 16):
            assert a['chains_ending_at_zero'] == a['cycles']
    assert all(b['all_chains_end_at_zero'] for b in d['part_B'])
    assert [c['n'] for c in d['part_C']] == [8, 32, 128, 512]
    assert all(c['final_state_is_the_carrier_word'] and c['c_of_carrier'] == c['c_of_last_domain_state'] + 2 for c in d['part_C'])
    assert [x['n'] for x in d['part_D']] == [6, 10, 12, 14, 18, 20]
    assert all(e['all_intermediate_states_are_periodic_domain_states'] for e in d['part_E'])
    assert all(f['path_of_resistance_2_reaches_111'] for f in d['part_F'])


def test_crosscheck_with_repository_data():
    d = js('crosscheck_data.json')
    assert d['all_agree']
    for k in ('rule94_vs_study', 'rule94_vs_part2_94', 'rule26_vs_study', 'rule26_vs_part2_154'):
        assert d[k]['ring_sizes'] and d[k]['disagreements'] == []
    assert d['rule26_vs_study']['k_c_compared']['16'] == dict(study=[0, 1, 1, 1, 1, 1, 1, 2], here=[0, 1, 1, 1, 1, 1, 1, 2])


# ------------------------------------------------------------------ documents
def test_tables_are_rebuilt_identically_and_copied_verbatim():
    for name, fn, docname in (('tables_94.md', make_tables.tables_94, 'PROOF_94_converse.md'),
                              ('tables_26.md', make_tables.tables_26, 'PROOF_26.md')):
        with open(os.path.join(OUT, name)) as fh:
            text = fh.read()
        assert fn() == text
        assert text in doc(docname)


def test_documents_have_status_tables_and_tags():
    for name in ('PROOF_94_converse.md', 'PROOF_26.md'):
        d = doc(name)
        assert '## 0. Result in brief' in d and '| item | statement | status | where |' in d
        for tag in TAGS:
            assert tag in d, (name, tag)
        assert 'No claim of novelty' in d or 'no claim of novelty' in d


def test_numbers_quoted_in_the_text_of_the_rule94_document():
    g = {r['n']: r for r in jl('g1_classes_94.jsonl')}
    desc = ', '.join('%d of %d for n = %d' % (g[n]['cycles_without_101_in_K'] - int(g[n]['zero_state_in_K']),
                                              g[n]['cycles_without_101'] - 1, n) for n in (10, 14, 20, 22))
    assert doc('PROOF_94_converse.md').count(desc) == 2
    t = doc('PROOF_94_converse.md')
    for n in (10, 14, 20, 22):
        row = [ln for ln in t.splitlines() if ln.startswith('| %d |' % n)][0]
        assert '%d of %d' % (g[n]['cycles_without_101_in_K'] - int(g[n]['zero_state_in_K']), g[n]['cycles_without_101'] - 1) in row
