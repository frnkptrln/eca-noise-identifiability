"""Validation of the solver against brute force that uses only the definitions.

Part A (all 256 rules, n = 3..8):
  * F table, code sets and cycles from a string-level implementation of the definitions;
  * R(u -> v) by Dijkstra on the dense graph with weights H(F(x), y); from it R(C -> x), V(C, C'),
    R(C -> D_c); compared with the fast 0-1 search (with and without the rotation shortcut);
  * gamma by a second method: one Chu-Liu/Edmonds minimum in-tree per root (pure Python, on the
    Dijkstra V), plus exhaustive enumeration of all in-trees when there are at most 7 cycles;
    compared with the all-roots contraction in core.c;
  * selected set, k_c, G1 edge set (V == 1) and closed classes (boolean transitive closure) and the
    geometry of the selected orbits, all recomputed from the reference quantities.
Part B (n = 3..6): stationary law of the noisy chain in exact rational arithmetic (GTH elimination
  with fractions) at eps = 1e-8, 1e-16, 1e-24; order of pi(x) from consecutive eps pairs compared with
  min_C [gamma(C) + R(C -> x)] - min gamma.
Writes logs/validation_A.jsonl, logs/validation_B.jsonl, logs/validation_summary.json.
"""
import itertools
import json
import math
import os
import random
import sys
import time
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eca_core as K
from solve import solve_case, bits

LOGS = os.path.join(HERE, "logs")
SAMPLE_RULES = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]


# ---------------------------------------------------------------- reference, string level
def F_ref_table(rule, n):
    tab, codes = [], []
    for X in range(1 << n):
        x = [int(ch) for ch in format(X, "0%db" % n)]          # x_0 ... x_{n-1}
        nb = [4 * x[(i - 1) % n] + 2 * x[i] + x[(i + 1) % n] for i in range(n)]
        y = [(rule >> c) & 1 for c in nb]
        tab.append(int("".join(map(str, y)), 2))
        codes.append(frozenset(nb))
    return tab, codes


def cycles_ref(Ft):
    N = len(Ft)
    seen, cycles = set(), []
    for x in range(N):
        y = x
        for _ in range(N):
            y = Ft[y]
        if y in seen:
            continue
        c = [y]
        z = Ft[y]
        while z != y:
            c.append(z)
            z = Ft[z]
        seen.update(c)
        cycles.append(c)
    cycles.sort(key=min)
    return cycles


def dense_dijkstra(Ft, n):
    """All-pairs R(u -> v): array Dijkstra from every source on weights H(F(x), y)."""
    N = 1 << n
    pc = np.array([bin(i).count("1") for i in range(N)], np.int64)
    Fa = np.array(Ft, np.int64)
    W = pc[Fa[:, None] ^ np.arange(N)[None, :]]
    BIG = 10 ** 6
    D = np.full((N, N), BIG, np.int64)
    ar = np.arange(N)
    D[ar, ar] = 0
    done = np.zeros((N, N), bool)
    for _ in range(N):
        pick = np.where(done, 2 * BIG, D).argmin(axis=1)
        done[ar, pick] = True
        D = np.minimum(D, D[ar, pick][:, None] + W[pick])
    return D


def min_intree_edmonds(W, root):
    """Chu-Liu/Edmonds, one root, recursive.  W[i][j] = weight of arc i -> j."""
    m = len(W)
    if m == 1:
        return 0
    Wd = W.astype(np.int64).copy()
    Wd[np.arange(m), np.arange(m)] = 10 ** 9
    pick = Wd.argmin(axis=1)
    pw = Wd[np.arange(m), pick]
    state = [0] * m
    state[root] = 2
    cyc = None
    for s in range(m):
        if state[s]:
            continue
        path = []
        v = s
        while state[v] == 0:
            state[v] = 1
            path.append(v)
            v = int(pick[v])
        if state[v] == 1:
            cyc = path[path.index(v):]
        for u in path:
            state[u] = 2
        if cyc:
            break
    if cyc is None:
        return int(pw.sum() - pw[root])
    incyc = set(cyc)
    others = [v for v in range(m) if v not in incyc]
    k = len(others)
    W2 = np.zeros((k + 1, k + 1), np.int64)
    W2[:k, :k] = W[np.ix_(others, others)]
    W2[:k, k] = W[np.ix_(others, cyc)].min(axis=1)
    W2[k, :k] = (W[np.ix_(cyc, others)] - pw[cyc][:, None]).min(axis=0)
    return int(pw[cyc].sum()) + min_intree_edmonds(W2, others.index(root))


