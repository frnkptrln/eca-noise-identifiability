"""All checks of VERIFICATION_boundaries.md that do not need the sweeps' worker pool.
Run from the repository root after the sweeps (see README in VERIFICATION_boundaries.md, Section D):
    python3 verify_boundaries/checks.py > verify_boundaries/out/checks_summary.txt
Imports nothing from code/fw or reader_checks; reads the study's data files only to compare."""
import os, sys, re, glob
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd, vb, local_sim as ls
REPO = os.environ.get('ECA_REPO', os.path.dirname(HERE)); D = os.path.join(REPO, 'data', 'boundaries') + '/'
R, Cm = vb.refl_rule, vb.comp_rule
def mstr(m): return ''.join(str(c) for c in range(8) if (m >> c) & 1)
def nz(s): return s if isinstance(s, str) and s != '-' else ''
def crefl(c): return ((c & 1) << 2) | (c & 2) | (c >> 2)
def st(bits): return sum(int(b) << i for i, b in enumerate(bits))
def H(t): print('\n## ' + t)
dt = {'union': str, 'cover': str, 'missed': str, 'kc': str, 'kstar': str, 'closed_cover': str}
O = os.path.join(HERE, 'out')
mine = pd.concat([pd.read_csv(f'{O}/{f}', dtype=dt) for f in ['null_all_n04_11.csv', 'null_reps_n12_16.csv', 'null_12cls_n17_20.csv']])
idx = {(r.n, r.rule): r for r in mine.itertuples()}
def rec(n, r): return idx[(n, min(r, R(r)))]
def kst(x): return '0' if x.bij else str(x.kstar)

H('1. classes (Section 2)')
nullcls = {}; ringcls = {}
for r in range(256):
    nullcls.setdefault(min(r, R(r)), set()).add(r); ringcls.setdefault(min(r, R(r), Cm(r), R(Cm(r))), set()).add(r)
sym = [r for r in range(256) if R(r) == r]
coinc = sorted(k for k in ringcls if min(Cm(k), R(Cm(k))) == min(k, R(k)))
print('null classes', len(nullcls), '; symmetric rules', len(sym), '; ring classes', len(ringcls), '; [R] = [R*] for', len(coinc), coinc)
for r in [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154, 150]:
    print('  ', r, sorted(nullcls[min(r, R(r))]), sorted(nullcls[min(Cm(r), R(Cm(r)))]))

H('2. conjugations, n = 1..10, all 256 rules, four boundaries')
def rev(x, n): return int(format(x, f'0{n}b')[::-1], 2)
def pm(m, p): return sum(1 << p[c] for c in range(8) if (m >> c) & 1)
bad = Counter(); PR = [crefl(c) for c in range(8)]; PC = [7 - c for c in range(8)]
for n in range(1, 11):
    N = 1 << n; rv = np.array([rev(x, n) for x in range(N)]); comp = np.arange(N) ^ (N - 1)
    for r in range(256):
        for b in ['ring', 'null', 'one', 'reflect']:
            A, B = vb.Sys(r, n, b), vb.Sys(R(r), n, b)
            if not np.array_equal(B.succ[rv], rv[A.succ]) or any(B.mask[rv[x]] != pm(A.mask[x], PR) for x in range(N)): bad['refl', b] += 1
        A, B = vb.Sys(r, n, 'null'), vb.Sys(Cm(r), n, 'one')
        if not np.array_equal(B.succ[comp], comp[A.succ]) or any(B.mask[x ^ (N - 1)] != pm(A.mask[x], PC) for x in range(N)): bad['comp null->one'] += 1
        for b in ['ring', 'reflect']:
            A, B = vb.Sys(r, n, b), vb.Sys(Cm(r), n, b)
            if not np.array_equal(B.succ[comp], comp[A.succ]): bad['comp', b] += 1
print('failures:', dict(bad) or 'none')

