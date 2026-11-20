"""T07 -- Section 5 and Appendix B (rule 26): every numbered statement on small rings, with the smallest ring sizes
of each statement. (Verified before by a separate session; this is the check of the edges of the ranges asked for in
Part 2, with own code written from Definition 5.1.)

 All states, even n = 4..NS:
   L5.2 moving frame (all n = 3..NS); L5.3 chi; L5.4 domain states (a), (b), (c); L5.5 singleton groups; L5.6 one
   parity class; LB.1 ancestors of 111; LB.2 periodic states; LB.4 codes on the cycles.
   LB.3 carrier words: every cyclic word over 11100 and 100, every rotation, n = 3..NCW (any parity).
 From the definitions (V, gamma for every root, k_v), even n = 4..NG:
   n = 2^k:   T5.7 (a)-(d); P5.8 (a), (b), (c) for n >= 8; LB.5; the computed values quoted in the text for n = 4, 16.
   other even n >= 6: P5.9, with the list of n for which k* = 0.
   all even n: LB.6, LB.7.
Output: out/T07.txt, out/T07_rule26.csv.   Usage: python3 T07_rule26.py [NS=18] [NG=20] [NCW=40]
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def step(rule, x, n):
    full = (1 << n) - 1
    a = ((x << 1) | (x >> (n - 1))) & full
    c = ((x >> 1) | (x << (n - 1))) & full
    y = 0
    for v in range(8):
        if (rule >> v) & 1:
            y |= (a if v & 4 else ~a) & (x if v & 2 else ~x) & (c if v & 1 else ~c)
    return y & full

def analyse(x, n):
    """Definition 5.1 for one state: (chi, sources, sizes of the groups, is a domain state)."""
    ones = [i for i in range(n) if (x >> i) & 1]
    k = len(ones)
    if k < 2:
        return 0, [], [], False
    diff = [(ones[t] - ones[t - 1]) % 2 == 1 for t in range(k)]     # diff[t]: ones[t] and its predecessor differ in parity
    chi = sum(diff)
    if chi == 0:
        return 0, [], [], False
    src_idx = [t for t in range(k) if diff[t]]
    sources = [ones[t] for t in src_idx]
    sizes = [((src_idx[(q + 1) % len(src_idx)] - src_idx[q] - 1) % k) + 1 for q in range(len(src_idx))]
    dom = all(((sources[(q + 1) % len(sources)] - sources[q] - 1) % n) + 1 >= 3 for q in range(len(sources)))
    return chi, sources, sizes, dom

def main():
    arg = lambda k, d: int(sys.argv[k]) if len(sys.argv) > k else d
    NS, NG, NCW = arg(1, 18), arg(2, 20), arg(3, 40)
    t0 = time.process_time(); w0 = time.time()
    L = []; fails = 0
    rows = ["n,m,closed_classes,selected,gamma_min,gamma_min_minus_(m-1),k000,k001,k010,k011,k100,k101,k110,k111,kstar,cycles_with_111,verdict"]
    def rec(name, ok, msg, report_only=False):
        nonlocal fails
        if not ok and not report_only: fails += 1
        L.append("%-6s %s  %s" % (name, "ok  " if ok else ("no   (reported only)" if report_only else "FAIL"), msg))
        print(L[-1], flush=True)
    info = {}
    for n in range(3, NS + 1):
        S = vc.System(26, n, level=0)
        N = 1 << n; F = S.F
        x = np.arange(N, dtype=np.uint32); full = np.uint32(N - 1)
        rl = lambda z: ((z << np.uint32(1)) | (z >> np.uint32(n - 1))) & full       # sigma
        rr = lambda z: ((z >> np.uint32(1)) | (z << np.uint32(n - 1))) & full
        U = rl(F)                                                                     # U = sigma F
        um2, um1 = rl(rl(x)), rl(x)                                                   # u_{j-2}, u_{j-1} at bit j
        form = x ^ (um2 & ~(um1 & ~x) & full)
        # f(u_{j-2}, u_{j-1}, u_j) with f = rule 26
        fv = np.zeros(N, dtype=np.uint32)
        for v in (1, 3, 4):
            fv |= (um2 if v & 4 else ~um2) & (um1 if v & 2 else ~um1) & (x if v & 1 else ~x)
        fv &= full
        rec("L5.2", bool((U == fv).all() and (U == form).all()), "n=%d all %d states, all cells" % (n, N))
        if n % 2:
            continue
        ev = sum(1 << i for i in range(0, n, 2)); od = sum(1 << i for i in range(1, n, 2))
        inE = (x & np.uint32(od)) == 0; inO = (x & np.uint32(ev)) == 0; inM = ~(inE | inO)
        chi = np.zeros(N, dtype=np.int64); dom = np.zeros(N, dtype=bool); sing = np.zeros(N, dtype=bool)
        srcmask = np.zeros(N, dtype=np.int64); singmask = np.zeros(N, dtype=np.int64)
        for xs in range(N):
            c, sources, sizes, d = analyse(xs, n)
            chi[xs] = c; dom[xs] = d
            sm = 0; gm = 0
            for s_, z_ in zip(sources, sizes):
                sm |= 1 << s_
                if z_ == 1: gm |= 1 << s_
            srcmask[xs] = sm; singmask[xs] = gm; sing[xs] = gm != 0
        ok = (chi % 2 == 0).all() and ((chi == 0) == (inE | inO)).all()
        # L5.3
        ok3 = ok and (chi[F] <= chi).all()
        px = S.cyc_states
        ok3 = ok3 and (chi[F[px]] == chi[px]).all()
        for j in range(n):
            y = x ^ np.uint32(1 << j)
            dchi = chi[y] - chi
            hasj = ((x >> np.uint32(j)) & 1) == 1
            ok3 = ok3 and np.isin(dchi, (-2, 0, 2)).all() and (dchi[hasj] <= 0).all()
        rec("L5.3", bool(ok3), "n=%d all states: chi(Fx) <= chi(x); constant on all %d cycles; every flip changes chi by -2, 0 or 2; deleting a one does not increase chi" % (n, S.m))
        # L5.4 (a)
        oka = True
        for xs in np.nonzero(inM)[0]:
            xs = int(xs)
            ones = [i for i in range(n) if (xs >> i) & 1]
            bad = False
            for t, j in enumerate(ones):
                if (xs >> ((j + 1) % n)) & 1:
                    pre = ones[t - 1]
                    dist = (j - pre) % n
                    if dist == 0: dist = n
                    if dist % 2 == 1: bad = True
            oka = oka and (dom[xs] == (not bad))
        # (b), (c)
        dx = x[dom]
        okb = dom[U[dx]].all() and (srcmask[U[dx]] == srcmask[dx]).all()
        for xs in dx.tolist():
            c, sources, sizes, d = analyse(xs, n)
            Ux = int(U[xs])
            for q, s_ in enumerate(sources):
                dlen = ((sources[(q + 1) % len(sources)] - s_ - 1) % n) + 1
                z = [1] + [(xs >> ((s_ + 2 * k) % n)) & 1 for k in range(1, (dlen - 1) // 2 + 1)]
                for k in range(1, (dlen - 1) // 2 + 1):
                    okb = okb and ((Ux >> ((s_ + 2 * k) % n)) & 1) == (z[k] ^ z[k - 1])
                    y = xs ^ (1 << ((s_ + 2 * k) % n))          # flip of a free cell
                    okb = okb and dom[y] and srcmask[y] == srcmask[xs]
                # the cells s+1, s+3, .. carry 0
                okb = okb and all(((xs >> ((s_ + o) % n)) & 1) == 0 for o in range(1, dlen - 1, 2))
        srcF = srcmask[F[dx]]
        shifted = np.array([((int(a) >> 1) | (int(a) << (n - 1))) & (N - 1) for a in srcmask[dx]], dtype=np.int64)
        okc = dom[F[dx]].all() and len(np.unique(F[dx])) == len(dx) and (srcF == shifted).all() and (S.per[dx] == 1).all()
        okc = okc and ((S.codes[dx] >> 7) & 1 == 0).all()
        rec("L5.4", bool(oka and okb and okc), "n=%d (a) all %d states of M; (b), (c) all %d domain states, all free cells" % (n, int(inM.sum()), len(dx)))
        # L5.5
        nd = inM & ~dom
        ok5 = sing[nd].all()
        for j in range(n):
            sj = ((singmask >> j) & 1) == 1
            ok5 = ok5 and (chi[x[sj] ^ np.uint32(1 << j)] == chi[sj] - 2).all()
        rec("L5.5", bool(ok5), "n=%d (a) all %d states of M that are not domain states; (b) all singleton groups" % (n, int(nd.sum())))
        # L5.6
        Lx = rl(x) ^ rr(x)
        EO = inE | inO
        ok6 = (F[EO] == Lx[EO]).all() and inO[F[inE]].all() and inE[F[inO]].all()
        msg = "n=%d F = rule 90 on E u O, E -> O -> E" % n
        if n & (n - 1) == 0:
            y = x[EO].copy()
            for t in range(n // 2): y = F[y]
            ok6 = ok6 and (y == 0).all() and int((S.per == 1)[EO].sum()) == 1 and S.per[0] == 1
            ok6 = ok6 and all(int(S.lab[1 << j]) == int(S.lab[0]) for j in range(n))
            msg += "; n = 2^k: F^(n/2) x = 0 on E u O, 0 the only periodic state there, flips of 0 return to 0"
        rec("L5.6", bool(ok6), msg)
        # LB.1
        okB1 = True; ncase = 0
        has111 = ((S.codes >> 7) & 1) == 1
        for xs in range(N):
            ones = [i for i in range(n) if (xs >> i) & 1]
            for t, j in enumerate(ones):
                if (xs >> ((j + 1) % n)) & 1:
                    dist = (j - ones[t - 1]) % n
                    if dist == 0: dist = n
                    if dist % 2 == 1:
                        r_ = (dist - 1) // 2
                        y = xs
                        for _ in range(r_): y = int(U[y])
                        okB1 = okB1 and all((y >> ((j + o) % n)) & 1 for o in (-1, 0, 1))
                        ncase += 1
        y = x[nd].copy(); seen = has111[y].copy()
        for t in range(n // 2 - 1):
            y = F[y]; seen |= has111[y]
        okB1 = okB1 and seen.all()
        rec("LB.1", bool(okB1), "n=%d %d triples (u, j, r); every state of M that is not a domain state has 111 on its orbit within n/2 - 1 steps" % (n, ncase))
        # LB.2
        per = S.per == 1
        pos = -np.ones(N, dtype=np.int64); EOs = x[EO]; pos[EOs] = np.arange(len(EOs))
        G = pos[Lx[EOs]]; k = 1
        while k < len(EOs): G = G[G]; k *= 2
        perL = np.zeros(N, dtype=bool); perL[EOs[G]] = True
        okB2 = per[perL].all() and per[dom].all()
        other = per & ~perL & ~dom
        cyc111 = np.zeros(S.m, dtype=bool); cyc111[S.lab[px[has111[px]]]] = True
        okB2 = okB2 and inM[other].all() and cyc111[S.lab[other]].all() and not (per & EO & ~perL).any()
        # every cycle: inside E u O, or domain cycle, or contains 111
        cycEO = np.ones(S.m, dtype=bool); cycEO[S.lab[px[~EO[px]]]] = False
        cycDom = np.ones(S.m, dtype=bool); cycDom[S.lab[px[~dom[px]]]] = False
        okB2 = okB2 and (cycEO | cycDom | cyc111).all()
        if n & (n - 1) == 0:
            okB2 = okB2 and int(cycEO.sum()) == 1 and cycEO[S.lab[0]]
        rec("LB.2", bool(okB2), "n=%d %d cycles: %d inside E u O, %d domain cycles, %d contain 111" % (n, S.m, int(cycEO.sum()), int(cycDom.sum()), int(cyc111.sum())))
        # LB.4
        cc = S.cycle_codes()
        six = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
        okB4 = ((cc[cycDom] & six) == six).all()
        if n & (n - 1) == 0:
            oth = np.arange(S.m) != S.lab[0]
            okB4 = okB4 and ((cc[oth] & 0b1001000) == 0b1001000).all()
        rec("LB.4", bool(okB4), "n=%d all domain cycles%s" % (n, "; n = 2^k: all cycles other than {0}" if n & (n - 1) == 0 else ""))
        info[n] = dict(cycEO=cycEO, cycDom=cycDom, cyc111=cyc111, chi_c=None)
    # LB.3 carrier words
    okB3 = True; nw = 0
    for n in range(3, NCW + 1):
        words = set()
        def gen(prefix, left, hasc):
            if left == 0:
                words.add((prefix, hasc)); return
            if left >= 5: gen(prefix + "11100", left - 5, True)
            if left >= 3: gen(prefix + "100", left - 3, hasc)
        gen("", n, False)
        for wd, hasc in words:
            w = vc.from_word(wd)
            for s in range(n):
                ws = vc.rot(w, n, s)
                y1 = step(26, ws, n); y2 = step(26, y1, n)
                okB3 = okB3 and y2 == vc.rot(ws, n, 1)
                nw += 1
                if hasc:
                    c0 = any(all((ws >> ((i + o) % n)) & 1 for o in (0, 1, 2)) for i in range(n))
                    c1 = any(all((y1 >> ((i + o) % n)) & 1 for o in (0, 1, 2)) for i in range(n))
                    okB3 = okB3 and (c0 or c1)
    rec("LB.3", okB3, "n = 3..%d: %d rotated words over 11100 and 100: F^2 w = sigma w (hence the period divides 2n); for carrier words w or Fw contains 111 (hence every second state of the cycle)" % (NCW, nw))
    # from the definitions
    kzero = []; kpos = []
    for n in range(4, NG + 1, 2):
        w1 = time.time()
        S = vc.System(26, n, level=2, workers=2)
        m = S.m; V = S.V; g = S.gamma; lab = S.lab
        kv, kstar, gmin, sel = S.indices()
        classes, comp = S.closed_classes()
        px = S.cyc_states
        cc = S.cycle_codes()
        ev = sum(1 << i for i in range(0, n, 2)); od = sum(1 << i for i in range(1, n, 2))
        stEO = ((px & np.uint32(od)) == 0) | ((px & np.uint32(ev)) == 0)
        cycEO = np.ones(m, dtype=bool); cycEO[lab[px[~stEO]]] = False
        domst = np.array([analyse(int(q), n)[3] for q in px])
        cycDom = np.ones(m, dtype=bool); cycDom[lab[px[~domst]]] = False
        cyc111 = ((cc >> 7) & 1) == 1
        zero = int(lab[0])
        G1 = S.g1()
        ok = True
        # LB.6, LB.7
        dist = S.g1_dist_to(np.nonzero(cycEO)[0].tolist())
        b6 = bool((dist >= 0).all())
        b7 = len({int(comp[q]) for q in np.nonzero(cycEO)[0]}) == 1
        rec("LB.6", b6, "n=%d every cycle has a G1 path to a cycle inside E u O" % n)
        rec("LB.7", b7, "n=%d the %d cycles inside E u O lie in one strongly connected component" % (n, int(cycEO.sum())))
        ok = ok and b6 and b7
        if n & (n - 1) == 0:
            others = np.arange(m) != zero
            d0 = S.g1_dist_to([zero])
            a = bool((d0 >= 0).all())
            b = bool((V[zero][others] >= 2).all())
            c = len(classes) == 1 and list(classes[0]) == [zero]
            C1 = np.nonzero(V[zero] == 2)[0]
            reach = np.zeros(m, dtype=bool); reach[C1] = True; front = C1.tolist()
            while front:
                nf = []
                for u in front:
                    for w_ in np.nonzero(G1[u])[0]:
                        if not reach[w_]: reach[w_] = True; nf.append(int(w_))
                front = nf
            d = g[zero] == m - 1 and bool((g[others] >= m).all()) and bool(((g == m) == reach)[others].all()) and sel.sum() == 1 and sel[zero]
            rec("T5.7", bool(a and b and c and d), "n=%d m=%d (a) %s (b) %s (c) %s (d) %s [cycles with gamma = m: %d of %d; largest gamma - (m-1): %d]" % (n, m, a, b, c, d, int((g == m).sum()), m - 1, int(g.max()) - (m - 1)))
            ok = ok and a and b and c and d
            if n >= 8:
                pa = kv[0] == 0 and kv[1:7] == [1] * 6
                pb = kv[7] in (1, 2) and (kv[7] == 1) == bool((cyc111 & (g == m)).any()) and kstar == kv[7]
                pc = True; msgc = ""
                kk = n.bit_length() - 1
                if kk % 2 == 1:
                    wd = vc.from_word("11100" + "100" * ((n - 5) // 3))
                    pc = S.per[wd] == 1 and g[lab[wd]] == m and kv[7] == 1 and kstar == 1
                    msgc = "; (c) k odd: carrier word on a cycle with gamma = m, k_111 = 1, k* = 1: %s" % pc
                rec("P5.8", bool(pa and pb and pc), "n=%d (a) %s (b) %s [k_111 = %d, k* = %d]%s" % (n, pa, pb, kv[7], kstar, msgc))
                b5 = bool((g[cycDom] == m).all())
                rec("LB.5", b5, "n=%d all %d domain cycles have gamma = m" % (n, int(cycDom.sum())))
                ok = ok and pa and pb and pc and b5
            if n == 4:
                rec("n=4", m == 1 and kv == [0, 1, 1, 2, 1, 1, 2, 2] and kstar == 2, "computed values quoted in the text: m = %d, k_v = %s, k* = %d" % (m, kv, kstar))
            if n == 16:
                # cycles that pass through a carrier word
                carr = set()
                def gen(prefix, left, hasc):
                    if left == 0:
                        if hasc:
                            w = vc.from_word(prefix)
                            for s in range(n): carr.add(vc.rot(w, n, s))
                        return
                    if left >= 5: gen(prefix + "11100", left - 5, True)
                    if left >= 3: gen(prefix + "100", left - 3, hasc)
                gen("", n, False)
                thr = {int(lab[q]) for q in carr if S.per[q]}
                rec("n=16", kv[7] == 2 and kstar == 2 and int(cyc111.sum()) == 3 and int((cyc111 & reach).sum()) == 0 and len(thr & set(np.nonzero(cyc111)[0].tolist())) == 2,
                    "computed values quoted in the text: k_111 = %d, k* = %d, cycles with 111: %d, of these reachable from a C_1 with V({0}, C_1) = 2: %d, passing through a carrier word: %d" % (
                        kv[7], kstar, int(cyc111.sum()), int((cyc111 & reach).sum()), len(thr & set(np.nonzero(cyc111)[0].tolist()))))
        else:
            K = np.zeros(m, dtype=bool)
            for Kc in classes: K[Kc] = True
            a = len(classes) == 1
            b = bool(K[zero] and K[cycEO].all() and K[cycDom].all())
            c = bool(cyc111[~K].all())
            d = (int(np.bitwise_or.reduce(cc[K])) & 0x7F) == 0x7F
            e = bool((sel == K).all()) and gmin == m - 1 and kv[:7] == [0] * 7 and (kstar == 0) == bool((cyc111 & K).any())
            rec("P5.9", bool(a and b and c and d and e), "n=%d m=%d one closed class %s (|K| = %d); contains {0}, the cycles in E u O and the domain cycles %s; cycles outside K contain 111 %s; codes other than 111 in K %s; S = K, gamma_min = m-1, k_v = 0 (v != 111), k* = 0 iff a cycle with 111 is in K %s [k* = %d; cycles with 111: %d, in K: %d]" % (
                n, m, a, int(K.sum()), b, c, d, e, kstar, int(cyc111.sum()), int((cyc111 & K).sum())))
            ok = ok and a and b and c and d and e
            (kzero if kstar == 0 else kpos).append(n)
        rows.append("%d,%d,%d,%d,%d,%d,%s,%d,%d,%s" % (n, m, len(classes), int(sel.sum()), gmin, gmin - (m - 1), ",".join(map(str, kv)), kstar, int(cyc111.sum()), "ok" if ok else "FAIL"))
        print("   [n=%d wall %.1f s]" % (n, time.time() - w1), flush=True)
    L.append("even n that is not a power of two, n <= %d: k* = 0 at n = %s; k* > 0 at n = %s (the paper's macros: zero at 14, 20, 22; positive at 10, 12, 18; Table 1 has 1 at n = 6)" % (NG, kzero, kpos))
    print(L[-1])
    L.append("T07 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T07.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(HERE, "out", "T07_rule26.csv"), "w").write("\n".join(rows) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
