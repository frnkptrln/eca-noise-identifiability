"""T02 -- Section 3.1 (rule 154), Lemmas 3.2 to 3.8: every state, every cell, every cycle.

 L3.2 local form          f(a,b,c) = c + a(1+b) on the eight codes; (Fx)_i = x_{i+1} + x_{i-1}(1 + x_i), all states, n = 3..NS.
 L3.3 rule 90 on E, O     even n = 4..NS: every x in E (resp. O): F(x) = Lx, F(x) in O (resp. E); F^t = L^t on E u O
                          for t = 0..n.
 L3.4 nilpotency          (a) n = 4, 8, 16, 32: F^{n/2}(x) = 0 for EVERY x in E u O (with F itself for n <= NS, with
                              L for n = 32, where F = L on E u O is L3.3); n = 64..4096: for every e_j (L, big integers).
                          (b) even n <= NS, not a power of two: the orbit of every e_j under F is followed until a state
                              repeats and never contains 0; even n <= 4096: L^n e_0 != 0 (which decides it, see output).
 L3.5 invariance of M     even n = 4..NS: F(M) inside M.
 L3.6 collisions          n = 3..NS: all pairs x != y with F(x) = F(y) are of the three kinds; F bijective for odd n.
                          Also recorded: whether, conversely, every pair of the three kinds collides.
 L3.7 periodic states     even n = 4..NS: F permutes M; periodic states = M u (periodic states of L in E u O);
                          n = 2^k: periodic states = M u {0}.
 L3.8 one-flip moves      even n = 4..NG: (a) for every x in M, every cell j with x + e_j in M: same cycle or both
                          edges in G1 (G1 from the matrix V of the definitions); (b) the sub-graph of G1 on the cycles
                          contained in M is strongly connected.
Output: out/T02.txt.   Usage: python3 T02_rule154_lemmas.py [NS (default 22)] [NG (default 16)]
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def masks(n):
    even = sum(1 << i for i in range(0, n, 2))
    odd = sum(1 << i for i in range(1, n, 2))
    return even, odd

def Lmap(x, n):
    """rule 90 on integer arrays or Python ints: (Lx)_i = x_{i-1} + x_{i+1}."""
    full = (1 << n) - 1
    return (((x << 1) | (x >> (n - 1))) ^ ((x >> 1) | (x << (n - 1)))) & full

def main():
    NS = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    NG = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    t0 = time.process_time(); w0 = time.time()
    L = []
    fails = 0
    def rec(name, ok, msg):
        nonlocal fails
        if not ok:
            fails += 1
        L.append("%-5s %s  %s" % (name, "ok  " if ok else "FAIL", msg))
    # L3.2 codes
    vals = [(c + a * (1 + b)) % 2 for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    rec("L3.2", vals == [(154 >> v) & 1 for v in range(8)] and vals == [0, 1, 0, 1, 1, 0, 0, 1], "eight codes: values %s" % vals)
    for n in range(3, NS + 1):
        S = vc.System(154, n, level=0)
        N = 1 << n
        x = np.arange(N, dtype=np.uint32)
        F = S.F
        full = np.uint32(N - 1)
        xm = ((x << np.uint32(1)) | (x >> np.uint32(n - 1))) & full       # (xm)_i = x_{i-1}
        xp = ((x >> np.uint32(1)) | (x << np.uint32(n - 1))) & full       # (xp)_i = x_{i+1}
        ok = (F == (xp ^ (xm & ~x & full))).all()
        rec("L3.2", ok, "n=%d all %d states, all cells" % (n, N))
        # L3.6 collisions
        cntimg = np.bincount(F, minlength=N)          # size of the fibre of every state
        maxfib = int(cntimg.max())
        ev, od = masks(n)
        okc = True
        npairs = 0
        if n % 2 == 1:
            okc = maxfib == 1
        else:
            inE = (x & od) == 0
            inO = (x & ev) == 0
            multi = x[cntimg[F] >= 2]                  # all states that share their image with another state
            fib = {}
            for xa in multi.tolist():
                fib.setdefault(int(F[xa]), []).append(xa)
            for run in fib.values():                   # ALL pairs x != y with F(x) = F(y)
                for a_ in range(len(run)):
                    for b_ in range(a_ + 1, len(run)):
                        xa, xb = run[a_], run[b_]
                        npairs += 1
                        k1 = (xa & od) == 0 and (xb & od) == 0 and (xa ^ xb) == ev
                        k2 = (xa & ev) == 0 and (xb & ev) == 0 and (xa ^ xb) == od
                        k3 = {xa, xb} == {ev, od}
                        okc = okc and (k1 or k2 or k3)
            # converse (not claimed by the lemma): pairs of the three kinds
            E_states = x[inE]
            conv = (F[E_states] == F[E_states ^ np.uint32(ev)]).all() and (F[x[inO]] == F[x[inO] ^ np.uint32(od)]).all() and F[ev] == F[od]
        rec("L3.6", okc, "n=%d %s" % (n, "odd: F is a bijection" if n % 2 else "%d colliding pairs, all of the three kinds; largest fibre %d; converse (every such pair collides): %s" % (npairs, maxfib, conv)))
        if n % 2 == 0:
            inE = (x & od) == 0
            inO = (x & ev) == 0
            inM = ~(inE | inO)
            Lx = Lmap(x, n)
            ok3 = (F[inE] == Lx[inE]).all() and (F[inO] == Lx[inO]).all() and ((F[inE] & ev) == 0).all() and ((F[inO] & od) == 0).all()
            # F^t = L^t on E u O, t = 0..n
            EO = x[inE | inO]
            a_ = EO.copy(); b_ = EO.copy()
            for t in range(n + 1):
                ok3 = ok3 and (a_ == b_).all()
                a_ = F[a_]; b_ = Lmap(b_, n)
            rec("L3.3", ok3, "n=%d all %d states of E u O" % (n, len(EO)))
            ok5 = inM[F[inM]].all()
            rec("L3.5", ok5, "n=%d all %d states of M" % (n, int(inM.sum())))
            # L3.7
            per = S.per == 1
            perm_ok = len(np.unique(F[inM])) == int(inM.sum()) and inM[F[inM]].all()
            # periodic states of L in E u O, computed with L alone
            # image of L^K on E u O for K >= number of states of E u O: use index map and repeated squaring
            pos = -np.ones(N, dtype=np.int64); pos[EO] = np.arange(len(EO))
            G = pos[Lmap(EO, n)]
            K = 1
            while K < len(EO):
                G = G[G]; K *= 2
            perL = np.zeros(N, dtype=bool); perL[EO[G]] = True
            ok7 = perm_ok and per[inM].all() and (per == (inM | perL)).all()
            msg = "n=%d F permutes M; periodic = M u per(L|EuO) (%d + %d states)" % (n, int(inM.sum()), int(perL.sum()))
            if n & (n - 1) == 0:
                ok7 = ok7 and int(perL.sum()) == 1 and perL[0]
                # cycles: {0} and cycles inside M
                msg += "; power of two: periodic = M u {0}"
            rec("L3.7", ok7, msg)
            # L3.4 with F
            if n & (n - 1) == 0:
                a_ = EO.copy()
                for t in range(n // 2):
                    a_ = F[a_]
                rec("L3.4a", (a_ == 0).all(), "n=%d F^(n/2) x = 0 for all %d states of E u O" % (n, len(EO)))
            else:
                ok4 = True
                for j in range(n):
                    y = 1 << j
                    seen = set()
                    while y not in seen:
                        seen.add(y)
                        if y == 0:
                            ok4 = False
                        y = int(F[y])
                rec("L3.4b", ok4, "n=%d orbit of every e_j under F followed until it repeats: never 0" % n)
    # L3.4 beyond NS with L
    n = 32
    ev, od = masks(n)
    xs = np.arange(1 << 16, dtype=np.uint64)
    # spread 16 bits to even cells
    sp = np.zeros(1 << 16, dtype=np.uint64)
    for i in range(16):
        sp |= ((xs >> np.uint64(i)) & np.uint64(1)) << np.uint64(2 * i)
    okb = True
    for start in (sp, sp << np.uint64(1)):
        a_ = start.copy()
        for t in range(n // 2):
            a_ = (((a_ << np.uint64(1)) | (a_ >> np.uint64(n - 1))) ^ ((a_ >> np.uint64(1)) | (a_ << np.uint64(n - 1)))) & np.uint64((1 << n) - 1)
        okb = okb and (a_ == 0).all()
    rec("L3.4a", okb, "n=32 L^(n/2) x = 0 for all 2*65536 states of E u O (F = L there by L3.3)")
    okc_ = True
    for k in range(6, 13):
        n = 1 << k
        y = 1
        for t in range(n // 2):
            y = Lmap(y, n)
        okc_ = okc_ and y == 0
    rec("L3.4a", okc_, "n=64..4096 (powers of two): L^(n/2) e_0 = 0 (e_j by rotation)")
    okd = True
    cnt = 0
    for n in range(6, 4097, 2):
        if n & (n - 1) == 0:
            continue
        y = 1
        for t in range(n):
            y = Lmap(y, n)
        okd = okd and y != 0
        cnt += 1
    rec("L3.4b", okd, "even n = 6..4096 not a power of two (%d ring sizes): L^n e_0 != 0. For a linear map on an n-dimensional space, L^t x = 0 for some t iff L^n x = 0, so this decides 'never 0'" % cnt)
    # L3.8 with G1
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    for n in range(4, NG + 1, 2):
        S = vc.System(154, n, level=1, workers=2)
        ev, od = masks(n)
        N = 1 << n
        x = np.arange(N, dtype=np.uint32)
        inM = ~(((x & od) == 0) | ((x & ev) == 0))
        xm = x[inM]
        G1 = S.V == 1
        oka = True
        nmoves = 0
        for j in range(n):
            y = xm ^ np.uint32(1 << j)
            keep = inM[y]
            a_, b_ = S.lab[xm[keep]], S.lab[y[keep]]
            dif = a_ != b_
            oka = oka and S.per[y[keep]].all() and G1[a_[dif], b_[dif]].all() and G1[b_[dif], a_[dif]].all()
            nmoves += int(keep.sum())
        cycM = np.unique(S.lab[xm])
        sub = G1[np.ix_(cycM, cycM)]
        ncomp, _ = connected_components(csr_matrix(sub), directed=True, connection="strong")
        rec("L3.8", bool(oka and ncomp == 1), "n=%d (a) %d flips inside M checked; (b) G1 on the %d cycles in M has %d strongly connected component(s)" % (n, nmoves, len(cycM), ncomp))
    L.append("T02 %s   NS=%d NG=%d   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", NS, NG, time.process_time() - t0, time.time() - w0))
    txt = "\n".join(L)
    print(txt)
    open(os.path.join(HERE, "out", "T02.txt"), "w").write(txt + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