def min_intree_exhaustive(W, root):
    m = len(W)
    nonroot = [v for v in range(m) if v != root]
    best = None
    for choice in itertools.product(*[[j for j in range(m) if j != v] for v in nonroot]):
        out = dict(zip(nonroot, choice))
        ok = True
        for v in nonroot:
            u, steps = v, 0
            while u != root and steps <= m:
                u = out[u]
                steps += 1
            if u != root:
                ok = False
                break
        if ok:
            w = sum(int(W[v][out[v]]) for v in nonroot)
            if best is None or w < best:
                best = w
    return best


def closed_classes_ref(A):
    """A: boolean adjacency (m x m).  Returns list of frozensets (closed strongly connected classes)."""
    m = len(A)
    R = A.copy() | np.eye(m, dtype=bool)
    for k in range(m):
        R |= R[:, k][:, None] & R[k][None, :]
    out = set()
    for c in range(m):
        if all(R[d, c] for d in range(m) if R[c, d]):
            out.add(frozenset(int(d) for d in range(m) if R[c, d]))
    return out


def rot_right(s):
    return s[-1] + s[:-1]


def geometry_ref(rule, n, rep, Ft):
    x = int(rep, 2)
    cyc = [x]
    y = Ft[x]
    while y != x:
        cyc.append(y)
        y = Ft[y]
    allrot = set()
    for z in cyc:
        s = format(z, "0%db" % n)
        for _ in range(n):
            allrot.add(s)
            s = rot_right(s)
    is_min = rep == min(allrot)
    sp, s = 1, rot_right(rep)
    while s != rep:
        s = rot_right(s)
        sp += 1
    rots = [rep]
    for _ in range(n - 1):
        rots.append(rot_right(rots[-1]))
    t, y = 1, Ft[x]
    while format(y, "0%db" % n) not in rots:
        y = Ft[y]
        t += 1
    r = rots.index(format(y, "0%db" % n))
    return is_min, len(cyc), sp, t, r


