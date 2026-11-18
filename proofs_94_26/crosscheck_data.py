"""Comparison of the computations of proofs_94_26/ with data already in the repository (read only):
  data/ring_size/mechanisms.csv                          (the study: cycles, selected cycles, gamma_min, k_c, k*)
  verify_ring_size/part2_94/out/g1_classes.jsonl         (rule 94: G1 and its closed classes)
  verify_ring_size/part2_154/out/explore_122_26.jsonl    (rule 26: closed classes of G1)
Writes out/crosscheck_data.json. The repository root is the parent of this folder.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def jl(path):
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main():
    mine94 = {r['n']: r for r in jl(os.path.join(HERE, 'out', 'g1_classes_94.jsonl'))}
    mine26 = {r['n']: r for r in jl(os.path.join(HERE, 'out', 'g1_26.jsonl'))}
    with open(os.path.join(ROOT, 'data', 'ring_size', 'mechanisms.csv')) as fh:
        study = {(int(r['rule']), int(r['n'])): r for r in csv.DictReader(fh)}
    out = {}

    # rule 94 against the study: cycles, selected cycles = closed class, gamma_min = m - 1, k* = 0
    ns, bad = [], []
    for n, r in sorted(mine94.items()):
        s = study.get((94, n))
        if s is None or n < 5:
            continue
        ns.append(n)
        good = (int(s['cycles']) == r['cycles'] and int(s['n_selected']) == r['closed_classes'][0]
                and int(float(s['gamma_min'])) == r['cycles'] - 1 and int(s['kstar']) == 0
                and [int(v) for v in s['k_c'].split('-')] == [0] * 8
                and len(r['closed_classes']) == 1 and r['codes_on_K'] == list(range(8)))
        if not good:
            bad.append(n)
    out['rule94_vs_study'] = dict(source='data/ring_size/mechanisms.csv', ring_sizes=ns, disagreements=bad,
                                  fields='cycles; selected cycles = size of the closed class; gamma_min = m - 1; k_c = 0 for all c; k* = 0')

    # rule 94 against the direct computation of PROOF_94.md
    ref = {r['n']: r for r in jl(os.path.join(ROOT, 'verify_ring_size', 'part2_94', 'out', 'g1_classes.jsonl'))}
    ns, bad = [], []
    for n, r in sorted(mine94.items()):
        if n not in ref:
            continue
        q = ref[n]
        ns.append(n)
        good = (q['cycles'] == r['cycles'] and q['periodic_states'] == r['periodic_states'] and q['g1_edges'] == r['g1_edges']
                and q['strong_components'] == r['strong_components'] and sorted(q['closed_class_sizes']) == r['closed_classes'])
        if not good:
            bad.append(n)
    out['rule94_vs_part2_94'] = dict(source='verify_ring_size/part2_94/out/g1_classes.jsonl', ring_sizes=ns, disagreements=bad,
                                     fields='cycles; periodic states; G1 edges; strong components; closed-class sizes')

    # rule 26 against the study
    ns, bad, kc = [], [], {}
    for n, r in sorted(mine26.items()):
        s = study.get((26, n))
        if s is None:
            continue
        ns.append(n)
        sk = [int(v) for v in s['k_c'].split('-')]
        good = (int(s['cycles']) == r['cycles'] and int(s['n_selected']) == r['closed_classes'][0]
                and int(float(s['gamma_min'])) == r['cycles'] - 1)
        mk = r.get('k_c_from_the_definition')
        if mk is not None:
            good = good and mk == sk and int(s['kstar']) == max(mk)
            kc[str(n)] = dict(study=sk, here=mk)
        else:
            # not a power of two: k_c = 0 exactly for the codes carried by the closed class (Corollary 5)
            good = good and [c for c in range(8) if sk[c] == 0] == r['codes_on_K']
        if not good:
            bad.append(n)
    out['rule26_vs_study'] = dict(source='data/ring_size/mechanisms.csv', ring_sizes=ns, disagreements=bad, k_c_compared=kc,
                                  fields='cycles; selected cycles = size of the closed class; gamma_min = m - 1; k_c and k* '
                                         '(n = 8, 16: all values; other n: the codes with k_c = 0 are the codes on the closed class)')

    # rule 26 against the exploration of PROOF_154.md, section 7.2
    ref = {r['n']: r for r in jl(os.path.join(ROOT, 'verify_ring_size', 'part2_154', 'out', 'explore_122_26.jsonl'))
           if r.get('rule') == 26}
    ns, bad = [], []
    for n, r in sorted(mine26.items()):
        if n not in ref:
            continue
        q = ref[n]
        ns.append(n)
        good = sorted(q['closed_class_sizes']) == r['closed_classes']
        if 'n_cycles' in q:
            good = good and q['n_cycles'] == r['cycles']
        if 'cycles_with_code7' in q:
            good = good and q['cycles_with_code7'] == r['cycles_by_kind'].get('with_111', 0)
        if not good:
            bad.append(n)
    out['rule26_vs_part2_154'] = dict(source='verify_ring_size/part2_154/out/explore_122_26.jsonl', ring_sizes=ns, disagreements=bad,
                                      fields='closed-class sizes; cycles; cycles that contain 111 (where recorded)')

    out['all_agree'] = all(not v['disagreements'] and v['ring_sizes'] for v in out.values())
    with open(os.path.join(HERE, 'out', 'crosscheck_data.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    for k, v in out.items():
        if isinstance(v, dict):
            print(k, 'n =', v['ring_sizes'], 'disagreements:', v['disagreements'])
    print('all agree:', out['all_agree'])


if __name__ == '__main__':
    main()