H('3. Lemma M (null n -> ring 2n+2) and Lemma M\' (reflect n -> ring 2n), n = 1..10')
def lift(x, n, N, off):
    y = 0
    for j in range(n):
        if (x >> j) & 1: y |= (1 << j) | (1 << (N - off - j))
    return y
okM, okMp = [], []
def emb_ok(r, n, bnd, N, off):
    a = vb.Sys(r, N, 'ring').succ; b = vb.Sys(r, n, bnd).succ
    return all(a[lift(x, n, N, off)] == lift(b[x], n, N, off) for x in range(2 ** n))
for r in range(256):
    if all(emb_ok(r, n, 'null', 2 * n + 2, 2) for n in range(1, 11)): okM.append(r)
    if all(emb_ok(r, n, 'reflect', 2 * n, 1) for n in range(1, 11)): okMp.append(r)
print('Lemma M holds for', len(okM), okM, '; = symmetric with f(000)=f(101)=0:', okM == [r for r in sym if not r & 1 and not (r >> 5) & 1])
print("Lemma M' holds for", len(okMp), '; = the 64 symmetric rules:', okMp == sym)
print('the two reflections of Lemma M coincide: (-2-j) = (2n-j) mod 2n+2 for all j, n <= 30:', all((-2 - j) % (2 * n + 2) == (2 * n - j) % (2 * n + 2) for n in range(1, 31) for j in range(2 * n + 2)))

H('4. deterministic facts')
fp = []
for n in range(1, 21):
    s = vb.Sys(94, n, 'null'); f = [x for x in np.flatnonzero(s.succ == np.arange(1 << n)) if s.mask[x] == 0b1101000]
    if f: fp.append(n)
print('rule 94 null: fixed point with codes exactly {3,5,6} at n =', fp, '(n = 1..20)')
def nil(rule, n, b):
    s = vb.Sys(rule, n, b); x = np.arange(1 << n)
    for _ in range(n + 1): x = s.succ[x]
    return bool((x == 0).all())
print('rule 90 null nilpotent at n =', [n for n in range(1, 21) if nil(90, n, 'null')])
print('rule 90 reflect nilpotent at n =', [n for n in range(1, 17) if nil(90, n, 'reflect')])
print('rule 150 reflect bijective at n =', [n for n in range(1, 17) if vb.Sys(150, n, 'reflect').bijective], '; rule 60 reflect bijective at n =', [n for n in range(1, 17) if vb.Sys(60, n, 'reflect').bijective])
print('kernel (110)^k 11 of null 150 at n = 2 mod 3 (2..20):', all(vb.Sys(150, n, 'null').succ[st(('110' * n)[:n])] == 0 for n in range(2, 21, 3)))
print('kernel (101)^k of reflect 150 at 3 | n (3..18):', all(vb.Sys(150, n, 'reflect').succ[st(('101' * n)[:n])] == 0 for n in range(3, 19, 3)))
def ncodes(x, n):
    m = 0
    for i in range(n):
        l = (x >> (i - 1)) & 1 if i else 0; r = (x >> (i + 1)) & 1 if i < n - 1 else 0
        m |= 1 << (4 * l + 2 * ((x >> i) & 1) + r)
    return m
for rule in [150, 105]:
    s = vb.Sys(rule, 5, 'null'); P = [x for x in range(32) if s.per[x]]
    print(f'rule {rule}, n = 5: periodic', [format(x, "05b")[::-1] for x in P], 'codes', mstr(int(np.bitwise_or.reduce([ncodes(x, 5) for x in P]))),
          'codes after one flip', mstr(int(np.bitwise_or.reduce([ncodes(x ^ (1 << i), 5) for x in P for i in range(5)]))))

