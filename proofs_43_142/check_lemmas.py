"""Exhaustive tests of the lemmas of PROOF_43_142.md at small ring sizes (one process; writes out/check_lemmas.json).

Every test loops over ALL states (or all periodic states, all cells) of the ring sizes named in its record and counts
violations. The tests are tests: the proofs in PROOF_43_142.md do not rely on them.

Wall rules: rule 43 -> rule 184, rule 142 -> rule 226 (Lemma 1).
Bit masks: bit i of P is set iff d_i = d_(i+1) = 1, bit i of Q iff d_i = d_(i+1) = 0 (d a wall word);
bit j of iso iff cell j of x differs from both neighbours, bit j of inte iff it equals both neighbours.
"""
import json
import os
import resource
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ring  # noqa: E402

OUT = os.path.join(HERE, "out")
WALL_RULE = {43: 184, 142: 226}
N_ALL = list(range(3, 21))          # ring sizes for the tests over all states
RESULTS = []


def rec(test, statement, rule, ns, cases, unit, violations, extra=None):
    r = dict(test=test, statement=statement, rule=rule, n_min=min(ns), n_max=max(ns), n_list=list(ns), cases=int(cases),
             unit=unit, violations=int(violations))
    if extra:
        r.update(extra)
    RESULTS.append(r)
    print(f"{test:4s} rule {rule!s:>4s} n = {min(ns)}..{max(ns)}: {cases} {unit}, violations {violations}", flush=True)


def rd(x, n):   # y_i = x_(i+1)
    return (x >> np.uint32(1)) | ((x & np.uint32(1)) << np.uint32(n - 1))


def ru(x, n):   # y_i = x_(i-1)
    return ((x << np.uint32(1)) | (x >> np.uint32(n - 1))) & np.uint32((1 << n) - 1)


def bitset(v, j):
    return ((v >> np.uint32(j)) & np.uint32(1)) == 1


def levels(n):
    """Largest even w < n/2 and smallest even w > n/2."""
    lo = max(w for w in range(0, n + 1, 2) if 2 * w < n)
    hi = min(w for w in range(0, n + 2, 2) if 2 * w > n)
    return lo, hi