# ---------------------------------------------------------------- part A
def validate_A(rule, n, rng):
    res = {"rule": rule, "n": n}
    Ft, codes = F_ref_table(rule, n)
    F, cm = K.build_F(rule, n)
    res["F_table_ok"] = bool((F == np.array(Ft, np.uint32)).all())
    res["codes_ok"] = all(set(c for c in range(8) if (int(cm[x]) >> c) & 1) == set(codes[x]) for x in range(1 << n))
    cycles = cycles_ref(Ft)
    m = len(cycles)
    res["m"] = m
    rec, A = solve_case(rule, n, return_arrays=True)
    rec2, A2 = solve_case(rule, n, use_rot=False, return_arrays=True)
    res["cycles_ok"] = (m == rec["n_cycles"]) and sorted(min(c) for c in cycles) == sorted(int(v) for v in A["minstate"]) \
        and all(len(c) == int(A["length"][int(A["cyc"][min(c)])]) for c in cycles) \
        and all(int(A["cyc"][z]) == int(A["cyc"][min(c)]) for c in cycles for z in c) \
        and int((A["cyc"] >= 0).sum()) == sum(len(c) for c in cycles)
    # map reference cycle index -> solver cycle id
    cid = [int(A["cyc"][min(c)]) for c in cycles]
    D = dense_dijkstra(Ft, n)
    RC = np.stack([D[c].min(axis=0) for c in cycles])                 # R(C -> x)
    ok = True
    for j, c in enumerate(cycles):
        d = K.bfs_from_cycle(n, F, min(c))
        ok &= bool((d.astype(np.int64) == RC[j]).all())
    res["R_cycle_to_state_ok"] = ok
    Vref = np.stack([[RC[j][c2].min() for c2 in cycles] for j in range(m)]).astype(np.int64)
    Vsolver = A["V"][np.ix_(cid, cid)].astype(np.int64)
    res["V_ok"] = bool((Vsolver == Vref).all())
    res["V_norot_ok"] = bool((A2["V"][np.ix_(cid, cid)].astype(np.int64) == Vref).all())
    res["max_V"] = int(Vref.max())
    # gamma: second and third method
    if m <= 64:
        roots = list(range(m))
    else:
        roots = sorted(rng.sample(range(m), 16))
    g_ed = {r: min_intree_edmonds(Vref, r) for r in roots}
    g_sol = {r: int(A["gamma"][cid[r]]) for r in roots}
    res["gamma_roots_checked"] = len(roots)
    res["gamma_edmonds_per_root_ok"] = g_ed == g_sol
    if m <= 7:
        g_ex = {r: min_intree_exhaustive(Vref, r) for r in roots}
        res["gamma_exhaustive_ok"] = (g_ex == g_sol) if m > 1 else (g_sol == {0: 0})
    res["gamma_norot_equal"] = bool((A["gamma"] == A2["gamma"]).all())
    if len(roots) == m:
        gam = np.array([g_ed[r] for r in range(m)])
        gmin = int(gam.min())
        res["min_gamma_ok"] = gmin == rec["min_gamma"]
        sel_ref = sorted(min(cycles[r]) for r in range(m) if gam[r] == gmin)
        res["selected_ok"] = sel_ref == sorted(int(v) for v in A["minstate"][A["sel"]])
        kref = []
        for c in range(8):
            Dc = [x for x in range(1 << n) if c in codes[x]]
            kref.append(int(min(gam[r] + (RC[r][Dc].min() if Dc else 10 ** 6) for r in range(m)) - gmin))
        res["k_ok"] = kref == rec["k"]
        joint = set()
        for r in range(m):
            if gam[r] == gmin:
                for z in cycles[r]:
                    joint |= codes[z]
        res["codes_joint_ok"] = sorted(joint) == rec["codes_joint"]
        res["kstar0_iff_all_codes"] = (max(kref) == 0) == (len(joint) == 8)
        # G1 and closed classes from the definition V == 1
        Aref = (Vref == 1)
        np.fill_diagonal(Aref, False)
        e_ref = {(min(cycles[i]), min(cycles[j])) for i in range(m) for j in range(m) if Aref[i, j]}
        e_sol = {(int(A["minstate"][a]), int(A["minstate"][b])) for a, b in zip(A["src"], A["dst"])}
        res["G1_edges_ok"] = e_ref == e_sol
        cl_ref = {frozenset(min(cycles[i]) for i in cls) for cls in closed_classes_ref(Aref)}
        lab, inc = A["lab"], A["in_closed"]
        cl_sol = {}
        for c in range(m):
            if inc[c]:
                cl_sol.setdefault(int(lab[c]), set()).add(int(A["minstate"][c]))
        cl_sol = {frozenset(s) for s in cl_sol.values()}
        res["closed_classes_ok"] = cl_ref == cl_sol
        sel_set = set(sel_ref)
        union_closed = set().union(*cl_ref) if cl_ref else set()
        res["sel_eq_union_ok"] = (sel_set == union_closed) == rec["g1"]["selected_equals_union_closed"]
        some = all((cls <= sel_set) or not (cls & sel_set) for cls in cl_ref) and sel_set <= union_closed
        res["sel_union_some_ok"] = some == rec["g1"]["selected_is_union_of_some_closed"]
        # cannot reach the selected set
        Rm = Aref | np.eye(m, dtype=bool)
        for k in range(m):
            Rm |= Rm[:, k][:, None] & Rm[k][None, :]
        sel_idx = [r for r in range(m) if gam[r] == gmin]
        cannot = sum(1 for r in range(m) if not Rm[r, sel_idx].any())
        res["cannot_reach_ok"] = cannot == rec["g1"]["n_cannot_reach_selected"]
        res["selected_equals_union_closed"] = rec["g1"]["selected_equals_union_closed"]
    # geometry of the listed selected orbits
    gok = True
    for o in rec["selected"]["orbits"]:
        is_min, T, sp, t, r = geometry_ref(rule, n, o["rep"], Ft)
        gok &= is_min and T == o["temporal_period"] and sp == o["spatial_period"] and t == o["t_rot"] and r == o["rot"]
        gok &= sorted(set().union(*[codes[z] for z in _cycle(Ft, int(o["rep"], 2))])) == o["codes"]
    res["geometry_ok"] = bool(gok)
    res["solver_checks_all_true"] = rec["checks_all_true"] and rec2["checks_all_true"]
    res["bijective"] = rec["bijective"]
    return res


def _cycle(Ft, x):
    c = [x]
    y = Ft[x]
    while y != x:
        c.append(y)
        y = Ft[y]
    return c


