"""Exhaustive tests of the statements of PROOF_43_142.md, Sections 1-6, at small n.

Every check compares a statement with a quantity computed from the definitions (rule table, functional graph
of F on all 2^n states, single flips). Output: out/lemma_tests.json (per statement, per n: number of cases
checked and number of failures, with up to 5 counterexamples).

Usage: python test_lemmas.py NMAX   (default 16)
"""
import json, os, sys, time
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eca import (Dynamics, global_map, rot_left_neighbour as Lsh, rot_right_neighbour as Rsh, popcount,
                 walls, sccs)

RULES = (43, 142)
results = {}


def rec(name, n, checked, fails):
    d = results.setdefault(name, {})
    e = d.setdefault(str(n), {"checked": 0, "failures": 0, "examples": []})
    e["checked"] += int(checked)
    fl = list(fails)
    e["failures"] += len(fl)
    e["examples"] = (e["examples"] + [str(f) for f in fl[:5]])[:5]


def mask(n):
    return (1 << n) - 1


def delta(n, x):
    return x ^ Rsh(x, n)


def P_of(n, d):
    return d & Rsh(d, n)


def Q_of(n, d):
    return (~d) & (~Rsh(d, n)) & mask(n)


def sigma(n, x, r=1):
    """(sigma x)_i = x_(i-1): bit i of the result is bit i-1 of x (pattern moves right)."""
    r %= n
    if r == 0:
        return x
    return ((x << r) | (x >> (n - r))) & mask(n)


def comp(n, x):
    return (~x) & mask(n)


def runs(n, x):
    """run lengths of a non-constant state, starting at a run boundary at the smallest cell i with
    x_(i-1) != x_i; also returns that start cell."""
    b = [(x >> i) & 1 for i in range(n)]
    starts = [i for i in range(n) if b[i] != b[i - 1]]
    s = starts[0]
    L = []
    for k in range(len(starts)):
        a = starts[k]; e = starts[(k + 1) % len(starts)]
        L.append((e - a) % n or n)
    return L, s


def run_word_from(n, x):
    """all cyclic readings of the run lengths starting at a run boundary, with the colour of the first run."""
    b = [(x >> i) & 1 for i in range(n)]
    starts = [i for i in range(n) if b[i] != b[i - 1]]
    out = []
    for k in range(len(starts)):
        L = []
        for t in range(len(starts)):
            a = starts[(k + t) % len(starts)]; e = starts[(k + t + 1) % len(starts)]
            L.append((e - a) % n or n)
        out.append((tuple(L), b[starts[k]], starts[k]))
    return out


def test_tables():
    # (R): f(a,b,c) = c if a != c; = b (142) / 1-b (43) if a = c. Agreement codes.
    fails = []
    for c in range(8):
        a, b, cc = (c >> 2) & 1, (c >> 1) & 1, c & 1
        for rule in RULES:
            f = (rule >> c) & 1
            exp = cc if a != cc else (b if rule == 142 else 1 - b)
            if f != exp:
                fails.append((rule, c))
    rec("(R) form of the tables", 0, 16, fails)
    agree = [c for c in range(8) if ((43 >> c) & 1) == ((142 >> c) & 1)]
    rec("rules agree exactly on codes 1,3,4,6", 0, 1, [] if agree == [1, 3, 4, 6] else [agree])
    ones142 = [c for c in range(8) if (142 >> c) & 1]
    ones43 = [c for c in range(8) if (43 >> c) & 1]
    rec("142 ones on 001,010,011,111; 43 on 000,001,011,101", 0, 1,
        [] if (ones142 == [1, 2, 3, 7] and ones43 == [0, 1, 3, 5]) else [(ones142, ones43)])
    # rule 184 / 226 descriptions, and g226(a,b,c) = g184(c,b,a)
    f = []
    for c in range(8):
        a, b, cc = (c >> 2) & 1, (c >> 1) & 1, c & 1
        g184 = int((b, cc) == (1, 1) or (a, b) == (1, 0))
        g226 = int((a, b) == (1, 1) or (b, cc) == (0, 1))
        if g184 != (184 >> c) & 1 or g226 != (226 >> c) & 1:
            f.append(c)
        if (226 >> c) & 1 != (184 >> (4 * cc + 2 * b + a)) & 1:
            f.append(("refl", c))
    rec("descriptions of rules 184, 226; g226(a,b,c)=g184(c,b,a)", 0, 8, f)


