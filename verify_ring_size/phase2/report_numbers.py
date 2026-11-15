"""Step 2, part D: every number of report_ring_size.md that the sealed sample (plus the phase-2 supplement and
the own small-n sweep) can decide.  Writes out/report_numbers.json: one entry per check with the report line,
the report value, the own value, the own source file and equal true/false."""
import csv
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P

OUT = os.path.join(P.HERE, "out")
D = os.path.join(P.REPO, "data", "ring_size")
lines = open(os.path.join(P.REPO, "report_ring_size.md")).read().split("\n")
sample = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(P.ROOT, "out", "sample.jsonl")))}
extras = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(OUT, "extras.jsonl")))}
sweep = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(OUT, "sweep88.jsonl")))}
derived = json.load(open(os.path.join(OUT, "compare_derived.json")))
RULES = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]
checks = []


def lno(pattern, start=0):
    for i in range(start, len(lines)):
        if re.search(pattern, lines[i]):
            return i + 1
    raise KeyError(pattern)


def add(cid, line, statement, report, own, source):
    checks.append({"id": cid, "line": line, "statement": statement, "report": report, "own": own,
                   "source": source, "equal": report == own})


def table_at(header_pattern):
    i = lno(header_pattern) - 1
    hdr = [c.strip() for c in lines[i].strip().strip("|").split("|")]
    rows = []
    j = i + 2
    while j < len(lines) and lines[j].startswith("|"):
        rows.append((j + 1, [c.strip() for c in lines[j].replace("\\|", "/").strip().strip("|").split("|")]))
        j += 1
    return hdr, rows


def sel_rows(rule, n):
    s = sample[(rule, n)]["selected"]
    if s["orbits_complete"]:
        return [dict(rep=o["rep"], T=o["temporal_period"], S=o["spatial_period"],
                     codes="".join(map(str, o["codes"]))) for o in s["orbits"]]
    with open(os.path.join(P.ROOT, "out", "selected", "sel_r%d_n%d.tsv" % (rule, n))) as fh:
        return [dict(rep=r["rep"], T=int(r["temporal_period"]), S=int(r["spatial_period"]), codes=r["codes"])
                for r in csv.DictReader(fh, delimiter="\t")]


def own_orbits(rule, n):
    with open(os.path.join(OUT, "own_orbits", "orb_r%d_n%d.csv" % (rule, n))) as fh:
        return {r["rep"]: r for r in csv.DictReader(fh)}


# ---- k* table (line 186 ff.)
hdr, rows = table_at(r"^\| class \| 4 \| 5 \| 6")
ns = [int(h) for h in hdr[1:]]
n_cells = {"sealed": [0, 0], "sweep": [0, 0]}
for ln, cells in rows:
    rule = int(cells[0])
    for n, v in zip(ns, cells[1:]):
        if n >= 8:
            own = str(sample[(rule, n)]["kstar"]) if (rule, n) in sample else "."
            src = "sealed"
            add("kstar_table", ln, "k* class %d n=%d" % (rule, n), v, own, "../out/sample.jsonl")
        else:
            own = str(sweep[(rule, n)]["kstar"])
            src = "sweep"
            add("kstar_table_n4_7", ln, "k* class %d n=%d" % (rule, n), v, own, "out/sweep88.jsonl")
        n_cells[src][0] += 1
        n_cells[src][1] += int(v == own)
    # the same k* for n = 8..17 from the sweep (second own computation)
    for n in range(8, 18):
        if (rule, n) in sweep and "kstar" in sweep[(rule, n)]:
            add("kstar_sweep_vs_sample", ln, "own sweep k* equals sealed sample, class %d n=%d" % (rule, n),
                sample[(rule, n)]["kstar"], sweep[(rule, n)]["kstar"], "out/sweep88.jsonl")

