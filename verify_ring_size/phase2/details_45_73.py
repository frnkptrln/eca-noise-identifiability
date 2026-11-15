"""Details behind findings F4 (class 45) and F5 (class 73): which cycles are not selected, from the sealed sample
and the phase-2 orbit tables, and the same rows in the study's own cycle_orbits.csv.gz.
Writes out/details_45_73.json."""
import csv
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
OUT = os.path.join(HERE, "out")
sample = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(ROOT, "out", "sample.jsonl")))}


def sel_reps(rule, n):
    s = sample[(rule, n)]["selected"]
    if s["orbits_complete"]:
        return {o["rep"]: o for o in s["orbits"]}
    with open(os.path.join(ROOT, "out", "selected", "sel_r%d_n%d.tsv" % (rule, n))) as fh:
        return {r["rep"]: r for r in csv.DictReader(fh, delimiter="\t")}


def orbits(rule, n):
    with open(os.path.join(OUT, "own_orbits", "orb_r%d_n%d.csv" % (rule, n))) as fh:
        return list(csv.DictReader(fh))


study = {}
with gzip.open(os.path.join(REPO, "data", "ring_size", "cycle_orbits.csv.gz"), "rt") as fh:
    for r in csv.DictReader(fh):
        if int(r["rule"]) in (45, 73):
            study.setdefault((int(r["rule"]), int(r["n"])), []).append(r)

res = {"class45_even_n": {}, "class73": {}}
for n in range(10, 23, 2):
    s = sample[(45, n)]
    sel = sel_reps(45, n)
    uns = [o for o in orbits(45, n) if o["rep"] not in sel]
    st_uns = [r for r in study[(45, n)] if r["selected"] != "True"]
    res["class45_even_n"][str(n)] = {
        "cycles": s["n_cycles"], "selected_cycles": s["selected"]["n_cycles"], "gamma_hist": s["gamma_hist"],
        "uniform_2cycle_selected": ("0" * n) in sel,
        "uniform_2cycle_radius": int([o for o in orbits(45, n) if o["rep"] == "0" * n][0]["radius"]),
        "unselected_orbits_own": [[o["rep"], int(o["orbit_size"]), int(o["temporal_period"]), int(o["spatial_period"]), o["codes"]] for o in uns],
        "unselected_orbits_in_study_file": [[r["pattern"], int(r["orbit_size"]), int(r["gamma"])] for r in st_uns],
        "kstar": s["kstar"]}
res["class45_n_with_unselected_cycles"] = [int(n) for n, d in res["class45_even_n"].items() if d["selected_cycles"] != d["cycles"]]
for n in range(8, 23):
    s = sample[(73, n)]
    sel = sel_reps(73, n)
    st_u = [r for r in study[(73, n)] if set(r["pattern"]) == {"0"}][0]
    car = [o for o in orbits(73, n) if "7" in o["codes"]]
    res["class73"][str(n)] = {
        "kstar": s["kstar"], "cycles": s["n_cycles"], "selected_cycles": s["selected"]["n_cycles"],
        "uniform_2cycle_selected_own": ("0" * n) in sel,
        "uniform_2cycle_selected_in_study_file": st_u["selected"] == "True",
        "uniform_2cycle_gamma_in_study_file": int(st_u["gamma"]), "gamma_min": s["min_gamma"],
        "carriers_of_code_7": len(car), "selected_carriers_of_code_7": sum(o["rep"] in sel for o in car)}
res["class73_n_uniform_not_selected"] = [int(n) for n, d in res["class73"].items() if not d["uniform_2cycle_selected_own"]]
sel9 = sel_reps(73, 9)
res["class73_n9_selected_orbits"] = [[rep, o["temporal_period"], o["spatial_period"], o["n_cycles_in_orbit"]] for rep, o in sel9.items()]
res["class73_n9_all_orbits"] = [[o["rep"], int(o["temporal_period"]), int(o["spatial_period"]), o["codes"], o["rep"] in sel9] for o in orbits(73, 9)]
json.dump(res, open(os.path.join(OUT, "details_45_73.json"), "w"), indent=1)
print(res["class45_n_with_unselected_cycles"], res["class73_n_uniform_not_selected"])
print({n: (d["selected_cycles"], d["cycles"], d["unselected_orbits_own"]) for n, d in res["class45_even_n"].items() if d["selected_cycles"] != d["cycles"]})
print(res["class73_n9_all_orbits"])
print(res["class73"]["22"])
