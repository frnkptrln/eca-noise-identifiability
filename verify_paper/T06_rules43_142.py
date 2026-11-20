"""T06 -- Section 3.2 (rules 43 and 142): every numbered statement on small rings, with the smallest ring sizes of
each statement and the sizes just below. (These proofs were verified before by a separate session; this is the check of
the edges of the ranges asked for in Part 2, done with own code.)

 All states, n = 3..NS:  L3.12 common form; L3.13 wall map; L3.14 conservation; L3.15 flip; L3.16 pairs (all words d);
                         L3.17 periodic wall words; L3.18 periodic states (a), (b), (c); L3.19 the level n/2.
 From the definitions (V, gamma for every root, k_v), n = 3..NG:
   4 | n:      T3.20 (1)-(3), C3.21, P3.22 healing time (also by direct simulation for 4 | n up to 64);
   4 not | n:  L3.23 (a)-(d), L3.25, T3.26, C3.27;
   every n >= 3: L3.24 slides (first statement for all slides; (a), (b) by a search over slides, n <= NSL);
   T3.28 for n >= 4;  n = 3 is reported (outside the range of the theorems).
Output: out/T06.txt, out/T06_rules43_142.csv.   Usage: python3 T06_rules43_142.py [NS=16] [NG=18] [NSL=13]
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

def popcount(a):
    a = a.astype(np.uint64); c = np.zeros(a.shape, dtype=np.int64)
    while a.any():
        c += (a & np.uint64(1)).astype(np.int64); a >>= np.uint64(1)
    return c

def runs(x, n):
    """cyclic run lengths of a non-constant state, starting at a run boundary."""
    s = next(i for i in range(n) if ((x >> i) & 1) != ((x >> ((i - 1) % n)) & 1))
    out = []; i = 0
    while i < n:
        l = 1
        while i + l < n and ((x >> ((s + i + l) % n)) & 1) == ((x >> ((s + i) % n)) & 1): l += 1
        out.append(l); i += l
    return out

def is_rotation(seq, target):
    k = len(seq)
    return k == len(target) and any(seq[s:] + seq[:s] == target for s in range(k))

def main():
    arg = lambda k, d: int(sys.argv[k]) if len(sys.argv) > k else d
    NS, NG, NSL = arg(1, 16), arg(2, 18), arg(3, 13)
    t0 = time.process_time(); w0 = time.time()
    L = []; fails = 0
    rows = ["rule,n,m,closed_classes,selected,gamma_min,k000,k001,k010,k011,k100,k101,k110,k111,kstar,verdict"]
    def rec(name, ok, msg, report_only=False):
        nonlocal fails
        if not ok and not report_only: fails += 1
        L.append("%-6s %s  %s" % (name, "ok  " if ok else ("no   (outside the stated range, reported only)" if report_only else "FAIL"), msg))
        print(L[-1], flush=True)
    # L3.12
    ok = True
    for rule in (43, 142):
        for v in range(8):
            a, b, c = (v >> 2) & 1, (v >> 1) & 1, v & 1
            want = c if a != c else (b if rule == 142 else 1 - b)
            ok = ok and ((rule >> v) & 1) == want
    rec("L3.12", ok, "both rules, eight codes")
    for n in range(3, NS + 1):
        N = 1 << n; full = np.uint32(N - 1)
        x = np.arange(N, dtype=np.uint32)
        rl = lambda z: ((z << np.uint32(1)) | (z >> np.uint32(n - 1))) & full        # (rl z)_i = z_{i-1}  = sigma
        rr = lambda z: ((z >> np.uint32(1)) | (z << np.uint32(n - 1))) & full        # (rr z)_i = z_{i+1}  = sigma^{-1}
        delta = x ^ rr(x)
        G184 = (x & rr(x)) | (rl(x) & ~x & full)
        G226 = (rl(x) & x) | (~x & rr(x) & full)
        Pm = x & rr(x); Qm = ~x & ~rr(x) & full                 # P(d), Q(d) for d = x
        cnt = popcount(x)
        # L3.14a
        ok14 = (popcount(G184) == cnt).all() and (popcount(G226) == cnt).all()
        # L3.16
        Nm = Qm & rr(rr(Pm)); Npm = Pm & rr(rr(Qm))
        d1 = G184
        a_ = ((Pm[d1] == (rr(Pm) & ~rl(Qm) & full)).all() and (Qm[d1] == (rl(Qm) & ~rr(Pm) & full)).all()
              and (popcount(Pm[d1]) == popcount(Pm) - popcount(Nm)).all() and (popcount(Qm[d1]) == popcount(Qm) - popcount(Nm)).all())
        z = Nm == 0
        a_ = a_ and (Pm[d1][z] == rr(Pm)[z]).all() and (Qm[d1][z] == rl(Qm)[z]).all()
        d2 = G226
        b_ = ((Pm[d2] == (rl(Pm) & ~rr(Qm) & full)).all() and (Qm[d2] == (rr(Qm) & ~rl(Pm) & full)).all()
              and (popcount(Pm[d2]) == popcount(Pm) - popcount(Npm)).all() and (popcount(Qm[d2]) == popcount(Qm) - popcount(Npm)).all())
        z = Npm == 0
        b_ = b_ and (Pm[d2][z] == rl(Pm)[z]).all() and (Qm[d2][z] == rr(Qm)[z]).all()
        c_ = (popcount(Pm) - popcount(Qm) == 2 * cnt - n).all()
        rec("L3.16", bool(a_ and b_ and c_), "n=%d all %d words d: (a), (b), (c)" % (n, N))
        # L3.17
        ok17 = True
        for G, sP, sQ in ((G184, rl, rr), (G226, rr, rl)):
            H = G.copy(); k = 1
            while k < N: H = H[H]; k *= 2
            per = np.zeros(N, dtype=bool); per[H] = True
            ok17 = ok17 and (per == ((Pm == 0) | (Qm == 0))).all()
            ok17 = ok17 and (G[Pm == 0] == sP(x)[Pm == 0]).all() and (G[Qm == 0] == sQ(x)[Qm == 0]).all()
        rec("L3.17", bool(ok17), "n=%d all words d, both maps" % n)
        iso = (x ^ rl(x)) & (x ^ rr(x)); inter = ~(x ^ rl(x)) & ~(x ^ rr(x)) & full
        w = popcount(delta)
        for rule in (43, 142):
            S = vc.System(rule, n, level=0)
            F = S.F
            d = delta
            if rule == 142:
                form = x ^ (d & ~rl(d) & full); Gd = G226
            else:
                form = x ^ full ^ (rl(d) & ~d & full); Gd = G184
            rec("L3.13", bool((F == form).all() and (delta[F] == Gd[delta]).all()), "rule %d n=%d all states" % (rule, n))
            ok = ok14 and (F[x ^ full] == (F ^ full)).all() and (w[F] == w).all() and (w % 2 == 0).all()
            rec("L3.14", bool(ok), "rule %d n=%d (a) all words, (b) all states" % (rule, n))
            per = S.per == 1
            a_ = (per == ((iso == 0) | (inter == 0))).all()
            cs = rl(x) ^ full
            if rule == 43:
                b_ = (F[iso == 0] == cs[iso == 0]).all() and (F[inter == 0] == rr(x)[inter == 0]).all()
            else:
                b_ = (F[iso == 0] == rr(x)[iso == 0]).all() and (F[inter == 0] == cs[inter == 0]).all()
            # preserved by F, sigma, complement
            for prop in (iso == 0, inter == 0):
                b_ = b_ and prop[F[prop]].all() and prop[rl(x)[prop]].all() and prop[(x ^ full)[prop]].all()
            px = x[per]
            c_ = True
            y = px.copy()
            for s in range(n):
                y = rl(y)
                c_ = c_ and ((S.lab[y] == S.lab[px]) | (S.lab[y] == S.lab[px ^ full])).all()
            rec("L3.18", bool(a_ and b_ and c_), "rule %d n=%d (a) all states, (b), (c) all periodic states and all rotations" % (rule, n))
            if n % 2 == 0:
                alt = (Pm[delta] == 0) & (Qm[delta] == 0)
                if n % 4 == 0:
                    xh = vc.from_word("0011" * (n // 4))
                    X = sorted({vc.rot(xh, n, s) for s in range(4)})
                    ok = sorted(x[alt].tolist()) == X and sorted(x[per & (w == n // 2)].tolist()) == X
                    ok = ok and len({int(S.lab[q]) for q in X}) == 1 and all(int(F[q]) == vc.rot(q, n, n - 1) for q in X)
                    cm = 0
                    for q in X: cm |= int(S.codes[q])
                    ok = ok and cm == (1 << 1) | (1 << 3) | (1 << 6) | (1 << 4) and len(S.states_of(int(S.lab[X[0]]))) == 4
                else:
                    ok = not alt.any()
                rec("L3.19", bool(ok), "rule %d n=%d" % (rule, n))
        # L3.15
        ok = True
        for j in range(n):
            dw = w[x ^ np.uint32(1 << j)] - w
            ij = ((iso >> np.uint32(j)) & 1) == 1; nj = ((inter >> np.uint32(j)) & 1) == 1
            ok = ok and (dw[nj] == 2).all() and (dw[ij] == -2).all() and (dw[~ij & ~nj] == 0).all()
        rec("L3.15", bool(ok), "n=%d all states, all cells" % n)
    # healing time by simulation, 4 | n up to 64
    okh = True
    for n in range(4, 65, 4):
        xh = vc.from_word("0011" * (n // 4))
        X = {vc.rot(xh, n, s) for s in range(4)}
        for rule in (43, 142):
            for xs in X:
                for j in range(n):
                    b = lambda i: (xs >> (i % n)) & 1
                    left = b(j - 1) != b(j) == b(j + 1); right = b(j - 1) == b(j) != b(j + 1)
                    okh = okh and (left != right)
                    y = xs ^ (1 << j); t = 0
                    while True:
                        y = step(rule, y, n); t += 1
                        if y in X or t > n: break
                    want = (1 if left else n // 2 - 1) if rule == 43 else (n // 2 - 1 if left else 1)
                    okh = okh and t == want
    rec("P3.22", okh, "4 | n, n = 4..64: both rules, all four states of X, all cells: tau as stated (n = 4: tau = 1 for both kinds)")
    # G1-based
    for n in range(3, NG + 1):
        for rule in (43, 142):
            S = vc.System(rule, n, level=2, workers=2)
            m = S.m; V = S.V; g = S.gamma; lab = S.lab
            kv, kstar, gmin, sel = S.indices()
            classes, comp = S.closed_classes()
            px = S.cyc_states
            N = 1 << n; fullp = N - 1
            wst = np.array([bin(int(q) ^ (((int(q) >> 1) | (int(q) << (n - 1))) & fullp)).count("1") for q in px])
            wc = np.zeros(m, dtype=np.int64); wc[lab[px]] = wst
            G1 = S.g1()
            cc = S.cycle_codes()
            verdict = True
            ps = px
            isoP = np.array([any(((int(q) >> i) & 1) != ((int(q) >> ((i - 1) % n)) & 1) and ((int(q) >> i) & 1) != ((int(q) >> ((i + 1) % n)) & 1) for i in range(n)) for q in ps])
            intP = np.array([any(((int(q) >> i) & 1) == ((int(q) >> ((i - 1) % n)) & 1) and ((int(q) >> i) & 1) == ((int(q) >> ((i + 1) % n)) & 1) for i in range(n)) for q in ps])
            oks = True
            if n % 4 == 0:
                xh = vc.from_word("0011" * (n // 4))
                Xc = int(lab[xh])
                a = len(S.states_of(Xc)) == 4 and all(int(lab[int(q) ^ (1 << j)]) == Xc for q in S.states_of(Xc) for j in range(n))
                others = np.arange(m) != Xc
                a = a and bool((V[Xc][others] >= 2).all())
                dist = S.g1_dist_to([Xc])
                b = bool((dist == np.abs(wc - n // 2) // 2).all())
                c = len(classes) == 1 and list(classes[0]) == [Xc]
                rec("T3.20", bool(a and b and c), "rule %d n=%d m=%d (1) %s (2) %s (3) %s" % (rule, n, m, a, b, c))
                d = sel.sum() == 1 and sel[Xc] and gmin == m - 1 and kv == [1, 0, 1, 0, 0, 1, 0, 1] and kstar == 1
                rec("C3.21", bool(d), "rule %d n=%d S = {X}, gamma_min = m-1 = %d, k_v = %s, k* = %d" % (rule, n, gmin, kv, kstar))
                verdict = a and b and c and d
            elif n >= 5:
                wm = max(q for q in range(0, n, 2) if q < n / 2); wp = wm + 2
                K = (wc == wm) | (wc == wp)
                a = bool((intP[wst == wm] & ~isoP[wst == wm]).all() and (isoP[wst == wp] & ~intP[wst == wp]).all())
                inK = K[lab[ps]]
                b = all(K[lab[ps[inK] ^ np.uint32(1 << j)]].all() for j in range(n)) and not G1[np.ix_(K, ~K)].any()
                c = bool(G1[np.ix_(wc == wm, wc == wp)].any(axis=1).all() and G1[np.ix_(wc == wp, wc == wm)].any(axis=1).all())
                dist = S.g1_dist_to(np.nonzero(K)[0].tolist())
                d = bool((dist >= 0).all())
                rec("L3.23", bool(a and b and c and d), "rule %d n=%d w- = %d, w+ = %d, |K| = %d of %d cycles: (a) %s (b) %s (c) %s (d) %s" % (rule, n, wm, wp, int(K.sum()), m, a, b, c, d))
                eta = n - 2 * wm
                z = vc.from_word("0" * (eta + 2) + "1100" * ((wm - 2) // 2) + "11")
                zi = int(np.nonzero(ps == z)[0][0]) if S.per[z] else -1
                okz = zi >= 0 and not isoP[zi] and wst[zi] == wm
                Z, Zc = int(lab[z]), int(lab[z ^ fullp])
                okz = okz and comp[Z] == comp[Zc]
                rec("L3.25", bool(okz), "rule %d n=%d z = %s; Z and its complement cycle are %s" % (rule, n, vc.word(z, n), "equal" if Z == Zc else "in one strongly connected component of G1"))
                Kset = sorted(np.nonzero(K)[0].tolist())
                t = len(classes) == 1 and sorted(classes[0].tolist()) == Kset and d
                rec("T3.26", bool(t), "rule %d n=%d K is the only closed class" % (rule, n))
                e = bool((sel == K).all()) and gmin == m - 1 and int(np.bitwise_or.reduce(cc[K])) == 255 and kv == [0] * 8 and kstar == 0
                rec("C3.27", bool(e), "rule %d n=%d S = K, gamma_min = m-1 = %d, all codes in K, k_v = 0" % (rule, n, gmin))
                verdict = a and b and c and d and okz and t and e
            # slides: first statement
            for j in range(n):
                y = ps ^ np.uint32(1 << j)
                wy = np.array([bin(int(q) ^ (((int(q) >> 1) | (int(q) << (n - 1))) & fullp)).count("1") for q in y])
                sl = (S.per[y] == 1) & (wy == wst)
                a_, b_ = lab[ps[sl]], lab[y[sl]]
                dif = a_ != b_
                oks = oks and bool(G1[a_[dif], b_[dif]].all() and G1[b_[dif], a_[dif]].all())
            msg = "rule %d n=%d first statement (all slides)" % (rule, n)
            if n <= NSL:
                # components of the periodic states under slides
                idx = {int(q): i for i, q in enumerate(ps)}
                parent = list(range(len(ps)))
                def find(u):
                    while parent[u] != u:
                        parent[u] = parent[parent[u]]; u = parent[u]
                    return u
                for j in range(n):
                    y = ps ^ np.uint32(1 << j)
                    for i, q in enumerate(y):
                        k_ = idx.get(int(q))
                        if k_ is not None and wst[k_] == wst[i]:
                            parent[find(i)] = find(k_)
                good = {}
                for i, q in enumerate(ps):
                    q = int(q)
                    if q == 0 or q == fullp: continue
                    rn = runs(q, n); w_ = int(wst[i])
                    if not isoP[i] and w_ >= 2 and is_rotation(rn, [n - 2 * w_ + 2] + [2] * (w_ - 1)): good[(find(i), "a")] = True
                    if not intP[i] and n / 2 < w_ < n and is_rotation(rn, [2] * (n - w_) + [1] * (2 * w_ - n)): good[(find(i), "b")] = True
                na = nb = 0
                for i, q in enumerate(ps):
                    w_ = int(wst[i])
                    if not isoP[i] and w_ >= 2:
                        na += 1; oks = oks and good.get((find(i), "a"), False)
                    if not intP[i] and n / 2 < w_ < n:
                        nb += 1; oks = oks and good.get((find(i), "b"), False)
                msg += "; (a) %d states, (b) %d states: the state x* is reached by slides" % (na, nb)
            rec("L3.24", bool(oks), msg)
            verdict = verdict and oks
            if n >= 4:
                t28 = kstar == (1 if n % 4 == 0 else 0)
                rec("T3.28", t28, "rule %d n=%d k* = %d" % (rule, n, kstar))
                verdict = verdict and t28
            else:
                rec("n=3", False, "rule %d n=3: m = %d, closed classes %d, selected %d, k_v = %s, k* = %d (the theorems start at n = 4)" % (rule, m, len(classes), int(sel.sum()), kv, kstar), report_only=True)
            rows.append("%d,%d,%d,%d,%d,%d,%s,%d,%s" % (rule, n, m, len(classes), int(sel.sum()), gmin, ",".join(map(str, kv)), kstar, "ok" if verdict else "FAIL"))
    L.append("T06 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T06.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(HERE, "out", "T06_rules43_142.csv"), "w").write("\n".join(rows) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