H('5. affine rules, own GF(2) linear algebra, n = 3..128, vs data/boundaries/affine_null.csv')
def aff(rule):
    e = rule & 1; a = ((rule >> 4) & 1) ^ e; b = ((rule >> 2) & 1) ^ e; d = ((rule >> 1) & 1) ^ e
    return (a, b, d, e) if all(((rule >> k) & 1) == ((a * (k >> 2 & 1)) ^ (b * (k >> 1 & 1)) ^ (d * (k & 1)) ^ e) for k in range(8)) else None
def basis(vs):
    B = []
    for v in vs:
        for p, bv in B:
            if (v >> p) & 1: v ^= bv
        if v:
            p = v.bit_length() - 1; B = [(q, bv ^ v if (bv >> p) & 1 else bv) for q, bv in B]; B.append((p, v))
    return [bv for _, bv in B]
def affine_info(rule, n):
    a, b, d, e = aff(rule)
    def M(x):
        y = 0
        for i in range(n):
            l = (x >> (i - 1)) & 1 if i else 0; r = (x >> (i + 1)) & 1 if i < n - 1 else 0
            if (a * l) ^ (b * ((x >> i) & 1)) ^ (d * r): y |= 1 << i
        return y
    cols = [1 << j for j in range(n)]
    for _ in range(n): cols = [M(c) for c in cols]
    B = basis(cols); p0 = 0
    for _ in range(n): p0 = M(p0) ^ (((1 << n) - 1) if e else 0)
    cov = 0
    for i in range(n):
        pr = lambda x: tuple(((x >> j) & 1) if 0 <= j < n else 0 for j in (i - 1, i, i + 1))
        pats = {pr(p0)}
        for bv in B:
            q = pr(bv); pats |= {tuple(u ^ w for u, w in zip(p, q)) for p in pats}
        for p in pats: cov |= 1 << (4 * p[0] + 2 * p[1] + p[2])
    return len(B), len(B) == n, cov
AF = [r for r in range(256) if aff(r)]
af = pd.read_csv(D + 'affine_null.csv', dtype={'missed': str}); res = {}; bad = 0
for row in af.itertuples():
    dim, bij, cov = affine_info(row.rule, row.n); res[(row.rule, row.n)] = cov
    if dim != row.dim_periodic or int(bij) != row.bijective or mstr(255 & ~cov) != nz(row.missed) or int(cov != 255) != row.kstar_ge1: bad += 1
print('affine rules', AF, '; records', len(af), '; disagreements', bad)
for r in [90, 165, 150, 105, 60, 102, 153, 195]:
    print('  rule', r, 'misses a code at n =', [n for n in range(3, 129) if res[(r, n)] != 255])

H('6. null sweep vs data/boundaries/null_sweep.csv (field by field)')
ns = pd.read_csv(D + 'null_sweep.csv', dtype={'missed_codes': str, 'k_c': str})
cnt = Counter(); diffs = []
for r in ns.itertuples():
    me = idx[(r.n, r.rule)]; d = []
    if me.m != r.cycles: d.append('m')
    if me.bij != r.bijective: d.append('bij')
    if nz(me.union) != mstr(int(r.cycle_codes_union)): d.append('union')
    if r.bijective:
        cnt['bijective'] += 1
        if r.kstar != 0: d.append('k*')
        if me.exact == 1: cnt['bijective, potentials computed'] += 1; d += [] if me.kstar == '0' else ['k*exact']
    else:
        if me.nsel != r.n_stable: d.append('nsel')
        if me.gmin != r.gamma_min: d.append('gmin')
        if nz(me.missed) != nz(r.missed_codes): d.append('missed')
        if me.exact == 1:
            cnt['exact (every k_c compared)'] += 1
            if me.kc != r.k_c or int(me.kstar) != r.kstar: d.append('k_c')
        else:
            cnt['one-flip graph only (side compared)'] += 1
            if (me.kstar != '0') != (r.kstar >= 1): d.append('side')
    if d: diffs.append((r.n, r.rule, d))