# ---------------------------------------------------------------- part B
def stationary_exact(Ft, n, q):
    """Exact stationary law for eps = 1/q by GTH state reduction (subtraction-free), fractions."""
    N = 1 << n
    pc = [bin(i).count("1") for i in range(N)]
    eps = Fraction(1, q)
    pw = [eps ** r * (1 - eps) ** (n - r) for r in range(n + 1)]
    P = [[pw[pc[Ft[x] ^ y]] for y in range(N)] for x in range(N)]
    for k in range(N - 1, 0, -1):
        s = sum(P[k][j] for j in range(k))
        for i in range(k):
            P[i][k] = P[i][k] / s
        for i in range(k):
            pik = P[i][k]
            row_i, row_k = P[i], P[k]
            for j in range(k):
                row_i[j] += pik * row_k[j]
    pi = [Fraction(1)] + [Fraction(0)] * (N - 1)
    for k in range(1, N):
        pi[k] = sum(pi[i] * P[i][k] for i in range(k))
    tot = sum(pi)
    return [p / tot for p in pi]


def flog(fr):
    return math.log(fr.numerator) - math.log(fr.denominator)


def validate_B(rule, n, qs=(10 ** 8, 10 ** 16, 10 ** 24)):
    res = {"rule": rule, "n": n, "eps": ["1e-8", "1e-16", "1e-24"]}
    Ft, _ = F_ref_table(rule, n)
    rec, A = solve_case(rule, n, return_arrays=True)
    N, m = 1 << n, rec["n_cycles"]
    R = np.stack([K.bfs_from_cycle(n, A["F"], A["minstate"][c]).astype(np.int64) for c in range(m)])
    pred = (A["gamma"][:, None] + R).min(axis=0) - int(A["gamma"].min())
    pis = [stationary_exact(Ft, n, q) for q in qs]
    res["pi_is_stationary"] = True
    # exact check of pi P = pi at the first eps
    q = qs[0]
    eps = Fraction(1, q)
    pc = [bin(i).count("1") for i in range(N)]
    pw = [eps ** r * (1 - eps) ** (n - r) for r in range(n + 1)]
    for y in range(0, N, max(1, N // 8)):
        if sum(pis[0][x] * pw[pc[Ft[x] ^ y]] for x in range(N)) != pis[0][y]:
            res["pi_is_stationary"] = False
    worst = 0.0
    okall = True
    for a in range(len(qs) - 1):
        dl = math.log(qs[a]) - math.log(qs[a + 1])     # log(eps_{a+1}) - log(eps_a)
        for x in range(N):
            est = (flog(pis[a + 1][x]) - flog(pis[a][x])) / dl
            worst = max(worst, abs(est - pred[x]))
            okall &= abs(est - pred[x]) < 1e-3
    res["order_ok"] = bool(okall)
    res["max_abs_dev"] = float(worst)
    res["max_order"] = int(pred.max())
    res["m"] = m
    return res


# ---------------------------------------------------------------- part C
def validate_C(rule, n, rng):
    """Rotation shortcut versus one search per cycle, and sampled per-root Edmonds, at n = 9..12."""
    rec, A = solve_case(rule, n, return_arrays=True)
    rec2, A2 = solve_case(rule, n, use_rot=False, return_arrays=True)
    m = rec["n_cycles"]
    res = {"rule": rule, "n": n, "m": m, "bijective": rec["bijective"]}
    res["V_rot_vs_norot_ok"] = bool((A["V"] == A2["V"]).all())
    res["kd_rot_vs_norot_ok"] = bool((A["kd"] == A2["kd"]).all())
    res["gamma_rot_vs_norot_ok"] = bool((A["gamma"] == A2["gamma"]).all())
    strip = lambda r: {k: v for k, v in r.items() if k not in ("cpu_seconds", "peak_rss_mb")}
    res["records_identical_ok"] = strip(rec) == strip(rec2)
    res["solver_checks_all_true"] = rec["checks_all_true"] and rec2["checks_all_true"]
    if m <= 400:
        roots = sorted(rng.sample(range(m), min(m, 8)))
        W = A2["V"].astype(np.int64)
        res["gamma_edmonds_per_root_ok"] = all(min_intree_edmonds(W, r) == int(A["gamma"][r]) for r in roots)
        res["gamma_roots_checked"] = len(roots)
    else:
        res["gamma_roots_checked"] = 0
    return res


def main():
    t0 = time.process_time()
    rng = random.Random(20261114)
    os.makedirs(LOGS, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "AB"
    summary = {}
    if "A" in which:
        nfail, ncase, rows = 0, 0, []
        with open(os.path.join(LOGS, "validation_A.jsonl"), "w") as fh:
            for n in range(3, 9):
                for rule in range(256):
                    r = validate_A(rule, n, rng)
                    flags = [k for k, v in r.items() if k.endswith("_ok") or k in ("solver_checks_all_true", "kstar0_iff_all_codes", "gamma_norot_equal")]
                    r["all_ok"] = all(r[k] is True for k in flags)
                    nfail += 0 if r["all_ok"] else 1
                    ncase += 1
                    rows.append(r)
                    fh.write(json.dumps(r, sort_keys=True) + "\n")
                    fh.flush()
                print("A: n=%d done, failures so far %d, cpu %.1fs" % (n, nfail, time.process_time() - t0), flush=True)
        summary["A"] = {"cases": ncase, "failures": nfail, "n_range": [3, 8], "rules": 256,
                        "cases_gamma_all_roots": sum(1 for r in rows if r["gamma_roots_checked"] == r["m"]),
                        "cases_gamma_16_sampled_roots": sum(1 for r in rows if r["gamma_roots_checked"] != r["m"]),
                        "cases_gamma_exhaustive": sum(1 for r in rows if "gamma_exhaustive_ok" in r),
                        "max_cycles": max(r["m"] for r in rows), "max_V_seen": max(r["max_V"] for r in rows),
                        "bijective_cases": sum(1 for r in rows if r["bijective"]),
                        "cases_selected_equals_union_closed_false": sum(1 for r in rows if r.get("selected_equals_union_closed") is False),
                        "cpu_seconds": round(time.process_time() - t0, 1)}
    if "B" in which:
        t1 = time.process_time()
        extra = [0, 1, 4, 18, 30, 50, 54, 110, 150, 184, 204, 232]
        nfail, ncase, worst = 0, 0, 0.0
        with open(os.path.join(LOGS, "validation_B.jsonl"), "w") as fh:
            for n in range(3, 7):
                rules = list(range(256)) if n <= 4 else SAMPLE_RULES + extra
                for rule in rules:
                    r = validate_B(rule, n)
                    r["all_ok"] = bool(r["order_ok"] and r["pi_is_stationary"])
                    nfail += 0 if r["all_ok"] else 1
                    ncase += 1
                    worst = max(worst, r["max_abs_dev"])
                    fh.write(json.dumps(r, sort_keys=True) + "\n")
                    fh.flush()
                print("B: n=%d done, failures so far %d, cpu %.1fs" % (n, nfail, time.process_time() - t1), flush=True)
        summary["B"] = {"cases": ncase, "failures": nfail, "n_range": [3, 6], "rules_n3_n4": 256,
                        "rules_n5_n6": SAMPLE_RULES + extra, "eps": ["1e-8", "1e-16", "1e-24"],
                        "max_abs_dev_order": float(worst), "cpu_seconds": round(time.process_time() - t1, 1)}
    if "C" in which:
        t2 = time.process_time()
        nfail, ncase, nroot = 0, 0, 0
        with open(os.path.join(LOGS, "validation_C.jsonl"), "w") as fh:
            for n in range(9, 13):
                for rule in SAMPLE_RULES:
                    r = validate_C(rule, n, rng)
                    flags = [k for k in r if k.endswith("_ok") or k == "solver_checks_all_true"]
                    r["all_ok"] = all(r[k] is True for k in flags)
                    nfail += 0 if r["all_ok"] else 1
                    ncase += 1
                    nroot += 1 if r["gamma_roots_checked"] else 0
                    fh.write(json.dumps(r, sort_keys=True) + "\n")
                    fh.flush()
        summary["C"] = {"cases": ncase, "failures": nfail, "n_range": [9, 12], "rules": SAMPLE_RULES,
                        "cases_with_per_root_edmonds": nroot, "cpu_seconds": round(time.process_time() - t2, 1),
                        "peak_rss_mb": round(__import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss / 2 ** 20, 1)}
    path = os.path.join(LOGS, "validation_summary.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(summary)
    json.dump(old, open(path, "w"), indent=1, sort_keys=True)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