def test_state_level(n):
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    M = mask(n)
    d = delta(n, xs)
    w = popcount(d)
    G184 = global_map(184, n, xs)        # applied to words: xs are also all words
    G226 = global_map(226, n, xs)
    # (D1): delta(x) = delta(y) iff y in {x, Cx}
    cnt = np.bincount(d, minlength=N)
    ok = np.all(cnt[d] == 2) and np.all(d == delta(n, comp(n, xs)))
    rec("D1", n, N, [] if ok else ["D1"])
    rec("D2 (w even)", n, N, xs[(w % 2) != 0][:5])
    # D3 and Lemma 6
    Pd, Qd = P_of(n, d), Q_of(n, d)
    for j in range(n):
        y = xs ^ (1 << j)
        dj = delta(n, y)
        tog = (1 << ((j - 1) % n)) | (1 << j)
        rec("D3", n, N, xs[dj != (d ^ tog)][:5])
        iso = ((Pd >> ((j - 1) % n)) & 1) == 1
        inter = ((Qd >> ((j - 1) % n)) & 1) == 1
        # definitions of isolated / interior directly from the cells
        xj = (xs >> j) & 1; xl = (xs >> ((j - 1) % n)) & 1; xr = (xs >> ((j + 1) % n)) & 1
        rec("isolated/interior via P/Q", n, N,
            xs[(iso != ((xj != xl) & (xj != xr))) | (inter != ((xj == xl) & (xj == xr)))][:5])
        exp = np.where(inter, 2, np.where(iso, -2, 0))
        rec("Lemma 6", n, N, xs[(popcount(dj) - w) != exp][:5])
    # D: isolated cell = run of length 1; interior iff run >= 3 (non-constant states); constant: all interior
    if n <= 12:
        f = []
        for x in range(N):
            Pm, Qm = int(Pd[x]), int(Qd[x])
            if x in (0, M):
                if Qm != M:
                    f.append(x)
                continue
            L, _ = runs(n, x)
            if (Pm != 0) != (1 in L) or (Qm != 0) != (max(L) >= 3):
                f.append(x)
        rec("runs: isolated = run 1, interior iff run >= 3", n, N, f)
    for rule in RULES:
        F = global_map(rule, n, xs)
        dF = delta(n, F)
        Ld = Lsh(d, n)
        if rule == 142:
            rec("Lemma 1 (142) cell formula", n, N, xs[F != (xs ^ (d & (~Ld) & M))][:5])
            rec("Lemma 1 (142) delta(Fx)=G226(delta x)", n, N, xs[dF != G226[d]][:5])
        else:
            rec("Lemma 1 (43) cell formula", n, N, xs[F != (xs ^ ((~(Ld & (~d))) & M))][:5])
            rec("Lemma 1 (43) delta(Fx)=G184(delta x)", n, N, xs[dF != G184[d]][:5])
        # Lemma 5
        rec(f"Lemma 5 FC=CF ({rule})", n, N, xs[global_map(rule, n, comp(n, xs)) != comp(n, F)][:5])
        rec(f"Lemma 5 w(Fx)=w(x) ({rule})", n, N, xs[popcount(dF) != w][:5])
    # Lemma 2
    rec("Lemma 2 |G184 d|=|d|", n, N, xs[popcount(G184) != popcount(xs)][:5])
    rec("Lemma 2 |G226 d|=|d|", n, N, xs[popcount(G226) != popcount(xs)][:5])
    # Lemma 3 on all words d = xs
    D = xs
    P, Q = P_of(n, D), Q_of(n, D)
    for name, G in (("a", G184), ("b", G226)):
        P2, Q2 = P_of(n, G), Q_of(n, G)
        if name == "a":
            eP = Rsh(P, n) & (~Lsh(Q, n)) & M
            eQ = Lsh(Q, n) & (~Rsh(P, n)) & M
            A = Q & Rsh(Rsh(P, n), n)
            shP, shQ = Rsh(P, n), Lsh(Q, n)
        else:
            eP = Lsh(P, n) & (~Rsh(Q, n)) & M
            eQ = Rsh(Q, n) & (~Lsh(P, n)) & M
            A = P & Rsh(Rsh(Q, n), n)
            shP, shQ = Lsh(P, n), Rsh(Q, n)
        rec(f"Lemma 3({name}) P equivalence", n, N, D[P2 != eP][:5])
        rec(f"Lemma 3({name}) Q equivalence", n, N, D[Q2 != eQ][:5])
        rec(f"Lemma 3({name}) counts", n, N,
            D[(popcount(P2) != popcount(P) - popcount(A)) | (popcount(Q2) != popcount(Q) - popcount(A))][:5])
        e = A == 0
        rec(f"Lemma 3({name}) translation when A empty", n, int(e.sum()),
            D[e & ((P2 != shP) | (Q2 != shQ))][:5])
    rec("Lemma 3(c)", n, N, D[(popcount(P) - popcount(Q)) != 2 * popcount(D) - n][:5])
    # Lemma 4: periodicity under G184, G226 (from the functional graph), and the action
    for rule, Pact, Qact in ((184, 1, -1), (226, -1, 1)):
        dyn = Dynamics(rule, n)
        per = dyn.periodic
        crit = (P == 0) | (Q == 0)
        rec(f"Lemma 4 periodic iff P or Q empty ({rule})", n, N, D[per != crit][:5])
        G = dyn.succ
        selP = P == 0
        rec(f"Lemma 4 action, P empty ({rule})", n, int(selP.sum()),
            D[selP & (G != sigma(n, D, Pact))][:5])
        selQ = Q == 0
        rec(f"Lemma 4 action, Q empty ({rule})", n, int(selQ.sum()),
            D[selQ & (G != sigma(n, D, Qact))][:5])


