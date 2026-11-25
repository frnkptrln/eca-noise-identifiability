"""Inspection helper for the mechanism analysis under walls: selected cycles, their states (cell 0 first),
codes, missed codes, radius r(C) = min_{C' != C} V(C, C'), closed classes of G1 (weight-1 graph between
cycles), and whether the selected set is the union of all closed classes.
Usage: python3 inspect_boundaries.py RULE N [boundary]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fwlib


def bits(x, n):
    return "".join(str((int(x) >> i) & 1) for i in range(n))


def codes_str(mask):
    return "".join(str(c) for c in range(8) if (int(mask) >> c) & 1) or "-"


def vmatrix(res):
    es = res["es"]; m = res["m"]
    return np.array([[es.weight(j, i) if i != j else 0 for i in range(m)] for j in range(m)], dtype=np.int64)


def closed_classes(V):
    """Closed strongly connected classes of G1 (edges with V == 1)."""
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    m = len(V)
    A = sp.csr_matrix((V == 1) & ~np.eye(m, dtype=bool))
    k, lab = connected_components(A, directed=True, connection="strong")
    out = []
    for c in range(k):
        mem = np.flatnonzero(lab == c)
        targets = np.unique(lab[A[mem].indices]) if A[mem].nnz else np.array([], int)
        if set(targets.tolist()) <= {c}:
            out.append(mem)
    return out


def inspect(rule, n, boundary="null", show=12, with_g1=True):
    res = fwlib.classify(rule, n, boundary=boundary)
    cs = res["cs"]; st = res["stable"]
    out = dict(rule=rule, n=n, m=res["m"], gmin=res["gmin"], n_stable=len(st), kstar=res["kstar"],
               k_c=[int(v) for v in res["k_c"]], missed=codes_str(255 & ~res["stable_cover"]))
    if with_g1 and res["m"] <= 3000:
        V = vmatrix(res)
        rad = np.where(np.eye(res["m"], dtype=bool), 10 ** 6, V).min(axis=1) if res["m"] > 1 else np.array([0])
        cc = closed_classes(V) if res["m"] > 1 else [np.array([0])]
        out["closed_classes"] = [len(c) for c in cc]
        out["S_is_union_closed"] = bool(set(np.concatenate(cc).tolist()) == set(st.tolist()))
        out["radius_selected"] = sorted(set(int(rad[s]) for s in st))
        out["max_radius_others"] = int(max([rad[j] for j in range(res["m"]) if j not in set(st.tolist())], default=0))
    sel = []
    for s in st[:show]:
        states = cs.states_of(int(s))
        z = int(cs.cyc_min[s]); orb = [z]
        while int(cs.F[orb[-1]]) != z:
            orb.append(int(cs.F[orb[-1]]))
        sel.append(dict(period=len(orb), codes=codes_str(cs.cyc_codes[s]), gamma=int(res["gamma"][s]),
                        states=[bits(v, n) for v in orb[:6]]))
    out["selected"] = sel
    return out, res


if __name__ == "__main__":
    rule, n = int(sys.argv[1]), int(sys.argv[2]); b = sys.argv[3] if len(sys.argv) > 3 else "null"
    o, _ = inspect(rule, n, b)
    for k, v in o.items():
        if k != "selected":
            print(k, v)
    for s in o["selected"]:
        print("  ", s)
