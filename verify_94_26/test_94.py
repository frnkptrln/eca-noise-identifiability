"""Tests of PROOF_94_converse.md (rule 94), own code from the rule table and the statements.

usage: python verify_94_26/test_94.py [nmax]      (default nmax = 20)
output: verify_94_26/out/test_94.json
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca

RULE = 94
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
t0 = time.process_time()
results = []


def record(test, statement, nrange, cases, viol, examples=None, extra=None):
    r = dict(test=test, statement=statement, n=nrange, cases=int(cases), violations=int(viol))
    if examples:
        r['examples'] = examples[:5]
    if extra is not None:
        r['extra'] = extra
    results.append(r)
    eca.log(f'{test:6s} n={nrange:12s} cases={cases:9d} violations={viol}')


def A_letter(i):
    return 0 if i % 6 in (4, 5) else 1


def B_letter(i):
    return 0 if i % 6 in (1, 2) else 1


def A_w(w):
    return tuple(A_letter(i) for i in range(1, w + 1))


def B_w(w):
    return tuple(B_letter(i) for i in range(1, w + 1))


def live_claimed(w):
    """the live window contents as stated in Theorem 1 / Lemma 8"""
    if w % 3 == 2:
        return {A_w(w), B_w(w)}
    if w == 4:
        return {(0, 0, 0, 0), (1, 0, 0, 1), (1, 1, 1, 1)}
    return set()


def occ_all(x, n):
    mask = (1 << n) - 1
    x = np.asarray(x, dtype=np.int64)
    a = ((x << 1) | (x >> (n - 1))) & mask
    c = ((x >> 1) | (x << (n - 1))) & mask
    return a & ~x & c & mask


def W_all(x, n):
    mask = (1 << n) - 1
    o = occ_all(x, n)
    return (o | ((o << 1) | (o >> (n - 1))) | ((o >> 1) | (o << (n - 1)))) & mask


def occ1(x, n):
    return int(occ_all(np.array([x]), n)[0])


def W1(x, n):
    return int(W_all(np.array([x]), n)[0])


def windows(x, n, Wm):
    """maximal runs of cells outside W: list of (first cell, width, content tuple); None if W empty or full"""
    full = (1 << n) - 1
    if Wm == 0 or Wm == full:
        return None
    f = (Wm & -Wm).bit_length() - 1
    res, cur = [], None
    for k in range(1, n + 1):
        cell = (f + k) % n
        if (Wm >> cell) & 1:
            if cur is not None:
                res.append(cur)
                cur = None
        else:
            if cur is None:
                cur = [cell, []]
            cur[1].append((x >> cell) & 1)
    return [(s, len(c), tuple(c)) for s, c in res]


def phi(u):
    """window map on a tuple, both outer neighbours held at 1"""
    w = len(u)
    pad = (1,) + tuple(u) + (1,)
    return tuple((RULE >> (4 * pad[i - 1] + 2 * pad[i] + pad[i + 1])) & 1 for i in range(1, w + 1))


def is_block_word(x, n):
    return W1(x, n) == (1 << n) - 1


def block_words(n):
    xs = np.arange(1 << n, dtype=np.int64)
    return np.nonzero(W_all(xs, n) == (1 << n) - 1)[0]


def doubled(v, p, n):
    h = n // 2
    x = 0
    for k in range(h):
        if (v >> k) & 1:
            x |= 1 << ((2 * k + p) % n)
            x |= 1 << ((2 * k + p + 1) % n)
    return x


def vper(h):
    """periodic points of v -> v + Sv on GF(2)^h, (Sv)_k = v_(k+1)"""
    def ap(v):
        s = (v >> 1) | ((v & 1) << (h - 1))
        return v ^ s
    return eca.periodic_points_linear(h, ap)


def dw_set(n):
    if n % 2:
        return set()
    V = vper(n // 2)
    return {doubled(v, p, n) for v in V if v != 0 for p in (0, 1)}


def v2(n):
    e = 0
    while n % 2 == 0:
        n //= 2
        e += 1
    return e, n


# ---------------------------------------------------------------- Lemma 8 (window map), vectorised
def test_L8(wmax=22):
    viol, cases, ex, found = 0, 0, [], {}
    for w in range(1, wmax + 1):
        N = 1 << w
        mask = N - 1
        u = np.arange(N, dtype=np.int64)
        a = ((u << 1) | 1) & mask                 # bit k = window cell k (cell k+1 in 1-based) left neighbour
        c = (u >> 1) | (1 << (w - 1))
        out = np.zeros_like(u)
        for code in range(8):
            if (RULE >> code) & 1:
                p, q, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
                out |= (a if p else ~a) & (u if q else ~u) & (c if r else ~c)
        P = out & mask
        frozen = (a & ~u & c & mask) != 0
        G = P.copy()
        for _ in range(w + 1):
            G = G[G]
        per = np.zeros(N, dtype=bool)
        per[G] = True
        bad = frozen.copy()
        Q = P.copy()
        for _ in range(w + 1):
            bad = bad | bad[Q]
            Q = Q[Q]
        live = np.nonzero(per & ~bad)[0]
        live_t = {tuple((int(v) >> k) & 1 for k in range(w)) for v in live}
        found[w] = sorted(''.join(map(str, t)) for t in live_t)
        cases += N
        if live_t != live_claimed(w):
            viol += 1
            ex.append(dict(w=w, found=found[w]))
        # orbit structure
        for t in live_t:
            img = phi(t)
            if w % 3 == 2 and img != (B_w(w) if t == A_w(w) else A_w(w)):
                viol += 1
                ex.append(dict(w=w, state=t, img=img))
            if w == 4:
                nxt = {(0, 0, 0, 0): (1, 0, 0, 1), (1, 0, 0, 1): (1, 1, 1, 1), (1, 1, 1, 1): (0, 0, 0, 0)}
                if img != nxt[t]:
                    viol += 1
                    ex.append(dict(w=w, state=t, img=img))
    record('L8', 'Lemma 8: live window orbits = {A_w,B_w} (w=2 mod 3), 0000->1001->1111 (w=4), none otherwise',
           f'w=1..{wmax}', cases, viol, ex, extra={w: found[w] for w in found if found[w]})


# ---------------------------------------------------------------- Lemma 7 (a), (b)
def test_L7(nmin=5, nmax=14, T=8):
    viol = cases = 0
    ex = []
    for n in range(nmin, nmax + 1):
        xs = np.arange(1 << n, dtype=np.int64)
        Wa = W_all(xs, n)
        full = (1 << n) - 1
        sel = np.nonzero((Wa != 0) & (Wa != full))[0]
        F = eca.step_all(RULE, n)
        for x in sel:
            x = int(x)
            Wm = int(Wa[x])
            wins = windows(x, n, Wm)
            cases += 1
            ok = True
            for s, w, cont in wins:
                left, right = (s - 1) % n, (s + w) % n
                if not ((Wm >> left) & 1 and (Wm >> right) & 1 and (x >> left) & 1 and (x >> right) & 1 and w <= n - 3):
                    ok = False
            y = x
            conts = [cont for _, _, cont in wins]
            for t in range(1, T + 1):
                y = int(F[y])
                if (y & Wm) != (x & Wm):
                    ok = False
                conts = [phi(cn) for cn in conts]
                for (s, w, _), cn in zip(wins, conts):
                    if tuple((y >> ((s + k) % n)) & 1 for k in range(w)) != cn:
                        ok = False
            if not ok:
                viol += 1
                ex.append(eca.word(x, n))
    record('L7ab', 'Lemma 7(a),(b): window neighbours frozen ones, width <= n-3; F^t = id on W, = phi^t on windows (t<=8)',
           f'{nmin}..{nmax}', cases, viol, ex)


# ---------------------------------------------------------------- Theorem 1, Lemma 7(c), Lemma 9 counts
def test_T1(nmin=3, nmax=NMAX):
    viol = cases = 0
    ex = []
    counts = {}
    viol9 = 0
    viol6 = 0
    for n in range(nmin, nmax + 1):
        R = eca.Ring(RULE, n)
        per = R.periodic
        xs = np.arange(1 << n, dtype=np.int64)
        Wa = W_all(xs, n)
        full = (1 << n) - 1
        DW = dw_set(n)
        # W empty
        e = np.nonzero(Wa == 0)[0]
        pred_e = np.isin(e, np.array(sorted(DW | {0}), dtype=np.int64))
        bad = np.nonzero(pred_e != per[e])[0]
        viol += len(bad)
        ex += [('emptyW', eca.word(int(e[b]), n)) for b in bad[:3]]
        cases += len(e)
        # W full: block words, must be fixed points
        f_ = np.nonzero(Wa == full)[0]
        badf = np.nonzero(R.F[f_] != f_)[0]
        viol += len(badf)
        cases += len(f_)
        # W proper: windows live
        mid = np.nonzero((Wa != 0) & (Wa != full))[0]
        LIVE = {w: live_claimed(w) for w in range(1, n + 1)}
        F6 = R.F.copy()
        for _ in range(5):
            F6 = R.F[F6]
        for x in mid:
            x = int(x)
            wins = windows(x, n, int(Wa[x]))
            pred = all(cont in LIVE[w] for _, w, cont in wins)
            cases += 1
            if pred != bool(per[x]):
                viol += 1
                if len(ex) < 6:
                    ex.append(('properW', eca.word(x, n), pred, bool(per[x])))
            if pred and F6[x] != x:
                viol6 += 1
        # Lemma 9 count, Theorem 1 case-2 count
        ne = int(np.sum(per[e]))
        if n % 2 == 1:
            exp = 1
        else:
            ee, q = v2(n)
            ee -= 1
            exp = 2 * (2 ** (n // 2 - 2 ** ee) - 1) + 1
        counts[n] = ne
        if ne != exp:
            viol9 += 1
    record('T1', 'Theorem 1: x periodic iff x=0, or doubled word D_p(v), v in V_per\\{0}, or W nonempty and every window live (A_w/B_w, w=2 mod 3; 0000/1001/1111, w=4); every state',
           f'{nmin}..{nmax}', cases, viol, ex)
    record('T1p6', 'Theorem 1: the period of a case-3 state divides 6 (F^6 x = x)', f'{nmin}..{nmax}', cases, viol6)
    record('L9n', 'Lemma 9 / Theorem 1 case 2: number of periodic states with empty frozen set = 1 (n odd), 2(2^(n/2-2^e)-1)+1 (n = 2^(e+1) q)',
           f'{nmin}..{nmax}', nmax - nmin + 1, viol9, extra=counts)


# ---------------------------------------------------------------- Lemma 10 (reversible freezing)
def test_L10(nmin=3, nmax=NMAX):
    viol = cases = 0
    ex = []
    cyc_without_move = 0
    ncyc = 0
    for n in range(nmin, nmax + 1):
        R = eca.Ring(RULE, n)
        full = (1 << n) - 1
        Wp = W_all(R.reps, n)
        for cid in range(R.m):
            if Wp[cid] == 0 or Wp[cid] == full:
                continue
            ncyc += 1
            any_move = False
            for y in R.cycle_states(cid):
                Wm = W1(y, n)
                O = occ1(y, n)
                for s, w, cont in windows(y, n, Wm):
                    p = (s - 1) % n
                    if w % 3 == 2 and cont == A_w(w):
                        j, centre, rest = p + 2, p + 2, (p + 4, w - 3, B_w(w - 3))
                    elif w % 3 == 2 and cont == B_w(w):
                        j, centre, rest = p + 1, p + 2, (p + 4, w - 3, A_w(w - 3))
                    elif w == 4 and cont == (1, 1, 1, 1):
                        j, centre, rest = p + 1, p + 1, (p + 3, 2, (1, 1))
                    elif w == 4 and cont == (0, 0, 0, 0):
                        j, centre, rest = p + 2, p + 1, (p + 3, 2, (0, 0))
                    else:
                        continue
                    any_move = True
                    cases += 1
                    j %= n
                    centre %= n
                    z = y ^ (1 << j)
                    Wz = W1(z, n)
                    Oz = occ1(z, n)
                    ok = bool(R.periodic[z]) and R.label[z] != cid and (Wz & Wm) == Wm and Wz != Wm
                    ok &= bin(Wz & ~Wm).count('1') in (2, 3)
                    ok &= Oz == (O | (1 << centre))
                    if rest[1] > 0:
                        wz = windows(z, n, Wz) or []
                        ok &= (rest[0] % n, rest[1], rest[2]) in wz
                    if not ok:
                        viol += 1
                        ex.append((n, eca.word(y, n), s, w))
            if not any_move:
                cyc_without_move += 1
    record('L10', 'Lemma 10: in every state of every cycle with W neither empty nor full, every window with content A_w, B_w, 0000, 1111: the named flip gives a periodic state of another cycle, W grows by the named occurrence (2 or 3 cells), the rest of the window is the named live window',
           f'{nmin}..{nmax}', cases, viol + cyc_without_move, ex, extra=dict(cycles=ncyc, cycles_without_applicable_window=cyc_without_move))


# ---------------------------------------------------------------- Lemma W
def test_LW(nmin=5, nmax=12, wmax=7, T=6):
    viol = cases = 0
    ex = []
    for n in range(nmin, nmax + 1):
        F = eca.step_all(RULE, n)
        for x in block_words(n):
            x = int(x)
            for p in range(n):
                if not (((x >> ((p - 1) % n)) & 1) == 0 and ((x >> p) & 1) == 1):
                    continue
                for w in range(1, min(wmax, n - 3) + 1):
                    if not (((x >> ((p + w + 1) % n)) & 1) == 1 and ((x >> ((p + w + 2) % n)) & 1) == 0):
                        continue
                    Imask = sum(1 << ((p + k) % n) for k in range(1, w + 1))
                    for u in range(1 << w):
                        cont = tuple((u >> k) & 1 for k in range(w))
                        y = (x & ~Imask) | sum(cont[k] << ((p + 1 + k) % n) for k in range(w))
                        cases += 1
                        ok = (W1(y, n) | Imask) == (1 << n) - 1
                        z, cn = y, cont
                        for t in range(T):
                            z = int(F[z])
                            cn = phi(cn)
                            ok &= (z & ~Imask) == (y & ~Imask)
                            ok &= tuple((z >> ((p + 1 + k) % n)) & 1 for k in range(w)) == cn
                        if not ok:
                            viol += 1
                            ex.append((n, eca.word(x, n), p, w, cont))
    record('LW', 'Lemma W: windows cut out of a block word: cells outside I frozen, F^t = id outside I and phi^t inside (t<=6), every content',
           f'{nmin}..{nmax}, w<={wmax}', cases, viol, ex)


# ---------------------------------------------------------------- Lemmas 11, 12, 13
def cells_eq(x, n, p, pat):
    return all(((x >> ((p + k) % n)) & 1) == int(ch) for k, ch in enumerate(pat))


def replace(x, n, p, pat):
    for k, ch in enumerate(pat):
        cell = (p + k) % n
        x = (x & ~(1 << cell)) | (int(ch) << cell)
    return x


def test_L11_13(nmax=NMAX):
    v11 = v12 = v13 = c11 = c12 = c13 = 0
    ex = []
    for n in range(5, nmax + 1):
        F = eca.step_all(RULE, n)
        for x in block_words(n):
            x = int(x)
            for p in range(n):
                if cells_eq(x, n, p, '01011'):
                    c11 += 1
                    y1, y2 = x ^ (1 << ((p + 2) % n)), x ^ (1 << ((p + 3) % n))
                    xp = replace(x, n, p, '01101')
                    ok = F[y1] == y2 and F[y2] == y1 and y1 != y2 and xp == (y1 ^ (1 << ((p + 3) % n)))
                    ok &= is_block_word(xp, n) and F[xp] == xp and F[x] == x
                    if not ok:
                        v11 += 1
                        ex.append(('L11', n, eca.word(x, n), p))
                if n >= 6 and cells_eq(x, n, p, '010101') and ((x >> ((p + 6) % n)) & 1) == 0:
                    c12 += 1
                    x2 = replace(x, n, p, '011011')
                    ok = F[x ^ (1 << ((p + 3) % n))] == x2 and is_block_word(x2, n) and x2 != x
                    if not ok:
                        v12 += 1
                        ex.append(('L12', n, eca.word(x, n), p))
                if n >= 8 and cells_eq(x, n, p, '01011011'):
                    c13 += 1
                    y = x ^ (1 << ((p + 2) % n))
                    x2 = replace(x, n, p, '01010101')
                    z = int(F[y]) ^ (1 << ((p + 6) % n))
                    for _ in range(5):
                        z = int(F[z])
                    ok = F[F[y]] == y and F[y] != y and z == x2 and is_block_word(x2, n)
                    if not ok:
                        v13 += 1
                        ex.append(('L13', n, eca.word(x, n), p))
    record('L11', 'Lemma 11 (swap): x+e_(p+2), x+e_(p+3) form a 2-cycle, x+e_(p+2)+e_(p+3) = block word with l s; every block word, every s l', f'5..{nmax}', c11, v11, [e for e in ex if e[0] == 'L11'])
    record('L12', 'Lemma 12 (merge): F(x+e_(p+3)) = x with s s s -> l l; every block word, every s s s followed by a block start', f'6..{nmax}', c12, v12, [e for e in ex if e[0] == 'L12'])
    record('L13', 'Lemma 13 (split): x+e_(p+2) has period 2, F^5(F(y)+e_(p+6)) = x with s l l -> s s s s; every block word, every s l l', f'8..{nmax}', c13, v13, [e for e in ex if e[0] == 'L13'])


# ---------------------------------------------------------------- Lemma 16 (basin of 0)
def is_word_001_0011(x, n):
    """cyclic word over the blocks 001 and 0011 (at least one block)"""
    s = eca.word(x, n)
    if '1' not in s or '0' not in s:
        return False
    # rotate to start at the beginning of a run of zeros
    k = next(i for i in range(n) if s[i] == '0' and s[i - 1] == '1')
    t = s[k:] + s[:k]
    i = 0
    while i < n:
        if t.startswith('0011', i):
            i += 4
        elif t.startswith('001', i):
            i += 3
        else:
            return False
    return True


def test_L16(nmin=3, nmax=NMAX):
    vi = vii = viii = vb = cases = 0
    ex = []
    extra = {}
    for n in range(nmin, nmax + 1):
        R = eca.Ring(RULE, n)
        F = R.F
        full = (1 << n) - 1
        words = np.array([x for x in range(1 << n) if is_word_001_0011(x, n)], dtype=np.int64)
        isw = np.zeros(1 << n, dtype=bool)
        isw[words] = True
        cases += 1 << n
        zero_pre = set(np.nonzero(F == 0)[0].tolist())
        if zero_pre != {0, full}:
            vi += 1
            ex.append(('i', n))
        one_pre = np.nonzero(F == full)[0]
        if set(one_pre.tolist()) != set(words.tolist()):
            vii += 1
            ex.append(('ii', n))
        pre_words = np.nonzero(isw[F])[0]
        if len(pre_words) and n % 8 != 0:
            viii += 1
            ex.append(('iii', n))
        basin = set(np.nonzero(R.label == R.label[0])[0].tolist())
        desc = {0, full} | set(words.tolist())
        if n % 8 != 0 and basin != desc:
            vb += 1
            ex.append(('basin', n))
        if n % 8 == 0:
            z = eca.from_word('00001111' * (n // 8))
            extra[n] = dict(basin_size=len(basin), described=len(desc), z00001111_in_basin=z in basin,
                            z_in_described=z in desc)
    record('L16', 'Lemma 16 (i) F(x)=0 iff x in {0,1^n}; (ii) F(x)=1^n iff x word over 001,0011; (iii) F(z) such a word => 8|n; basin of 0 described when 8 does not divide n; every state',
           f'{nmin}..{nmax}', cases, vi + vii + viii + vb, ex, extra=extra)


# ---------------------------------------------------------------- Lemma 15 (code 000), Prop 3(i)
def z15(n):
    if n == 7:
        return '0100001'
    m = n - 7
    for b in range(m // 3 + 1):
        if (m - 3 * b) % 2 == 0:
            a = (m - 3 * b) // 2
            return '0100001' + '011' * b + '01' * a
    return None


def test_L15(nmax=NMAX, big=200):
    viol = cases = 0
    ex = []
    for n in [7] + list(range(10, big + 1)):
        if n % 3 == 0:
            continue
        s = z15(n)
        cells = [int(ch) for ch in s]
        cases += 1
        # frozen set by hand: W = complement of {2,3,4,5}; z periodic (F^3 z = z); 000 present
        y = cells
        for _ in range(3):
            y = eca.step_list(RULE, y)
        x = eca.from_cells(cells)
        ok = y == cells and '000' in (s + s[:2])
        if n <= 60:
            ok &= W1(x, n) == ((1 << n) - 1) & ~0b111100
        if n <= nmax:
            R = eca.Ring(RULE, n)
            ok &= bool(R.periodic[x])
        if not ok:
            viol += 1
            ex.append(n)
    # n = 5, 7, 8: chains into {0}
    for n, s, j in ((5, '01111', 0), (7, '0111111', 0), (8, '01111010', 5)):
        R = eca.Ring(RULE, n)
        x = eca.from_word(s)
        cases += 1
        ok = bool(R.periodic[x]) and W1(x, n) != 0 and R.label[x ^ (1 << j)] == R.label[0]
        if not ok:
            viol += 1
            ex.append((n, s))
    record('L15', 'Lemma 15 / Prop. 3(i): z = 0100001+block word is periodic with W = complement of {2..5} and contains 000 (n=7, 10..200, 3 not dividing n; periodicity by enumeration for n<=NMAX); chains into {0} for n=5,7,8',
           f'7..{big}', cases, viol, ex)


# ---------------------------------------------------------------- Lemma 14, Theorem 2, Prop. 3, Section 0 numbers
def test_T2(nlist):
    rows = []
    viol = 0
    ex = []
    for n in nlist:
        R = eca.Ring(RULE, n)
        full = (1 << n) - 1
        ncomp, comp, closed = R.closed_classes()
        Wp = W_all(R.pstates, n)
        cyc_W = np.zeros(R.m, dtype=bool)          # cycle has non-empty frozen set (W constant on a cycle?)
        cyc_W[R.pcyc[Wp != 0]] = True
        # W constant on cycles
        wconst = True
        for cid in range(R.m):
            st = R.cycle_states(cid)
            ws = {W1(y, n) for y in st}
            if len(ws) != 1:
                wconst = False
        bw = block_words(n)
        bw_c = sorted(set(R.label[bw].tolist()))
        bw_one_scc = len(set(comp[bw_c].tolist())) == 1
        K = set(closed[0].tolist()) if len(closed) == 1 else None
        z = int(R.label[0])
        DW = dw_set(n)
        dw_cycles = sorted(set(R.label[np.array(sorted(DW), dtype=np.int64)].tolist())) if DW else []
        A, e = R.g1()
        into0 = int(np.sum(e[:, 1] == z)) if len(e) else 0
        row = dict(n=n, cycles=R.m, periodic_states=int(len(R.pstates)), g1_edges=int(len(e)), sccs=int(ncomp),
                   closed_sizes=[len(c) for c in closed], block_words=int(len(bw)), block_words_one_scc=bw_one_scc,
                   W_constant_on_cycles=wconst, edges_into_zero=into0)
        if K is not None:
            reachK = R.reach_from(bw_c)
            row['K_eq_reach_from_block_words'] = reachK == K
            row['cycles_with_101_in_K'] = f'{sum(1 for c in K if cyc_W[c])} of {int(cyc_W.sum())}'
            row['zero_in_K'] = z in K
            row['dw_cycles_in_K'] = f'{sum(1 for c in dw_cycles if c in K)} of {len(dw_cycles)}'
            outside = [c for c in range(R.m) if c not in K]
            row['outside_K_all_no101_and_zero_or_dw'] = all((not cyc_W[c]) and (c == z or c in dw_cycles) for c in outside)
            row['codes_on_K'] = sorted(R.codes_of_cycles(K))
            per_in = {}
            per_out = {}
            for c in range(R.m):
                if cyc_W[c]:
                    continue
                L = len(R.cycle_states(c))
                d = per_in if c in K else per_out
                d[L] = d.get(L, 0) + 1
            row['periods_no101_in_K'] = per_in
            row['periods_no101_outside_K'] = per_out
        rows.append(row)
        # checks of the theorems (n >= 5, 3 does not divide n)
        if n >= 5 and n % 3 != 0:
            ok = K is not None and bw_one_scc and wconst and row['K_eq_reach_from_block_words']
            ok &= row['outside_K_all_no101_and_zero_or_dw'] and row['codes_on_K'] == list(range(8))
            ok &= all(cyc_W[c] <= (c in K) for c in range(R.m))
            if n in (5, 7, 8):
                ok &= row['zero_in_K']
            if n >= 10 and n % 8 != 0:
                ok &= into0 == 0 and not row['zero_in_K']
            if n % 2 == 1 and n >= 11:
                ok &= K == set(range(R.m)) - {z}
            if n in (5, 7):
                ok &= K == set(range(R.m))
            if not ok:
                viol += 1
                ex.append(n)
        eca.log('  T2 row', n, row['closed_sizes'], row.get('dw_cycles_in_K'), row.get('zero_in_K'), into0)
    record('T2', 'Lemma 14, Theorem 2 (a)-(d), Proposition 3 (ii), (iii): unique closed class K, contains every cycle with 101, = reachable from block words, outside K only {0} and doubled-word cycles, 8 codes on K; no edge into {0} for n>=10, 8 not dividing n',
           ','.join(map(str, nlist)), len(nlist), viol, ex, extra=rows)
    return rows


if __name__ == '__main__':
    test_L8()
    test_L7()
    test_T1()
    test_L9 = None
    test_L10()
    test_LW()
    test_L11_13()
    test_L15()
    test_L16()
    nl = [n for n in range(4, NMAX + 1) if n % 3 != 0] + [16]
    nl = sorted(set(nl))
    test_T2(nl)
    out = dict(rule=RULE, nmax=NMAX, results=results, cpu_seconds=round(time.process_time() - t0, 2),
               all_passed=all(r['violations'] == 0 for r in results))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'test_94.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    eca.log('ALL PASSED:', out['all_passed'], 'CPU s', out['cpu_seconds'])
