"""Step 3 (c): own seed orbits (out/seed_orbits_own.jsonl) against data/ring_size/seed_orbits.csv and against the
sentences of the report.  Writes out/seed_compare.json and out/seed_orbits_own.csv."""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
D = os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "ring_size")
CAP = 400000
best = {}
cpu = 0.0
for l in open(os.path.join(OUT, "seed_orbits_own.jsonl")):
    r = json.loads(l)
    cpu += r["cpu_seconds"]
    k = (r["rule"], r["n"])
    if k not in best or (r["determined"] and not best[k]["determined"]) or (not best[k]["determined"] and r["budget"] > best[k]["budget"]):
        best[k] = r
study = {(int(r["rule"]), int(r["n"])): r for r in csv.DictReader(open(os.path.join(D, "seed_orbits.csv")))}


def pow2(n):
    return n & (n - 1) == 0


def by_proof(rule, n):
    """Decision without simulation, where a proof applies (None otherwise)."""
    if rule in (154, 26) and n % 2 == 0:
        return int(pow2(n)), "Proposition R154 (even n: orbit equals the rule-90 orbit)"
    if rule == 154 and n % 2 == 1:
        return 0, "Lemma P: F bijective at odd n, so e_0 never maps to the fixed point 0"
    if rule == 26 and n % 2 == 1:
        return 0, "at odd n the only preimages of 0 under rule 26 are 0 and 1^n, and 1^n has no preimage (finding note)"
    if rule == 22 and n % 4 == 0:
        return int(pow2(n)), "Proposition R22 (4 | n)"
    return None, ""


rows, diffs = [], []
summ = {}
for rule in (22, 26, 122, 154):
    s = {"n_values": 0, "study_capped": [], "own_undetermined": [], "study_capped_settled_by_own_simulation": [],
         "study_capped_settled_by_proof_only": [], "study_capped_open": [], "returns_own": [],
         "returns_study": [], "proof_vs_simulation_conflicts": [], "study_determined_rows_equal": 0,
         "study_determined_rows": 0, "cap_classification_conflicts": []}
    for n in range(4, 257):
        o, st = best[(rule, n)], study[(rule, n)]
        s["n_values"] += 1
        pr, why = by_proof(rule, n)
        capped = int(st["capped"]) == 1
        row = {"rule": rule, "n": n, "determined": int(o["determined"]), "returns_to_zero": o["returns_to_zero"],
               "transient": o["transient"], "limit_period": o["limit_period"], "budget": o["budget"],
               "decided_by_proof": pr, "proof": why, "study_capped": int(capped)}
        rows.append(row)
        if o["determined"]:
            if o["returns_to_zero"]:
                s["returns_own"].append(n)
            if pr is not None and pr != o["returns_to_zero"]:
                s["proof_vs_simulation_conflicts"].append(n)
        else:
            s["own_undetermined"].append(n)
        if not capped:
            s["study_determined_rows"] += 1
            eq = (o["determined"] and int(float(st["returns_to_zero"])) == o["returns_to_zero"]
                  and int(st["transient"]) == o["transient"] and int(st["limit_period"]) == o["limit_period"])
            s["study_determined_rows_equal"] += int(eq)
            if int(float(st["returns_to_zero"])) == 1:
                s["returns_study"].append(n)
            if not eq:
                diffs.append({"rule": rule, "n": n, "study": [st["returns_to_zero"], st["transient"], st["limit_period"]],
                              "own": [o["returns_to_zero"], o["transient"], o["limit_period"]]})
            if o["determined"] and o["transient"] + o["limit_period"] > CAP + 1:
                s["cap_classification_conflicts"].append(n)
        else:
            s["study_capped"].append(n)
            if o["determined"]:
                s["study_capped_settled_by_own_simulation"].append([n, o["returns_to_zero"], o["transient"], o["limit_period"]])
                if o["transient"] + o["limit_period"] <= CAP:
                    s["cap_classification_conflicts"].append(n)
            elif pr is not None:
                s["study_capped_settled_by_proof_only"].append(n)
            else:
                s["study_capped_open"].append(n)
    s["final_return_set_complete"] = len(s["study_capped_open"]) == 0
    summ[str(rule)] = s
with open(os.path.join(OUT, "seed_orbits_own.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0]))
    w.writeheader()
    w.writerows(rows)
res = {"cap_of_the_study": CAP, "rows": len(rows), "differences_on_study_determined_rows": diffs,
       "by_rule": summ, "cpu_seconds_all_passes": round(cpu, 1)}
json.dump(res, open(os.path.join(OUT, "seed_compare.json"), "w"), indent=1)
for rule, s in summ.items():
    print(rule, {k: (v if not isinstance(v, list) or len(v) < 40 else str(len(v)) + " items") for k, v in s.items()})
print(len(diffs), res["cpu_seconds_all_passes"])
