"""CPU time of the one-flip-graph part alone for rule 154 at n = 22 (cycles, rotation orbits, G1, strongly connected
components), which already decides the case.  Writes out/v154_n22_g1_timing.json."""
import json
import os
import resource
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P

t0 = time.process_time()
c = P.Case(154, 22)
dt = time.process_time() - t0
res = {"rule": 154, "n": 22, "cycles": int(c.m), "g1_edges": int(len(c.src)), "g1_scc": int(c.ncomp),
       "cycles_without_out_edge": int((~c.has_out).sum()), "cpu_seconds": round(dt, 3),
       "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1)}
json.dump(res, open(os.path.join(P.HERE, "out", "v154_n22_g1_timing.json"), "w"), indent=1)
print(res)
