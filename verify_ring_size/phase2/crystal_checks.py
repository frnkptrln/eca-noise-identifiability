"""Step 3 (b): healing times on the line (Lemma H input) and the crystal radius for p | n up to 400, own code.
Compared with data/ring_size/lightcone.csv and crystal_radius.csv.  Writes out/crystal_checks.json,
out/crystal_radius_own.csv, out/lightcone_own.csv."""
import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbitlib as O

OUT = os.path.join(O.HERE, "out")
D = os.path.join(os.path.dirname(os.path.dirname(O.HERE)), "data", "ring_size")
t0 = time.process_time()


def crystal_cycle(rule, word, n):
    x0 = O.word_state(word, n)
    cyc = [x0]
    x = O.step(rule, n, x0)
    while x != x0:
        cyc.append(x)
        x = O.step(rule, n, x)
        assert len(cyc) <= 4 * n, "the word is not on a cycle"
    return cyc


def flips_return(rule, word, n, positions, tmax=None):
    """For every state of the crystal cycle and every flipped cell in `positions`: first time the orbit is back on
    the crystal cycle (None if it enters another cycle, or does not return within tmax when tmax is given)."""
    cyc = crystal_cycle(rule, word, n)
    cset = set(cyc)
    times = []
    for x in cyc:
        for j in positions:
            y = x ^ (1 << j)
            t = 0
            seen = set()
            while y not in cset:
                if (tmax is not None and t >= tmax) or y in seen:
                    t = None
                    break
                seen.add(y)
                y = O.step(rule, n, y)
                t += 1
            times.append(t)
    return len(cyc), times


# ---- (b1) healing on the line: ring of size N >= 401 (multiple of p), t <= 200
lc_rows = []
study_lc = list(csv.DictReader(open(os.path.join(D, "lightcone.csv"))))
lc_cmp = []
for r in study_lc:
    rule, word, p = int(r["rule"]), r["word"], int(r["p"])
    N = p * ((401 + p - 1) // p)
    L, times = flips_return(rule, word, N, range(p), tmax=200)
    healed = all(t is not None for t in times)
    tau = max(times) if healed else None
    row = {"rule": rule, "word": word, "p": p, "cycle_length": L, "N": N, "healed": healed,
           "tau": tau, "n0": (2 * tau + 1) if healed else None,
           "flips_not_healed_within_200": sum(t is None for t in times), "flips": len(times)}
    lc_rows.append(row)
    lc_cmp.append({"rule": rule, "word": word,
                   "equal": (str(healed) == r["healed"] and (r["tau"] or None) == (str(tau) if tau is not None else None)
                             and int(r["cycle_length"]) == L and int(r["N"]) == N
                             and (r["n0"] or None) == (str(row["n0"]) if row["n0"] is not None else None))})
with open(os.path.join(OUT, "lightcone_own.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(lc_rows[0]))
    w.writeheader()
    w.writerows(lc_rows)

# rule 94, crystal 011 on the line: the three single flips in detail (space-time rows around the flip)
detail94 = []
N = 402
x0 = O.word_state("011", N)
for j in range(3):
    y = x0 ^ (1 << (201 + j))          # cells 201, 202, 203: word positions 0, 1, 2
    t = 0
    rows = []
    while y != x0 and t < 50:
        d = y ^ x0
        cells = [i for i in range(N) if (d >> i) & 1]
        rows.append({"t": t, "differing_cells": cells})
        y = O.step(94, N, y)
        t += 1
    detail94.append({"flipped_word_position": j, "heal_time": t, "differences": rows})

# ---- (b2) crystal radius on rings p | n up to 400
own_rows = []
sym_checks = 0
sym_bad = 0
for rule, word in ((94, "011"), (43, "0011"), (142, "0011")):
    p = len(word)
    for n in range(p, 401, p):
        L, times = flips_return(rule, word, n, range(min(p, n)))
        if n <= 64:   # all n cells, to confirm that p flip positions suffice (translation by p)
            L2, t2 = flips_return(rule, word, n, range(n))
            sym_checks += 1
            sym_bad += not (L2 == L and all(t is not None for t in t2) == all(t is not None for t in times)
                            and max((t for t in t2 if t is not None), default=0) == max((t for t in times if t is not None), default=0))
        ok = all(t is not None for t in times)
        own_rows.append({"rule": rule, "word": word, "n": n, "cycle_length": L, "radius_ge2": int(ok),
                         "max_return_time": max((t for t in times if t is not None), default=0),
                         "flips_leaving": sum(t is None for t in times)})
with open(os.path.join(OUT, "crystal_radius_own.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(own_rows[0]))
    w.writeheader()
    w.writerows(own_rows)
study = {(int(r["rule"]), int(r["n"])): r for r in csv.DictReader(open(os.path.join(D, "crystal_radius.csv")))}
diff = []
for r in own_rows:
    s = study.get((r["rule"], r["n"]))
    if s is None:
        diff.append({"rule": r["rule"], "n": r["n"], "what": "row missing in the study file"})
        continue
    for f in ("cycle_length", "radius_ge2", "max_return_time"):
        if int(s[f]) != r[f]:
            diff.append({"rule": r["rule"], "n": r["n"], "what": f, "study": s[f], "own": r[f]})
res = {
    "lightcone": {"rows": lc_rows, "comparison_with_study": lc_cmp, "all_equal": all(c["equal"] for c in lc_cmp)},
    "rule94_line_flips": detail94,
    "crystal_radius": {
        "rows_own": len(own_rows), "rows_study": len(study), "differences": diff,
        "radius_lt2": [[r["rule"], r["n"]] for r in own_rows if not r["radius_ge2"]],
        "rule94_radius_ge2_all_3_divides_n_from_6_to_399": all(r["radius_ge2"] for r in own_rows if r["rule"] == 94 and r["n"] >= 6),
        "rule94_max_return_time_n_ge_6": sorted({r["max_return_time"] for r in own_rows if r["rule"] == 94 and r["n"] >= 6}),
        "rule43_142_radius_ge2_all_4_divides_n_to_400": all(r["radius_ge2"] for r in own_rows if r["rule"] in (43, 142)),
        "rule43_max_return_time_first_last": [[r["n"], r["max_return_time"]] for r in own_rows if r["rule"] == 43][:3]
                                             + [[r["n"], r["max_return_time"]] for r in own_rows if r["rule"] == 43][-2:],
        "return_time_grows_linearly_43": all(r["max_return_time"] >= r["n"] // 4 for r in own_rows if r["rule"] == 43 and r["n"] >= 8),
        "translation_symmetry_checks_n_le_64": sym_checks, "translation_symmetry_failures": sym_bad},
    "cpu_seconds": round(time.process_time() - t0, 2)}
json.dump(res, open(os.path.join(OUT, "crystal_checks.json"), "w"), indent=1)
print(json.dumps(res["lightcone"]["comparison_with_study"]), res["lightcone"]["all_equal"])
print(json.dumps(res["crystal_radius"]))
print([(d["flipped_word_position"], d["heal_time"]) for d in detail94], res["cpu_seconds"])
