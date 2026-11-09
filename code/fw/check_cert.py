"""Independent checker for certificates written by cert.py.

Uses only numpy/scipy and the definitions: its own successor map, its own cycle enumeration, and all
minimum resistances V(C, C') and R(C -> D_c) by Dijkstra (scipy.sparse.csgraph) on the explicit
two-layer graph (state x -> pre-noise point F(x) at cost 0; pre-noise z -> z XOR e_i at cost 1;
pre-noise z -> state z at cost 0). It accepts a certificate only if all upper and lower bounds
coincide. Usage: python3 check_cert.py data/fw_certificates_n12/rule_*.json.gz
"""
import json, sys
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra


def succ(rule, n):
    x = np.arange(1 << n)
    out = np.zeros_like(x)
    for i in range(n):
        c = 4 * ((x >> ((i - 1) % n)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % n)) & 1)
        out |= ((rule >> c) & 1) << i
    return out


def codes_of(n):
    x = np.arange(1 << n)
    m = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        c = 4 * ((x >> ((i - 1) % n)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % n)) & 1)
        m |= 1 << c
    return m


def check(cert):
    rule, n = cert["rule"], cert["n"]
    S = 1 << n
    F = succ(rule, n)
    errs = []
    if cert.get("bijective"):
        if len(np.unique(F)) != S:
            errs.append("claimed bijective, but F is not")
        if any(item["k"] != 0 for item in cert["k_c"]) or cert["kstar"] != 0:
            errs.append("bijective rule must have all k_c = 0")
        return errs
    m = cert["m"]
    # cycles: each listed cycle is a cycle of F; together they are all cycle states
    img = np.arange(S)
    for _ in range(S):                      # image of F^t stabilises on the cycle states
        nxt = np.unique(F[img])
        if len(nxt) == len(img):
            break
        img = nxt
    oncyc = set(int(v) for v in img)
    listed = [s for cyc in cert["cycles"] for s in cyc]
    if len(listed) != len(set(listed)) or set(listed) != oncyc:
        errs.append("cycle list is not exactly the set of cycle states")
    for cyc in cert["cycles"]:
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            if F[a] != b:
                errs.append("listed cycle is not an orbit"); break
    if len(cert["cycles"]) != m:
        errs.append("m differs from the number of listed cycles")
    if errs:                                # nothing below is meaningful without the right cycles
        return errs
    # two-layer graph and Dijkstra from every cycle
    x = np.arange(S)
    rows = [x] + [S + x for _ in range(n)] + [S + x]
    cols = [S + F] + [S + (x ^ (1 << i)) for i in range(n)] + [x]
    wts = [np.zeros(S)] + [np.ones(S) for _ in range(n)] + [np.zeros(S)]
    # csgraph treats explicit zeros as absent edges: shift weights by a tiny amount and round
    A = sp.csr_matrix((np.concatenate(wts) + 1e-7, (np.concatenate(rows), np.concatenate(cols))), shape=(2 * S, 2 * S))
    cyc_of = np.full(S, -1)
    for j, cyc in enumerate(cert["cycles"]):
        cyc_of[cyc] = j
    cm = codes_of(n)
    V = np.zeros((m, m), dtype=np.int16)
    R = np.zeros((m, 8), dtype=np.int64)
    allst = np.concatenate([np.array(cyc) for cyc in cert["cycles"]])
    starts = np.cumsum([0] + [len(cyc) for cyc in cert["cycles"]])[:-1]
    cmasks = [((cm >> c) & 1).astype(bool) for c in range(8)]
    for j, cyc in enumerate(cert["cycles"]):
        d = np.rint(dijkstra(A, indices=cyc, min_only=True)[:S]).astype(np.int64)
        V[j] = np.minimum.reduceat(d[allst], starts)
        for c in range(8):
            R[j, c] = d[cmasks[c]].min()
    # hierarchy: parent pointers form a rooted tree with leaves 0..m-1
    Hh = cert["hierarchy"]
    par = np.array(Hh["parent"]); y = np.array(Hh["y"], dtype=np.int64)
    st_, sh_ = np.array(Hh["sel_tail"]), np.array(Hh["sel_head"]); top = Hh["top"]
    ns = len(par)
    if (y < 0).any():
        errs.append("negative dual")
    ch = [[] for _ in range(ns)]
    for X in range(ns):
        if X != top:
            if par[X] < 0 or par[X] <= X:
                errs.append("hierarchy parent pointers malformed"); break
            ch[par[X]].append(X)
    if any(ch[v] for v in range(m)) or any(not ch[X] for X in range(m, ns)):
        errs.append("leaves of the hierarchy are not exactly the cycles")
    # depth-first order of the cycles: every set is an interval [lo, hi)
    order, lo, hi = [], np.zeros(ns, dtype=np.int64), np.zeros(ns, dtype=np.int64)
    stack = [(top, 0)]
    while stack:
        X, state = stack.pop()
        if state == 0:
            lo[X] = len(order)
            if X < m:
                order.append(X); hi[X] = len(order)
            else:
                stack.append((X, 1))
                for Y in reversed(ch[X]):
                    stack.append((Y, 0))
        else:
            hi[X] = len(order)
    order = np.array(order)
    if sorted(order.tolist()) != list(range(m)):
        errs.append("hierarchy does not cover every cycle exactly once")
    pos = np.empty(m, dtype=np.int64); pos[order] = np.arange(m)
    # Dsum[v]: sum of y over non-top sets containing v; up[X]: sum of y over sets S with v in S, S in X
    T = int(y[[X for X in range(ns) if X != top]].sum())
    Dsum = np.zeros(m, dtype=np.int64)
    for X in range(ns):
        if X != top and y[X]:
            Dsum[order[lo[X]:hi[X]]] += y[X]
    # (1) tightness
    def chain_sum(t, X):
        s, z = 0, t
        while True:
            s += int(y[z])
            if z == X:
                return s
            z = int(par[z])
    for X in range(ns):
        if X == top:
            continue
        t, h = int(st_[X]), int(sh_[X])
        if not (lo[X] <= pos[t] < hi[X]) or (lo[X] <= pos[h] < hi[X]):
            errs.append(f"selected edge of set {X} does not leave it"); break
        if V[t, h] != chain_sum(t, X):
            errs.append(f"selected edge of set {X} is not tight"); break
    # (2) cycle condition
    for Q in range(m, ns):
        kids = sorted(ch[Q], key=lambda Y: lo[Y])
        los = np.array([lo[Y] for Y in kids])
        def child_of(v):
            k = int(np.searchsorted(los, pos[v], side="right")) - 1
            return kids[k] if k >= 0 and lo[kids[k]] <= pos[v] < hi[kids[k]] else None
        nxt = {Y: child_of(int(sh_[Y])) for Y in kids}
        if any(v is None for v in nxt.values()):
            errs.append(f"a selected edge in set {Q} leaves it"); break
        z, seen = kids[0], set()
        while z not in seen:
            seen.add(z); z = nxt[z]
        if not (z == kids[0] and len(seen) == len(kids)):
            errs.append(f"children of set {Q} do not form one cycle"); break
    # (3) dual feasibility, in depth-first coordinates: load[a, b] = sum of y over sets containing
    # the a-th cycle but not the b-th
    Vp = V[np.ix_(order, order)]
    load = np.zeros((m, m), dtype=np.int64)
    for X in range(ns):
        if X != top and y[X]:
            a_, b_ = lo[X], hi[X]
            load[a_:b_, :a_] += y[X]; load[a_:b_, b_:] += y[X]
    offd = ~np.eye(m, dtype=bool)
    if (load[offd] > Vp[offd]).any():
        errs.append("dual infeasible")
    glow = T - Dsum            # by (1)-(3), also the upper bound for every root
    gup = glow.copy()
    # one explicit tree, checked edge by edge
    tr = cert["tree"]; r = tr["root"]; tp = np.array(tr["parent"])
    ok = tp[r] == -1 and all(tp[j] >= 0 for j in range(m) if j != r)
    for j in range(m):
        z, k = j, 0
        while ok and z != r:
            z = tp[z]; k += 1
            if k > m:
                ok = False
    if not ok or sum(int(V[j, tp[j]]) for j in range(m) if j != r) != glow[r]:
        errs.append("explicit tree invalid or not optimal")
    gamma = np.array(cert["gamma"])
    gmin_low = int(glow.min())
    stable = cert["stable"]
    gmin_up = int(min(gup[s] for s in stable))
    if not np.array_equal(glow, np.array(cert["gamma"])):
        errs.append("claimed gamma differs from T - D")
    if not (gmin_low == gmin_up == cert["gamma_min"]):
        errs.append(f"gamma_min not certified: low {gmin_low} up {gmin_up} claimed {cert['gamma_min']}")
    # stable set: every claimed stable cycle has gamma_up = gamma_min; every other has gamma_low > gamma_min
    if any(gup[s] != gmin_up for s in stable):
        errs.append("a claimed stable cycle is not certified optimal")
    sset = set(stable)
    others = [j for j in range(m) if j not in sset]
    if any(glow[j] <= gmin_low for j in others):
        errs.append("a non-claimed cycle may be stable")
    if (glow > gamma).any():
        errs.append("claimed gamma below dual lower bound")
    # k_c: upper bound by witness, lower bound by duals and Dijkstra
    for item in cert["k_c"]:
        c, k, C, traj = item["code"], item["k"], item["root"], item["trajectory"]
        if cyc_of[traj[0]] != C:
            errs.append(f"code {c}: trajectory does not start on its root cycle")
        if not (cm[traj[-1]] >> c) & 1:
            errs.append(f"code {c}: trajectory does not end in a state with the code")
        res = sum(bin(int(F[a]) ^ int(b)).count("1") for a, b in zip(traj, traj[1:]))
        up = int(gup[C]) + res - gmin_low
        low = int((glow + R[:, c]).min()) - gmin_up
        if not (up == low == k):
            errs.append(f"code {c}: k_c not certified (low {low}, up {up}, claimed {k})")
    ks = max(item["k"] for item in cert["k_c"])
    if ks != cert["kstar"]:
        errs.append("kstar is not max k_c")
    cover = 0
    for s in stable:
        for v in cert["cycles"][s]:
            cover |= int(cm[v])
    if cover != cert["stable_cover_mask"]:
        errs.append("stable cover mask wrong")
    if cert["kstar"] == 0:
        cc = 0
        if "covering_cycles" not in cert:
            errs.append("k* = 0 but no covering cycles given"); return errs
        for s in cert["covering_cycles"]:
            if s not in stable:
                errs.append("covering cycle not stable")
            for v in cert["cycles"][s]:
                cc |= int(cm[v])
        if cc != 255:
            errs.append("covering cycles do not cover all codes")
    else:
        if "uncovered_codes" not in cert:
            errs.append("k* >= 1 but no uncovered codes given"); return errs
        for c in cert["uncovered_codes"]:
            if any((cm[v] >> c) & 1 for s in stable for v in cert["cycles"][s]):
                errs.append(f"code {c} claimed uncovered but on a stable cycle")
    return errs


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        import gzip
        e = check(json.load(gzip.open(p, "rt") if p.endswith(".gz") else open(p)))
        if e:
            bad += 1
            print(p, "FAILED:", "; ".join(e))
    print(f"{len(sys.argv) - 1} certificates checked, {bad} failed")
    sys.exit(1 if bad else 0)
