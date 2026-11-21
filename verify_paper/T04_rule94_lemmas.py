"""T04 -- Section 3.3 and Appendix A (rule 94): the lemmas, every state, every cell, every cycle on small rings.

Group A: statements used by Theorem 3.43(i) (no separate verification is recorded for Lemma 3.32 and part (i)).
 L3.29 freeze    n = 3..NS: (i) Occ(x) in Occ(Fx), Fx = x on Fz(x), Fz(x) in Fz(Fx), all states; (ii) Fz constant on
                 every cycle.
 L3.30 block     n = 3..NS: fully frozen <=> block word (block words generated independently as cyclic words of blocks
                 01 and 011, and by the description 'zeros isolated, runs of ones of length 1 or 2, at least one 0');
                 every block word is a fixed point.
 L3.31 growth    n = 5..NS: every state x that is not fully frozen has a cell j outside Fz(x) with Fz(F^2(x+e_j))
                 properly containing Fz(x) (this gives all t >= 2 by L3.29); x = 0: every j, with an occurrence centred
                 at j in F^2(e_j); every cycle that is not fully frozen has a G1 edge to a cycle with a properly larger
                 frozen set. The six cases of the proof are executed for every x != 0 and EVERY cell i outside Fz(x)
                 (n <= NP). The same checks are reported for n = 3 and 4, which the lemma excludes.
 L3.32 crystal   3 | n, n = 6..300: every crystal phase, every cell j: F^3(x+e_j) = x; second statement (the words
                 100, 111, 000 on p-1, p, p+1); n = 3 reported.
 L3.34 cut       n = 4..NC: every block word, every admissible window I, EVERY filling y of I.
 L3.38 swap      n = 5..NG: (a) every block word, every pair of blocks s l: the 2-cycle D, x', the four G1 edges;
                 (b) every block word, every block start q: x and the sorted word l^b s^a (read from q) are in the
                 same strongly connected component of G1.
 L3.39 merge     n = 6..NG: every block word, every sss: x'' is a block word, F(x+e_{p+3}) = x'', G1 edge.
Group B: the other statements of the section (verified before by a separate session; here for the edges of the ranges).
 L3.33 windows (n = 3..NW), L3.35 live orbits (window width 1..LW, all words), L3.36 empty frozen set (n = 3..NS),
 L3.37 freezing flips (n = 3..NG), L3.40 split (n = 8..NG), L3.41 component (n = 5..NG, 3 not dividing n; n = 4
 reported), L3.42 code 000 (same n), Proposition A.1 (n = 3..NA).
G1 is taken from the matrix V of the definitions (vp_core), not from Lemma 2.3.
Output: out/T04.txt.  Usage: python3 T04_rule94_lemmas.py [NS=20] [NG=18] [NP=14] [NC=13] [NW=13] [LW=18] [NA=18]
"""
import sys, time, os
from math import gcd
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def step94(x, n):
    """rule 94 on a Python integer."""
    full = (1 << n) - 1
    a = ((x << 1) | (x >> (n - 1))) & full
    c = ((x >> 1) | (x << (n - 1))) & full
    return ((x & ~(a & c)) | (~x & (a ^ c))) & full

def occ_fz(x, n):
    full = (1 << n) - 1
    a = ((x << 1) | (x >> (n - 1))) & full
    c = ((x >> 1) | (x << (n - 1))) & full
    occ = a & ~x & c & full
    fz = (occ | ((occ << 1) | (occ >> (n - 1))) | ((occ >> 1) | (occ << (n - 1)))) & full
    return occ, fz

def block_words(n):
    """All block words: cyclic concatenations of 01 and 011, in every rotation. Returns {state: (a, b)}."""
    res = {}
    def rec(prefix, left, a, b):
        if left == 0:
            w = vc.from_word(prefix)
            for s in range(n):
                res[vc.rot(w, n, s)] = (a, b)
            return
        if left >= 2:
            rec(prefix + "01", left - 2, a + 1, b)
        if left >= 3:
            rec(prefix + "011", left - 3, a, b + 1)
    rec("", n, 0, 0)
    return res

