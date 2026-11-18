"""Comparison of the statements of PROOF_43_142.md and of the direct computation in this folder with the data of the
ring-size study (read only): data/ring_size/mechanisms.csv, data/ring_size/crystal_radius.csv,
data/ring_size/sampled_reach/. Writes out/crosscheck_data.json. Needs out/g1_classes.jsonl, out/check_lemmas.json and
out/constructive_paths.json.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")


def main():
    g1 = {}
    with open(os.path.join(OUT, "g1_classes.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            g1[(r["rule"], r["n"])] = r
    with open(os.path.join(OUT, "check_lemmas.json")) as fh:
        lem = json.load(fh)
    with open(os.path.join(OUT, "constructive_paths.json")) as fh:
        paths = json.load(fh)

    # ---------------------------------------------------------------- mechanisms.csv
    with open(os.path.join(ROOT, "data", "ring_size", "mechanisms.csv"), newline="") as fh:
        mech = [r for r in csv.DictReader(fh) if r["rule"] in ("43", "142")]
    fields = ["cycles", "g1_closed", "g1_sccs", "n_selected", "gamma_min", "kstar", "k_c", "selected_cover",
              "entry_cost_max", "radius_selected_min"]
    mism = []
    compared = 0
    for r in mech:
        rule, n = int(r["rule"]), int(r["n"])
        g = g1[(rule, n)]
        four = n % 4 == 0
        pred = dict(
            cycles=g["cycles"], g1_closed=g["closed_classes"], g1_sccs=g["strong_components"],
            n_selected=1 if four else g["cycles_on_levels"],                # Theorem 1 / Theorem 2
            gamma_min=g["cycles"] - 1,                                     # Theorem A, unique closed class
            kstar=1 if four else 0,
            k_c="1-0-1-0-0-1-0-1" if four else "0-0-0-0-0-0-0-0",
            selected_cover="1346" if four else "01234567",
            entry_cost_max=(n // 4) if four else -1,                       # Proposition 3 (the study stores -1 otherwise)
            radius_selected_min=2 if four else 1)                          # radius >= 2 is stored as 2
        for f in fields:
            compared += 1
            have = r[f]
            want = pred[f]
            same = (have == want) if isinstance(want, str) else (float(have) == float(want))
            if not same:
                mism.append(dict(rule=rule, n=n, field=f, study=have, here=want))
    mech_out = dict(records=len(mech), n_min=min(int(r["n"]) for r in mech), n_max=max(int(r["n"]) for r in mech),
                    fields=fields, values_compared=compared, mismatches=mism)

    # ---------------------------------------------------------------- crystal_radius.csv
    with open(os.path.join(ROOT, "data", "ring_size", "crystal_radius.csv"), newline="") as fh:
        rad = [r for r in csv.DictReader(fh) if r["rule"] in ("43", "142")]
    t1 = {int(r["rule"]): r for r in lem["results"] if r["test"] == "T1"}
    bad = []
    for r in rad:
        rule, n = int(r["rule"]), int(r["n"])
        formula = max(1, n // 2 - 1)                                       # Proposition 2
        mine = t1[rule]["max_return_time"].get(str(n))
        if not (r["word"] == "0011" and int(r["cycle_length"]) == 4 and int(r["radius_ge2"]) == 1
                and int(r["max_return_time"]) == formula and mine == formula):
            bad.append(dict(rule=rule, n=n, study=r, formula=formula, here=mine))
    rad_out = dict(rows=len(rad), n_min=min(int(r["n"]) for r in rad), n_max=max(int(r["n"]) for r in rad),
                   rows_per_rule={str(k): sum(1 for r in rad if int(r["rule"]) == k) for k in (43, 142)},
                   rows_not_matching=bad)

    # ---------------------------------------------------------------- sampled_reach
    partC = [r for r in paths["rows"] if r["part"] == "C"]
    samp_out = dict(files=len(partC), starts=sum(r["starts"] for r in partC),
                    stored_equal=sum(r["stored_equal"] for r in partC),
                    stored_longer=sum(r["stored_longer"] for r in partC),
                    stored_shorter=sum(r["stored_shorter"] for r in partC))

    # ---------------------------------------------------------------- entry cost: study vs exhaustive search here
    e = {int(r["rule"]): r["max_entry_cost"] for r in lem["results"] if r["test"] == "E"}
    entry = []
    for r in mech:
        rule, n = int(r["rule"]), int(r["n"])
        if n % 4 == 0 and str(n) in e[rule]:
            entry.append(dict(rule=rule, n=n, study=float(r["entry_cost_max"]), here=e[rule][str(n)],
                              equal=float(r["entry_cost_max"]) == e[rule][str(n)]))

    ok = (not mism) and (not bad) and samp_out["stored_shorter"] == 0 and all(x["equal"] for x in entry)
    out = dict(script="crosscheck_data.py", all_agree=bool(ok), mechanisms=mech_out, crystal_radius=rad_out,
               sampled_reach=samp_out, entry_cost=entry)
    with open(os.path.join(OUT, "crosscheck_data.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"mechanisms.csv: {len(mech)} records, {compared} values compared, {len(mism)} mismatches")
    print(f"crystal_radius.csv: {len(rad)} rows, {len(bad)} not matching")
    print(f"sampled_reach: {samp_out}")
    print(f"entry cost rows: {len(entry)}, all equal: {all(x['equal'] for x in entry)}")
    print(f"all agree: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
