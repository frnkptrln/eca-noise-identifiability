"""Step 2: field-by-field comparison of the sealed sample (../out/sample.jsonl, ../out/selected/) and of the
phase-2 supplement (out/extras.jsonl, out/own_orbits/) with the study's files in data/ring_size/.
Writes out/compare_sample.json (counts per field) and out/compare_mismatches.csv (one row per mismatch).
Source tags: 'sealed' = value from the sealed sample; 'supplement' = computed after the seal with own code."""
import csv
import gzip
import json
import os
import sys
import time
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P
from p2lib import K

t_start = time.process_time()
D = os.path.join(P.REPO, "data", "ring_size")
OUT = os.path.join(P.HERE, "out")
sample = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(P.ROOT, "out", "sample.jsonl")))}
extras = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(OUT, "extras.jsonl")))}

counts = defaultdict(lambda: {"compared": 0, "equal": 0, "mismatch": 0, "study_has_no_value": 0, "source": ""})
mism = []


def cmp(field, key, study, own, source, note=""):
    c = counts[field]
    c["source"] = source
    if study is None:
        c["study_has_no_value"] += 1
        return
    c["compared"] += 1
    if study == own:
        c["equal"] += 1
    else:
        c["mismatch"] += 1
        mism.append({"field": field, "rule": key[0], "n": key[1], "item": key[2] if len(key) > 2 else "",
                     "study": str(study)[:200], "own": str(own)[:200], "source": source, "note": note})


def selected_rows(rule, n):
    s = sample[(rule, n)]["selected"]
    if s["orbits_complete"]:
        return [dict(rep=o["rep"], T=o["temporal_period"], S=o["spatial_period"], size=o["n_cycles_in_orbit"],
                     codes="".join(map(str, o["codes"]))) for o in s["orbits"]]
    rows = []
    with open(os.path.join(P.ROOT, "out", "selected", "sel_r%d_n%d.tsv" % (rule, n))) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            rows.append(dict(rep=r["rep"], T=int(r["temporal_period"]), S=int(r["spatial_period"]),
                             size=int(r["n_cycles_in_orbit"]), codes=r["codes"]))
    assert len(rows) == s["n_orbits"]
    return rows


def own_orbits(rule, n):
    with open(os.path.join(OUT, "own_orbits", "orb_r%d_n%d.csv" % (rule, n))) as fh:
        return {r["rep"]: r for r in csv.DictReader(fh)}


def nan(v):
    return v is None or v == "" or v == "nan"


def fnum(v):
    return None if nan(v) else int(float(v))


def fbool(v):
    return None if nan(v) else (v == "True")


# ---------------------------------------------------------------- A. mechanisms.csv, record level
mech = {}
with open(os.path.join(D, "mechanisms.csv")) as fh:
    for r in csv.DictReader(fh):
        mech[(int(r["rule"]), int(r["n"]))] = r
