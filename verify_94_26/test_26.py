"""Tests of PROOF_26.md (rule 26), own code from the rule table and the statements.

usage: python verify_94_26/test_26.py [nmax]     (default 20; even n only)
output: verify_94_26/out/test_26.json
"""
import os, sys, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca

RULE = 26
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
t0 = time.process_time()
results = []
EVEN = list(range(4, NMAX + 1, 2))
POW2 = (4, 8, 16, 32, 64, 128, 256, 512, 1024)


def record(test, statement, nrange, cases, viol, examples=None, extra=None):
    r = dict(test=test, statement=statement, n=nrange, cases=int(cases), violations=int(viol))
    if examples:
        r['examples'] = examples[:5]
    if extra is not None:
        r['extra'] = extra
    results.append(r)
    eca.log(f'{test:6s} n={nrange:14s} cases={cases:9d} violations={viol}')


def popcount(a):
    return np.bitwise_count(np.asarray(a, dtype=np.uint64)).astype(np.int64)


def ror(x, n, d):
    """bit p of the result = x_(p+d)"""
    mask = (1 << n) - 1
    d %= n
    return ((x >> d) | (x << (n - d))) & mask if d else x


def c_all(xs, n):
    """c(x) for an array of states: number of ones p whose next one (cyclically) is at odd distance"""
    xs = np.asarray(xs, dtype=np.int64)
    rem = xs.copy()
    cnt = np.zeros(len(xs), dtype=np.int64)
    for d in range(1, n + 1):
        hit = rem & ror(xs, n, d)
        if d % 2 == 1:
            cnt += popcount(hit)
        rem &= ~hit
    return cnt


def ones(x, n):
    return [i for i in range(n) if (x >> i) & 1]


def c1(x, n):
    o = ones(x, n)
    if len(o) < 2:
        return 0
    return sum(1 for k in range(len(o)) if (o[k] - o[k - 1]) % 2 == 1)


EVENMASK = {}


def parity_masks(n):
    if n not in EVENMASK:
        e = sum(1 << i for i in range(0, n, 2))
        EVENMASK[n] = (e, ((1 << n) - 1) ^ e)
    return EVENMASK[n]


def in_M(x, n):
    e, o = parity_masks(n)
    return (x & e) != 0 and (x & o) != 0


def sources(x, n):
    """sources = first one of every maximal run of equal parity in the cyclic sequence of ones (x in M)"""
    o = ones(x, n)
    return [o[k] for k in range(len(o)) if (o[k] - o[k - 1]) % 2 == 1]


def is_domain(x, n):
    if not in_M(x, n):
        return False
    s = sources(x, n)
    return all((s[(k + 1) % len(s)] - s[k]) % n >= 3 for k in range(len(s)))


def is_domain_3a(x, n):
    """characterisation of Lemma 3(a)"""
    if not in_M(x, n):
        return False
    o = ones(x, n)
    for k in range(len(o)):
        j = o[k]
        if (x >> ((j + 1) % n)) & 1:
            prev = o[k - 1]          # preceding one in cyclic order (may be j+1 itself)
            if (j - prev) % n % 2 == 1:
                return False
    return True


def U_all(xs, n):
    return np.array([eca.rot(int(v), n, 1) for v in eca.step_all(RULE, n, xs)], dtype=np.int64)


def has111(x, n):
    return eca.has_code(x, n, 7)


def has111_all(xs, n):
    mask = (1 << n) - 1
    xs = np.asarray(xs, dtype=np.int64)
    a = ((xs << 1) | (xs >> (n - 1))) & mask
    c = ((xs >> 1) | (xs << (n - 1))) & mask
    return (a & xs & c) != 0


