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
    V = np.zeros((m, m), dtype=np.int64)
    R = np.zeros((m, 8), dtype=np.int64)
    for j, cyc in enumerate(cert["cycles"]):
        d = np.rint(dijkstra(A, indices=cyc, min_only=True)[:S]).astype(np.int64)
        for i, cyc2 in enumerate(cert["cycles"]):
            V[j, i] = d[cyc2].min()
        for c in range(8):
            R[j, c] = d[((cm >> c) & 1).astype(bool)].min()
    # duals: y > 0, feasibility, lower bounds on gamma
    sets = [(set(mem), y) for mem, y in cert["duals"]]
    if any(y <= 0 for _, y in sets):
        errs.append("non-positive dual")
    Mem = np.zeros((len(sets), m), dtype=bool)
    yv = np.array([y for _, y in sets], dtype=np.int64)
    for k, (mem, _) in enumerate(sets):
        Mem[k, list(mem)] = True
    # laminarity: every pairwise intersection is empty or one of the two sets
    Mi = Mem.astype(np.float64)
    inter = Mi @ Mi.T
    size = Mem.sum(axis=1)
    lam_ok = (inter == 0) | (inter == size[:, None]) | (inter == size[None, :])
    if not lam_ok.all():
        errs.append("dual family not laminar")
    # sum over sets containing j but not i  <=  V[j, i]
    inc = Mem.T.astype(np.int64) * yv[None, :]            # (m, sets)
    load = inc @ (~Mem).astype(np.int64)                  # load[j, i] = sum_{S: j in S, i not in S} y_S
    off = ~np.eye(m, dtype=bool)
    if (load[off] > V[off]).any():
        errs.append("dual infeasible")
    glow = yv.sum() - (Mem.astype(np.int64) * yv[:, None]).sum(axis=0)   # sum of y over sets not containing C
    # trees: upper bounds
    gup = np.full(m, np.iinfo(np.int64).max)
    for r, par in cert["trees"].items():
        r = int(r); par = np.array(par)
        ok = par[r] == -1 and all(par[j] >= 0 for j in range(m) if j != r)
        for j in range(m):                                  # every node reaches r
            z, k = j, 0
            while ok and z != r:
                z = par[z]; k += 1
                if k > m:
                    ok = False
        if not ok:
            errs.append(f"tree for root {r} is not an in-tree"); continue
        gup[r] = sum(int(V[j, par[j]]) for j in range(m) if j != r)
    gamma = np.array(cert["gamma"])
    gmin_low = int(glow.min())
    stable = cert["stable"]
    gmin_up = int(min(gup[s] for s in stable))
    if not (gmin_low == gmin_up == cert["gamma_min"]):
        errs.append(f"gamma_min not certified: low {gmin_low} up {gmin_up} claimed {cert['gamma_min']}")
    # stable set: every claimed stable cycle has gamma_up = gamma_min; every other has gamma_low > gamma_min
    if any(gup[s] != gmin_up for s in stable):
        errs.append("a claimed stable cycle is not certified optimal")
    others = [j for j in range(m) if j not in set(stable)]
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
        for s in cert["covering_cycles"]:
            if s not in stable:
                errs.append("covering cycle not stable")
            for v in cert["cycles"][s]:
                cc |= int(cm[v])
        if cc != 255:
            errs.append("covering cycles do not cover all codes")
    else:
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
