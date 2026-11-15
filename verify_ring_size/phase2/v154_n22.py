"""Step 6: rule 154 at n = 22 with a memory-lean method (no dense V).
(1) cycles, rotation orbits, one-flip graph G1 (sparse definition), strongly connected components, closed classes;
(2) V rows for one representative per rotation orbit by the 0-1 search (streamed, never stored): every row is checked
    (diagonal 0, off-diagonal minimum, the set {V = 1} against the G1 out-neighbours), histogram of V;
(3) Edmonds' algorithm, level 1: rho(C) = min_{C'} V(C, C'); arcs of reduced weight 0 = {V(C, C') = rho(C)}, rebuilt from
    the streamed rows and extended to all cycles by V(sigma C, sigma C') = V(C, C'); if they form one strongly connected
    component the contraction ends after level 1 and gamma(C) = sum rho - rho(C) for every cycle.  Otherwise the script
    stops and reports that the second level (lean_edmonds.lean_gamma) is needed.
Checkpoint every 1000 orbits in out/v154_n22_ckpt.npz; result in out/v154_n22.json.  1 process."""
import json
import os
import resource
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P

RULE, N = 154, 22
OUT = os.path.join(P.HERE, "out")
CK = os.path.join(OUT, "v154_n22_ckpt.npz")
t0 = time.process_time()
c = P.Case(RULE, N)
m = c.m
res = {"rule": RULE, "n": N, "cycles": int(m), "rotation_orbits": int(c.no), "cycle_states": int(c.length.sum()),
       "states": 1 << N, "bijective": bool(c.bijective), "g1_edges": int(len(c.src)), "g1_scc": int(c.ncomp),
       "g1_closed_classes": int(c.closed_comp.sum()),
       "g1_closed_class_sizes": sorted(int(v) for v in np.bincount(c.lab)[c.closed_comp])[:10],
       "cycles_without_g1_out_edge": int((~c.has_out).sum()),
       "codes_on_cycles": P.codes_str(int(np.bitwise_or.reduce(c.ccodes))),
       "orbit_size_hist": [[int(a), int(b)] for a, b in zip(*np.unique(c.osz, return_counts=True))],
       "cycle_length_max": int(c.length.max())}
# out-neighbours of every cycle in G1 (sparse definition), for the row-by-row comparison
order = np.argsort(c.src, kind="stable")
gs, gd = c.src[order], c.dst[order]
gstart = np.searchsorted(gs, np.arange(m + 1))

start, hist, n1, arcs_s, arcs_d, rho_rep, bad = 0, np.zeros(256, np.int64), 0, [], [], np.zeros(c.no, np.int64), []
cpu_prev = 0.0
if os.path.exists(CK):
    z = np.load(CK, allow_pickle=True)
    start, hist, n1 = int(z["start"]), z["hist"], int(z["n1"])
    arcs_s, arcs_d = [z["arcs_s"]], [z["arcs_d"]]
    rho_rep, bad, cpu_prev = z["rho_rep"], list(z["bad"]), float(z["cpu"])


def save(nxt):
    tmp = CK + ".tmp.npz"
    np.savez(tmp, start=nxt, hist=hist, n1=n1, arcs_s=np.concatenate(arcs_s) if arcs_s else np.zeros(0, np.int32),
             arcs_d=np.concatenate(arcs_d) if arcs_d else np.zeros(0, np.int32), rho_rep=rho_rep,
             bad=np.array(bad, dtype=np.int64), cpu=cpu_prev + time.process_time() - t0)
    os.replace(tmp, CK)


