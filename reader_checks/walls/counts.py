"""Recomputes the global counts of report_boundaries.md, Section 4, from the reader's own records
(out/null_n04_20.csv) and from own step tables. Claude, 25 November 2026.
Only the list of the 160 null classes and their members is taken from the study (data/boundaries/null_classes.csv)."""
import csv, os, numpy as np
from walls import model, cycles
here = os.path.dirname(os.path.abspath(__file__))
Z = os.environ.get('WALLS_DATA', os.path.join(here, '..', '..', 'data', 'boundaries')) + '/'
rows = {(int(r['rule']), int(r['n'])): r for r in csv.DictReader(open(os.path.join(here, 'out', 'null_n04_20.csv')))}
cls = {int(r['null_rep']): [int(x) for x in r['members'].replace(';', ' ').replace('|', ' ').replace(',', ' ').split()]
       for r in csv.DictReader(open(Z + 'null_classes.csv'))}
reps = sorted(cls)
assert sorted(x for v in cls.values() for x in v) == list(range(256))
side = lambda r, n: int(rows[(r, n)]['side'])
one = [r for r in reps if all(side(r, n) for n in range(8, 17))]
zero = [r for r in reps if not any(side(r, n) for n in range(8, 17))]
print('null classes, n = 8..16: k* >= 1 at every n:', len(one), '; k* = 0 at every n:', len(zero),
      '; change side:', [r for r in reps if r not in one and r not in zero])
print('change side somewhere in n = 4..14:', sum(len({side(r, n) for n in range(4, 15)}) == 2 for r in reps),
      '; in n = 8..14:', sum(len({side(r, n) for n in range(8, 15)}) == 2 for r in reps))
for n in (12, 13, 14, 16):
    print('n =', n, ': rules with k* >= 1:', sum(len(cls[r]) * side(r, n) for r in reps),
          '; rules whose cycles jointly miss a code:', sum(len(cls[r]) * int(rows[(r, n)]['btype']) for r in reps))
nb = [(k, v) for k, v in rows.items() if k[0] in cls]
print('records of class representatives:', len(nb), '; with a single cycle:', sum(v['cycles'] == '1' for k, v in nb),
      '; with more than one closed class of G_1:', sorted(k for k, v in nb if v['closed_classes'] != '1'))
bij = {}
for r in reps:
    b = [n for n in range(4, 17) if len(np.unique(model(r, n, 'null')[0])) == (1 << n)]
    if b: bij[r] = b
print('bijective under null walls (class: sizes in 4..16):', bij)
for b in ('ring', 'null'):
    cnt = 0
    for r in range(256):
        F, mask = model(r, 12, b); lab, m = cycles(F)
        cnt += int(np.bitwise_or.reduce(mask[lab >= 0])) != 255
    print('n = 12,', b, ': rules whose cycles jointly miss a code:', cnt)
print('k* by n = 4..20 (side only, 1 means k* >= 1):')
for r in (22, 37, 75, 90, 91, 94, 122, 126, 133, 135, 137, 165):
    print(' ', r, ''.join(str(side(r, n)) for n in range(4, 21)))
