"""Cross-check of out/g1_classes.jsonl against the sealed blind sample verify_ring_size/out/sample.jsonl
(rule 94, n = 8..22): number of cycles, number of periodic states, number of G1 edges, sizes of the closed
classes.  The sample was produced by different code (C core); only its output file is read here.

Run from the repository root:  python verify_ring_size/part2_94/crosscheck_sample.py
Output: verify_ring_size/part2_94/out/crosscheck_sample.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
samp = {}
for line in open(os.path.join(HERE, "..", "out", "sample.jsonl")):
    r = json.loads(line)
    if r["rule"] == 94:
        samp[r["n"]] = r
rows = []
for line in open(os.path.join(HERE, "out", "g1_classes.jsonl")):
    r = json.loads(line)
    s = samp.get(r["n"])
    if s is None:
        continue
    rows.append(dict(
        n=r["n"],
        cycles=(r["cycles"], s["n_cycles"]),
        periodic_states=(r["periodic_states"], s["n_cycle_states"]),
        g1_edges=(r["g1_edges"], s["g1"]["n_edges"]),
        closed_class_sizes=(r["closed_class_sizes"], sorted(s["g1"]["closed_class_sizes"])),
        agree=(r["cycles"] == s["n_cycles"] and r["periodic_states"] == s["n_cycle_states"]
               and r["g1_edges"] == s["g1"]["n_edges"]
               and r["closed_class_sizes"] == sorted(s["g1"]["closed_class_sizes"]))))
rows.sort(key=lambda d: d["n"])
out = dict(compared_n=[d["n"] for d in rows], all_agree=all(d["agree"] for d in rows), rows=rows)
with open(os.path.join(HERE, "out", "crosscheck_sample.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("compared n =", out["compared_n"], " all agree:", out["all_agree"])