print('records', len(ns), dict(cnt), '; disagreements', diffs or 'none')
bad = 0
for (n, r), me in idx.items():
    if n > 11: continue
    o = idx[(n, R(r))]
    if me.m != o.m or me.kstar != o.kstar: bad += 1
    elif me.exact == 1 and [int(v) for v in me.kc.split('-')] != [int(o.kc.split('-')[crefl(c)]) for c in range(8)]: bad += 1
print('all 256 rules n = 4..11: reflection partners with different m, k* or unmirrored k_c:', bad)
ex = mine[mine.exact == 1]
print('Theorem A check (exact records):', len(ex), '; one closed class:', int((ex.n_closed == 1).sum()), '; S = closed class and gmin = m-1 in all of these:',
      bool(ex[ex.n_closed == 1].sel_eq_closed.all() and (ex[ex.n_closed == 1].gmin == ex[ex.n_closed == 1].m - 1).all()))
print('records with more than one closed class:', [(x.n, x.rule, x.m, x.closed_sizes, x.nsel) for x in mine.itertuples() if x.n_closed > 1])

H('7. global counts of Section 4')
reps = sorted(nullcls)
S = {(n, r): (0 if (rec(n, r).bij or rec(n, r).kstar == '0') else 1) for n in range(4, 17) for r in reps}
a1 = [r for r in reps if all(S[(n, r)] for n in range(8, 17))]; a0 = [r for r in reps if not any(S[(n, r)] for n in range(8, 17))]
print('n = 8..16: always k*>=1', len(a1), '; always 0', len(a0), '; change', [r for r in reps if r not in a1 + a0])
print('classes changing side in n = 4..14:', sum(len({S[(n, r)] for n in range(4, 15)}) > 1 for r in reps), '; in 8..14:', sum(len({S[(n, r)] for n in range(8, 15)}) > 1 for r in reps))
cs = {k: len(v) for k, v in nullcls.items()}
for n in [12, 13, 14, 16]:
    print(f'  n = {n}: rules with k* >= 1: {sum(cs[r] * S[(n, r)] for r in reps)}; B-type rules: {sum(cs[r] * rec(n, r).btype for r in reps)}')
print('bijective classes n = 4..16:', {r: [n for n in range(4, 17) if rec(n, r).bij] for r in reps if any(rec(n, r).bij for n in range(4, 17))})
nb = [x for x in idx.values() if x.rule in nullcls and not x.bij]
print('non-bijective records (n = 4..16, 160 classes; n = 17..20, 12 classes):', len(nb), '; one closed class:', sum(x.n_closed == 1 for x in nb), '; single cycle:', sum(x.m == 1 for x in nb))

H('8. table of Section 5.0 (report lines 218-265), null and fixed-1 rows vs own records; ring rows vs data/fw_sweep.csv')
lines = open(os.path.join(REPO, 'report_boundaries.md')).read().split('\n')
fw = pd.read_csv(os.path.join(REPO, 'data', 'fw_sweep.csv')); fwi = {(int(a), int(b)): (int(c), int(j)) for a, b, c, j in zip(fw.n, fw.rule, fw.kstar, fw.bijective)}
rc = {r: min(r, R(r), Cm(r), R(Cm(r))) for r in range(256)}
mm, side_only, ncell = [], [], 0; cur = None
for ln in lines[217:265]:
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if c[0]: cur = int(c[0])
    for n, v in zip(range(4, 21), c[3:]):
        if v == '': continue
        ncell += 1
        if c[1] == 'ring':
            k = str(fwi[(n, rc[int(c[2])])][0])
        else:
            k = kst(rec(n, int(c[2])))
            if k == '>=1':
                if v == '0': mm.append((c[2], n, v, k))
                else: side_only.append((int(c[2]), n))
                continue
        if k != v: mm.append((c[2], c[1], n, v, k))
print('cells', ncell, '; disagreements', mm or 'none', '; side confirmed, value not recomputed:', side_only)

