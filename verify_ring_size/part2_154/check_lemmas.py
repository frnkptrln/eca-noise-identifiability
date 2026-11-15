"""Exhaustive tests of the lemmas of PROOF_154.md for rule 154 on rings of n = 3..16 cells.

Written from the definitions; uses numpy only (no code of the study, no solver of the parent folder).
Conventions as in ../SAMPLE.md section 2: state x = x_0 ... x_(n-1), integer = bit string read as a binary
numeral (x_0 most significant); (F x)_i = f(x_(i-1), x_i, x_(i+1)), f(a,b,c) = bit (4a+2b+c) of the rule.

Output: out/check_lemmas.jsonl (one record per n), out/check_lemmas.txt (summary table).
Usage: python check_lemmas.py [NMAX]   (default 16; single process, about 1 CPU-second in total)
"""
import json
import os
import sys
import time
from collections import deque

import numpy as np

RULE = 154
HERE = os.path.dirname(os.path.abspath(__file__))


def bit_table(n):
    s = np.arange(1 << n, dtype=np.int64)
    return ((s[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.int64)


def to_int(X):
    n = X.shape[1]
    return (X << (n - 1 - np.arange(n))).sum(1)


def build_F(n, rule):
    X = bit_table(n)
    a = np.roll(X, 1, axis=1)    # a_i = x_(i-1)
    c = np.roll(X, -1, axis=1)   # c_i = x_(i+1)
    return to_int((rule >> (4 * a + 2 * X + c)) & 1), X


def power_map(F, T):
    """F^T' for the first power of two T' >= T, by repeated squaring."""
    P, t = F.copy(), 1
    while t < T:
        P, t = P[P], 2 * t
    return P


def check(n):
    N = 1 << n
    rec = {"n": n, "rule": RULE}
    F, X = build_F(n, RULE)
    a, b, c = np.roll(X, 1, axis=1), X, np.roll(X, -1, axis=1)
    # L1: f(a,b,c) = c + a(1+b) mod 2
    rec["L1_formula"] = bool((to_int((c + a * (1 - b)) % 2) == F).all())
    F90, _ = build_F(n, 90)
    even_sites = (np.arange(n) % 2 == 0)
    ones_even = X[:, even_sites].sum(1)
    ones_odd = X[:, ~even_sites].sum(1)
    ids = np.arange(N)
    P = power_map(F, N)                 # F^T, T >= 2^n: every image is a periodic point
    periodic = np.zeros(N, bool)
    periodic[P] = True
    rec["n_periodic"] = int(periodic.sum())
    # cycles
    cid = -np.ones(N, np.int64)
    cycles = []
    for s in np.nonzero(periodic)[0]:
        if cid[s] >= 0:
            continue
        t, members = int(s), []
        while cid[t] < 0:
            cid[t] = len(cycles)
            members.append(t)
            t = int(F[t])
        cycles.append(members)
    m = len(cycles)
    rec["n_cycles"] = m
    rec["cycle_length_hist"] = sorted(
        [int(L), int(k)] for L, k in zip(*np.unique([len(cy) for cy in cycles], return_counts=True)))
    att = cid[P]                        # cycle reached from each state
    # L5: collisions of F (any n)
    order = np.argsort(F, kind="stable")
    Fs = F[order]
    same = np.nonzero(Fs[1:] == Fs[:-1])[0]
    rec["n_collision_pairs_adjacent"] = int(len(same))
    rec["bijective"] = bool(len(same) == 0)
    if n % 2 == 1:
        rec["L5_odd_bijective"] = rec["bijective"]
    else:
        E = (ones_odd == 0)             # support in the even sites (contains 0)
        O = (ones_even == 0)
        M = ~(E | O)
        oneE = int(to_int(np.tile(even_sites.astype(np.int64), (1, 1)))[0])
        oneO = (N - 1) ^ oneE
        rec["size_M"] = int(M.sum())
        # L2: on E and O rule 154 acts as rule 90 and swaps the two sets
        rec["L2_F_eq_F90_on_E_and_O"] = bool((F[E | O] == F90[E | O]).all())
        rec["L2_F_E_in_O_and_F_O_in_E"] = bool(O[F[E]].all() and E[F[O]].all())
        # L3: nilpotency on E u O iff n is a power of two
        Q = power_map(F, n // 2) if (n & (n - 1)) == 0 else None
        if Q is not None:
            Fh = ids.copy()
            for _ in range(n // 2):
                Fh = F[Fh]
            rec["L3_F_pow_half_n_kills_E_and_O"] = bool((Fh[E | O] == 0).all())
        else:
            # orbit of a single one never reaches 0 (it is eventually periodic and the cycle is not {0})
            rec["L3_single_one_not_attracted_to_0"] = bool(att[1 << (n - 1)] != cid[0] and att[1] != cid[0])
        # L4: F(M) in M
        rec["L4_F_M_in_M"] = bool(M[F[M]].all())
        # L5: every pair x != x' with F(x) = F(x') is {x, x+1_E} in E, {x, x+1_O} in O, or {1_E, 1_O}
        ok = True
        groups = {}
        dup_vals = np.unique(Fs[same])
        isdup = np.isin(F, dup_vals)
        for s in np.nonzero(isdup)[0]:
            groups.setdefault(int(F[s]), []).append(int(s))
        npairs = 0
        for y, pre in groups.items():
            for i in range(len(pre)):
                for j in range(i + 1, len(pre)):
                    u, v = pre[i], pre[j]
                    npairs += 1
                    good = ((E[u] and E[v] and (u ^ v) == oneE) or (O[u] and O[v] and (u ^ v) == oneO)
                            or {u, v} == {oneE, oneO})
                    ok = ok and bool(good)
        rec["n_collision_pairs"] = npairs
        # expected number of pairs: 2^(n/2-1) in E, the same in O, one pair {1_E, 1_O}
        rec["L5_collisions_only_inside_E_or_O"] = ok
        rec["L5_pair_count_as_expected"] = bool(npairs == 2 * (1 << (n // 2 - 1)) + 1)
        # L6: F restricted to M is a permutation of M; every state of M is periodic
        rec["L6_F_injective_on_M"] = bool(len(np.unique(F[M])) == int(M.sum()))
        rec["L6_all_of_M_periodic"] = bool(periodic[M].all())
        rec["periodic_outside_M"] = int((periodic & ~M).sum())
        if Q is not None:
            rec["L7_periodic_eq_M_plus_0"] = bool((periodic == (M | (ids == 0))).all())
            rec["L7_count_formula"] = bool(rec["n_periodic"] == N - 2 * (1 << (n // 2)) + 2)
            Fn = ids.copy()
            for _ in range(n):
                Fn = F[Fn]
            rec["obs_F_pow_n_identity_on_M"] = bool((Fn[M] == ids[M]).all())
    # one-flip graph G1 from the definition: flip one cell of a periodic state, iterate F
    per = np.nonzero(periodic)[0]
    src, dst = [], []
    for i in range(n):
        tgt = att[per ^ (1 << i)]
        keep = tgt != cid[per]
        src.append(cid[per][keep])
        dst.append(tgt[keep])
    src, dst = np.concatenate(src), np.concatenate(dst)
    edges = set(zip(src.tolist(), dst.tolist()))
    rec["G1_edges"] = len(edges)
    out = [[] for _ in range(m)]
    inn = [[] for _ in range(m)]
    for u, v in edges:
        out[u].append(v)
        inn[v].append(u)

    def reach(start, adj):
        dist = {start: 0}
        dq = deque([start])
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    dq.append(v)
        return dist

    z = int(cid[0])
    to_zero = reach(z, inn)             # G1 distance of every cycle to the cycle {0}
    from_zero = reach(z, out)
    rec["out_degree_of_zero"] = len(out[z])
    rec["all_cycles_reach_zero"] = bool(len(to_zero) == m)
    rec["max_G1_distance_to_zero"] = int(max(to_zero.values()))
    rec["G1_strongly_connected"] = bool(len(to_zero) == m and len(from_zero) == m)
    if n % 2 == 0:
        Mc = np.zeros(m, bool)
        Mc[cid[per[M[per]]]] = True     # cycles inside M
        rec["n_cycles_in_M"] = int(Mc.sum())
        # L8a: G1 edges between cycles of M are symmetric
        rec["L8_edges_inside_M_symmetric"] = all(((v, u) in edges) for (u, v) in edges if Mc[u] and Mc[v])
        # L8b: the cycles of M are mutually reachable using only cycles of M
        one = int(cid[N - 1])
        d1 = {one: 0}
        dq = deque([one])
        while dq:
            u = dq.popleft()
            for v in out[u]:
                if Mc[v] and v not in d1:
                    d1[v] = d1[u] + 1
                    dq.append(v)
        rec["L8_M_cycles_connected_inside_M"] = bool(len(d1) == int(Mc.sum()))
        # L8c: distance bound d(C, 0) <= min over states of C of min(#ones even, #ones odd)  (n = 2^k)
        if (n & (n - 1)) == 0:
            bound = np.full(m, n, np.int64)
            np.minimum.at(bound, cid[per], np.minimum(ones_even[per], ones_odd[per]))
            d = np.array([to_zero[c] for c in range(m)])
            rec["L8_distance_le_min_parity_count"] = bool((d <= bound).all())
            rec["distance_eq_bound_for_all_cycles"] = bool((d == bound).all())
            rec["distance_hist"] = sorted([int(k), int(v)] for k, v in zip(*np.unique(d, return_counts=True)))
            rec["distance_of_all_ones"] = int(to_zero[one])
            rec["closed_classes_only_zero"] = bool(len(out[z]) == 0 and len(to_zero) == m)
            # gamma: in-tree of G1 edges rooted at {0} has weight m-1; any other root needs an edge leaving {0}
            rec["gamma_zero_equals_m_minus_1"] = bool(len(to_zero) == m)
    return rec


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    t0 = time.process_time()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    recs = []
    with open(os.path.join(HERE, "out", "check_lemmas.jsonl"), "w") as fh:
        for n in range(3, nmax + 1):
            r = check(n)
            r["cpu_seconds_cumulative"] = round(time.process_time() - t0, 2)
            fh.write(json.dumps(r, sort_keys=True) + "\n")
            fh.flush()
            recs.append(r)
    lines = []
    allok = True
    for r in recs:
        tests = {k: v for k, v in r.items() if k.startswith("L")}
        bad = [k for k, v in tests.items() if v is not True]
        allok = allok and not bad
        lines.append("n=%2d periodic=%6d cycles=%5d G1_edges=%7d out(0)=%3d all->0=%-5s maxdist=%2d strongly_conn=%-5s "
                     "lemma_tests=%2d failed=%s" % (
                         r["n"], r["n_periodic"], r["n_cycles"], r["G1_edges"], r["out_degree_of_zero"],
                         r["all_cycles_reach_zero"], r["max_G1_distance_to_zero"], r["G1_strongly_connected"],
                         len(tests), bad))
    lines.append("ALL LEMMA TESTS PASSED: %s" % allok)
    lines.append("cpu seconds: %.2f" % (time.process_time() - t0))
    txt = "\n".join(lines) + "\n"
    open(os.path.join(HERE, "out", "check_lemmas.txt"), "w").write(txt)
    sys.stdout.write(txt)
