"""Solve one (rule, n): cycles, V, stochastic potentials, noise-selected cycles, k*, one-flip graph G1.

Usage: python solve.py RULE N [--mcap M] [--norot]
Prints one JSON line.  Conventions: see core.c header and SAMPLE.md.
If more than LIST_ORBITS orbits are selected, the complete list goes to out/selected/sel_r<RULE>_n<N>.tsv;
if the selected set differs from the union of the closed classes of G1, the complete closed classes go to
out/closed/closed_r<RULE>_n<N>.tsv.
"""
import hashlib
import json
import os
import resource
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order, connected_components

import eca_core as K

LIST_ORBITS = 60      # list selected orbits individually up to this many
LIST_CLASSES = 60     # describe closed classes individually up to this many
LIST_MEMBERS = 24     # list class members individually up to this size
LIST_UNREACH = 24
DEFAULT_MCAP = 46000  # dense V needs m*m bytes


def bits(x, n):
    return format(int(x), "0%db" % n)


def sha_members(strings):
    return hashlib.sha256("\n".join(sorted(strings)).encode()).hexdigest()


def codes_of(mask):
    return [c for c in range(8) if (int(mask) >> c) & 1]


def solve_case(rule, n, mcap=DEFAULT_MCAP, use_rot=True, return_arrays=False, dump_dir=None):
    N = 1 << n
    F, cm = K.build_F(rule, n)
    m, cyc, attr, minstate, length, ccodes = K.find_cycles(n, F, cm)
    n_cycle_states = int(length.sum())
    bijective = n_cycle_states == N
    no, rot1, orb, reps, osz, omin = K.rotation_orbits(n, m, cyc, minstate)
    rec = {"rule": rule, "n": n, "n_states": N, "n_cycles": m, "n_cycle_states": n_cycle_states,
           "n_orbits": no, "bijective": bool(bijective)}
    checks = {}

    # ---- one-flip graph G1 (sparse definition) and its strongly connected components
    src, dst = K.g1_edges(n, F, attr, m, minstate, length)
    ne = len(src)
    G = csr_matrix((np.ones(ne, np.int8), (src, dst)), shape=(m, m))
    ncomp, lab = connected_components(G, directed=True, connection="strong")
    leaving = np.zeros(ncomp, bool)
    cross = lab[src] != lab[dst]
    leaving[lab[src[cross]]] = True
    closed_comp = ~leaving
    in_closed = closed_comp[lab]
    comp_size = np.bincount(lab, minlength=ncomp)
    g1_symmetric = None
    if ne <= 60_000_000:
        a = src.astype(np.int64) * m + dst
        b = dst.astype(np.int64) * m + src
        g1_symmetric = bool(np.array_equal(np.sort(a), np.sort(b)))

    # ---- stochastic potentials
    full = m <= mcap
    arrays = {}
    if full:
        V, kd = K.compute_V(n, F, cyc, cm, m, minstate, rot1, reps if use_rot else np.arange(m, dtype=np.int32),
                            use_rot=use_rot)
        if not use_rot:
            kd = kd[reps]
        checks["V_diag_zero"] = bool((np.diagonal(V) == 0).all())
        vh = np.zeros(256, np.int64)
        step = max(1, 4_000_000 // max(m, 1))
        for i in range(0, m, step):
            vh += np.bincount(V[i:i + step].ravel(), minlength=256)
        checks["V_offdiag_min_ge_1"] = bool(vh[0] == m)
        checks["G1_count_matches_V_eq_1"] = bool(vh[1] == ne)
        checks["G1_edges_have_V_1"] = bool((V[src, dst] == 1).all()) if ne else True
        rec["V_hist"] = [[int(v), int(c)] for v, c in enumerate(vh) if c and v > 0]
        rec["max_V"] = int(np.nonzero(vh)[0].max())
        if return_arrays:
            arrays["V"] = V.copy()
            arrays["kd"] = kd.copy()
        gamma = K.edmonds_all_roots(V)
        del V
        checks["gamma_rotation_invariant"] = bool((gamma[rot1] == gamma).all())
        if bijective:
            checks["bijection_shortcut_confirmed"] = bool((gamma == m - 1).all())
        rec["method"] = "full"
    elif bijective:
        # Shortcut (proof in SAMPLE.md): if F is a bijection then G1 is symmetric and connected
        # and gamma(C) = m - 1 for every cycle.  The two premises are checked on the computed G1.
        checks["shortcut_G1_symmetric"] = g1_symmetric
        checks["shortcut_G1_one_component"] = bool(ncomp == 1)
        if not (g1_symmetric and ncomp == 1):
            raise RuntimeError("bijection shortcut premises failed")
        gamma = np.full(m, m - 1, np.int64)
        kd = np.zeros((no, 8), np.uint8)  # every state is periodic, so R(C -> D_c) = 0 for a cycle inside D_c
        rec["method"] = "bijection_shortcut"
    else:
        raise RuntimeError("m=%d exceeds mcap=%d and F is not a bijection" % (m, mcap))

    gmin = int(gamma.min())
    rec["min_gamma"] = gmin
    rec["max_gamma"] = int(gamma.max())
    gv, gc = np.unique(gamma, return_counts=True)
    rec["gamma_hist"] = [[int(a), int(b)] for a, b in zip(gv[:40], gc[:40])]
    rec["gamma_hist_truncated"] = bool(len(gv) > 40)
    sel = gamma == gmin

    # ---- k_c = min_C [gamma(C) + R(C -> D_c)] - min gamma
    if rec["method"] == "full":
        kc = (gamma[reps][:, None] + kd.astype(np.int64)).min(axis=0) - gmin
    else:
        # all gamma equal; some periodic state contains code c (checked), so k_c = 0
        allc = int(np.bitwise_or.reduce(ccodes))
        kc = np.array([0 if (allc >> c) & 1 else -1 for c in range(8)], np.int64)
        assert (kc >= 0).all()
    rec["k"] = [int(v) for v in kc]
    rec["kstar"] = int(kc.max())

    # ---- selected cycles by rotation orbit
    sel_orb_mask = np.zeros(no, bool)
    sel_orb_mask[orb[sel]] = True
    checks["selected_rotation_invariant"] = bool(int(osz[sel_orb_mask].sum()) == int(sel.sum()))
    so = np.nonzero(sel_orb_mask)[0]
    so = so[np.argsort(omin[so], kind="stable")]
    sp, tr, sr = K.cycle_geometry(n, F, omin[so])
    tper = length[reps[so]]
    ocodes = ccodes[reps[so]]
    joint = int(np.bitwise_or.reduce(ccodes[sel]))
    rep_strings = [bits(x, n) for x in omin[so]]
    selrec = {"n_cycles": int(sel.sum()), "n_orbits": int(len(so)),
              "orbit_reps_sha256": sha_members(rep_strings)}
    def orow(i):
        return {"rep": rep_strings[i], "n_cycles_in_orbit": int(osz[so[i]]), "temporal_period": int(tper[i]),
                "spatial_period": int(sp[i]), "t_rot": int(tr[i]), "rot": int(sr[i]),
                "codes": codes_of(ocodes[i])}
    nlist = len(so) if len(so) <= LIST_ORBITS else 12
    selrec["orbits"] = [orow(i) for i in range(nlist)]
    selrec["orbits_complete"] = bool(nlist == len(so))
    summ = {}
    for i in range(len(so)):
        key = (int(tper[i]), int(sp[i]), int(tr[i]), int(sr[i]), int(ocodes[i]))
        a = summ.setdefault(key, [0, 0])
        a[0] += 1
        a[1] += int(osz[so[i]])
    selrec["type_summary"] = [{"temporal_period": k[0], "spatial_period": k[1], "t_rot": k[2], "rot": k[3],
                               "codes": codes_of(k[4]), "n_orbits": v[0], "n_cycles": v[1]}
                              for k, v in sorted(summ.items())]
    rec["selected"] = selrec
    if dump_dir is not None and nlist < len(so):
        # complete list of selected orbits when it is too long for the JSON record
        os.makedirs(os.path.join(dump_dir, "selected"), exist_ok=True)
        tmp = os.path.join(dump_dir, "selected", "sel_r%d_n%d.tsv.%d.tmp" % (rule, n, os.getpid()))
        with open(tmp, "w") as fh:
            fh.write("rep\tn_cycles_in_orbit\ttemporal_period\tspatial_period\tt_rot\trot\tcodes\n")
            for i in range(len(so)):
                fh.write("%s\t%d\t%d\t%d\t%d\t%d\t%s\n" % (rep_strings[i], osz[so[i]], tper[i], sp[i], tr[i], sr[i],
                                                             "".join(map(str, codes_of(ocodes[i])))))
        os.replace(tmp, os.path.join(dump_dir, "selected", "sel_r%d_n%d.tsv" % (rule, n)))
    rec["codes_joint"] = codes_of(joint)
    rec["codes_missing"] = [c for c in range(8) if not (joint >> c) & 1]
    checks["kstar0_iff_all_codes"] = bool((rec["kstar"] == 0) == (joint == 255))

    # ---- G1 closed classes versus the selected set
    closed_ids = np.nonzero(closed_comp)[0]
    sizes = comp_size[closed_ids]
    sel_in_comp = np.bincount(lab[sel], minlength=ncomp)
    g1 = {"n_edges": int(ne), "n_scc": int(ncomp), "symmetric": g1_symmetric,
          "n_closed_classes": int(len(closed_ids)),
          "closed_class_sizes": sorted(int(s) for s in sizes) if len(sizes) <= 200 else None,
          "closed_class_size_hist": [[int(a), int(b)] for a, b in zip(*np.unique(sizes, return_counts=True))],
          "n_cycles_in_closed_classes": int(sizes.sum())}
    members_all = np.nonzero(in_closed)[0]
    g1["closed_union_sha256"] = sha_members([bits(x, n) for x in minstate[members_all]])
    g1["selected_cycles_sha256"] = sha_members([bits(x, n) for x in minstate[sel]])
    order = np.argsort(lab[members_all], kind="stable")
    members_sorted = members_all[order]
    bounds = np.r_[0, np.cumsum(comp_size[np.unique(lab[members_all])])]
    cls = []
    for j, cid in enumerate(np.unique(lab[members_all])):
        mem = members_sorted[bounds[j]:bounds[j + 1]]
        ms = sorted(bits(x, n) for x in minstate[mem])
        d = {"size": int(len(mem)), "min_member": ms[0], "n_selected": int(sel_in_comp[cid]),
             "n_rotation_orbits": int(len(np.unique(orb[mem])))}
        if len(mem) <= LIST_MEMBERS:
            d["members"] = ms
        else:
            d["members_sha256"] = sha_members(ms)
        cls.append(d)
    cls.sort(key=lambda d: d["min_member"])
    g1["closed_classes"] = cls[:LIST_CLASSES]
    g1["closed_classes_complete"] = bool(len(cls) <= LIST_CLASSES)
    g1["selected_equals_union_closed"] = bool(np.array_equal(sel, in_closed))
    part = all(d["n_selected"] in (0, d["size"]) for d in cls)
    g1["selected_is_union_of_some_closed"] = bool(part and not (sel & ~in_closed).any())
    # cycles that cannot reach the selected set along directed G1 edges
    sidx = np.nonzero(sel)[0]
    rs = np.r_[dst, np.full(len(sidx), m, np.int32)]   # reversed graph plus a sink node m fed by the selected set
    rd = np.r_[src, sidx.astype(np.int32)]
    GT = csr_matrix((np.ones(len(rs), np.int8), (rs, rd)), shape=(m + 1, m + 1))
    reach = breadth_first_order(GT, m, directed=True, return_predecessors=False)
    can = np.zeros(m + 1, bool)
    can[reach] = True
    cannot = np.nonzero(~can[:m])[0]
    g1["n_cannot_reach_selected"] = int(len(cannot))
    if 0 < len(cannot) <= LIST_UNREACH:
        g1["cannot_reach_selected"] = sorted(bits(x, n) for x in minstate[cannot])
    elif len(cannot):
        g1["cannot_reach_selected_sha256"] = sha_members([bits(x, n) for x in minstate[cannot]])
    rec["g1"] = g1
    if dump_dir is not None and not g1["selected_equals_union_closed"]:
        # complete closed classes whenever they differ from the selected set
        os.makedirs(os.path.join(dump_dir, "closed"), exist_ok=True)
        tmp = os.path.join(dump_dir, "closed", "closed_r%d_n%d.tsv.%d.tmp" % (rule, n, os.getpid()))
        with open(tmp, "w") as fh:
            fh.write("cycle_min_state\tclosed_class_min_member\tselected\n")
            for j, cid in enumerate(np.unique(lab[members_all])):
                mem = members_sorted[bounds[j]:bounds[j + 1]]
                cmin = bits(minstate[mem].min(), n)
                for c in mem[np.argsort(minstate[mem])]:
                    fh.write("%s\t%s\t%d\n" % (bits(minstate[c], n), cmin, int(sel[c])))
        os.replace(tmp, os.path.join(dump_dir, "closed", "closed_r%d_n%d.tsv" % (rule, n)))
    rec["checks"] = checks
    rec["checks_all_true"] = bool(all(v is True for v in checks.values()))
    if return_arrays:
        arrays.update(F=F, cm=cm, cyc=cyc, attr=attr, minstate=minstate, length=length, ccodes=ccodes,
                      gamma=gamma, sel=sel, src=src, dst=dst, rot1=rot1, orb=orb, reps=reps, lab=lab,
                      in_closed=in_closed)
        return rec, arrays
    return rec


if __name__ == "__main__":
    rule, n = int(sys.argv[1]), int(sys.argv[2])
    mcap = DEFAULT_MCAP
    if "--mcap" in sys.argv:
        mcap = int(sys.argv[sys.argv.index("--mcap") + 1])
    rec = solve_case(rule, n, mcap=mcap, use_rot="--norot" not in sys.argv,
                     dump_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
    rec["cpu_seconds"] = round(time.process_time(), 3)
    rec["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1)
    print(json.dumps(rec, sort_keys=True))