H('9. reflecting walls (Section 6) and own ring, 88 classes, n = 4..12')
rf = pd.read_csv(f'{O}/reflect_reps_n04_12.csv', dtype=dt); rg = pd.read_csv(f'{O}/ring_reps_n04_12.csv', dtype=dt)
rfi = {(r.n, r.rule): r for r in rf.itertuples()}; rgi = {(r.n, r.rule): r for r in rg.itertuples()}
rs = pd.read_csv(D + 'reflect_sweep.csv', dtype={'missed_codes': str, 'k_c': str}); bad = []
for r in rs.itertuples():
    me = rfi[(r.n, r.rule)]
    if me.m != r.cycles or me.bij != r.bijective: bad.append((r.n, r.rule))
    elif not r.bijective and (me.kc != r.k_c or me.nsel != r.n_stable or me.gmin != r.gamma_min or nz(me.missed) != nz(r.missed_codes)): bad.append((r.n, r.rule))
print('reflect_sweep.csv records', len(rs), '; disagreements', bad or 'none')
print('own ring k* vs fw_sweep.csv (n = 4..12, 88 classes): disagreements', [(r.n, r.rule) for r in rg.itertuples() if (0 if r.bij else int(r.kstar)) != fwi[(r.n, r.rule)][0]] or 'none')
def sd(x): return 0 if (x.bij or str(x.kstar) == '0') else 1
r88 = sorted(set(rf.rule)); size88 = {k: len(v) for k, v in ringcls.items()}
for nm, ii in [('ring', rgi), ('reflect', rfi)]:
    print(f'  {nm}: classes k*>=1 at n=12: {sum(sd(ii[(12, r)]) for r in r88)}; B-type classes at 12: {sum(ii[(12, r)].btype for r in r88)}; B-type rules at 12: {sum(size88[r] * ii[(12, r)].btype for r in r88)}; change side in 8..12: {[r for r in r88 if len({sd(ii[(n, r)]) for n in range(8, 13)}) > 1]}')
print('  same side as ring at every n = 8..12: reflect', sum(all(sd(rgi[(n, r)]) == sd(rfi[(n, r)]) for n in range(8, 13)) for r in r88),
      '; null (both null classes of the ring class)', sum(all(S[(n, min(r, R(r)))] == sd(rgi[(n, r)]) and S[(n, min(Cm(r), R(Cm(r))))] == sd(rgi[(n, r)]) for n in range(8, 13)) for r in r88))
mm = []; cur = None
for ln in lines[529:557]:
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if c[0]: cur = int(c[0])
    ii = rgi if c[1] == 'ring' else rfi
    for n, v in zip(range(4, 13), c[2:]):
        x = ii[(n, rc[cur])]
        if ('0' if x.bij else str(x.kstar)) != v: mm.append((cur, c[1], n))
print('table of Section 6: disagreements', mm or 'none')

H('10. descriptions of Sections 5.2-5.5 (own records)')
def row(r, n): x = rec(n, r); return f'n={n}: m={x.m} sel={x.nsel} missed={nz(x.missed) or "-"} k*={kst(x)}'
for r, rng in [(94, range(4, 21)), (133, range(4, 21)), (75, range(4, 21)), (22, range(4, 21)), (122, range(4, 21)), (126, range(4, 21)), (137, range(4, 21)), (135, range(4, 21)), (91, range(4, 21)), (37, range(4, 21))]:
    print(f'rule {r}:', '; '.join(row(r, n) for n in rng))
