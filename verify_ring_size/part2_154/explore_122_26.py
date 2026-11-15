"""Closed classes of G1 for rules 122 and 26 (step 9; computed, not proved).

Usage: python explore_122_26.py NMIN NMAX    appends one JSON line per (rule, n) to out/explore_122_26.jsonl
(cases already present are skipped, so the script can be restarted).
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g1lib import G1  # noqa: E402

OUT = os.path.join(HERE, "out", "explore_122_26.jsonl")


def record(rule, n):
    t0 = time.process_time()
    g = G1(n, rule)
    r = {"rule": rule, "n": n, "n_cycles": g.m, "n_periodic": int(len(g.per)), "G1_edges": int(len(g.src)),
         "n_scc": int(g.ncomp), "n_closed_classes": int(len(g.closed_labels)),
         "closed_class_sizes": sorted(int((g.lab == L).sum()) for L in g.closed_labels),
         "n_transient_cycles": int((~g.in_closed).sum())}
    z = int(g.cid[0])
    r["zero_in_closed_class"] = bool(g.in_closed[z])
    r["zero_out_degree"] = int(len(g.out_nbrs(z)))
    union = 0
    for c in np.nonzero(g.in_closed)[0]:
        union |= int(g.cycle_codes[c])
    r["codes_missing_on_closed_classes"] = [c for c in range(8) if not (union >> c) & 1]
    tr = np.nonzero(~g.in_closed)[0]
    r["transient_reps_first12"] = sorted(g.rep(int(c)) for c in tr)[:12]
    if rule == 122 and n % 2 == 0:
        cb = int(g.cid[int("10" * (n // 2), 2)])
        assert cb >= 0
        r["cb_cycle_length"] = len(g.cycles[cb])
        r["edge_zero_to_cb"] = bool(((g.src == z) & (g.dst == cb)).any())
        r["zero_out_nbrs_reps"] = sorted(g.rep(int(c)) for c in g.out_nbrs(z))
        r["cb_in_closed_class"] = bool(g.in_closed[cb])
        r["cb_out_degree"] = int(len(g.out_nbrs(cb)))
        r["cb_out_nbrs_reps"] = sorted(g.rep(int(c)) for c in g.out_nbrs(cb))[:12]
        reach = g.reachable_from(cb)
        r["cb_reaches_zero"] = bool(reach[z])
        r["cb_scc_size"] = int((g.lab == g.lab[cb]).sum())
        r["zero_cb_same_scc"] = bool(g.lab[z] == g.lab[cb])
        r["n_cycles_reachable_from_cb"] = int(reach.sum())
        # which cycles can reach the checkerboard at all
        gT_seen = np.zeros(g.m, bool)
        gT_seen[cb] = True
        AT = g.A.T.tocsr()
        stack = [cb]
        while stack:
            u = stack.pop()
            for v in AT.indices[AT.indptr[u]:AT.indptr[u + 1]]:
                if not gT_seen[v]:
                    gT_seen[v] = True
                    stack.append(int(v))
        r["n_cycles_reaching_cb"] = int(gT_seen.sum())
        r["cycles_with_code2"] = int(((g.cycle_codes >> 2) & 1).sum())
    if rule == 26:
        has7 = ((g.cycle_codes >> 7) & 1).astype(bool)
        r["cycles_with_code7"] = int(has7.sum())
        r["cycles_with_code7_in_closed"] = int((has7 & g.in_closed).sum())
        r["code7_closed_reps_first6"] = sorted(g.rep(int(c)) for c in np.nonzero(has7 & g.in_closed)[0])[:6]
        r["code7_transient_reps_first6"] = sorted(g.rep(int(c)) for c in np.nonzero(has7 & ~g.in_closed)[0])[:6]
        r["code7_cycle_lengths_closed"] = sorted(set(len(g.cycles[int(c)]) for c in np.nonzero(has7 & g.in_closed)[0]))[:10]
    r["cpu_seconds"] = round(time.process_time() - t0, 2)
    return r


if __name__ == "__main__":
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            d = json.loads(line)
            done.add((d["rule"], d["n"]))
    with open(OUT, "a") as fh:
        for n in range(nmin, nmax + 1):
            for rule in (122, 26):
                if (rule, n) in done:
                    continue
                r = record(rule, n)
                fh.write(json.dumps(r, sort_keys=True) + "\n")
                fh.flush()
                print(rule, n, r["n_cycles"], r["closed_class_sizes"], r["cpu_seconds"])
