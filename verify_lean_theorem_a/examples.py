"""Concrete examples quoted in VERIFICATION_lean_theorem_a.md. Run from this directory after sweep.py."""
import csv
import sys
from instance import Instance, bits
from lean_defs import CODES, D, contains

out = []
def say(s=''):
    out.append(s); print(s)

# E1. n = 2: Lemma 2.2 without the hypothesis 3 <= n.
I = Instance(204, 2)
v = (1, 0, 0)
I.check_statements()
say(f'E1 rule 204, n = 2: D_100 has {len(D(2, v))} states; R(C -> D_100) = {I.RCD[(0, v)]} (sInf of the empty set); '
    f'k_100 = {I.k[v]}, k* = {I.kstar}; some state of a selected cycle contains 100: {I.sel_contains[v]}; '
    f'so part 1 of Lemma_2_2 fails at n = 2 and the hypothesis 3 <= n is needed')
for n in (1, 2):
    say(f'   codes occurring in some state at n = {n}: ' + ' '.join(bits(v) for v in CODES if D(n, v)))

# E2. Orientation: rows of fw_sweep.csv where the k_v vector is not invariant under abc -> cba.
rev = [CODES.index((c, b, a)) for a, b, c in CODES]
rows = list(csv.DictReader(open('out/sweep_n1_6.csv')))
data = {(r['n'], r['rule']): r for r in csv.DictReader(open(sys.argv[1] if len(sys.argv) > 1 else '../data/fw_sweep.csv'))}
asym = []
for r in rows:
    kv = r['k_v'].split('-')
    if [kv[i] for i in rev] != kv and (r['n'], r['rule']) in data:
        asym.append((r['n'], r['rule'], r['k_v'], data[(r['n'], r['rule'])]['k_c']))
all_asym = sum(1 for r in rows if int(r['n']) >= 3 and [r['k_v'].split('-')[i] for i in rev] != r['k_v'].split('-'))
say(f'E2 instances of the sweep with n = 3..6 whose k_v vector changes under abc -> cba: {all_asym} of '
    f'{sum(1 for r in rows if int(r["n"]) >= 3)}')
say(f'E2 rows of data/fw_sweep.csv (n = 4..6) whose k_v vector changes under abc -> cba: {len(asym)}; '
    f'model = data on all of them: {all(a[2] == a[3] for a in asym)}; first: {asym[:3]}')

# E3. Bijective rows: the column gamma_min of fw_sweep.csv is not gamma_min of the paper.
bij = [(r['n'], r['rule'], r['gamma_min'], data[(r['n'], r['rule'])]['gamma_min'], r['m'])
       for r in rows if (r['n'], r['rule']) in data and data[(r['n'], r['rule'])]['bijective'] == '1']
say(f'E3 bijective rows: {len(bij)}; model gamma_min = m - 1 on all: {all(int(b[2]) == int(b[4]) - 1 for b in bij)}; '
    f'data gamma_min values: {sorted(set(b[3] for b in bij))}; e.g. {bij[:3]}')

# E4. Several closed classes (n = 3..6): the hypothesis "unique closed class" of Theorem 2.8 matters,
# and on these sizes S is always the union of all closed classes.
several = [r for r in rows if int(r['n']) >= 3 and int(r['n_closed']) >= 2]
proper = 0
for r in several:
    I = Instance(int(r['rule']), int(r['n']), crosscheck_R=False, brute_gamma_max=0, brute_cc_max=0)
    proper += set().union(*I.cc) != I.Sel
say(f'E4 instances with n = 3..6 and at least two closed classes: {len(several)}; '
    f'in {proper} of them S is a proper subset of the union of the closed classes')
I = Instance(232, 3)
say('   example: ' + I.summary().replace('\n', '\n   '))
say(f'   here gamma_min = {I.gammaMin} != m - 1 = {I.m - 1}: without uniqueness the second sentence of Theorem 2.8 fails')
open('out/examples.txt', 'w').write('\n'.join(out) + '\n')