# ------------------------------------------------------------------- Lemma 1
def test_M1():
    viol = cases = 0
    for n in range(3, NMAX + 1):
        mask = (1 << n) - 1
        u = np.arange(1 << n, dtype=np.int64)
        Uu = eca.step_all(RULE, n)
        Uu = ((Uu << 1) | (Uu >> (n - 1))) & mask      # sigma F
        u1 = ((u << 1) | (u >> (n - 1))) & mask          # bit j = u(j-1)
        u2 = ((u << 2) | (u >> (n - 2))) & mask          # bit j = u(j-2)
        rhs = u ^ (u2 & ~(u1 & ~u)) & mask
        viol += int(np.sum(Uu != (rhs & mask)))
        cases += 1 << n
    record('M1', 'Lemma 1: sigma F(u)(j) = u(j) + u(j-2)[1 + u(j-1)(1 + u(j))]; every state', f'3..{NMAX}', cases, viol)


# ------------------------------------------------------------------- Lemma 2
def test_M2():
    viol = cases = vf = cf = 0
    for n in EVEN:
        xs = np.arange(1 << n, dtype=np.int64)
        c = c_all(xs, n)
        if n <= 12:
            assert all(c[x] == c1(x, n) for x in range(1 << n))
        F = eca.step_all(RULE, n)
        viol += int(np.sum(c[F] > c))
        cases += 1 << n
        for j in range(n):
            y = xs ^ (1 << j)
            d = c[y] - c
            bad = ~np.isin(d, [-2, 0, 2])
            dele = ((xs >> j) & 1) == 1
            bad |= dele & (d > 0)
            vf += int(np.sum(bad))
            cf += 1 << n
    record('M2', 'Lemma 2: c(Fx) <= c(x); every state', f'4..{NMAX} even', cases, viol)
    record('M2f', 'Lemma 2: a flip changes c by -2, 0, 2; deleting a one does not increase c; every state and cell', f'4..{NMAX} even', cf, vf)


# ------------------------------------------------------------------- Lemma 3, Lemma 5, Lemma 8 (domain part)
def test_M3(nmax=None):
    nmax = nmax or NMAX
    v_a = v_b = v_c = v_111 = v_free = v5 = cases = 0
    ex = []
    counts = {}
    f_keeps_sources = 0
    f_moves_sources = 0
    counterexample = None
    for n in [k for k in EVEN if k <= nmax]:
        F = eca.step_all(RULE, n)
        dom = []
        for x in range(1 << n):
            d1 = is_domain(x, n)
            if d1 != is_domain_3a(x, n):
                v_a += 1
                ex.append(('3a', n, eca.word(x, n)))
            if d1:
                dom.append(x)
            elif in_M(x, n):
                # Lemma 5: a singleton group exists and its deletion lowers c by 2
                o = ones(x, n)
                sing = [o[k] for k in range(len(o)) if (o[k] - o[k - 1]) % 2 == 1 and (o[(k + 1) % len(o)] - o[k]) % 2 == 1]
                if not sing or any(c1(x ^ (1 << j), n) != c1(x, n) - 2 for j in sing):
                    v5 += 1
        counts[n] = len(dom)
        dset = set(dom)
        cases += len(dom)
        img = set()
        for x in dom:
            s = sources(x, n)
            u = eca.rot(int(F[x]), n, 1)          # U = sigma F
            img.add(int(F[x]))
            # (b): same sources, odd offsets 0, free cells c_k + c_(k-1)
            ok = is_domain(u, n) and sorted(sources(u, n)) == sorted(s)
            ss = sorted(s)
            for k, a in enumerate(ss):
                b = ss[(k + 1) % len(ss)]
                dlen = (b - a) % n
                prev = 1
                for t in range(1, dlen):
                    cell = (a + t) % n
                    if t % 2 == 1:
                        ok &= ((u >> cell) & 1) == 0
                    else:
                        ck = (x >> cell) & 1
                        ok &= ((u >> cell) & 1) == (ck ^ prev)
                        prev = ck
            if not ok:
                v_b += 1
                ex.append(('3b', n, eca.word(x, n)))
            if has111(x, n):
                v_111 += 1
            fs = sorted(sources(int(F[x]), n))
            if fs == ss:
                f_keeps_sources += 1
            else:
                f_moves_sources += 1
                if counterexample is None:
                    counterexample = dict(n=n, x=eca.word(x, n), sources_x=ss, Fx=eca.word(int(F[x]), n), sources_Fx=fs)
            # flipping a free cell keeps a domain state with the same sources
            for k, a in enumerate(ss):
                b = ss[(k + 1) % len(ss)]
                for t in range(2, (b - a) % n, 2):
                    y = x ^ (1 << ((a + t) % n))
                    if not (is_domain(y, n) and sorted(sources(y, n)) == ss):
                        v_free += 1
        if img != dset:
            v_c += 1
            ex.append(('3c', n))
    record('M3a', 'Lemma 3(a): domain state (sources at distances >= 3) iff no adjacent ones (j, j+1) whose preceding one is at odd distance; every state', f'4..{nmax} even', 2 ** (nmax + 1), v_a, ex)
    record('M3b', 'Lemma 3(b): U(u) is a domain state with the same sources, zeros at odd offsets, free cells c_k + c_(k-1); every domain state', f'4..{nmax} even', cases, v_b)
    record('M3c', 'Lemma 3(c): F maps the set of domain states onto itself; no domain state contains 111; flipping a free cell keeps a domain state with the same sources', f'4..{nmax} even', cases, v_c + v_111 + v_free,
           extra=dict(domain_state_counts=counts))
    record('M3F', 'Lemma 3(c), wording: does F (not U) preserve the set of sources? (finding C1 expects: no)', f'4..{nmax} even', cases, 0,
           extra=dict(F_keeps_sources=f_keeps_sources, F_changes_sources=f_moves_sources, counterexample=counterexample))
    record('M5', 'Lemma 5: every state of M that is not a domain state has a singleton group; deleting a singleton group lowers c by 2', f'4..{nmax} even', 2 ** (nmax + 1), v5)