for o in range(start, c.no):
    r = int(c.reps[o])
    row, _ = c.row(r)
    if row[r] != 0:
        bad.append(o)
    w = row.astype(np.int64)
    w[r] = 1 << 20
    rho = int(w.min())
    rho_rep[o] = rho
    if rho < 1:
        bad.append(o)
    one = np.nonzero(row == 1)[0]
    if not np.array_equal(one, np.sort(gd[gstart[r]:gstart[r + 1]])):
        bad.append(o)
    zero_arcs = np.nonzero(w == rho)[0].astype(np.int32)
    arcs_s.append(np.full(len(zero_arcs), r, np.int32))
    arcs_d.append(zero_arcs)
    h = np.bincount(row, minlength=256)
    h[0] -= 1                                  # the diagonal entry
    hist += h * int(c.osz[o])
    n1 += len(one) * int(c.osz[o])
    if (o + 1) % 1000 == 0:
        save(o + 1)
        print("orbit", o + 1, "of", c.no, "cpu", round(cpu_prev + time.process_time() - t0, 1), flush=True)
save(c.no)

# ---- Edmonds, level 1, on the arcs rebuilt from the V rows
S, Dd = np.concatenate(arcs_s), np.concatenate(arcs_d)
rho_all = rho_rep[c.orb]
src_all, dst_all = [S], [Dd]
cs, cd = S.copy(), Dd.copy()
for k in range(1, N):                          # V(sigma C, sigma C') = V(C, C')
    cs, cd = c.rot1[cs], c.rot1[cd]
    src_all.append(cs)
    dst_all.append(cd)
A = np.unique(np.concatenate(src_all).astype(np.int64) * m + np.concatenate(dst_all))
G = csr_matrix((np.ones(len(A), np.int8), (A // m, A % m)), shape=(m, m))
ncomp, lab = connected_components(G, directed=True, connection="strong")
g1set = np.unique(c.src.astype(np.int64) * m + c.dst)
res.update({
    "V_rows_computed": int(c.no), "row_check_failures": [int(b) for b in bad],
    "V_offdiag_hist": [[int(v), int(k)] for v, k in enumerate(hist) if k and v > 0],
    "V_offdiag_zero_entries": int(hist[0]), "V_max": int(np.nonzero(hist)[0].max()),
    "V_equal_1_entries": int(n1), "V_equal_1_entries_equals_g1_edges": bool(n1 == len(c.src)),
    "rho_min": int(rho_all.min()), "rho_max": int(rho_all.max()),
    "zero_reduced_arcs_from_V": int(len(A)), "zero_reduced_arcs_equal_g1_edge_set": bool(np.array_equal(A, g1set)),
    "level1_strong_components": int(ncomp)})
if ncomp == 1:
    gamma = int(rho_all.sum()) - rho_all                      # all roots
    gmin = int(gamma.min())
    sel = gamma == gmin
    joint = int(np.bitwise_or.reduce(c.ccodes[sel]))
    # k_c = min_C [gamma(C) + R(C -> D_c)] - gamma_min; R(C -> D_c) = 0 iff a state of C contains code c
    kc = [0 if (joint >> code) & 1 else None for code in range(8)]
    res.update({"edmonds_levels": 1, "gamma_min": gmin, "gamma_max": int(gamma.max()), "m_minus_1": int(m - 1),
                "selected_cycles": int(sel.sum()), "selected_rotation_orbits": int(len(np.unique(c.orb[sel]))),
                "selected_cover": P.codes_str(joint), "k_c": kc,
                "kstar": 0 if all(v == 0 for v in kc) else None,
                "selected_equals_union_of_closed_classes": bool(np.array_equal(sel, c.in_closed)),
                "theoremA_unique_closed_class_S_equals_K_and_gmin_m_minus_1":
                    bool(res["g1_closed_classes"] == 1 and np.array_equal(sel, c.in_closed) and gmin == m - 1)})
else:
    res["edmonds_levels"] = "more than one level needed; not completed here"
res["cpu_seconds"] = round(cpu_prev + time.process_time() - t0, 1)
res["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1)
json.dump(res, open(os.path.join(OUT, "v154_n22.json"), "w"), indent=1)
print(json.dumps(res))
