"""Write the complete selected-orbit lists for cases that were solved before solve.py wrote them.

Re-solves every case in out/sample.jsonl whose record lists only part of the selected orbits and
has no out/selected/sel_r<RULE>_n<N>.tsv yet, checks that the new record is identical to the stored
one (apart from cpu_seconds and peak_rss_mb), and writes the list.  One process, sequential.
Appends one line per case to logs/supplement_lists.jsonl.
"""
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from solve import solve_case

strip = lambda r: {k: v for k, v in r.items() if k not in ("cpu_seconds", "peak_rss_mb")}
rows = [json.loads(l) for l in open(os.path.join(HERE, "out", "sample.jsonl")) if l.strip()]
with open(os.path.join(HERE, "logs", "supplement_lists.jsonl"), "a") as log:
    for r in sorted(rows, key=lambda r: (r["n"], r["rule"])):
        f = os.path.join(HERE, "out", "selected", "sel_r%d_n%d.tsv" % (r["rule"], r["n"]))
        if r["selected"]["orbits_complete"] or os.path.exists(f):
            continue
        t0 = time.process_time()
        rec = solve_case(r["rule"], r["n"], dump_dir=os.path.join(HERE, "out"))
        same = json.loads(json.dumps(rec, sort_keys=True)) == strip(r)
        log.write(json.dumps({"rule": r["rule"], "n": r["n"], "record_identical_to_stored": same,
                              "cpu_seconds": round(time.process_time() - t0, 2),
                              "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, 1)}) + "\n")
        log.flush()
print("supplement cpu", round(time.process_time(), 1))