keys_common = sorted(set(mech) & set(sample))
only_study = sorted(set(mech) - set(sample))
only_own = sorted(set(sample) - set(mech))
sel_cache = {}
for key in keys_common:
    rule, n = key
    st, s, ex = mech[key], sample[key], extras[key]
    oo = own_orbits(rule, n)
    sel = selected_rows(rule, n)
    sel_cache[key] = {o["rep"] for o in sel}
    selreps = sel_cache[key]
    cmp("cycles", key, int(st["cycles"]), s["n_cycles"], "sealed")
    cmp("bijective", key, int(st["bijective"]), int(s["bijective"]), "sealed")
    cmp("cycle_orbits", key, fnum(st["cycle_orbits"]), s["n_orbits"], "sealed")
    cmp("gamma_min", key, int(st["gamma_min"]), s["min_gamma"], "sealed")
    cmp("n_selected", key, int(st["n_selected"]), s["selected"]["n_cycles"], "sealed")
    cmp("selected_orbits", key, fnum(st["selected_orbits"]), s["selected"]["n_orbits"], "sealed")
    cmp("k_c", key, st["k_c"], "-".join(map(str, s["k"])), "sealed")
    cmp("kstar", key, int(st["kstar"]), s["kstar"], "sealed")
    cmp("selected_cover", key, st["selected_cover"], "".join(map(str, s["codes_joint"])), "sealed")
    cmp("g1_sccs", key, fnum(st["g1_sccs"]), s["g1"]["n_scc"], "sealed")
    cmp("g1_closed", key, fnum(st["g1_closed"]), s["g1"]["n_closed_classes"], "sealed")
    cmp("selected_eq_closed_union", key, fbool(st["selected_eq_closed_union"]),
        s["g1"]["selected_equals_union_closed"], "sealed")
    sp = ";".join(map(str, sorted({o["S"] for o in sel})))
    tp = ";".join(map(str, sorted({o["T"] for o in sel})))
    cmp("selected_spatial_periods", key, None if nan(st["selected_spatial_periods"]) else st["selected_spatial_periods"], sp, "sealed")
    cmp("selected_temporal_periods", key, None if nan(st["selected_temporal_periods"]) else st["selected_temporal_periods"], tp, "sealed")
    # radii (supplement); a single cycle has no radius: the study writes -1
    rs = [int(oo[r]["radius"]) for r in selreps]
    ro = [int(o["radius"]) for rep, o in oo.items() if rep not in selreps]
    if s["n_cycles"] == 1:
        rs = [-1]
    cmp("radius_selected_min", key, fnum(st["radius_selected_min"]), min(rs), "supplement")
    cmp("radius_selected_max", key, fnum(st["radius_selected_max"]), max(rs), "supplement")
    cmp("radius_other_min", key, fnum(st["radius_other_min"]), min(ro) if ro else -1, "supplement")
    cmp("radius_other_max", key, fnum(st["radius_other_max"]), max(ro) if ro else -1, "supplement")
    # crystal orbit: the selected set is one rotation orbit whose spatial period is smaller than n
    # (convention inferred from the study's rows; a single cycle in total does not count)
    one = len(sel) == 1 and sel[0]["S"] < n and s["n_cycles"] > 1
    cmp("crystal_orbit", key, fbool(st["crystal_orbit"]), one, "sealed")
    cmp("crystal_p", key, fnum(st["crystal_p"]), sel[0]["S"] if one else -1, "sealed")
    lb = {d["rep"]: d for d in ex["lemmaB_candidates"]}
    d = lb.get(sel[0]["rep"]) if one else None
    cmp("g2_holds", key, fbool(st["g2_holds"]), bool(d and d["g2_holds"]), "supplement")
    cmp("entry_cost_max", key, fnum(st["entry_cost_max"]), d["entry_cost_max"] if d else -1, "supplement")
    cmp("gamma_formula_ok", key, fbool(st["gamma_formula_ok"]),
        bool(d and d["g2_holds"] and s["min_gamma"] == s["n_cycles"] + d["q"] - 2), "supplement")

# ---------------------------------------------------------------- B. cycle_orbits.csv.gz, orbit level
orbs = defaultdict(list)
with gzip.open(os.path.join(D, "cycle_orbits.csv.gz"), "rt") as fh:
    for r in csv.DictReader(fh):
        orbs[(int(r["rule"]), int(r["n"]))].append(r)
n_orbit_rows = sum(len(v) for v in orbs.values())
conv = {"pattern_on_cycle_x0_first": 0, "pattern_not_on_cycle": 0, "rep_int_is_lsb_first": 0, "rep_int_other": 0,
        "rep_is_orbit_minimum_lsb_first": 0, "rep_not_orbit_minimum": 0, "drift_right_min": 0, "drift_left_min": 0,
        "drift_neither": 0, "drift_rows": 0}
