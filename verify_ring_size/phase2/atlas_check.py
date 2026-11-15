"""Step 2: the atlas (data/ring_size/atlas/) against the own sweep over all 88 classes (out/sweep88.jsonl), every
record with n <= NMAX_ATLAS that the sweep solved; selected orbits compared pattern by pattern for n <= 14.
Writes out/atlas_check.json and out/atlas_mismatches.csv."""
import csv
import gzip
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbitlib as O

HERE = O.HERE
OUT = os.path.join(HERE, "out")
D = os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "ring_size", "atlas")
SW = {22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154}
sweep = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(OUT, "sweep88.jsonl")))}
atlas = {(int(r["rule"]), int(r["n"])): r for r in csv.DictReader(open(os.path.join(D, "mechanisms_atlas.csv")))}
counts = defaultdict(lambda: [0, 0, 0])     # compared, equal, study has no value
mism = []


def cmp(field, key, study, own):
    c = counts[field]
    if study is None:
        c[2] += 1
        return
    c[0] += 1
    if study == own:
        c[1] += 1
    else:
        mism.append({"field": field, "rule": key[0], "n": key[1], "study": str(study)[:120], "own": str(own)[:120]})


def num(v):
    return None if v in ("", "nan") else int(float(v))


def canon(rule, n, pattern, T):
    """Lexicographically smallest string over all states of the cycle and all rotations."""
    x = sum(1 << i for i, ch in enumerate(pattern) if ch == "1")
    best = None
    for _ in range(T):
        s = O.to_str(x, n)
        d = s + s
        m = min(d[k:k + n] for k in range(n))
        best = m if best is None or m < best else best
        x = O.step(rule, n, x)
    assert O.to_str(x, n) == pattern, "pattern is not periodic with the stated temporal period"
    return best


orb = defaultdict(list)
with gzip.open(os.path.join(D, "cycle_orbits_atlas.csv.gz"), "rt") as fh:
    for r in csv.DictReader(fh):
        orb[(int(r["rule"]), int(r["n"]))].append(r)
compared, not_in_sweep = 0, []
classes = set()
for key in sorted(atlas):
    a = atlas[key]
    s = sweep.get(key)
    if s is None or "skipped" in s:
        not_in_sweep.append(list(key))
        continue
    compared += 1
    classes.add(key[0])
    bij = int(a["bijective"]) == 1
    cmp("cycles", key, int(a["cycles"]), s["m"])
    cmp("bijective", key, bij, s["bijective"])
    cmp("gamma_min", key, int(a["gamma_min"]), s["gmin"])
    cmp("n_selected", key, int(a["n_selected"]), s["n_selected"])
    cmp("k_c", key, a["k_c"], "-".join(map(str, s["k"])))
    cmp("kstar", key, int(a["kstar"]), s["kstar"])
    cmp("selected_cover", key, a["selected_cover"].zfill(1) if a["selected_cover"] != "" else "", s["cover"])
    cmp("cycle_orbits", key, num(a["cycle_orbits"]), s["n_orbits"])
    cmp("selected_orbits", key, num(a["selected_orbits"]), s["n_selected_orbits"])
    cmp("g1_sccs", key, num(a["g1_sccs"]), s["n_scc"])
    cmp("g1_closed", key, num(a["g1_closed"]), s["n_closed"])
    cmp("selected_eq_closed_union", key, None if a["selected_eq_closed_union"] == "" else a["selected_eq_closed_union"] == "True",
        s["S_equals_union_of_all_closed"])
    cmp("selected_spatial_periods", key, a["selected_spatial_periods"] or None, ";".join(map(str, s["sel_spatial"])))
    cmp("selected_temporal_periods", key, a["selected_temporal_periods"] or None, ";".join(map(str, s["sel_temporal"])))
    if s["m"] > 1 and not bij:
        cmp("radius_selected_min", key, num(a["radius_selected_min"]), s["radius_sel"][0])
        cmp("radius_selected_max", key, num(a["radius_selected_max"]), s["radius_sel"][1])
        cmp("radius_other_min", key, num(a["radius_other_min"]), s["radius_other"][0])
        cmp("radius_other_max", key, num(a["radius_other_max"]), s["radius_other"][1])
    if key[1] <= 14 and not bij and s["sel_reps"] is not None:
        reps = sorted(canon(key[0], key[1], r["pattern"], int(r["temporal_period"])) for r in orb[key] if r["selected"] == "True")
        cmp("selected_orbit_patterns_n_le_14", key, reps, sorted(s["sel_reps"]))
res = {"atlas_records": len(atlas), "records_compared": compared, "records_not_in_own_sweep": not_in_sweep,
       "classes_compared": len(classes), "non_switching_classes_compared": len(classes - SW),
       "n_range_compared": [min(k[1] for k in atlas if k in sweep and "skipped" not in sweep[k]),
                            max(k[1] for k in atlas if k in sweep and "skipped" not in sweep[k])],
       "fields": {k: {"compared": v[0], "equal": v[1], "study_has_no_value": v[2]} for k, v in sorted(counts.items())},
       "n_mismatches": len(mism),
       "mismatch_fields": {f: sum(1 for m in mism if m["field"] == f) for f in sorted({m["field"] for m in mism})},
       "gamma_min_mismatches_all_bijective": all(sweep[(m["rule"], m["n"])]["bijective"] for m in mism if m["field"] == "gamma_min")}
json.dump(res, open(os.path.join(OUT, "atlas_check.json"), "w"), indent=1)
with open(os.path.join(OUT, "atlas_mismatches.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, ["field", "rule", "n", "study", "own"])
    w.writeheader()
    w.writerows(mism)
print(json.dumps(res, indent=0)[:4000])