# ---- Section 4: 180 non-bijective records, 175 with a single closed class
ln = lno(r"^In all 180 non-bijective")
nb = [s for s in sample.values() if not s["bijective"]]
add("sec4_nonbijective_records", ln, "non-bijective (rule, n) records, n = 8..22", 180, len(nb), "../out/sample.jsonl")
add("sec4_selected_equals_union_closed", ln, "records among them with selected set = union of all closed classes",
    180, sum(s["g1"]["selected_equals_union_closed"] for s in nb), "../out/sample.jsonl")
add("sec4_single_closed_class", ln + 2, "records among them with a single closed class", 175,
    sum(s["g1"]["n_closed_classes"] == 1 for s in nb), "../out/sample.jsonl")
ln = lno(r"^432 \(rule, n\) pairs")
add("sec3_verifier_pairs", ln, "432 pairs = all 88 classes at n = 4..8 plus 13 classes at n = 9, 10 (88*5 + 13*2)",
    432, 88 * 5 + 13 * 2, "arithmetic; out/compare_derived.json (verify_mech_files)")
ln = lno(r"gamma_min, k_c and k\* for all 169")
add("sec3_169_pairs", ln, "13 classes x n = 8..20", 169, sum(1 for k in sample if k[1] <= 20), "../out/sample.jsonl")

# ---- 5.1 table
hdr, rows = table_at(r"^\| class \| n \| cycles \| q \(selected\)")
for ln, c in rows:
    rule, n = int(c[0]), int(c[1])
    s, ex = sample[(rule, n)], extras[(rule, n)]
    sel = sel_rows(rule, n)
    oo = own_orbits(rule, n)
    lb = {d["rep"]: d for d in ex["lemmaB_candidates"]}.get(sel[0]["rep"]) if len(sel) == 1 else None
    others = [int(o["radius"]) for rep, o in oo.items() if rep != sel[0]["rep"]]
    own = [str(s["n_cycles"]), str(s["selected"]["n_cycles"]), str(oo[sel[0]["rep"]]["radius"]), str(max(others)),
           str(lb["entry_cost_max"]) if lb else "?", str(bool(lb and lb["g2_holds"])), str(s["min_gamma"]),
           str(s["n_cycles"] + s["selected"]["n_cycles"] - 2)]
    for h, rv, ov in zip(hdr[2:], c[2:], own):
        add("table_5_1", ln, "class %d n=%d: %s" % (rule, n, h), rv, ov, "../out/sample.jsonl + out/extras.jsonl + out/own_orbits/")
# completeness of 5.1: all (rule, n) with p | n for classes 94 (p=3), 43, 142 (p=4) in n = 8..22
want = sorted([(94, n) for n in range(9, 23, 3)] + [(r, n) for r in (43, 142) for n in range(8, 23, 4)])
add("table_5_1_rows", rows[0][0], "rows = all p | n in 8..22 for classes 94, 43, 142", want,
    sorted((int(c[0]), int(c[1])) for _, c in rows), "enumeration")
