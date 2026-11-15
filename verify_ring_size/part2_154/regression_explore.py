"""Recompute the records of out/explore_122_26.jsonl for n = 4..NMAX with the present g1lib.py and compare
(the file was written in three runs, the first two before build_F was changed to work in chunks).
Output: out/regression_explore.txt
"""
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import explore_122_26 as ex  # noqa: E402

nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 24
old = {(d["rule"], d["n"]): d for d in map(json.loads, open(ex.OUT))}
t0 = time.process_time()
same, cases = True, 0
for n in range(4, nmax + 1):
    for rule in (122, 26):
        r = ex.record(rule, n)
        o = dict(old[(rule, n)])
        r.pop("cpu_seconds")
        o.pop("cpu_seconds")
        same &= (r == o)
        cases += 1
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
peak_mb = peak / 1e6 if sys.platform == "darwin" else peak / 1e3
txt = ("records recomputed for n = 4..%d (%d cases) identical to out/explore_122_26.jsonl apart from cpu_seconds: %s\n"
       "cpu seconds: %.1f\npeak RSS (MB): %.0f\n" % (nmax, cases, same, time.process_time() - t0, peak_mb))
open(os.path.join(HERE, "out", "regression_explore.txt"), "w").write(txt)
print(txt, end="")
