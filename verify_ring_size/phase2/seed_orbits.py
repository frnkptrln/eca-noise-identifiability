"""Step 3 (c): single-seed orbits of rules 22, 26, 122, 154 for n = 4..256 with own code (p2orbit.c, Brent's cycle
detection, no state enumeration).  Pass 1: budget 2e6 map evaluations (covers the study's cut-off of 400000 steps).
Pass 2: larger budget for the orbits still undetermined.  Checkpoint: out/seed_orbits_own.jsonl (one line per
(rule, n, pass)).  Usage: python seed_orbits.py 1|2"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbitlib as O

OUT = os.path.join(O.HERE, "out")
ck = os.path.join(OUT, "seed_orbits_own.jsonl")
ps = int(sys.argv[1])
BUDGET = {1: {r: 2 * 10 ** 6 for r in (22, 26, 122, 154)},
          2: {22: 10 ** 9, 122: 10 ** 9, 26: 2 * 10 ** 8, 154: 2 * 10 ** 8}}[ps]
recs = [json.loads(l) for l in open(ck)] if os.path.exists(ck) else []
best = {}
for r in recs:
    k = (r["rule"], r["n"])
    if k not in best or r["determined"] or r["budget"] > best[k]["budget"]:
        if not (k in best and best[k]["determined"]):
            best[k] = r
for rule in (22, 26, 122, 154):
    for n in range(4, 257):
        b = best.get((rule, n))
        if b and (b["determined"] or b["budget"] >= BUDGET[rule]):
            continue
        t0 = time.process_time()
        ok, mu, lam, zero, used = O.orbit_c(rule, n, 1, BUDGET[rule])
        rec = {"rule": rule, "n": n, "pass": ps, "budget": BUDGET[rule], "determined": ok,
               "transient": mu if ok else None, "limit_period": lam if ok else None,
               "returns_to_zero": (int(zero) if ok else None), "steps_used": used,
               "cpu_seconds": round(time.process_time() - t0, 3)}
        with open(ck, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("rule", rule, "pass", ps, "done", round(time.process_time(), 1), flush=True)