for r, f in [(43, lambda n: n // 2), (142, lambda n: (n + 1) // 2 + 1), (35, lambda n: 1), (59, lambda n: 1)]:
    print(f'rule {r}: m formula holds n=4..16: {all(rec(n, r).m == f(n) for n in range(4, 17))}; codes on cycles: {sorted({rec(n, r).union for n in range(4, 17)})}')
for r in [154, 26, 166, 161, 129, 30]:
    print(f'rule {r}: codes on cycles n=4..16: {[rec(n, r).union for n in range(4, 17)]}; cycles: {[rec(n, r).m for n in range(4, 17)]}')
ev = sum(1 << i for i in range(0, 20, 2)); od = ev << 1
print('154, 26: periodic states with ones on both parity classes, n = 4..16:', sum(1 for r in [154, 26] for n in range(4, 17) for x in np.flatnonzero(vb.Sys(r, n, 'null').per == 1) if (x & ev) and (x & od)))
for n in [8, 14]:
    s = vb.Sys(137, n, 'null'); print(f'137, n = {n}: codes of each cycle', [mstr(int(c)) for c in s.cycle_mask])
for rule, n, pat in [(94, 20, '110'), (94, 17, '110'), (133, 18, '010')]:
    s = vb.Sys(rule, n, 'null'); cl = s.closed_classes(); x0 = st((pat * n)[:n])
    print(f'{rule}, n = {n}: closed classes {[len(k) for k in cl]}; the crystal {pat}... is a fixed point and is that class: {bool(s.succ[x0] == x0 and int(s.cyc[x0]) in set(cl[0].tolist()))}')

H('11. single-flip simulations (own simulator), cross-checked against exact radii at small n')
def exr(rule, n, x0):
    s = vb.Sys(rule, n, 'null'); V, _ = s.resist(); c = s.cyc[x0]
    return True if s.m == 1 else int(np.delete(V[c], c).min()) >= 2
print('simulator vs exact radius, disagreements:', [(r, n) for r, p, nn in [(94, '110', [5, 8, 11, 14]), (133, '010', [6, 9, 12]), (122, '01', range(4, 14)), (137, '1000', range(5, 15)), (75, '110', [5, 8, 11, 14])] for n in nn if ls.radius2(r, n, st((p * n)[:n])) != exr(r, n, st((p * n)[:n]))] or 'none')
print('94 crystal radius 2 fails at n = 2 mod 3, 5..62:', [n for n in range(5, 63, 3) if ls.radius2(94, n, st(('110' * n)[:n])) is not True])
print('133 (010)^k radius 2 fails at 3|n, 6..60:', [n for n in range(6, 61, 3) if ls.radius2(133, n, st(('010' * n)[:n])) is not True])
print('75 crystal radius 2 at n = 2 mod 3, 5..62:', {n: ls.radius2(75, n, st(('110' * n)[:n])) for n in range(5, 63, 3)})
r122 = {n: ls.radius2(122, n, st(('01' * n)[:n])) for n in range(4, 62)}
print('122 checkerboard radius 2 at n (4..61):', [n for n, v in r122.items() if v], '; undecided at 2e4 steps:', [n for n, v in r122.items() if v is None],
      '; n = 56 at 4e5 steps:', ls.radius2(122, 56, st(('01' * 56)[:56]), limit=400000))
print('137 (1000)^k radius 2 at odd n (5..61):', [n for n in range(5, 62, 2) if ls.radius2(137, n, st(('1000' * n)[:n]))])
def seeds(rule, n, limit):
    F = ls.step_fn(rule, n); und = False
    for i in range(n):
        c = ls.orbit_cycle(F, 1 << i, limit)
        if c is None: und = True; continue
        if 0 not in c: return f'no (seed e_{i} ends on a cycle of period {len(c)})'
    return 'undecided' if und else 'yes'
s22 = {n: seeds(22, n, 20000) for n in range(4, 63)}
print('22: all single flips of 0 die at n =', [n for n, v in s22.items() if v == 'yes'], '; undecided at 2e4:', [n for n, v in s22.items() if v == 'undecided'])
print('   n = 55, 56, 57 at 2e4 steps:', {n: s22[n] for n in [55, 56, 57]}, '; n = 56 at 4e5 steps:', seeds(22, 56, 400000))
print('122 zero state: n in 4..62 where every single flip dies or is undecided:', [n for n in range(4, 63) if not seeds(122, n, 20000).startswith('no')])
def refl94(n):
    s = vb.Sys(94, n, 'reflect'); return [ls.radius2(94, n, int(x), 'reflect') for x in np.flatnonzero((s.succ == np.arange(1 << n)) & (s.mask == 0b1101000))]
print('94 reflect: radius-2 test of the fixed points with codes exactly {3,5,6}:', {n: refl94(n) for n in range(3, 16) if refl94(n)})

H('12. reader finding 2: data/boundaries/ring_vs_null.csv, column null_missed')
rvn = pd.read_csv(D + 'ring_vs_null.csv', dtype={'null_missed': str}); c2 = Counter()
for r in rvn.itertuples():
    if pd.isna(r.null_kstar): c2['no null data'] += 1; continue
    x = rec(r.n, r.rule); rep_m = '' if x.bij else nz(x.missed)
    true_m = ''.join(sorted(str(crefl(int(c))) for c in rep_m)) if r.rule != min(r.rule, R(r.rule)) else rep_m
    fm = nz(r.null_missed) if isinstance(r.null_missed, str) else ''
    c2['ok' if fm == true_m else ('representative instead of mirror image, n<=9' if r.n <= 9 else 'representative instead of mirror image, n>=10') if fm == rep_m else 'other'] += 1
    if kst(x) != '>=1' and int(float(r.null_kstar)) != int(kst(x)): c2['k* differs'] += 1
print(dict(c2))

H('13. prediction numbers (Section 7)')
print('shifts: k* of 170 and 15 at n = 4..16:', {r: sorted({rec(n, r).kstar for n in range(4, 17)}) for r in [170, 15]})
def rside(n, r): k, j = fwi[(n, r)]; return 0 if j else int(k >= 1)
for n in [12, 13, 14, 16]: print(f'  ring rules with k*>=1 at n = {n}: {sum(size88[r] * rside(n, r) for r in ringcls)}')
alw = [r for r in ringcls if all(rside(n, r) for n in range(8, 21))]; rl = sorted(set().union(*[ringcls[r] for r in alw]))
print('ring classes with k*>=1 at every n = 8..20:', len(alw), '; rules', len(rl), '; of these with null k*>=1 at n = 12, 13, 14:', [sum(S[(n, min(x, R(x)))] for x in rl) for n in [12, 13, 14]])

H('14. Wang et al. (2025), Table 1 (arXiv 2402.05404v2, p. 10): reversibility sequences n = 1..12, own brute force')
def revseq(sv, bnd):
    tab = {(k >> 2 & 1, k >> 1 & 1, k & 1): int(sv[7 - k]) for k in range(8)}; out = ''
    for n in range(1, 13):
        imgs = set()
        for x in range(2 ** n):
            g = lambda j: ((x >> j) & 1) if 0 <= j < n else (((x >> (j % n)) & 1) if bnd == 'p' else 0)
            imgs.add(tuple(tab[(g(i - 1), g(i), g(i + 1))] for i in range(n)))
        out += '1' if len(imgs) == 2 ** n else '0'
    return out
blockN = {'10101010': '000000000000', '10101001': '100000000000', '10100110': '100000000000', '10100101': '010101010101', '10010110': '101101101101'}
blockP = {'11100001': '000000000000', '11010010': '101010101010', '11000011': '000000000000', '10101001': '000000000000', '10100110': '101010101010', '10010110': '110110110110'}
for nm, blk, b in [('null block', blockN, 'n'), ('periodic block', blockP, 'p')]:
    for sv, seq in blk.items():
        print(f'  {nm}: {sv} (rule {int(sv, 2)}): table {seq}; own null {revseq(sv, "n")}; own periodic {revseq(sv, "p")}; table = own {b}: {revseq(sv, b) == seq}')