cases_without_orbit_rows = [k for k in keys_common if k not in orbs]
for key in sorted(orbs):
    rule, n = key
    rows = orbs[key]
    if key not in sample:
        continue
    s = sample[key]
    oo = own_orbits(rule, n)
    selreps = sel_cache[key]
    F, cm = K.build_F(rule, n)
    m, cyc, attr, minstate, length, ccodes = K.find_cycles(n, F, cm)
    no, rot1, orb, reps, osz, omin = K.rotation_orbits(n, m, cyc, minstate)
    # minimum of every rotation orbit in the study's integer encoding (cell i = bit i)
    idx = np.nonzero(cyc >= 0)[0].astype(np.int64)
    rev = np.zeros(len(idx), np.int64)
    for b in range(n):
        rev |= ((idx >> b) & 1) << (n - 1 - b)
    minrev = np.full(no, 1 << 40, np.int64)
    np.minimum.at(minrev, orb[cyc[idx]], rev)
    seen = set()
    ghist = defaultdict(int)
    mask = (1 << n) - 1
    for r in rows:
        x = int(r["pattern"], 2)
        c = int(cyc[x])
        item = r["pattern"]
        if c < 0:
            conv["pattern_not_on_cycle"] += 1
            cmp("orbit.pattern_is_periodic_state", key + (item,), False, True, "supplement")
            continue
        conv["pattern_on_cycle_x0_first"] += 1
        o = int(orb[c])
        rep = P.bits(omin[o], n)
        if rep in seen:
            cmp("orbit.one_row_per_orbit", key + (item,), "duplicate", "unique", "supplement")
        seen.add(rep)
        own = oo[rep]
        lsb = int(r["pattern"][::-1], 2)
        if lsb == int(r["orbit_rep_min_state"]):
            conv["rep_int_is_lsb_first"] += 1
        else:
            conv["rep_int_other"] += 1
        if lsb == int(minrev[o]):
            conv["rep_is_orbit_minimum_lsb_first"] += 1
        else:
            conv["rep_not_orbit_minimum"] += 1
        cmp("orbit.orbit_size", key + (item,), int(r["orbit_size"]), int(own["orbit_size"]), "supplement")
        cmp("orbit.temporal_period", key + (item,), int(r["temporal_period"]), int(own["temporal_period"]), "supplement")
        cmp("orbit.spatial_period", key + (item,), int(r["spatial_period"]), int(own["spatial_period"]), "supplement")
        cmp("orbit.codes", key + (item,), r["codes"], own["codes"], "supplement")
        cmp("orbit.radius", key + (item,), int(r["radius"]), int(own["radius"]) if m > 1 else -1, "supplement")
        cmp("orbit.selected", key + (item,), r["selected"] == "True", rep in selreps, "sealed")
        if own["gamma"] != "":
            cmp("orbit.gamma", key + (item,), int(r["gamma"]), int(own["gamma"]), "supplement")
        ghist[int(r["gamma"])] += int(r["orbit_size"])
        # drift: s with F(x) = x rotated by s places, -1 if F(x) is not a rotation of x
        fx = int(F[x])
        right = [k for k in range(n) if (((x >> k) | (x << (n - k))) & mask) == fx]
        left = [k for k in range(n) if (((x << k) | (x >> (n - k))) & mask) == fx]
        conv["drift_rows"] += 1
        dr = int(r["drift"])
        okr = dr == (min(right) if right else -1)
        okl = dr == (min(left) if left else -1)
        conv["drift_right_min"] += okr
        conv["drift_left_min"] += okl
        conv["drift_neither"] += (not okr and not okl)
    cmp("orbit.all_own_orbits_listed", key, len(seen), no, "supplement")
    cmp("orbit.gamma_histogram_by_cycles", key, sorted(ghist.items()),
        sorted((a, b) for a, b in s["gamma_hist"]), "sealed")

# ---------------------------------------------------------------- mech.jsonl versus the csv tables (study-internal)
n_mech = 0
jl_orbit_rows = 0
for line in open(os.path.join(D, "mech.jsonl")):
    r = json.loads(line)
    key = (r["rule"], r["n"])
    n_mech += 1
    st = mech.get(key)
    cmp("mech.jsonl_vs_mechanisms.csv:record_present", key, st is not None, True, "study-internal")
    if st is None:
        continue
    for f in ["cycles", "gamma_min", "kstar", "n_selected", "k_c"]:
        cmp("mech.jsonl_vs_mechanisms.csv:" + f, key, str(r[f]), st[f], "study-internal")
    a = sorted((o["pattern"], o["gamma"], o["radius"], str(o["selected"]), o["orbit_size"]) for o in r["orbits"])
    b = sorted((o["pattern"], int(o["gamma"]), int(o["radius"]), o["selected"], int(o["orbit_size"])) for o in orbs.get(key, []))
    jl_orbit_rows += len(a)
    cmp("mech.jsonl_vs_cycle_orbits.csv.gz:orbit_rows", key, a == b, True, "study-internal")

res = {"records_study": len(mech), "records_sample": len(sample), "records_common": len(keys_common),
       "only_in_study": only_study, "only_in_sample": only_own,
       "orbit_rows_study": n_orbit_rows, "cases_with_orbit_rows": len(orbs),
       "cases_without_orbit_rows": cases_without_orbit_rows,
       "mech_jsonl_records": n_mech, "mech_jsonl_orbit_rows": jl_orbit_rows,
       "conventions": conv, "fields": dict(counts),
       "n_fields": len(counts), "n_mismatches": len(mism),
       "cpu_seconds": round(time.process_time() - t_start, 2)}
json.dump(res, open(os.path.join(OUT, "compare_sample.json"), "w"), indent=1, sort_keys=True)
with open(os.path.join(OUT, "compare_mismatches.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, ["field", "rule", "n", "item", "study", "own", "source", "note"])
    w.writeheader()
    w.writerows(mism)
print(json.dumps({k: v for k, v in res.items() if k != "fields"}, indent=0))
for f, c in sorted(counts.items()):
    print("%-48s %s" % (f, c))