def test_cycles(n):
    """Lemma 7, 8, description of the cycles, Theorem 1, Prop. 2, Lemma 9, 10, 11, Theorem 2."""
    N = 1 << n
    xs = np.arange(N, dtype=np.int64)
    M = mask(n)
    d = delta(n, xs)
    w = popcount(d)
    P, Q = P_of(n, d), Q_of(n, d)
    noiso, nointer = P == 0, Q == 0
    info = {}
    for rule in RULES:
        dyn = Dynamics(rule, n)
        F = dyn.succ
        per = dyn.periodic
        # Lemma 7(a)
        rec(f"Lemma 7(a) ({rule})", n, N, xs[per != (noiso | nointer)][:5])
        # Lemma 7(b)
        CsX = comp(n, sigma(n, xs, 1))
        sinvX = sigma(n, xs, -1)
        if rule == 43:
            a1, a2 = CsX, sinvX
        else:
            a1, a2 = sinvX, CsX
        rec(f"Lemma 7(b) no isolated ({rule})", n, int(noiso.sum()), xs[noiso & (F != a1)][:5])
        rec(f"Lemma 7(b) no interior ({rule})", n, int(nointer.sum()), xs[nointer & (F != a2)][:5])
        for nm, prop in (("no isolated", noiso), ("no interior", nointer)):
            bad = prop & ~(prop[F] & prop[sigma(n, xs, 1)] & prop[comp(n, xs)])
            rec(f"Lemma 7(b) '{nm}' preserved by F, sigma, C ({rule})", n, int(prop.sum()), xs[bad][:5])
        # Lemma 7(c)
        cyc = dyn.cycle_of_periodic
        pu = np.flatnonzero(per)
        f = []
        for r in range(2 * n):
            s = sigma(n, pu, r)
            ok = (cyc[s] == cyc[pu]) | (cyc[s] == cyc[comp(n, pu)])
            f += [(int(u), r) for u in pu[~ok][:5]]
        rec(f"Lemma 7(c) ({rule})", n, len(pu) * 2 * n, f)
        # description: periods divide 2n; family wall bounds; families meet only in X
        lens = np.array([len(s) for s in dyn.cycle_states])
        rec(f"periods divide 2n ({rule})", n, dyn.m, [int(L) for L in lens if (2 * n) % L])
        rec(f"family 'no isolated' has w <= n/2 ({rule})", n, int(noiso.sum()), xs[noiso & (2 * w > n)][:5])
        rec(f"family 'no interior' has w >= n/2 ({rule})", n, int(nointer.sum()), xs[nointer & (2 * w < n)][:5])
        both = xs[noiso & nointer]
        x0 = int(sum(1 << i for i in range(n) if i % 4 in (2, 3))) if n % 4 == 0 else None
        Xset = sorted(int(sigma(n, np.array([x0]), r)[0]) for r in range(4)) if x0 is not None else []
        rec(f"families meet exactly in X ({rule})", n, 1, [] if sorted(both.tolist()) == Xset else [both.tolist()])
        # Lemma 8
        if n % 2 == 0:
            alt = xs[(P == 0) & (Q == 0)]
            rec(f"Lemma 8 neither 11 nor 00 in wall word => X and 4|n ({rule})", n, 1,
                [] if sorted(alt.tolist()) == Xset else [alt.tolist()])
        if n % 4 == 0:
            lvl = xs[per & (2 * w == n)]
            rec(f"Lemma 8 periodic with w=n/2 are X ({rule})", n, 1, [] if sorted(lvl.tolist()) == Xset else [lvl.tolist()])
            kX = int(cyc[x0])
            okc = sorted(dyn.cycle_states[kX].tolist()) == Xset and all(int(F[x]) == int(sigma(n, np.array([x]), -1)[0]) for x in Xset)
            rec(f"Lemma 8 X one cycle of length 4, F = sigma^-1 ({rule})", n, 1, [] if okc else ["X"])
            codesX = set()
            for x in Xset:
                for i in range(n):
                    codesX.add(4 * ((x >> ((i - 1) % n)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % n)) & 1))
            rec(f"codes on X are exactly 1,3,4,6 ({rule})", n, 1, [] if codesX == {1, 3, 4, 6} else [sorted(codesX)])
        # G1
        edges = dyn.one_flip_graph()
        comps, closed = sccs(dyn.m, edges)
        cw = np.array([int(w[s[0]]) for s in dyn.cycle_states])
        # all states of a cycle have the same wall count (Lemma 5 consequence)
        rec(f"wall count constant on cycles ({rule})", n, dyn.m,
            [k for k, s in enumerate(dyn.cycle_states) if len(set(w[s].tolist())) != 1])
        info[rule] = dict(m=dyn.m, n_edges=len(edges), closed=closed, cw=cw.tolist(),
                          n_periodic=int(per.sum()))
        if n % 4 == 0:
            kX = int(cyc[x0])
            # Theorem 1(1): every single flip of a state of X returns to X
            f = []
            for x in Xset:
                for j in range(n):
                    if int(dyn.attractor[x ^ (1 << j)]) != kX:
                        f.append((x, j))
            rec(f"Theorem 1(1) flips of X return to X ({rule})", n, 4 * n, f)
            rec(f"Theorem 1 only closed class is {{X}} ({rule})", n, 1, [] if closed == [[kX]] else [closed])
            # Theorem 1(2): G1 distance to X equals |w - n/2|/2 (reverse BFS)
            radj = [[] for _ in range(dyn.m)]
            for a, b in edges:
                radj[b].append(a)
            dist = [-1] * dyn.m; dist[kX] = 0; dq = deque([kX])
            while dq:
                v = dq.popleft()
                for u in radj[v]:
                    if dist[u] < 0:
                        dist[u] = dist[v] + 1; dq.append(u)
            f = [(k, dist[k], cw[k]) for k in range(dyn.m) if dist[k] != abs(cw[k] - n // 2) // 2]
            rec(f"Theorem 1(2) G1-distance to X = |w-n/2|/2 ({rule})", n, dyn.m, f)
            # the step used in the proof: flipping ANY interior (w<n/2) / isolated (w>n/2) cell of ANY state
            # of C gives a cycle with w +- 2
            f = []; cnt = 0
            for k, st in enumerate(dyn.cycle_states):
                if k == kX:
                    continue
                for x in st.tolist():
                    for j in range(n):
                        jm = (j - 1) % n
                        if cw[k] < n // 2 and (int(Q[x]) >> jm) & 1:
                            cnt += 1
                            if cw[int(dyn.attractor[x ^ (1 << j)])] != cw[k] + 2:
                                f.append((x, j))
                        if cw[k] > n // 2 and (int(P[x]) >> jm) & 1:
                            cnt += 1
                            if cw[int(dyn.attractor[x ^ (1 << j)])] != cw[k] - 2:
                                f.append((x, j))
                rec(f"Theorem 1(2) interior/isolated cell exists on every state ({rule})", n, len(st),
                    [x for x in st.tolist() if not ((cw[k] < n // 2 and Q[x]) or (cw[k] > n // 2 and P[x]))])
            rec(f"Theorem 1(2) proof step, every interior/isolated flip ({rule})", n, cnt, f)
            # Proposition 2: healing time
            f = []
            Xs = set(Xset)
            for x in Xset:
                for j in range(n):
                    xl, xj, xr = (x >> ((j - 1) % n)) & 1, (x >> j) & 1, (x >> ((j + 1) % n)) & 1
                    left = xl != xj and xj == xr
                    right = xl == xj and xj != xr
                    if left == right:
                        f.append(("neither/both", x, j)); continue
                    y = x ^ (1 << j); t = 0
                    while True:
                        y = int(F[y]); t += 1
                        if y in Xs:
                            break
                        if t > 4 * n:
                            break
                    if rule == 43:
                        exp = 1 if left else n // 2 - 1
                    else:
                        exp = n // 2 - 1 if left else 1
                    if t != exp:
                        f.append((x, j, t, exp))
            rec(f"Proposition 2 healing time ({rule})", n, 4 * n, f)
        if n % 4 != 0 and n >= 3:
            half = n / 2
            wm = max(v for v in range(0, n + 1, 2) if v < half)
            wp = min(v for v in range(0, n + 1, 2) if v > half)
            K = sorted(k for k in range(dyn.m) if cw[k] in (wm, wp))
            # Theorem 2 (and n = 3, which the document reports as computed only)
            rec(f"Theorem 2 unique closed class = K ({rule})", n, 1, [] if closed == [K] else [(closed, K)])
            if n >= 5:
                eps = n - 2 * wm
                rec("w- >= 2, w+ <= n-1, eps in {1,2,3}", n, 1,
                    [] if (wm >= 2 and wp <= n - 1 and eps == {1: 1, 2: 2, 3: 3}[n % 4] and wp - wm == 2) else [(wm, wp, eps)])
                # Lemma 9(a)
                lo = per & (w == wm); up = per & (w == wp)
                rec(f"Lemma 9(a) lower: interior, no isolated ({rule})", n, int(lo.sum()), xs[lo & ~((Q != 0) & (P == 0))][:5])
                rec(f"Lemma 9(a) upper: isolated, no interior ({rule})", n, int(up.sum()), xs[up & ~((P != 0) & (Q == 0))][:5])
                # Lemma 9(b): no flip of a state of K leaves K
                Kset = set(K)
                f = [(a, b) for a, b in edges if a in Kset and b not in Kset]
                rec(f"Lemma 9(b) no edge leaves K ({rule})", n, len(edges), f)
                # Lemma 9(c)
                lower = [k for k in K if cw[k] == wm]; upper = [k for k in K if cw[k] == wp]
                out = {}
                for a, b in edges:
                    out.setdefault(a, set()).add(b)
                f = [k for k in lower if not any(cw[b] == wp for b in out.get(k, ()))]
                f += [k for k in upper if not any(cw[b] == wm for b in out.get(k, ()))]
                rec(f"Lemma 9(c) edges between the levels ({rule})", n, len(K), f)
                # Lemma 9(d): every cycle reaches K
                radj = [[] for _ in range(dyn.m)]
                for a, b in edges:
                    radj[b].append(a)
                seen = set(K); dq = deque(K)
                while dq:
                    v = dq.popleft()
                    for u in radj[v]:
                        if u not in seen:
                            seen.add(u); dq.append(u)
                rec(f"Lemma 9(d) every cycle reaches K ({rule})", n, dyn.m, [k for k in range(dyn.m) if k not in seen])
                # Lemma 11: chain from z0 to sigma^2 C z0, slides, on the cycle of C z0
                bits = [0] * (eps + 2)
                tail = []
                for _ in range((wm - 2) // 2):
                    tail += [1, 1, 0, 0]
                tail += [1, 1]
                zb = bits + tail
                assert len(zb) == n
                z0 = sum(b << i for i, b in enumerate(zb))
                f = []
                if int(w[z0]) != wm or P[z0] != 0:
                    f.append("z0 walls/isolated")
                chain = [z0]
                for s in range(1, eps + 1):
                    ys = chain[-1] | (1 << (eps + 2 - s))
                    yb = [(ys >> i) & 1 for i in range(n)]
                    exp = [0] * (eps + 2 - s) + [1] * s + tail
                    if yb != exp:
                        f.append(("y_s cells", s))
                    if not per[ys] or w[ys] != wm or bin(ys ^ chain[-1]).count("1") != 1:
                        f.append(("not a slide", s))
                    L, _ = runs(n, ys)
                    chain.append(ys)
                cz0 = int(comp(n, np.array([z0]))[0])
                if chain[-1] != int(sigma(n, np.array([cz0]), 2)[0]):
                    f.append("y_eps != sigma^2 C z0")
                if cyc[chain[-1]] != cyc[cz0]:
                    f.append("y_eps not on cycle of C z0")
                # path Z -> CZ in G1 (reachability)
                adj = [[] for _ in range(dyn.m)]
                for a, b in edges:
                    adj[a].append(b)
                sZ, sCZ = int(cyc[z0]), int(cyc[cz0])
                seen = {sZ}; dq = deque([sZ])
                while dq:
                    v = dq.popleft()
                    for u in adj[v]:
                        if u not in seen:
                            seen.add(u); dq.append(u)
                if sCZ not in seen:
                    f.append("CZ not reachable from Z")
                rec(f"Lemma 11 ({rule})", n, 1, f)
                # Corollary 3 codes on K
                codes = set()
                for k in K:
                    for x in dyn.cycle_states[k].tolist():
                        for i in range(n):
                            codes.add(4 * ((x >> ((i - 1) % n)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % n)) & 1))
                rec(f"Corollary 3 all eight codes on K ({rule})", n, 1, [] if codes == set(range(8)) else [sorted(codes)])
                info[rule].update(K_size=len(K), w_minus=wm, w_plus=wp)
        # Lemma 10: every slide joins equal cycles or cycles with edges in both directions
        eset = edges
        pu = np.flatnonzero(per)
        f = []; cnt = 0
        for j in range(n):
            y2 = pu ^ (1 << j)
            sel = per[y2] & (w[y2] == w[pu])
            a = cyc[pu[sel]]; b = cyc[y2[sel]]
            cnt += int(sel.sum())
            for u, v in zip(a.tolist(), b.tolist()):
                if u != v and not ((u, v) in eset and (v, u) in eset):
                    f.append((u, v))
        rec(f"Lemma 10 slides join cycles both ways ({rule})", n, cnt, f[:5])
        # Lemma 10(a)/(b): run the slide procedures of the proof on every periodic state
        f = []; cnt_a = cnt_b = 0
        for x in pu.tolist():
            wx = int(w[x])
            if P[x] == 0 and wx >= 2:
                cnt_a += 1
                L, s = runs(n, x)
                col = (x >> s) & 1
                r = L[:]
                cur = x
                for k in range(len(r) - 1, 0, -1):
                    while r[k] >= 3:
                        pos = (s + sum(r[:k])) % n        # first cell of R_k
                        nxt = cur ^ (1 << pos)
                        if not (per[nxt] and w[nxt] == wx and P[nxt] == 0):
                            f.append(("a", x)); break
                        cur = nxt; r[k] -= 1; r[k - 1] += 1
                target = (n - 2 * wx + 2,) + (2,) * (wx - 1)
                if not any(rw == target for rw, _, _ in run_word_from(n, cur)):
                    f.append(("a-final", x))
            if Q[x] == 0 and 2 * wx > n and wx < n:
                cnt_b += 1
                L, s = runs(n, x)
                r = L[:]; cur = x
                changed = True
                while changed:
                    changed = False
                    for k in range(len(r) - 1):
                        if (r[k], r[k + 1]) == (1, 2):
                            pos = (s + sum(r[:k + 1])) % n   # first cell of R_(k+1)
                            nxt = cur ^ (1 << pos)
                            if not (per[nxt] and w[nxt] == wx and Q[nxt] == 0):
                                f.append(("b", x))
                            cur = nxt; r[k], r[k + 1] = 2, 1; changed = True
                            break
                target = (2,) * (n - wx) + (1,) * (2 * wx - n)
                if not any(rw == target for rw, _, _ in run_word_from(n, cur)):
                    f.append(("b-final", x))
        rec(f"Lemma 10(a) procedure ({rule})", n, cnt_a, f[:5] if any(t[0].startswith("a") for t in f) else [])
        rec(f"Lemma 10(b) procedure ({rule})", n, cnt_b, [t for t in f if t[0].startswith("b")][:5])
    return info


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    t0 = time.time()
    test_tables()
    infos = {}
    for n in range(3, nmax + 1):
        t1 = time.time()
        test_state_level(n)
        infos[n] = test_cycles(n)
        print(n, f"{time.time() - t1:.1f}s", flush=True)
    tot_fail = sum(e["failures"] for d in results.values() for e in d.values())
    out = {"nmax": nmax, "total_failures": tot_fail, "results": results,
           "cycle_info": {str(n): {str(r): {k: v for k, v in inf.items() if k != "cw"} for r, inf in d.items()} for n, d in infos.items()},
           "seconds": time.time() - t0}
    json.dump(out, open("out/lemma_tests.json", "w"), indent=1, default=str)
    print("statements:", len(results), "total failures:", tot_fail)
    for name, d in results.items():
        bad = {n: e for n, e in d.items() if e["failures"]}
        if bad:
            print("FAIL", name, bad)