def windows_of(fz, n):
    """Maximal cyclic runs of cells outside the frozen set: list of (first cell, length). fz neither 0 nor full."""
    out = []
    for i in range(n):
        if not (fz >> i) & 1 and (fz >> ((i - 1) % n)) & 1:
            l = 0
            while not (fz >> ((i + l) % n)) & 1:
                l += 1
            out.append((i, l))
    return out

def phi(u, l):
    """window map on a word u_1..u_l given as a tuple, neighbours held at 1."""
    c = (1,) + tuple(u) + (1,)
    return tuple((94 >> (4 * c[i - 1] + 2 * c[i] + c[i + 1])) & 1 for i in range(1, l + 1))

def alpha(i): return 1 if i % 6 in (0, 1, 2, 3) else 0
def beta(i): return 1 if i % 6 in (0, 3, 4, 5) else 0

def live_claim(l):
    if l % 3 == 2:
        return {tuple(alpha(i) for i in range(1, l + 1)), tuple(beta(i) for i in range(1, l + 1))}
    if l == 4:
        return {(0, 0, 0, 0), (1, 0, 0, 1), (1, 1, 1, 1)}
    return set()

def main():
    arg = lambda k, d: int(sys.argv[k]) if len(sys.argv) > k else d
    NS, NG, NP, NC, NW, LW, NA = arg(1, 20), arg(2, 18), arg(3, 14), arg(4, 13), arg(5, 13), arg(6, 18), arg(7, 18)
    t0 = time.process_time(); w0 = time.time()
    L = []
    fails = 0
    def rec(name, ok, msg, expected_fail=False):
        nonlocal fails
        if not ok and not expected_fail:
            fails += 1
        L.append("%-6s %s  %s" % (name, "ok  " if ok else ("no   (outside the stated range, reported only)" if expected_fail else "FAIL"), msg))
        print(L[-1], flush=True)

    # ---------------- live window orbits (L3.35), all words of width 1..LW
    okl = True
    for l in range(1, LW + 1):
        Nw = 1 << l
        u = np.arange(Nw, dtype=np.uint32)
        c = (u << np.uint32(1)) | np.uint32(1) | np.uint32(1 << (l + 1))          # padded word, bit i = c_i
        img = np.zeros(Nw, dtype=np.uint32)
        unf = np.ones(Nw, dtype=bool)
        for i in range(1, l + 1):
            a = (c >> np.uint32(i - 1)) & 1; b = (c >> np.uint32(i)) & 1; d = (c >> np.uint32(i + 1)) & 1
            v = 4 * a + 2 * b + d
            img |= ((np.uint32(94) >> v) & 1) << np.uint32(i - 1)
            unf &= ~((a == 1) & (b == 0) & (d == 1))
        G = img.copy(); k = 1
        while k < Nw:
            G = G[G]; k *= 2
        per = np.zeros(Nw, dtype=bool); per[G] = True
        live = per & unf
        while True:
            nl = live & live[img]
            if (nl == live).all():
                break
            live = nl
        got = {tuple((int(w) >> i) & 1 for i in range(l)) for w in np.nonzero(live)[0]}
        okl = okl and got == live_claim(l)
    rec("L3.35", okl, "window widths 1..%d, all words: the live orbits are exactly those of the lemma" % LW)

    BW = {}
    for n in range(3, NS + 1):
        S = vc.System(94, n, level=0)
        N = 1 << n; full = np.uint32(N - 1)
        x = np.arange(N, dtype=np.uint32); F = S.F
        rl = lambda z: ((z << np.uint32(1)) | (z >> np.uint32(n - 1))) & full
        rr = lambda z: ((z >> np.uint32(1)) | (z << np.uint32(n - 1))) & full
        xm, xp = rl(x), rr(x)
        occ = xm & ~x & xp & full
        fz = occ | rl(occ) | rr(occ)
        # L3.29
        ok = ((occ & ~occ[F]) == 0).all() and (((F ^ x) & fz) == 0).all() and ((fz & ~fz[F]) == 0).all()
        px = S.cyc_states
        ok = ok and (fz[F[px]] == fz[px]).all()
        rec("L3.29", bool(ok), "n=%d all %d states, all %d cycles" % (n, N, S.m))
        # L3.30
        bw = block_words(n); BW[n] = bw
        isbw = np.zeros(N, dtype=bool); isbw[list(bw.keys())] = True
        desc = (x != full) & ((~x & ~xm & full) == 0) & ((x & xm & xp) == 0)
        ok = (isbw == desc).all() and (isbw == (fz == full)).all() and (F[isbw] == x[isbw]).all()
        rec("L3.30", bool(ok), "n=%d %d block words" % (n, int(isbw.sum())))
        # L3.31
        notfull = fz != full
        found = np.zeros(N, dtype=bool)
        allj_zero = True
        for j in range(n):
            y = x ^ np.uint32(1 << j)
            g = fz[F[F[y]]]
            cond = (((fz >> np.uint32(j)) & 1) == 0) & ((g & fz) == fz) & (g != fz)
            found |= cond
            allj_zero = allj_zero and bool(cond[0]) and bool((occ[F[F[1 << j]]] >> j) & 1)
        ok = found[notfull].all() and allj_zero
        # cycles
        fzc = np.zeros(S.m, dtype=np.uint32); fzc[S.lab[px]] = fz[px]
        cyc_found = np.zeros(S.m, dtype=bool)
        for j in range(n):
            y = px ^ np.uint32(1 << j)
            a, b = S.lab[px], S.lab[y]
            good = ((fzc[b] & fzc[a]) == fzc[a]) & (fzc[b] != fzc[a])
            cyc_found[a[good]] = True
        okc = cyc_found[fzc != full].all()
        rec("L3.31", bool(ok and okc), "n=%d existence of j for all %d states that are not fully frozen (x = 0: every j); edge for all %d cycles that are not fully frozen" % (n, int(notfull.sum()), int((fzc != full).sum())), expected_fail=(n < 5))
        if n <= NP:
            okp = True; ncase = 0
            for xs in range(1, N):
                f = int(fz[xs])
                if f == N - 1:
                    continue
                bit = lambda i: (xs >> (i % n)) & 1
                for i in range(n):
                    if (f >> i) & 1:
                        continue
                    if bit(i) == 1:
                        if bit(i - 1) == 1 and bit(i + 1) == 1: j = i
                        elif bit(i - 1) == 0: j = i - 2
                        else: j = i + 2
                    else:
                        l_, r_ = bit(i - 1), bit(i + 1)
                        if l_ == 0 and r_ == 1: j = i - 1
                        elif l_ == 1 and r_ == 0: j = i + 1
                        elif l_ == 0 and r_ == 0:
                            k = 2
                            while bit(i + k) == 0: k += 1
                            j = i + k - 2
                        else:
                            okp = False; continue          # i would be a centre
                    j %= n
                    ys = xs ^ (1 << j)
                    o2, f2 = occ_fz(ys, n)
                    okp = okp and not (f >> j) & 1 and bool((f2 >> j) & 1) and (f2 & f) == f
                    ncase += 1
            rec("L3.31p", okp, "n=%d the cell j given by the six cases of the proof works for all %d pairs (x != 0, cell i outside Fz(x))" % (n, ncase))
        # L3.36
        emp = (S.per == 1) & (fz == 0)
        claim = np.zeros(N, dtype=bool); claim[0] = True
        if n % 2 == 0:
            h = n // 2
            v = np.arange(1 << h, dtype=np.uint32)
            tv = ((v >> np.uint32(1)) | (v << np.uint32(h - 1))) & np.uint32((1 << h) - 1)      # (tau v)_k = v_{k+1}
            T = v ^ tv
            G = T.copy(); k = 1
            while k < (1 << h):
                G = G[G]; k *= 2
            Ph = np.zeros(1 << h, dtype=bool); Ph[G] = True
            e = 0
            while (n >> (e + 1)) % 2 == 0: e += 1
            okcount = int(Ph.sum()) == 2 ** (n // 2 - 2 ** e)
            for p in (0, 1):
                for vv in np.nonzero(Ph)[0]:
                    if vv == 0: continue
                    s = 0
                    for k in range(h):
                        if (int(vv) >> k) & 1:
                            s |= (1 << ((2 * k + p) % n)) | (1 << ((2 * k + p + 1) % n))
                    claim[s] = True
        else:
            okcount = True
        rec("L3.36", bool((emp == claim).all() and okcount), "n=%d periodic states with empty frozen set: %d (0 and the doubled words of P_h); |P_h| formula %s" % (n, int(emp.sum()), okcount))

    # L3.32 crystal, big integers
    okc = True; rt = set()
    for n in range(6, 301, 3):
        base = vc.from_word("011" * (n // 3))
        for s in range(3):
            xph = vc.rot(base, n, s)
            okc = okc and step94(xph, n) == xph
            for j in range(n):
                y = xph ^ (1 << j)
                y1 = step94(y, n); y2 = step94(y1, n); y3 = step94(y2, n)
                okc = okc and y3 == xph
                kind = "0" if not (xph >> j) & 1 else ("first1" if not (xph >> ((j - 1) % n)) & 1 else "second1")
                rt.add((kind, 1 if y1 == xph else 2 if y2 == xph else 3))
            for p in range(n):
                if (xph >> p) & 1:
                    continue                    # a block starts at every 0
                y = xph ^ (1 << ((p + 1) % n))
                seq = [y, step94(y, n), step94(step94(y, n), n)]
                for st, wd in zip(seq, ("100", "111", "000")):
                    cells = [(p - 1) % n, p, (p + 1) % n]
                    okc = okc and "".join(str((st >> c) & 1) for c in cells) == wd
                    mask = sum(1 << c for c in cells)
                    okc = okc and (st & ~mask) == (xph & ~mask)
    rec("L3.32", okc, "3 | n, n = 6..300: all three phases, every cell: F^3(x+e_j) = x and the second statement; first return times by kind of cell: %s" % sorted(rt))
    xph = vc.from_word("011")
    esc = [j for j in range(3) if step94(step94(step94(xph ^ (1 << j), 3), 3), 3) != xph]
    rec("L3.32", not esc, "n=3: cells j with F^3(x+e_j) != x for x = 011: %s (Remark 3.44 says a single flip can leave the crystal phase)" % esc, expected_fail=True)

    # L3.34 cut
    for n in range(4, NC + 1):
        ok = True; cnt = 0
        for xs in BW[n]:
            b = lambda i: (xs >> (i % n)) & 1
            for p in range(n):
                if not (b(p - 1) == 0 and b(p) == 1):
                    continue
                for l in range(1, n - 2):
                    if not (b(p + l + 1) == 1 and b(p + l + 2) == 0):
                        continue
                    cells = [(p + 1 + i) % n for i in range(l)]
                    Imask = sum(1 << c for c in cells)
                    for fill in range(1 << l):
                        y = xs & ~Imask
                        u = tuple((fill >> i) & 1 for i in range(l))
                        for i, c in enumerate(cells):
                            if u[i]: y |= 1 << c
                        o, f = occ_fz(y, n)
                        Fy = step94(y, n)
                        ok = ok and (f | Imask) == (1 << n) - 1 and (Fy & ~Imask) == (y & ~Imask) and tuple((Fy >> c) & 1 for c in cells) == phi(u, l)
                        cnt += 1
        rec("L3.34", ok, "n=%d all block words, all admissible windows, all fillings: %d states y (one step; all t follow by induction since Fy again agrees with x outside I)" % (n, cnt))

    # L3.33 windows and Proposition A.1
    for n in range(3, max(NW, NA) + 1):
        S = vc.System(94, n, level=0)
        N = 1 << n
        okw = True; okA = True; nper = 0
        e = 0
        while n % 2 == 0 and (n >> (e + 1)) % 2 == 0: e += 1
        case2 = 0
        for y in range(N):
            o, f = occ_fz(y, n)
            isper = bool(S.per[y])
            if f == 0 or f == N - 1:
                if n <= NA:
                    if f == 0:
                        # case 1 or 2 is tested in L3.36; count case 2
                        if isper and y != 0: case2 += 1
                    else:
                        okA = okA and isper
                continue
            wins = windows_of(f, n)
            allper = True; alllive_claim = True; periods = []
            for (i0, l) in wins:
                u = tuple((y >> ((i0 + i) % n)) & 1 for i in range(l))
                if n <= NW:
                    okw = okw and (y >> ((i0 - 1) % n)) & 1 == 1 and (y >> ((i0 + l) % n)) & 1 == 1 and (f >> ((i0 - 1) % n)) & 1 and (f >> ((i0 + l) % n)) & 1 and l <= n - 3
                    Fy = int(S.F[y])
                    okw = okw and tuple((Fy >> ((i0 + i) % n)) & 1 for i in range(l)) == phi(u, l)
                # phi-periodic?
                seen = [u]; w = phi(u, l)
                while w not in seen:
                    seen.append(w); w = phi(w, l)
                isp = (w == u)
                allper = allper and isp
                if isp: periods.append(len(seen))
                alllive_claim = alllive_claim and (u in live_claim(l))
            if n <= NW:
                okw = okw and (isper == allper)
                if isper:
                    okw = okw and alllive_claim          # periodic => every window content is one of the live words
                    # period = lcm of window periods
                    t = 1; z = int(S.F[y])
                    while z != y: z = int(S.F[z]); t += 1
                    lc = 1
                    for q in periods: lc = lc * q // gcd(lc, q)
                    okw = okw and t == lc
            if n <= NA:
                okA = okA and (isper == alllive_claim)
                if isper:
                    t = 1; z = int(S.F[y])
                    while z != y: z = int(S.F[z]); t += 1
                    okA = okA and 6 % t == 0
        if n <= NW:
            rec("L3.33", okw, "n=%d all states with frozen set neither empty nor full: (a), (b) one step, (c) with periods" % n)
        if n <= NA:
            want2 = 2 * (2 ** (n // 2 - 2 ** e) - 1) if n % 2 == 0 else 0
            rec("PA.1", okA and case2 == want2, "n=%d periodic <=> cases 1-3 (all states); period divides 6 in case 3; case 2 has %d states (formula %d)" % (n, case2, want2))

    # ---------------- G1-dependent statements
    for n in range(4, NG + 1):
        S = vc.System(94, n, level=1, workers=2)
        G1 = S.V == 1
        classes, comp = S.closed_classes()
        bw = BW[n] if n in BW else block_words(n)
        lab = S.lab
        N = 1 << n
        px = S.cyc_states
        fzs = np.array([occ_fz(int(z), n)[1] for z in px], dtype=np.int64)
        fzc = np.zeros(S.m, dtype=np.int64); fzc[lab[px]] = fzs
        # L3.37
        need = (fzc != 0) & (fzc != N - 1)
        got = np.zeros(S.m, dtype=bool)
        for j in range(n):
            y = px ^ np.uint32(1 << j)
            fy = np.array([occ_fz(int(z), n)[1] for z in y], dtype=np.int64)
            good = (S.per[y] == 1) & ((fy & fzs) == fzs) & (fy != fzs)
            got[lab[px[good]]] = True
            a_, b_ = lab[px[good]], lab[y[good]]
            if len(a_) and not (G1[a_, b_].all() and G1[b_, a_].all()):
                got[:] = False
        rec("L3.37", bool(got[need].all()), "n=%d all %d cycles with frozen set neither empty nor full" % (n, int(need.sum())))
        if n >= 5:
            oka = okb = True; na = nb = 0
            for xs, (a, b) in bw.items():
                bit = lambda i: (xs >> (i % n)) & 1
                for p in range(n):
                    if [bit(p + i) for i in range(5)] == [0, 1, 0, 1, 1] and bit(p + 5) == 0:
                        y1 = xs ^ (1 << ((p + 2) % n)); y2 = xs ^ (1 << ((p + 3) % n)); x2 = y1 ^ (1 << ((p + 3) % n))
                        D = lab[y1]
                        oka = oka and S.per[y1] and S.per[y2] and int(S.F[y1]) == y2 and int(S.F[y2]) == y1 and y1 != y2
                        oka = oka and x2 in bw and [(x2 >> ((p + i) % n)) & 1 for i in range(5)] == [0, 1, 1, 0, 1]
                        oka = oka and G1[lab[xs], D] and G1[D, lab[x2]] and G1[lab[x2], D] and G1[D, lab[xs]]
                        na += 1
                    if bit(p) == 0:        # block start q = p
                        wd = ("011" * b + "01" * a)
                        xt = vc.rot(vc.from_word(wd), n, p)
                        okb = okb and xt in bw and comp[lab[xs]] == comp[lab[xt]]
                        nb += 1
            rec("L3.38", bool(oka and okb), "n=%d (a) %d pairs s l; (b) %d pairs (block word, block start)" % (n, na, nb))
        if n >= 6:
            okm = True; nm = 0
            for xs in bw:
                bit = lambda i: (xs >> (i % n)) & 1
                for p in range(n):
                    if [bit(p + i) for i in range(7)] == [0, 1, 0, 1, 0, 1, 0]:
                        x2 = xs
                        for i, ch in enumerate("011011"):
                            c = (p + i) % n
                            x2 = (x2 & ~(1 << c)) | (int(ch) << c)
                        okm = okm and x2 in bw and step94(xs ^ (1 << ((p + 3) % n)), n) == x2 and G1[lab[xs], lab[x2]]
                        nm += 1
            rec("L3.39", bool(okm), "n=%d %d triples sss" % (n, nm))
        if n >= 8:
            oks = True; ns_ = 0
            for xs in bw:
                bit = lambda i: (xs >> (i % n)) & 1
                for p in range(n):
                    if [bit(p + i) for i in range(9)] == [0, 1, 0, 1, 1, 0, 1, 1, 0]:
                        x2 = xs
                        for i, ch in enumerate("01010101"):
                            c = (p + i) % n
                            x2 = (x2 & ~(1 << c)) | (int(ch) << c)
                        y = xs ^ (1 << ((p + 2) % n))
                        Fy = step94(y, n)
                        z = Fy ^ (1 << ((p + 6) % n))
                        for _ in range(5): z = step94(z, n)
                        oks = oks and S.per[y] and step94(Fy, n) == y and Fy != y and z == x2 and x2 in bw
                        oks = oks and G1[lab[xs], lab[y]] and G1[lab[y], lab[x2]]
                        ns_ += 1
            rec("L3.40", bool(oks), "n=%d %d triples sll" % (n, ns_))
        if n % 3 != 0:
            comps = {int(comp[lab[xs]]) for xs in bw}
            rec("L3.41", len(comps) == 1, "n=%d the %d block words lie in %d strongly connected component(s) of G1" % (n, len(bw), len(comps)), expected_fail=(n < 5))
            # L3.42
            cc = S.cycle_codes()
            ok0 = True
            for K in classes:
                inK = np.zeros(S.m, dtype=bool); inK[K] = True
                if inK[fzc != 0].all():
                    ok0 = ok0 and bool(np.bitwise_or.reduce(cc[K]) & 1)
            rec("L3.42", ok0, "n=%d closed classes containing every cycle with non-empty frozen set contain 000" % n, expected_fail=(n < 5))
    L.append("T04 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T04.txt"), "w").write("\n".join(L) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