# 5.1 text: crystals and codes
ln = lno(r"Class 94: the three phases of the fixed point")
ok94 = all(len(sel_rows(94, n)) == 1 and sel_rows(94, n)[0]["rep"] == "011" * (n // 3) and sel_rows(94, n)[0]["T"] == 1
           and sel_rows(94, n)[0]["codes"] == "356" and sample[(94, n)]["selected"]["n_cycles"] == 3 for n in range(9, 23, 3))
add("sec5_1_class94_crystal", ln, "94, 3|n: selected = 3 phases of fixed point (011)^(n/3), codes 3,5,6", True, ok94, "../out/sample.jsonl")
ok43 = all(len(sel_rows(r, n)) == 1 and sel_rows(r, n)[0]["rep"] == "0011" * (n // 4) and sel_rows(r, n)[0]["T"] == 4
           and sel_rows(r, n)[0]["codes"] == "1346" and sample[(r, n)]["selected"]["n_cycles"] == 1
           for r in (43, 142) for n in range(8, 23, 4))
add("sec5_1_class43_142_crystal", ln + 1, "43/142, 4|n: selected = one cycle (0011)^(n/4), T = 4, codes 1,3,4,6", True, ok43, "../out/sample.jsonl")
agree = [c for c in range(8) if ((43 >> c) & 1) == ((142 >> c) & 1)]
add("sec5_1_rules_43_142_agree", ln + 2, "codes on which rules 43 and 142 agree", [1, 3, 4, 6], agree, "rule tables")
ln = lno(r"^\* At 3 ∤ n no cycle of class 94 has its codes within")
bad = 0
for n in range(8, 23):
    if n % 3:
        bad += sum(set(o["codes"]) <= set("356") for o in own_orbits(94, n).values())
add("sec5_1_no_356_cycle", ln, "94, 3 does not divide n (8..22): cycles with codes within {3,5,6}", 0, bad, "out/own_orbits/")
ln = lno(r"computed range G1 then has a single closed class that covers all eight codes")
ok = all(sample[(r, n)]["g1"]["n_closed_classes"] == 1 and sample[(r, n)]["codes_missing"] == [] and sample[(r, n)]["kstar"] == 0
         for r, p in ((94, 3), (43, 4), (142, 4)) for n in range(8, 23) if n % p)
add("sec5_1_other_direction", ln, "94/43/142, p does not divide n (8..22): single closed class, all codes, k* = 0", True, ok, "../out/sample.jsonl")

# ---- 5.2 table (class 35)
hdr, rows = table_at(r"^\| n \| a0 \| selected_a")
law = derived["rule35_blocks"]["law_by_n"]
for ln, c in rows:
    n = c[0]
    L = law[n]
    own = [str((2 * int(n)) % 3), ",".join(map(str, L["sel_a"])), ",".join(map(str, L["notsel_a"])),
           str(int(L["code5_selected"] == 0))]
    for h, rv, ov in zip(hdr[1:], c[1:], own):
        add("table_5_2", ln, "class 35 n=%s: %s" % (n, h), rv, ov, "out/compare_derived.json (rule35_blocks.law_by_n)")
ln = lno(r"every cycle containing 101 is a travelling word over the blocks 10 and 100")
add("sec5_2_block_law", ln, "violations of the block law of 5.2 over n = 8..22 (code-5 cycle not a {10,100}-word with a>=1; "
    "a state of a family cycle not such a word; non-family cycle not selected; selected a != a0 or unselected a = a0)", 0,
    sum(L["code5_not_family"] + L["family_state_not_word"] + L["nonfamily_not_selected"] + L["family_a_ge1_without_code5"]
        + int(L["sel_a"] != [(2 * int(n)) % 3]) + int((2 * int(n)) % 3 in L["notsel_a"]) for n, L in law.items()),
    "out/compare_derived.json")

# ---- 5.3
ln = lno(r"over the 59 \(rule, n\) pairs")
z = derived["zero_mechanism"]
add("sec5_3_59_pairs", ln, "pairs of classes 22, 26, 122, 154 in n = 8..22", 59, z["pairs_22_26_122_154"], "out/compare_derived.json")
add("sec5_3_coincide", ln, "pairs where 'seed orbit returns to 0' equals '0 selected alone'", 59, z["coincide_22_26_122_154"], "out/compare_derived.json")
add("sec5_3_lemmaB_zero", ln - 1, "(rule, n) in n = 8..22 with the zero state selected alone / with Lemma B holding for A = {0} "
    "(the study's own g2_holds column has the same count)", "all", "%d of %d (the other %d are maps with a single cycle: rules 60, 90 at n = 8, 16)"
    % (z["fields_equal"]["zero_alone_and_lemmaB"], z["fields_equal"]["zero_alone_cases"], z["fields_equal"]["zero_alone_single_cycle_map"]),
    "out/compare_derived.json")
ln = lno(r"only one \(31 and 4081 cycles")
g = derived["g1_distance_154"]["own"]
add("sec5_3_154_cycles", ln, "154: cycles at n = 8, 16", [31, 4081], [g["8"]["cycles"], g["16"]["cycles"]], "out/compare_derived.json")
add("sec5_3_154_radius", ln, "154 at n = 8, 16: number of cycles with radius >= 2 (only the zero state)", [1, 1],
    [g["8"]["cycles_radius_ge2"], g["16"]["cycles_radius_ge2"]], "out/compare_derived.json")
add("sec5_3_154_maxdist", ln + 1, "154: maximum G1 distance to 0 at n = 8, 16; unreachable cycles", [4, 8, 0, 0],
    [g["8"]["max_distance"], g["16"]["max_distance"], g["8"]["unreachable"], g["16"]["unreachable"]], "out/compare_derived.json")
add("sec5_3_154_spearman", ln + 2, "154: Spearman(mean ones, distance) at n = 8, 16 (2 decimals)", [0.94, 0.96],
    [round(g["8"]["spearman_mean_ones_vs_distance"], 2), round(g["16"]["spearman_mean_ones_vs_distance"], 2)], "out/compare_derived.json")
add("sec5_3_154_gamma", ln + 2, "154: gamma_min = m - 1 at n = 8, 16", True,
    all(sample[(154, n)]["min_gamma"] == sample[(154, n)]["n_cycles"] - 1 for n in (8, 16)), "../out/sample.jsonl")
ln = lno(r"cycles form one strongly connected G1 and are all selected")
ev = [n for n in range(10, 21, 2) if n != 16]
add("sec5_3_154_even", ln, "154, even n <= 20 not a power of two: one strongly connected G1, all cycles selected, n list",
    [10, 12, 14, 18, 20], [n for n in ev if sample[(154, n)]["g1"]["n_scc"] == 1
                           and sample[(154, n)]["selected"]["n_cycles"] == sample[(154, n)]["n_cycles"]], "../out/sample.jsonl")
ln = lno(r"^Class 26 at n = 2\^k is the same mechanism")
add("sec5_3_26_n16", ln, "26, n = 16: zero state alone, k* = 2; n = 8: zero state alone", True,
    sample[(26, 16)]["kstar"] == 2 and [r["rep"] for r in sel_rows(26, 16)] == ["0" * 16] and [r["rep"] for r in sel_rows(26, 8)] == ["0" * 8],
    "../out/sample.jsonl")

# ---- 5.4 (class 122)
ln = lno(r"The only cycle carrying code 2 \(010\) is the checkerboard")
car = {n: [rep for rep, o in own_orbits(122, n).items() if "2" in o["codes"]] for n in range(8, 23)}
add("sec5_4_only_carrier", ln, "122: carriers of code 2 are exactly the checkerboard at even n and none at odd n (n = 8..22)", True,
    all(car[n] == (["01" * (n // 2)] if n % 2 == 0 else []) for n in car), "out/own_orbits/")
selcb = [n for n in range(8, 23, 2) if "01" * (n // 2) in {r["rep"] for r in sel_rows(122, n)}]
add("sec5_4_checkerboard_selected", ln + 2, "122: n with the checkerboard selected", [8, 12, 14, 16, 20, 22], selcb, "../out/sample.jsonl")
add("sec5_4_checkerboard_not_selected", ln + 2, "122: even n with the checkerboard not selected", [10, 18],
    [n for n in range(8, 23, 2) if n not in selcb], "../out/sample.jsonl")
add("sec5_4_n14", ln + 3, "122, n = 14: selected = zero state and checkerboard, codes 0, 2, 5", True,
    sorted(r["rep"] for r in sel_rows(122, 14)) == ["0" * 14, "01" * 7] and sample[(122, 14)]["codes_joint"] == [0, 2, 5], "../out/sample.jsonl")
add("sec5_4_kstar0_iff_4_divides_n_fails_at_22", ln + 3, "122: n in 8..22 where (k* = 0) differs from (4 | n)", [22],
    [n for n in range(8, 23) if (sample[(122, n)]["kstar"] == 0) != (n % 4 == 0)], "../out/sample.jsonl")
add("sec5_4_code2_missing_odd", ln + 1, "122: odd n in 8..22 where code 2 is NOT missing from the selected set", [],
    [n for n in range(9, 23, 2) if 2 not in sample[(122, n)]["codes_missing"]], "../out/sample.jsonl")

# ---- 5.5
ln = lno(r"^\* \*\*22\.\*\* Every switch in n = 4\.\.22")
k1 = [n for n in range(4, 23) if (sample[(22, n)]["kstar"] if n >= 8 else sweep[(22, n)]["kstar"]) == 1]
add("sec5_5_22_kstar1", ln + 1, "22: n in 4..22 with k* = 1", [4, 5, 6, 7, 8, 14, 15, 16], k1, "../out/sample.jsonl, out/sweep88.jsonl")
add("sec5_5_22_kstar_values", ln + 1, "22: all k* in 4..22 are 0 or 1", True,
    all((sample[(22, n)]["kstar"] if n >= 8 else sweep[(22, n)]["kstar"]) in (0, 1) for n in range(4, 23)), "same")
za = [n for n in range(4, 23) if (([r["rep"] for r in sel_rows(22, n)] if n >= 8 else sweep[(22, n)]["sel_reps"]) == ["0" * n])]
add("sec5_5_22_zero_alone", ln + 2, "22: n in 4..22 with the zero state selected alone", [4, 5, 6, 7, 8, 14, 15, 16], za, "same")
ln = lno(r"^\* \*\*26\.\*\* At n = 2\^k")
oth = [n for n in range(8, 23) if sample[(26, n)]["kstar"] >= 1 and n not in (8, 16)]
add("sec5_5_26_missing7", ln, "26: n with k* >= 1 other than 8, 16, and whether the missing code is exactly 7 there",
    True, all(sample[(26, n)]["codes_missing"] == [7] for n in oth), "../out/sample.jsonl")
selcar = [n for n in range(9, 22) if any("7" in r["codes"] for r in sel_rows(26, n))]
add("sec5_5_26_mod3", ln + 2, "26: n in 9..21 with a selected carrier of code 7", [n for n in range(9, 22) if n % 3 == 2], selcar, "../out/sample.jsonl")
add("sec5_5_26_n22", ln + 2, "26, n = 22: k* = 0 and a selected carrier of code 7 exists", True,
    sample[(26, 22)]["kstar"] == 0 and any("7" in r["codes"] for r in sel_rows(26, 22)), "../out/sample.jsonl")
ln = lno(r"^\* \*\*37\.\*\* Codes 2 and 5 are missing except")
add("sec5_5_37_missing", ln, "37: n in 8..22 where codes 2 and 5 are not both missing", [11, 12, 17, 18],
    [n for n in range(8, 23) if not {2, 5} <= set(sample[(37, n)]["codes_missing"])], "../out/sample.jsonl")
add("sec5_5_37_missing_exact", ln, "37: at all other n the missing codes are exactly {2, 5}", True,
    all(sample[(37, n)]["codes_missing"] == [2, 5] for n in range(8, 23) if n not in (11, 12, 17, 18)), "../out/sample.jsonl")
add("sec5_5_37_mod6", ln, "37: n in 8..22 with k* = 0", [n for n in range(8, 23) if n % 6 in (0, 5)],
    [n for n in range(8, 23) if sample[(37, n)]["kstar"] == 0], "../out/sample.jsonl")
tp = {n: sorted({r["T"] for r in sel_rows(37, n) if set("25") & set(r["codes"])}) for n in (11, 12, 17, 18)}
add("sec5_5_37_periods", ln + 2, "37: temporal periods of the selected carriers of code 2 or 5 lie between 6 and 3n (n = 11, 12, 17, 18)",
    True, all(min(v) >= 6 and max(v) <= 3 * n for n, v in tp.items()), "../out/sample.jsonl; own values: %s" % json.dumps(tp))
ln = lno(r"^\* \*\*45\.\*\* Odd n: bijective")
s8 = sel_rows(45, 8)
add("sec5_5_45_n8", ln, "45, n = 8: uniform 2-cycle selected alone, radius 2, codes 0 and 7", True,
    len(s8) == 1 and s8[0]["rep"] == "0" * 8 and s8[0]["T"] == 2 and s8[0]["codes"] == "07" and own_orbits(45, 8)["0" * 8]["radius"] == "2", "../out/sample.jsonl, out/own_orbits/")
add("sec5_5_45_even", ln + 1, "45, even n in 10..22: uniform 2-cycle has radius 1 and all cycles are selected", True,
    all(own_orbits(45, n)["0" * n]["radius"] == "1" and sample[(45, n)]["selected"]["n_cycles"] == sample[(45, n)]["n_cycles"]
        for n in range(10, 23, 2)), "same")
add("sec5_5_45_odd_bijective", ln, "45, odd n in 9..21: F bijective (brute force), k* = 0", True,
    all(sample[(45, n)]["bijective"] and sample[(45, n)]["kstar"] == 0 for n in range(9, 22, 2)), "../out/sample.jsonl")
ln = lno(r"^\* \*\*73\.\*\* The only switch for n >= 8 is n = 9")
add("sec5_5_73_switch", ln, "73: n in 8..22 with k* >= 1", [9], [n for n in range(8, 23) if sample[(73, n)]["kstar"] >= 1], "../out/sample.jsonl")
add("sec5_5_73_uniform", ln, "73: n in 8..22 where the uniform 2-cycle is not selected", [9],
    [n for n in range(8, 23) if "0" * n not in {r["rep"] for r in sel_rows(73, n)}], "../out/sample.jsonl")
add("sec5_5_73_n9", ln + 1, "73, n = 9: missing code 7; selected cycles include temporal period 3", True,
    sample[(73, 9)]["codes_missing"] == [7] and 3 in {r["T"] for r in sel_rows(73, 9)}, "../out/sample.jsonl")

# ---- Section 9, cost line (from the study's own mech_cost.csv; arithmetic only)
ln = lno(r"^Cost \(2 worker processes")
mc = list(csv.DictReader(open(os.path.join(D, "mech_cost.csv"))))
tot = sum(float(r["cost_seconds"]) for r in mc)
big = max(mc, key=lambda r: float(r["cost_seconds"]))
add("sec9_jobs", ln, "mechanism jobs in mech_cost.csv", 194, len(mc), "data/ring_size/mech_cost.csv (study file)")
add("sec9_total_hours", ln, "sum of cost_seconds in hours, 1 decimal (the report calls it CPU; the column is wall time, see step 6)",
    1.9, round(tot / 3600, 1), "data/ring_size/mech_cost.csv (study file)")
add("sec9_longest", ln, "longest job: minutes, rule, n", [25, 35, 22], [round(float(big["cost_seconds"]) / 60), int(big["rule"]), int(big["n"])],
    "data/ring_size/mech_cost.csv (study file)")
add("sec9_peak_gb", ln, "peak memory GB, 1 decimal", 2.0, round(max(float(r["cost_maxrss_mb"]) for r in mc) / 1000, 1),
    "data/ring_size/mech_cost.csv (study file)")
ln = lno(r"^Atlas \(step 6\)")
add("sec8_atlas_records", ln, "atlas records: 75 classes x 17 sizes + 13 x 4", 1327,
    sum(1 for _ in open(os.path.join(D, "atlas", "mechanisms_atlas.csv"))) - 1, "data/ring_size/atlas/mechanisms_atlas.csv (study file)")

by = defaultdict(lambda: [0, 0])
for c in checks:
    by[c["id"]][0] += 1
    by[c["id"]][1] += int(c["equal"])
res = {"n_checks": len(checks), "n_equal": sum(c["equal"] for c in checks),
       "n_unequal": sum(not c["equal"] for c in checks),
       "by_id": {k: {"checks": v[0], "equal": v[1]} for k, v in sorted(by.items())},
       "unequal": [c for c in checks if not c["equal"]], "checks": checks}
json.dump(res, open(os.path.join(OUT, "report_numbers.json"), "w"), indent=1)
print(res["n_checks"], res["n_equal"], res["n_unequal"])
for c in res["unequal"]:
    print(c)