def main():
    t0 = time.process_time()
    Ftab = {}
    wall = {}

    # ------------------------------------------------------------------ Lemma 1: wall map and cell-change formulas
    for rule in (43, 142):
        cases = viol = 0
        for n in N_ALL:
            mask = np.uint32((1 << n) - 1)
            F = ring.build_F(rule, n)
            G = ring.build_F(WALL_RULE[rule], n)
            d = ring.delta_arr(n)
            x = np.arange(1 << n, dtype=np.uint32)
            dl = ru(d, n)                       # (dl)_i = d_(i-1)
            if rule == 142:
                change = d & ~dl & mask         # cell i changes iff d_i = 1 and d_(i-1) = 0
            else:
                change = ~(dl & ~d) & mask      # cell i changes unless d_(i-1) = 1 and d_i = 0
            viol += int((F != (x ^ change)).sum()) + int((d[F] != G[d]).sum())
            cases += 1 << n
            Ftab[(rule, n)] = F
        rec("L1", "Lemma 1: cell-change formula and delta(F x) = G(delta x)", rule, N_ALL, cases, "states", viol)

    # ------------------------------------------------------------------ Lemmas 2 and 3: wall rules 184 / 226
    for wrule in (184, 226):
        c2 = v2 = c3 = v3 = 0
        for n in N_ALL:
            mask = np.uint32((1 << n) - 1)
            G = ring.build_F(wrule, n)
            d = np.arange(1 << n, dtype=np.uint32)
            pc = ring.popcount_arr(d)
            v2 += int((pc[G] != pc).sum())
            c2 += 1 << n
            P = d & rd(d, n)
            Q = ~d & ~rd(d, n) & mask
            PG = G & rd(G, n)
            QG = ~G & ~rd(G, n) & mask
            if wrule == 184:
                predP = rd(P, n) & ~ru(Q, n) & mask      # i in P(Gd) iff i+1 in P(d) and i-1 not in Q(d)
                predQ = ru(Q, n) & ~rd(P, n) & mask      # i in Q(Gd) iff i-1 in Q(d) and i+1 not in P(d)
                Z = Q & rd(rd(P, n), n)                  # 0011 at i  (i in Q, i+2 in P)
            else:
                predP = ru(P, n) & ~rd(Q, n) & mask      # i in P(Gd) iff i-1 in P(d) and i+1 not in Q(d)
                predQ = rd(Q, n) & ~ru(P, n) & mask      # i in Q(Gd) iff i+1 in Q(d) and i-1 not in P(d)
                Z = P & rd(rd(Q, n), n)                  # 1100 at i  (i in P, i+2 in Q)
            nP, nQ, nZ = ring.popcount_arr(P), ring.popcount_arr(Q), ring.popcount_arr(Z)
            v3 += int((PG != predP).sum()) + int((QG != predQ).sum())
            v3 += int((ring.popcount_arr(PG) != nP - nZ).sum()) + int((ring.popcount_arr(QG) != nQ - nZ).sum())
            v3 += int((nP - nQ != 2 * pc - n).sum())
            c3 += 1 << n
            wall[(wrule, n)] = (P, Q, G)
        rec("L2", "Lemma 2: the wall rule conserves the number of ones", wrule, N_ALL, c2, "wall words", v2)
        rec("L3", "Lemma 3: the sets P and Q after one step; |P| and |Q| drop by the number of annihilating patterns; "
                  "|P| - |Q| = 2|d| - n", wrule, N_ALL, c3, "wall words", v3)

    # ------------------------------------------------------------------ Lemma 4: periodic wall words
    for wrule in (184, 226):
        cases = viol = nper = 0
        for n in N_ALL:
            P, Q, G = wall[(wrule, n)]
            d = np.arange(1 << n, dtype=np.uint32)
            on, _ = ring.periodic_mask(G, n)
            viol += int((on != ((P == 0) | (Q == 0))).sum())
            if wrule == 184:      # P empty: (Gd)_i = d_(i-1); Q empty: (Gd)_i = d_(i+1)
                viol += int((G[P == 0] != ru(d, n)[P == 0]).sum()) + int((G[Q == 0] != rd(d, n)[Q == 0]).sum())
            else:                 # P empty: (Gd)_i = d_(i+1); Q empty: (Gd)_i = d_(i-1)
                viol += int((G[P == 0] != rd(d, n)[P == 0]).sum()) + int((G[Q == 0] != ru(d, n)[Q == 0]).sum())
            cases += 1 << n
            nper += int(on.sum())
        rec("L4", "Lemma 4: a wall word is periodic iff it has no 11 or no 00; the wall rule is then a shift",
            wrule, N_ALL, cases, "wall words", viol, dict(periodic=nper))
    wall.clear()

    # ------------------------------------------------------------------ Lemmas 5, 6, 7: states of rules 43 / 142
    ana = {}
    for rule in (43, 142):
        c5 = v5 = c6 = v6 = c7 = v7 = nper = 0
        for n in N_ALL:
            mask = np.uint32((1 << n) - 1)
            F = Ftab[(rule, n)]
            x = np.arange(1 << n, dtype=np.uint32)
            d = ring.delta_arr(n)
            w = ring.popcount_arr(d)
            v5 += int((F[x ^ mask] != (F ^ mask)).sum()) + int((w[F] != w).sum()) + int((w % 2 != 0).sum())
            c5 += 1 << n
            iso = d & ru(d, n)                  # bit j: d_(j-1) = d_j = 1
            inte = ~d & ~ru(d, n) & mask        # bit j: d_(j-1) = d_j = 0
            for j in range(n):
                dw = w[x ^ np.uint32(1 << j)] - w
                pred = np.where(bitset(inte, j), 2, np.where(bitset(iso, j), -2, 0))
                v6 += int((dw != pred).sum())
                c6 += 1 << n
            A = ring.analyse(rule, n)
            ana[(rule, n)] = (A, w, iso, inte)
            on = A["on"]
            no_iso, no_int = iso == 0, inte == 0
            v7 += int((on != (no_iso | no_int)).sum())
            if rule == 43:    # no isolated cell: (F x)_i = 1 - x_(i-1); no interior cell: (F x)_i = x_(i+1)
                v7 += int((F[no_iso] != (ru(x, n) ^ mask)[no_iso]).sum()) + int((F[no_int] != rd(x, n)[no_int]).sum())
            else:             # no isolated cell: (F x)_i = x_(i+1); no interior cell: (F x)_i = 1 - x_(i-1)
                v7 += int((F[no_iso] != rd(x, n)[no_iso]).sum()) + int((F[no_int] != (ru(x, n) ^ mask)[no_int]).sum())
            c7 += 1 << n
            nper += int(on.sum())
        rec("L5", "Lemma 5: F commutes with the complement and conserves the wall count; the wall count is even",
            rule, N_ALL, c5, "states", v5)
        rec("L6", "Lemma 6: a flip changes the wall count by +2 (interior cell), -2 (isolated cell), 0 (otherwise)",
            rule, N_ALL, c6, "(state, cell) pairs", v6)
        rec("L7", "Lemma 7: a state is periodic iff it has no isolated cell or no interior cell; F is then a shift "
                  "or a shift followed by the complement", rule, N_ALL, c7, "states", v7, dict(periodic=nper))

    # ------------------------------------------------------------------ Lemma 7(c): rotations of periodic states
    for rule in (43, 142):
        cases = viol = 0
        for n in N_ALL:
            A, w, iso, inte = ana[(rule, n)]
            mask = (1 << n) - 1
            st = np.flatnonzero(A["on"])
            c_u, c_cu = A["cid"][st], A["cid"][st ^ mask]
            v = st.copy()
            for r in range(1, n):
                v = ((v << 1) | (v >> (n - 1))) & mask           # sigma^r u
                cv = A["cid"][v]
                viol += int(((cv != c_u) & (cv != c_cu)).sum())
                cases += len(st)
        rec("L7c", "Lemma 7(c): for a periodic state u and every r, sigma^r u lies on the cycle of u or on the cycle of "
                   "the complement of u", rule, N_ALL, cases, "(periodic state, r) pairs", viol)

    # ------------------------------------------------------------------ Lemma 8: the level n/2
    for rule in (43, 142):
        ns = [n for n in N_ALL if n % 4 == 0]
        cases = viol = 0
        for n in N_ALL:                          # last sentence of Lemma 8: wall word without 11 and without 00
            A, w, iso, inte = ana[(rule, n)]
            both = np.flatnonzero((iso == 0) & (inte == 0)).tolist()
            if n % 4 == 0:
                x0 = ring.from_string("0011" * (n // 4))
                viol += int(sorted(both) != sorted(ring.rot_up(x0, n, k) for k in range(4)))
            else:
                viol += len(both)
            cases += len(both)
        rec("L8b", "Lemma 8, last sentence: a state whose wall word has neither 11 nor 00 exists only for 4 | n and is "
                   "then one of the four rotations of (0011)^(n/4)", rule, N_ALL, cases, "such states", viol)
        cases = viol = 0
        for n in ns:
            A, w, iso, inte = ana[(rule, n)]
            x0 = ring.from_string("0011" * (n // 4))
            X = sorted(ring.rot_up(x0, n, k) for k in range(4))
            st = np.flatnonzero(A["on"] & (w == n // 2)).tolist()
            viol += int(sorted(st) != X)
            viol += int(len({int(A["cid"][s]) for s in X}) != 1)
            viol += int(len(A["cycles"][int(A["cid"][x0])]) != 4)
            viol += int(any(ring.step(rule, s, n) != ring.rot_down(s, n) for s in X))
            cases += len(st)
        rec("L8", "Lemma 8: for 4 | n the periodic states with n/2 walls are the four rotations of (0011)^(n/4); they "
                  "form one cycle of length 4 on which F is the left shift", rule, ns, cases,
            "periodic states with n/2 walls", viol)

    # ------------------------------------------------------------------ step of Theorem 1(2)
    for rule in (43, 142):
        cases = viol = npst = 0
        for n in N_ALL:
            A, w, iso, inte = ana[(rule, n)]
            st = np.flatnonzero(A["on"])
            ws = w[st]
            wcyc = np.array([w[c[0]] for c in A["cycles"]])
            low, high = st[2 * ws < n], st[2 * ws > n]
            viol += int((inte[low] == 0).sum())          # a periodic state below n/2 has an interior cell
            viol += int((iso[high] == 0).sum())          # a periodic state above n/2 has an isolated cell
            npst += len(low) + len(high)
            for j in range(n):
                a = low[bitset(inte[low], j)]
                viol += int((wcyc[A["label"][a ^ (1 << j)]] != w[a] + 2).sum())
                b = high[bitset(iso[high], j)]
                viol += int((wcyc[A["label"][b ^ (1 << j)]] != w[b] - 2).sum())
                cases += len(a) + len(b)
        rec("T2s", "step of Theorem 1(2): a periodic state with w < n/2 has an interior cell and every flip of an "
                   "interior cell ends on a cycle with w + 2 walls; with w > n/2: isolated cell, w - 2", rule, N_ALL,
            cases, "(periodic state, admissible cell) pairs", viol, dict(periodic_states_off_n_half=npst))

    # ------------------------------------------------------------------ Theorem 1(1), Proposition 2, codes
    ns_t1 = list(range(4, 401, 4))
    for rule in (43, 142):
        cases = viol = 0
        times = {}
        for n in ns_t1:
            x0 = ring.from_string("0011" * (n // 4))
            X = [ring.rot_up(x0, n, k) for k in range(4)]
            Xs = set(X)
            tset = set()
            for x in X:
                viol += int(ring.codes_of(x, n) != {1, 3, 4, 6})
                got = set()
                for j in range(n):
                    y = x ^ (1 << j)
                    got |= ring.codes_of(y, n)
                    viol += int(ring.wall_count(y, n) != n // 2)
                    # left cell of its pair <=> x_(j-1) != x_j. Proposition 2: rule 43 heals a flipped left cell in
                    # one step and a right cell in n/2 - 1 steps; rule 142 the other way round.
                    left = ((x >> ((j - 1) % n)) & 1) != ((x >> j) & 1)
                    slow = (not left) if rule == 43 else left
                    pred = max(1, n // 2 - 1) if slow else 1
                    t = 0
                    while y not in Xs and t <= n:
                        y = ring.step(rule, y, n)
                        t += 1
                    viol += int(t != pred)
                    tset.add(t)
                    cases += 1
                viol += int(not {0, 2, 5, 7} <= got)
            times[n] = sorted(tset)
        rec("T1", "Theorem 1(1) and Proposition 2: every flip of every state of X keeps n/2 walls and is back on X "
                  "after exactly 1 or n/2 - 1 steps; X has the codes 1, 3, 4, 6; its one-flip neighbours have 0, 2, 5, 7",
            rule, ns_t1, cases, "flips", viol,
            dict(max_return_time={str(n): max(v) for n, v in times.items()},
                 return_times_ok=all(v == sorted({1, max(1, n // 2 - 1)}) for n, v in times.items())))

    # ------------------------------------------------------------------ Proposition 3: entry cost by exhaustive search
    ns_e = [4, 8, 12, 16, 20]
    for rule in (43, 142):
        cases = viol = 0
        emax = {}
        for n in ns_e:
            A, w, _, _ = ana[(rule, n)]
            F = A["F"].astype(np.int64)
            x0 = ring.from_string("0011" * (n // 4))
            kX = int(A["cid"][x0])
            dist = np.where(A["label"] == kX, 0, 10 ** 6).astype(np.int64)
            x = np.arange(1 << n, dtype=np.int64)
            while True:
                new = dist.copy()
                for j in range(n):                       # one flip costs 1
                    np.minimum(new, dist[x ^ (1 << j)] + 1, out=new)
                H = F.copy()                             # steps of F are free: minimum along the forward orbit
                for _ in range(n + 2):
                    np.minimum(new, new[H], out=new)
                    H = H[H]
                if (new == dist).all():
                    break
                dist = new
            for c in A["cycles"]:
                V = int(dist[c].min())
                viol += int(V != abs(int(w[c[0]]) - n // 2) // 2) + int(int(dist[c].max()) != V)
                cases += 1
            emax[str(n)] = int(max(int(dist[c].min()) for c in A["cycles"]))
        rec("E", "Proposition 3: the least total resistance from a cycle C to X equals |w(C) - n/2| / 2 (shortest paths "
                 "over all states: a step of F costs 0, a flip costs 1)", rule, ns_e, cases, "cycles", viol,
            dict(max_entry_cost=emax))

    # ------------------------------------------------------------------ lemmas of Theorem 2 (4 does not divide n)
    ns_c = [n for n in N_ALL if n % 4 != 0 and n >= 5]
    for rule in (43, 142):
        c9 = v9 = c10 = v10 = 0
        comp_hist = {"lower": {}, "upper": {}}
        for n in ns_c:
            A, w, iso, inte = ana[(rule, n)]
            lo, hi = levels(n)
            st = np.flatnonzero(A["on"])
            wcyc = np.array([w[c[0]] for c in A["cycles"]])
            for lev, sign, name in ((lo, +1, "lower"), (hi, -1, "upper")):
                s = st[w[st] == lev]
                for j in range(n):
                    tgt = wcyc[A["label"][s ^ (1 << j)]]
                    v9 += int((~((tgt == lev) | (tgt == lev + 2 * sign))).sum())
                    c9 += len(s)
                sset = {int(v): k for k, v in enumerate(s.tolist())}
                parent = list(range(len(s)))

                def find(a):
                    while parent[a] != a:
                        parent[a] = parent[parent[a]]
                        a = parent[a]
                    return a
                for v, k in sset.items():
                    for j in range(n):
                        u = v ^ (1 << j)
                        if u in sset:                    # a slide: both states periodic, same level, one cell apart
                            c10 += 1
                            parent[find(k)] = find(sset[u])
                    parent[find(k)] = find(sset[int(A["F"][v])])      # states of one cycle
                comps = len({find(k) for k in range(len(s))})
                dm = {}
                for v, k in sset.items():
                    dm.setdefault(int(ring.delta(v, n)), []).append(k)
                for ks in dm.values():                   # identify x with its complement (same wall word)
                    for k in ks[1:]:
                        parent[find(k)] = find(ks[0])
                v10 += int(len({find(k) for k in range(len(s))}) != 1)
                comp_hist[name][str(n)] = comps
        rec("L9", "Lemma 9(b): from a periodic state on the lower (upper) level a flip leads to a cycle on the same level "
                  "or on the upper (lower) level", rule, ns_c, c9, "(periodic state, cell) pairs", v9)
        rec("L10", "consequence of Lemma 10 used in Theorem 2: the cycles of one level are connected by slides (single "
                   "flips between periodic states of the level) once x is identified with its complement", rule, ns_c, c10, "ordered slide pairs",
            v10, dict(components_before_identifying_complements=comp_hist))

    # Lemma 9 (a), (c), (d)
    for rule in (43, 142):
        cases = viol = 0
        for n in ns_c:
            A, w, iso, inte = ana[(rule, n)]
            lo, hi = levels(n)
            st = np.flatnonzero(A["on"])
            m = len(A["cycles"])
            wcyc = np.array([w[c[0]] for c in A["cycles"]])
            slo, shi = st[w[st] == lo], st[w[st] == hi]
            viol += int(((inte[slo] == 0) | (iso[slo] != 0)).sum()) + int(((iso[shi] == 0) | (inte[shi] != 0)).sum())   # (a)
            cases += len(slo) + len(shi)
            for s, other in ((slo, hi), (shi, lo)):                                                                       # (c)
                has = np.zeros(m, bool)
                for j in range(n):
                    has[A["cid"][s[wcyc[A["label"][s ^ (1 << j)]] == other]]] = True
                lev_cycles = np.unique(A["cid"][s])
                viol += int((~has[lev_cycles]).sum())
                cases += len(lev_cycles)
            E = ring.g1_edges(A)                                                                                           # (d)
            reach = ring.reaches(m, E, np.flatnonzero((wcyc == lo) | (wcyc == hi)).tolist())
            viol += int((~reach).sum())
            cases += m
        rec("L9b", "Lemma 9 (a), (c), (d): states of the lower (upper) level have an interior (isolated) cell and no "
                   "isolated (interior) cell; every cycle of a level has a G1 edge to the other level; every cycle has a "
                   "G1 path into the two levels", rule, ns_c, cases, "periodic states of the levels, cycles of the "
                   "levels and cycles", viol)

    # Lemma 10, first statement: every slide, all n
    for rule in (43, 142):
        cases = viol = 0
        for n in N_ALL:
            A, w, iso, inte = ana[(rule, n)]
            st = np.flatnonzero(A["on"])
            m = len(A["cycles"])
            E = ring.g1_edges(A)
            keys = E[:, 0] * m + E[:, 1] if len(E) else np.zeros(0, np.int64)
            for j in range(n):
                u = st ^ (1 << j)
                sl = A["on"][u] & (w[u] == w[st])
                a, b = A["cid"][st[sl]], A["cid"][u[sl]]
                viol += int((A["label"][u[sl]] != b).sum())
                viol += int((~((a == b) | (np.isin(a * m + b, keys) & np.isin(b * m + a, keys)))).sum())
                cases += int(sl.sum())
        rec("L10s", "Lemma 10, first statement: if a flip leads from a periodic state to a periodic state with the same "
                    "wall count, their cycles are equal or joined by G1 edges in both directions", rule, N_ALL, cases,
            "slides", viol)

    # Lemma 10 (a), (b): the two procedures, every admissible state and every cut of the ring at a run boundary
    def runs_of(x, n):
        s0 = next(i for i in range(n) if ((x >> ((i - 1) % n)) & 1) != ((x >> i) & 1))
        out, i = [], s0
        while True:
            L = 1
            while ((x >> ((i + L) % n)) & 1) == ((x >> (i % n)) & 1):
                L += 1
            out.append((i % n, L))
            i += L
            if i % n == s0:
                return out

    ns_p = list(range(3, 17))
    for rule in (43, 142):
        ca = va = cb = vb = 0
        for n in ns_p:
            A, w, iso, inte = ana[(rule, n)]
            on = A["on"]
            for x in np.flatnonzero(on & (iso == 0) & (w >= 2)).tolist():            # (a)
                rr = runs_of(x, n)
                wx = len(rr)
                for cut in range(wx):
                    starts = [rr[(cut + k) % wx][0] for k in range(wx)]
                    lens = [rr[(cut + k) % wx][1] for k in range(wx)]
                    y = x
                    for k in range(wx - 1, 0, -1):
                        while lens[k] > 2:
                            y ^= 1 << starts[k]
                            starts[k] = (starts[k] + 1) % n
                            lens[k] -= 1
                            lens[k - 1] += 1
                            va += int(not (on[y] and iso[y] == 0 and w[y] == wx))
                    va += int(lens != [n - 2 * wx + 2] + [2] * (wx - 1))
                    ca += 1
            for x in np.flatnonzero(on & (inte == 0) & (2 * w > n) & (w < n)).tolist():   # (b)
                rr = runs_of(x, n)
                wx = len(rr)
                for cut in range(wx):
                    for pick in (0, -1):                                              # first or last admissible pair
                        starts = [rr[(cut + k) % wx][0] for k in range(wx)]
                        lens = [rr[(cut + k) % wx][1] for k in range(wx)]
                        y = x
                        inv = sum(1 for a in range(wx) for b in range(a + 1, wx) if (lens[a], lens[b]) == (1, 2))
                        while True:
                            ks = [k for k in range(wx - 1) if lens[k] == 1 and lens[k + 1] == 2]
                            if not ks:
                                break
                            k = ks[pick]
                            y ^= 1 << starts[k + 1]
                            starts[k + 1] = (starts[k + 1] + 1) % n
                            lens[k], lens[k + 1] = 2, 1
                            inv -= 1
                            vb += int(not (on[y] and inte[y] == 0 and w[y] == wx))
                        vb += int(lens != [2] * (n - wx) + [1] * (2 * wx - n)) + int(inv != 0)
                        cb += 1
        rec("L10a", "Lemma 10(a): the procedure, from every state without isolated cell and with w >= 2 walls, for "
                    "every cut: every step is a slide and the final run lengths are (n - 2w + 2, 2, ..., 2)", rule, ns_p,
            ca, "(state, cut) pairs", va)
        rec("L10b", "Lemma 10(b): the procedure, from every state without interior cell and with n/2 < w < n walls, for "
                    "every cut and two choices of the pair: every step is a slide and lowers the number of inversions "
                    "by one; the final run lengths are (2, ..., 2, 1, ..., 1)", rule, ns_p, cb,
            "(state, cut, choice) triples", vb)

    ns_z = [n for n in range(5, 402) if n % 4 != 0]
    for rule in (43, 142):
        cases = viol = 0
        for n in ns_z:
            lo, hi = levels(n)
            e = n - 2 * lo
            x0 = ring.from_string("0" * (e + 2) + "1100" * ((lo - 2) // 2) + "11")
            viol += int(x0.bit_length() > n or ring.wall_count(x0, n) != lo or e not in (1, 2, 3))
            y = x0
            for cell in range(e + 1, 1, -1):
                y ^= 1 << cell
                d = ring.delta(y, n)
                viol += int(ring.count_pattern(d, n, "11") != 0 or ring.popcount(d) != lo)
                cases += 1
            cx = ring.comp(x0, n)
            target = ring.rot_up(cx, n, 2)
            viol += int(y != target)
            if rule == 43:      # on this level F^2 moves the pattern two cells to the right: F^2(C x0) = target
                viol += int(ring.step(rule, ring.step(rule, cx, n), n) != target)
            else:               # on this level F^2 moves the pattern two cells to the left: F^2(target) = C x0
                viol += int(ring.step(rule, ring.step(rule, target, n), n) != cx)
            viol += int(not {0, 1, 3, 4, 6} <= ring.codes_of(x0, n)) + int(7 not in ring.codes_of(cx, n))
        rec("L11", "Lemma 11: eps flips lead from z0 = 0^(eps+2) (1100)^((w-2)/2) 11 through periodic states of the "
                   "lower level to a state on the cycle of the complement of z0; z0 has the codes 0, 1, 3, 4, 6, its "
                   "complement the code 7", rule, ns_z, cases, "flips", viol)

    ok = all(r["violations"] == 0 for r in RESULTS) and all(r.get("return_times_ok", True) for r in RESULTS)
    cpu = time.process_time() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak / 1e6 if sys.platform == "darwin" else peak / 1e3
    out = dict(script="check_lemmas.py", all_passed=bool(ok), cpu_seconds=round(cpu, 2), peak_mb=round(peak_mb),
               results=RESULTS)
    with open(os.path.join(OUT, "check_lemmas.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"all passed: {ok}; CPU {cpu:.2f} s; peak {peak_mb:.0f} MB")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
