"""Third pass of the seed orbits: budget 6e9 map evaluations for the still-open (rule, n) whose expected limit
period (from the rule-90 period on the ring of size n + 1 for rule 122) is within reach, and for the four open n
of rule 22.  Appends to out/seed_orbits_own.jsonl."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbitlib as O

ck = os.path.join(O.HERE, "out", "seed_orbits_own.jsonl")
BUDGET = 6 * 10 ** 9
done = {(r["rule"], r["n"]) for r in map(json.loads, open(ck)) if r["determined"] or r["budget"] >= BUDGET}
for rule, n in [(122, 117), (122, 121), (122, 153), (122, 173), (122, 235), (22, 234), (22, 235), (22, 242), (22, 243)]:
    if (rule, n) in done:
        continue
    t0 = time.process_time()
    ok, mu, lam, zero, used = O.orbit_c(rule, n, 1, BUDGET)
    rec = {"rule": rule, "n": n, "pass": 3, "budget": BUDGET, "determined": ok, "transient": mu if ok else None,
           "limit_period": lam if ok else None, "returns_to_zero": (int(zero) if ok else None), "steps_used": used,
           "cpu_seconds": round(time.process_time() - t0, 3)}
    with open(ck, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(rec, flush=True)