# ------------------------------------------------------------------- Lemma 4
def test_M4(nmax=16):
    viol = cases = viol_h = 0
    for n in [k for k in EVEN if k <= nmax]:
        Ftab = eca.step_all(RULE, n)
        Utab = np.array([eca.rot(int(v), n, 1) for v in Ftab], dtype=np.int64)
        for u in range(1 << n):
            o = ones(u, n)
            if len(o) < 2:
                continue
            for k in range(len(o)):
                j = o[k]
                if not (u >> ((j + 1) % n)) & 1:
                    continue
                dist = (j - o[k - 1]) % n
                if dist % 2 == 0:
                    continue
                r = (dist - 1) // 2
                v = u
                for _ in range(r):
                    v = int(Utab[v])
                cases += 1
                if not all((v >> ((j + t) % n)) & 1 for t in (-1, 0, 1)):
                    viol += 1
            if in_M(u, n) and not is_domain(u, n):
                v = u
                found = has111(v, n)
                for _ in range(n // 2 - 1):
                    v = int(Ftab[v])
                    found = found or has111(v, n)
                if not found:
                    viol_h += 1
    record('M4', 'Lemma 4: u(j)=u(j+1)=1, preceding one at distance 2r+1 => U^r(u) has 111 at j-1, j, j+1; and every non-domain state of M meets 111 within n/2-1 steps', f'4..{nmax} even', cases, viol + viol_h)


# ------------------------------------------------------------------- Lemma 6
def test_M6():
    viol = cases = 0
    for n in EVEN:
        if n > 16:
            break
        e, o = parity_masks(n)
        F = eca.step_all(RULE, n)
        F90 = eca.step_all(90, n)
        for x in range(1 << n):
            if (x & o) == 0 or (x & e) == 0:
                cases += 1
                y = int(F[x])
                ok = y == int(F90[x])
                if x & o == 0:
                    ok &= (y & e) == 0
                else:
                    ok &= (y & o) == 0
                if n in POW2:
                    z = x
                    for _ in range(n // 2):
                        z = int(F[z])
                    ok &= z == 0
                if not ok:
                    viol += 1
    for n in (32, 64, 128, 256, 512, 1024):
        cells = [0] * n
        cells[0] = 1
        for _ in range(n // 2):
            cells = eca.step_list(RULE, cells)
            if any(cells[i] and cells[(i + 1) % n] for i in range(n)):
                viol += 1
                break
        cases += 1
        if any(cells):
            viol += 1
    record('M6', 'Lemma 6: on E and O rule 26 = rule 90, E -> O -> E; F^(n/2) = 0 there for n = 2^k (all of E u O for n<=16, single seed for n=32..1024)', f'4..16; 32..1024', cases, viol)


# ------------------------------------------------------------------- Lemma 7 (carrier words)
def test_M7(nmax=31):
    viol = cases = 0
    for n in range(5, nmax + 1):
        words = set()

        def gen(prefix, length):
            if length == n:
                if '11100' in prefix or False:
                    words.add(prefix)
                return
            for b in ('11100', '100'):
                if length + len(b) <= n:
                    gen(prefix + b, length + len(b))
        gen('', 0)
        ws = set()
        for w in words:
            if '11100' not in w:
                continue
            for k in range(n):
                ws.add(w[k:] + w[:k])
        for w in ws:
            cells = [int(ch) for ch in w]
            y = eca.step_list(RULE, eca.step_list(RULE, cells))
            cases += 1
            if y != [cells[-1]] + cells[:-1]:
                viol += 1
    record('M7', 'Lemma 7: F^2(w) = sigma w for every cyclic word over 11100, 100 with at least one 11100; every rotation', f'5..{nmax}', cases, viol)


# ------------------------------------------------------------------- Theorem 1, Lemma 8, Lemma 9, Theorems 2, 3, 5 (enumeration)
def r90_periodic_in_EO(n):
    """periodic states of rule 90 inside E u O (rule 90 iterated by its own table)"""
    F90 = eca.step_all(90, n)
    G = F90.copy()
    for _ in range(n + 1):
        G = G[G]
    per = np.zeros(1 << n, dtype=bool)
    per[G] = True
    e, o = parity_masks(n)
    xs = np.arange(1 << n, dtype=np.int64)
    eo = ((xs & o) == 0) | ((xs & e) == 0)
    return per & eo, eo


def test_enum():
    rows = []
    v_t1 = v_l8 = v_l9 = v_t2 = v_t3 = v_t5 = v_cconst = 0
    ex = []
    for n in EVEN:
        R = eca.Ring(RULE, n)
        xs = np.arange(1 << n, dtype=np.int64)
        per = R.periodic
        c = c_all(xs, n)
        p90, eo = r90_periodic_in_EO(n)
        isdom = np.zeros(1 << n, dtype=bool)
        for x in R.pstates:
            isdom[x] = is_domain(int(x), n)
        # all domain states are periodic (checked on all states for n <= 16)
        if n <= 16:
            alldom = np.array([is_domain(x, n) for x in range(1 << n)])
            if np.any(alldom & ~per):
                v_t1 += 1
                ex.append(('domain not periodic', n))
        # Theorem 1 classification
        cyc_kind = {}
        cyc_c = {}
        cyc_111 = {}
        for cid in range(R.m):
            st = R.cycle_states(cid)
            cs = {int(c[y]) for y in st}
            if len(cs) != 1:
                v_cconst += 1
            cyc_c[cid] = cs.pop()
            h = any(has111(y, n) for y in st)
            cyc_111[cid] = h
            kinds = set()
            for y in st:
                if eo[y]:
                    kinds.add('eo')
                elif isdom[y]:
                    kinds.add('dom')
                else:
                    kinds.add('other')
            if len(kinds) != 1:
                v_t1 += 1
                ex.append(('mixed kinds', n, cid))
            k = kinds.pop()
            if k == 'eo' and not all(p90[y] for y in st):
                v_t1 += 1
            if k == 'other' and not h:
                v_t1 += 1
                ex.append(('other without 111', n, eca.word(st[0], n)))
            if k == 'dom' and h:
                v_t1 += 1
            cyc_kind[cid] = 'zero' if st == [0] else k
        # periodic in E u O == rule-90 periodic in E u O
        if np.any((per & eo) != p90):
            v_t1 += 1
            ex.append(('EO periodic mismatch', n))
        if n in POW2 and int(np.sum(per & eo)) != 1:
            v_t1 += 1
        # Lemma 8 codes
        for cid, k in cyc_kind.items():
            codes = R.codes_of_cycles([cid])
            if k == 'dom' and not {1, 2, 3, 4, 5, 6} <= codes:
                v_l8 += 1
            if n in POW2 and k != 'zero' and not {3, 6} <= codes:
                v_l8 += 1
        ncomp, comp, closed = R.closed_classes()
        A, e = R.g1()
        z = int(R.label[0])
        r90c = [cid for cid, k in cyc_kind.items() if k in ('eo', 'zero')]
        dom_c = [cid for cid, k in cyc_kind.items() if k == 'dom']
        c111 = [cid for cid in range(R.m) if cyc_111[cid]]
        # Lemma 9: all E u O cycles in one strong component
        if len({int(comp[cid]) for cid in r90c}) != 1:
            v_l9 += 1
        # Theorem 2: every cycle reaches an E u O cycle
        # reverse reachability from r90c
        radj = [[] for _ in range(R.m)]
        for s_, d_ in e:
            radj[d_].append(s_)
        seen = set(r90c)
        stack = list(r90c)
        while stack:
            u = stack.pop()
            for v in radj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(seen) != R.m:
            v_t2 += 1
        maxinc = int(max((cyc_c[int(d_)] - cyc_c[int(s_)] for s_, d_ in e), default=0))
        if maxinc > 2:
            v_t2 += 1
        K = set(closed[0].tolist()) if len(closed) == 1 else None
        row = dict(n=n, cycles=R.m, periodic_states=int(len(R.pstates)), g1_edges=int(len(e)),
                   closed_sizes=[len(cc) for cc in closed], one_parity_cycles_not_zero=len(r90c) - 1,
                   domain_cycles=len(dom_c), cycles_with_111=len(c111),
                   c_domain=sorted({cyc_c[cid] for cid in dom_c}), c_111=sorted({cyc_c[cid] for cid in c111}),
                   max_c_increase_along_edge=maxinc,
                   periodic_by_kind=dict(zero=1, one_parity=int(np.sum(per & eo)) - 1,
                                         domain=int(np.sum(isdom)),
                                         orbit_111=int(len(R.pstates) - np.sum(per & eo) - np.sum(isdom))))
        # cycles with 111 through a carrier word
        carr = 0
        for cid in c111:
            if any(is_carrier(y, n) for y in R.cycle_states(cid)):
                carr += 1
        row['cycles_111_through_carrier'] = carr
        if K is not None:
            row['zero_in_K'] = z in K
            row['one_parity_in_K'] = f'{sum(1 for cc in r90c if cc in K)} of {len(r90c)}'
            row['domain_in_K'] = f'{sum(1 for cc in dom_c if cc in K)} of {len(dom_c)}'
            row['c111_in_K'] = f'{sum(1 for cc in c111 if cc in K)} of {len(c111)}'
            row['codes_on_K'] = sorted(R.codes_of_cycles(K))
        if n in POW2:
            ok = K == {z} and len(closed) == 1
            # Theorem 3(a): no edge leaves {0}
            ok &= not np.any(e[:, 0] == z) if len(e) else True
            if not ok:
                v_t3 += 1
        else:
            ok = K is not None and set(r90c) <= K and set(dom_c) <= K
            ok &= all(cyc_111[cc] for cc in range(R.m) if cc not in K)
            ok &= set(range(7)) <= set(row['codes_on_K'])
            if not ok:
                v_t5 += 1
                ex.append(('T5', n))
        rows.append(row)
        eca.log('  26 row', n, row['closed_sizes'], row.get('c111_in_K'), row['c_domain'], row['c_111'], carr)
    nl = f'4..{NMAX} even'
    record('T1', 'Theorem 1: c constant on cycles; periodic states = rule-90 periodic states in E u O, domain states (all periodic), and states of M (not domain) whose cycle contains 111', nl, len(EVEN), v_t1 + v_cconst, ex)
    record('L8', 'Lemma 8: every domain cycle has codes 1..6; for n = 2^k every cycle other than {0} has codes 3 and 6', nl, len(EVEN), v_l8)
    record('L9', 'Lemma 9: the cycles contained in E u O lie in one strong component of G1', nl, len(EVEN), v_l9)
    record('T2', 'Theorem 2: every cycle has a G1 path to a cycle contained in E u O; c rises by at most 2 along a G1 edge', nl, len(EVEN), v_t2)
    record('T3ab', 'Theorem 3(a),(b): for n = 2^k no G1 edge leaves {0}, and {0} is the only closed class', nl, len(EVEN), v_t3)
    record('T5', 'Theorem 5: for even n not a power of two one closed class K, containing {0}, all E u O cycles and all domain cycles; cycles outside K contain 111; codes 0..6 on K', nl, len(EVEN), v_t5, extra=rows)
    return rows


def is_carrier(x, n):
    s = eca.word(x, n)
    for k in range(n):
        t = s[k:] + s[:k]
        i, ok, big = 0, True, False
        while i < n:
            if t.startswith('11100', i):
                i += 5
                big = True
            elif t.startswith('100', i):
                i += 3
            else:
                ok = False
                break
        if ok and big:
            return True
    return False


# ------------------------------------------------------------------- Theorem 2 chain, executed (own reading of the proof)
def chain_T2(x, n, Ftab=None, cap=10 ** 6):
    """execute the chain of Theorem 2 from the cycle of the periodic state x; return number of flips and drops"""
    def F(y):
        if Ftab is not None:
            return int(Ftab[y])
        return eca.from_cells(eca.step_list(RULE, eca.to_cells(y, n)))

    def to_cycle(y):
        seen = {}
        t = 0
        while y not in seen:
            seen[y] = t
            y = F(y)
            t += 1
            if t > cap:
                raise RuntimeError('cap')
        # y is on the cycle
        cyc = [y]
        z = F(y)
        while z != y:
            cyc.append(z)
            z = F(z)
        return cyc

    cyc = to_cycle(x)
    flips = drops = 0
    while True:
        cval = c1(cyc[0], n)
        if cval == 0:
            return flips, drops, cyc
        # case 1: a state with a singleton group
        done = False
        for y in cyc:
            o = ones(y, n)
            sing = [o[k] for k in range(len(o)) if (o[k] - o[k - 1]) % 2 == 1 and (o[(k + 1) % len(o)] - o[k]) % 2 == 1]
            if sing:
                y2 = y ^ (1 << sing[0])
                assert c1(y2, n) == cval - 2
                new = to_cycle(y2)
                assert c1(new[0], n) <= cval - 2
                cyc = new
                flips += 1
                drops += 1
                done = True
                break
        if done:
            continue
        # case 2: all domain states; delete the further ones of one group, last first
        y = cyc[0]
        assert all(is_domain(v, n) for v in cyc)
        s = sorted(sources(y, n))
        a, b = s[0], s[1]
        further = [(a + t) % n for t in range(2, (b - a) % n, 2) if (y >> ((a + t) % n)) & 1]
        assert further
        for j in reversed(further):
            y ^= 1 << j
            assert is_domain(y, n) and sorted(sources(y, n)) == s
            flips += 1
        cyc = to_cycle(y)


def test_chains():
    viol = cases = 0
    stats = {}
    for n in EVEN:
        R = eca.Ring(RULE, n)
        mx = 0
        for cid in range(R.m):
            x = int(R.reps[cid])
            cases += 1
            try:
                fl, dr, end = chain_T2(x, n, R.F)
                ok = c1(end[0], n) == 0 and (n not in POW2 or end == [0])
            except AssertionError:
                ok = False
            if not ok:
                viol += 1
            mx = max(mx, fl)
        stats[n] = mx
    rnd = random.Random(26)
    for n in (32, 64, 128):
        for _ in range(30 if n < 128 else 10):
            x = rnd.getrandbits(n)
            cells = eca.to_cells(x, n)
            for _ in range(4 * n):
                cells = eca.step_list(RULE, cells)
            cases += 1
            try:
                fl, dr, end = chain_T2(eca.from_cells(cells), n)
                ok = end == [0]
            except (AssertionError, RuntimeError):
                ok = False
            if not ok:
                viol += 1
    record('T2ch', 'Theorem 2: the chain of the proof (case 1 singleton deletion, case 2 deletion inside a group) executed from every cycle (even n<=NMAX) and from random cycles (n=32, 64, 128) ends on E u O, at {0} for n=2^k', f'4..{NMAX}; 32..128', cases, viol, extra=dict(max_flips=stats))


# ------------------------------------------------------------------- Theorem 3(d), 4(b), 4(c) chains on larger rings
def periodic_sim(x, n, cap=200000):
    cells = eca.to_cells(x, n)
    c0 = cells
    for t in range(1, cap + 1):
        cells = eca.step_list(RULE, cells)
        if cells == c0:
            return t
    return None


def test_T34_chains():
    viol = cases = 0
    ex = []
    # 4(c): n = 2^k, k odd
    for n in (8, 32, 128, 512):
        q = (n - 5) // 3
        y = eca.from_word('11100' + '100' * q)
        x = y ^ (1 << 1)
        cases += 1
        ok = is_domain(x, n) and sorted(sources(x, n)) == [0] + list(range(5, n - 2, 3))
        ok &= periodic_sim(x, n) is not None and periodic_sim(y, n) is not None and has111(y, n)
        # chain of 3(d) from e_0 + e_5 to x through domain states
        s = sorted(sources(x, n))
        st = (1 << s[0]) | (1 << s[1])
        ok &= is_domain(st, n)
        for a in s[2:]:
            st |= 1 << a
            ok &= is_domain(st, n)
        for j in ones(x, n):
            if not (st >> j) & 1:
                st |= 1 << j
                ok &= is_domain(st, n)
        ok &= st == x
        if not ok:
            viol += 1
            ex.append(('4c', n))
    # 4(b): 0, e_0, F(e_0), F^2(e_0)+e_1 -> next state has 111 at -1,0,1
    for n in (8, 16, 32, 64, 128, 256, 512, 1024):
        cells = [0] * n
        cells[0] = 1
        c1_ = eca.step_list(RULE, cells)
        c2_ = eca.step_list(RULE, c1_)
        c2_[1] ^= 1
        c3_ = eca.step_list(RULE, c2_)
        cases += 1
        if not (c3_[-1] == c3_[0] == c3_[1] == 1):
            viol += 1
    # 3(d): from e_s1 + e_s2 to random domain states at n = 32, 64
    rnd = random.Random(3)
    for n in (16, 32, 64):
        for _ in range(100):
            # random domain state: random domain lengths (odd >= 3) summing to n, even number of domains
            while True:
                lens = []
                tot = 0
                while tot < n:
                    L = rnd.choice(range(3, min(n, 15) + 1, 2))
                    lens.append(L)
                    tot += L
                if tot == n and len(lens) % 2 == 0:
                    break
            x = 0
            pos = rnd.randrange(n)
            for L in lens:
                x |= 1 << (pos % n)
                for t in range(2, L, 2):
                    if rnd.random() < 0.5:
                        x |= 1 << ((pos + t) % n)
                pos += L
            if not is_domain(x, n):
                viol += 1
                continue
            s = sorted(sources(x, n), key=lambda v: v)
            st = (1 << s[0]) | (1 << s[1])
            ok = is_domain(st, n)
            for a in s[2:]:
                st |= 1 << a
                ok &= is_domain(st, n)
            for j in ones(x, n):
                if not (st >> j) & 1:
                    st |= 1 << j
                    ok &= is_domain(st, n)
            ok &= st == x
            cases += 1
            if not ok:
                viol += 1
                ex.append(('3d', n, eca.word(x, n)))
    record('T34ch', 'Theorems 3(d), 4(b), 4(c): the chains of the proofs (sources s1, s2, then further sources, then free cells: domain states throughout; the resistance-2 path to 111; 10100(100)^q periodic domain state next to the periodic carrier 11100(100)^q)', '8..1024', cases, viol, ex)


# ------------------------------------------------------------------- Theorem 5 chain for domain cycles (n not a power of two)
def test_T5_chain():
    viol = cases = 0
    for n in [k for k in EVEN if k not in POW2]:
        R = eca.Ring(RULE, n)
        e2 = 0
        q = n
        while q % 2 == 0:
            q //= 2
            e2 += 1
        e_ = e2 - 1
        step = 2 ** (e_ + 1)
        for cid in range(R.m):
            x = int(R.reps[cid])
            if not is_domain(x, n):
                continue
            cases += 1
            ok = True
            # reduce to two domains
            while len(sources(x, n)) > 2:
                s = sorted(sources(x, n))
                a, b = s[0], s[1]
                grp = [(a + t) % n for t in range(2, (b - a) % n, 2) if (x >> ((a + t) % n)) & 1]
                for j in reversed(grp):
                    x ^= 1 << j
                    ok &= is_domain(x, n) and bool(R.periodic[x])
                x ^= 1 << a
                ok &= is_domain(x, n) and bool(R.periodic[x])
            s = sorted(sources(x, n))
            L1 = (s[1] - s[0]) % n
            a, b = (s[0], s[1]) if L1 >= n - L1 else (s[1], s[0])
            L = max(L1, n - L1)
            ok &= L >= step + 1
            target = (1 << a) | (1 << ((a + step) % n)) | (1 << b)
            # flips of free cells, one at a time
            diff = x ^ target
            for j in range(n):
                if (diff >> j) & 1:
                    x ^= 1 << j
                    ok &= is_domain(x, n) and bool(R.periodic[x])
            y = (1 << a) | (1 << ((a + step) % n))
            ok &= bool(R.periodic[y])
            if not ok:
                viol += 1
    record('T5ch', 'Theorem 5 proof: every domain cycle is joined to the one-parity state e_a + e_(a+2^(e+1)) by flips between periodic domain states (executed for every domain cycle)', f'even n<={NMAX}, not 2^k', cases, viol)


# ------------------------------------------------------------------- Section 7: a cycle with 111 and c = 6 at n = 22
def test_n22():
    """periodic flags only (no G1) at n = 22: one vectorised pass over the 2^22 states"""
    n = 22
    F = eca.step_all(RULE, n)
    G = F.copy()
    for _ in range(n + 1):
        G = G[G]
    per = np.zeros(1 << n, dtype=bool)
    per[G] = True
    ps = np.nonzero(per)[0]
    cs = c_all(ps, n)
    h = has111_all(ps, n)
    cand = ps[(cs == 6) & h]
    found = None
    if len(cand):
        x = int(cand.min())
        found = dict(state=eca.word(x, n), period=periodic_sim(x, n), c=c1(x, n), contains_111=has111(x, n),
                     periodic_states_with_111_and_c6=int(len(cand)),
                     c_values_of_periodic_states_with_111=sorted(set(cs[h].tolist())))
    record('S7n22', 'Section 7: at n = 22 some cycle contains 111 and has c = 6 (periodic flags of all 2^22 states, no G1)', '22', 1, 0 if found else 1, extra=found)


if __name__ == '__main__':
    test_M1()
    test_M2()
    test_M3(min(NMAX, 18))
    test_M4()
    test_M6()
    test_M7()
    test_enum()
    test_chains()
    test_T34_chains()
    test_T5_chain()
    test_n22()
    out = dict(rule=RULE, nmax=NMAX, results=results, cpu_seconds=round(time.process_time() - t0, 2),
               all_passed=all(r['violations'] == 0 for r in results))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'test_26.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    eca.log('ALL PASSED:', out['all_passed'], 'CPU s', out['cpu_seconds'])
