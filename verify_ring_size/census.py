"""Cycle census and single-search timing, used only to choose the larger n (no potentials computed).

For each sample rule and n = 8..22: number of cycles, of periodic states, of rotation orbits,
bijectivity, CPU time of one 0-1 search from one cycle.  Appends to out/census.jsonl.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eca_core as K

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]
with open(os.path.join(HERE, "out", "census.jsonl"), "w") as fh:
    for n in range(8, 23):
        for rule in RULES:
            t0 = time.process_time()
            F, cm = K.build_F(rule, n)
            m, cyc, attr, mn, ln, cc = K.find_cycles(n, F, cm)
            no, rot1, orb, reps, osz, omin = K.rotation_orbits(n, m, cyc, mn)
            t1 = time.process_time()
            K.bfs_from_cycle(n, F, mn[0])
            t2 = time.process_time()
            ncs = int(ln.sum())
            fh.write(json.dumps({"rule": rule, "n": n, "n_cycles": m, "n_cycle_states": ncs, "n_orbits": no,
                                 "bijective": ncs == (1 << n), "max_cycle_len": int(ln.max()),
                                 "cpu_setup": round(t1 - t0, 3), "cpu_one_search": round(t2 - t1, 4)}) + "\n")
            fh.flush()
print("census cpu", round(time.process_time(), 1))
