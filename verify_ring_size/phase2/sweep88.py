"""Step 3: counterexample search over all 88 classes (smallest rule number per class under reflection and
complementation, derived in p2lib.class_reps) for the general statements of Section 4 of the report:
re-rooting, Lemma 1, Lemma 2, Theorem A, Lemma B; plus the record fields used for the atlas comparison and a
validation of the memory-lean Edmonds variant.  One JSON line per (rule, n) in out/sweep88.jsonl (checkpoint).
Usage: python sweep88.py NMIN NMAX [MCAP]"""
import json
import os
import resource
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P
from p2lib import K
from lean_edmonds import lean_gamma

OUT = os.path.join(P.HERE, "out")
nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
MCAP = int(sys.argv[3]) if len(sys.argv) > 3 else 30000
ck = os.path.join(OUT, "sweep88.jsonl")
done = set()
if os.path.exists(ck):
    done = {(r["rule"], r["n"]) for r in map(json.loads, open(ck))}
reps, refl, comp = P.class_reps()
assert len(reps) == 88


def run(rule, n):
    t0 = time.process_time()
    F, cm = K.build_F(rule, n)
    m0 = K.find_cycles(n, F, cm)[0]
    rec = {"rule": rule, "n": n, "m": int(m0)}
    if m0 > MCAP:
        rec["skipped"] = "more than %d cycles" % MCAP
        return rec
    c = P.solve_full(rule, n)
    m, V, gamma, sel = c.m, c.V, c.gamma, c.sel
    np.fill_diagonal(V, 255)
    rad = V.min(axis=1).astype(np.int64) if m > 1 else np.zeros(1, np.int64)
    vmin_offdiag = int(V.min())
    np.fill_diagonal(V, 0)
    rec.update(n_orbits=int(c.no), bijective=bool(c.bijective), gmin=c.gmin, n_selected=int(sel.sum()),
               n_selected_orbits=int(len(np.unique(c.orb[sel]))), k=[int(v) for v in c.kc], kstar=c.kstar,
               cover=P.codes_str(c.joint), n_scc=int(c.ncomp), n_closed=int(c.closed_comp.sum()),
               n_edges=int(len(c.src)))
    so = np.unique(c.orb[sel])
    sp, tr, sr = K.cycle_geometry(n, c.F, c.omin[so])
    rec["sel_spatial"] = sorted({int(v) for v in sp})
    rec["sel_temporal"] = sorted({int(v) for v in c.length[c.reps[so]]})
    rec["sel_reps"] = [P.bits(v, n) for v in sorted(c.omin[so])] if len(so) <= 400 else None
    rec["sel_reps_count"] = int(len(so))
    if m > 1:
        rec["radius_sel"] = [int(rad[sel].min()), int(rad[sel].max())]
        rec["radius_other"] = [int(rad[~sel].min()), int(rad[~sel].max())] if (~sel).any() else [-1, -1]
    # ---- consistency of G1 with V
    t = {}
    t["g1_equals_V1"] = bool(len(c.src) == int((V == 1).sum()) and (len(c.src) == 0 or (V[c.src, c.dst] == 1).all()))
    t["V_offdiag_ge1"] = bool(m == 1 or vmin_offdiag >= 1)
    # ---- re-rooting: gamma(N) <= gamma(R) + V(R, N) - 1 for all R != N
    ok = True
    g32 = gamma.astype(np.int64)
    for i in range(0, m, 1024):
        blk = g32[i:i + 1024, None] + V[i:i + 1024].astype(np.int64) - 1
        j = np.arange(blk.shape[0])
        blk[j, i + j] = 1 << 40            # R = N is excluded
        ok &= bool((g32[None, :] <= blk).all())
    t["rerooting_inequality"] = ok
    # ---- Lemma 1 and its potential form
    t["lemma1"] = bool(not (sel[c.src] & ~sel[c.dst]).any())
    t["lemma1_gamma_monotone_on_G1"] = bool((gamma[c.dst] <= gamma[c.src]).all())
    # ---- Lemma 2
    t["lemma2"] = bool(not (sel & ~c.in_closed).any())
    # ---- Theorem A
    selcount = np.bincount(c.lab[sel], minlength=c.ncomp)
    size = np.bincount(c.lab, minlength=c.ncomp)
    cl = np.nonzero(c.closed_comp)[0]
    t["thmA_union_of_closed_classes"] = bool(t["lemma2"] and all(selcount[j] in (0, size[j]) for j in cl))
    rec["unique_closed_class"] = bool(len(cl) == 1)
    if len(cl) == 1:
        t["thmA_unique_S_equals_K"] = bool(np.array_equal(sel, c.in_closed))
        t["thmA_unique_gmin_m_minus_1"] = bool(c.gmin == m - 1)
    t["kstar0_iff_selected_cover_all_codes"] = bool((c.kstar == 0) == (c.joint == 255))
    rec["S_equals_union_of_all_closed"] = bool(np.array_equal(sel, c.in_closed))
    rec["n_closed_selected"] = int(sum(selcount[j] > 0 for j in cl))
    # ---- Lemma B: rotation orbits A with r(A_i) >= 2
    cand = [o for o in range(c.no) if rad[c.reps[o]] >= 2] if m > 1 else []
    rec["lemmaB_candidate_orbits"] = len(cand)
    lb = []
    n_big = int((rad >= 2).sum()) if m > 1 else 0
    for o in cand[:60]:
        A = c.orbit_members(o)
        q = len(A)
        inA = np.zeros(m, bool)
        inA[A] = True
        keep = ~inA[c.src]
        s1, d1 = c.src[keep], c.dst[keep]
        s2 = np.concatenate([np.full(int((V[a] == 2).sum()), a, np.int32) for a in A])
        d2 = np.concatenate([np.nonzero(V[a] == 2)[0].astype(np.int32) for a in A])
        g2 = bool(c.reach_to(np.r_[s1, s2], np.r_[d1, d2], [int(A[0])]).all())
        w = bool(c.reach_to(s1, d1, [int(a) for a in A]).all())
        d = {"rep": P.bits(c.omin[o], n), "q": int(q), "g2_holds": g2, "g1_reach_A": w,
             "S_equals_A": bool(np.array_equal(sel, inA)), "gmin_minus_formula": int(c.gmin - (m + q - 2)),
             "shortcut_predicts_g2_false": bool(n_big != q)}
        lb.append(d)
    rec["lemmaB"] = lb
    t["lemmaB_conclusion_when_hypotheses_hold"] = bool(all(d["S_equals_A"] and d["gmin_minus_formula"] == 0
                                                           for d in lb if d["g2_holds"]))
    t["weak_hypothesis_gives_S_equals_A"] = bool(all(d["S_equals_A"] for d in lb if d["g1_reach_A"]))
    t["g2_implies_no_other_radius_ge2"] = bool(all(not d["shortcut_predicts_g2_false"] for d in lb if d["g2_holds"]))
    # ---- memory-lean Edmonds against the dense one
    if m > 1:
        gl, info = lean_gamma(c, radius=rad)
        t["lean_edmonds_equals_dense"] = bool(np.array_equal(gl, gamma))
        rec["lean_info"] = info
    rec["tests"] = t
    rec["all_tests_true"] = bool(all(t.values()))
    rec["cpu_seconds"] = round(time.process_time() - t0, 3)
    rec["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1)
    return rec


for n in range(nmin, nmax + 1):
    for rule in reps:
        if (rule, n) in done:
            continue
        rec = run(rule, n)
        with open(ck, "a") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
    print("n", n, "done", round(time.process_time(), 1), flush=True)
