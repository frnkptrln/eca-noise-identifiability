"""Step 4: every [proved] / [computed] / [observed] tag of report_ring_size.md with line number, the tagged text
and the verdict of this verification.  The verdicts are written by hand below (keyed by line and position on the
line); the script fails if a tag has no verdict.  Writes out/tags_audit.csv and out/tags_audit.json."""
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
lines = open(os.path.join(REPO, "report_ring_size.md")).read().split("\n")
OK, OVER, WRONG, DEF = "matches the evidence", "overstated", "statement under the tag is wrong", "definition of the tag"
V = {
    (9, 0): (DEF, ""), (10, 0): (DEF, ""), (11, 0): (DEF, ""),
    (67, 0): (OK, "rebuilt: out/misc_checks.json (same 8 counts; targets 154 and 166 only)"),
    (91, 0): (OK, "the periods of a ring configuration form a subgroup of Z/nZ"),
    (110, 0): (OK, "proof read; 0 counterexamples in out/sweep88_summary.json"),
    (113, 0): (OK, "proof read line by line; 0 counterexamples in out/sweep88_summary.json"),
    (125, 0): (OK, "proof read; 0 counterexamples in out/sweep88_summary.json"),
    (134, 0): (OK, "180 and 175 reproduced from the sealed sample (out/report_numbers.json)"),
    (137, 0): (OK, "proof read; hypotheses hold in the sweep cases counted in out/sweep88_summary.json, conclusion never fails"),
    (155, 0): (OK, "proof read; out/lemmaZP.json"),
    (159, 0): (OK, "proof read; healing check rebuilt in out/crystal_checks.json"),
    (168, 0): (OK, "proof read; out/lemmaZP.json (trace identity and criterion against brute force)"),
    (175, 0): (OK, "pair graphs of rules 154 and 45 rebuilt: out/pairgraph_all256.csv"),
    (176, 0): (OK, "follows from Lemma P and the bijective case (all cycles at potential m - 1); n >= 3 understood"),
    (218, 0): (OK, "table 5.1 reproduced: out/report_numbers.json"),
    (247, 0): (OK, "tau = 3 rebuilt (out/crystal_checks.json); Lemma H gives n >= 7"),
    (247, 1): (OK, "n = 6 in out/crystal_radius_own.csv"),
    (252, 0): (OK, "out/crystal_radius_own.csv, all 4 | n up to 400"),
    (255, 0): (OK, "sampled test rebuilt: out/sampled_reach_check.json"),
    (256, 0): (OVER, "for classes 43 and 142 the conclusion is also conditional on the radius beyond n = 400, which is computed, not proved (finding F13)"),
    (257, 0): (OK, "trivial (spatial period divides n)"),
    (259, 0): (OK, "single closed class with all codes at p not dividing n, n = 8..22: out/report_numbers.json"),
    (260, 0): (OK, "out/report_numbers.json (sec5_1_no_356_cycle)"),
    (262, 0): (OK, "out/compare_derived.json (rule35_blocks)"),
    (265, 0): (OK, "block law reproduced for n = 8..22: out/compare_derived.json"),
    (299, 0): (OVER, "Lemma B is flagged in 9 of the 13 cases; the other 4 are single-cycle maps (rules 60, 90 at n = 8, 16) where the study's own flag is False (finding F16)"),
    (300, 0): (OK, "59 of 59: out/compare_derived.json"),
    (311, 0): (OK, "proof read; orbit identities simulated for all even n <= 256: out/rule90_identities.json"),
    (320, 0): (OK, "every case of the induction read; identities simulated for all 4 | n <= 256: out/rule90_identities.json"),
    (332, 0): (WRONG, "the list is incomplete: rule 22 returns at n = 241 as well; the study's file has this n and 24 other n not divisible by 4 as undetermined (finding F1)"),
    (338, 0): (OK, "out/compare_derived.json (g1_distance_154) and the sealed sample"),
    (342, 0): None,   # decided below from the sealed sample and the completed result file out/v154_n22.json
    (343, 0): (OK, "sampled test rebuilt"),
    (349, 0): (OVER, "'exactly' is not supported: 33 values of n were undetermined in the study; 13 are still open after this verification (finding F2)"),
    (350, 0): (OK, "the capped n of rule 122 are those of rules 26 and 154 minus one: out/seed_compare.json"),
    (352, 0): (OK, "out/report_numbers.json (sec5_4_*)"),
    (363, 0): (OK, "n = 8..22 from the sealed sample, n = 4..7 from out/sweep88.jsonl"),
    (369, 0): (OK, "out/report_numbers.json (sec5_5_26_*)"),
    (371, 0): (OK, "codes and the mod-6 fit: out/report_numbers.json; the description of the carriers was not checked"),
    (374, 0): (OK, "Lemma P; brute force at odd n = 9..21 in the sealed sample"),
    (376, 0): (WRONG, "'all cycles are selected' fails at n = 18 and n = 22 (finding F4)"),
    (378, 0): (WRONG, "the uniform 2-cycle is not selected at n = 22 either; the temporal period-3 cycles are not selected at n = 9 (finding F5)"),
    (387, 0): (OK, "table 5.6 rebuilt: out/sampled_reach_check.json"),
    (511, 0): (OK, "atlas records compared with the own sweep: out/atlas_check.json (gamma_min placeholder in bijective records, finding F15)"),
}
# line 342 ('all cycles form one strongly connected G1 and are all selected [computed for even n <= 20]'):
# the verdict is computed here, not typed, and the script fails if the result file for n = 22 is missing or incomplete
ROOT = os.path.dirname(HERE)
sample = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(ROOT, "out", "sample.jsonl")))}
ev = [n for n in (10, 12, 14, 18, 20)
      if sample[(154, n)]["g1"]["n_scc"] == 1 and sample[(154, n)]["selected"]["n_cycles"] == sample[(154, n)]["n_cycles"]]
v22 = json.load(open(os.path.join(HERE, "out", "v154_n22.json")))
complete22 = (v22["V_rows_computed"] == v22["rotation_orbits"] and v22.get("edmonds_levels") == 1)
ok22 = complete22 and v22["g1_scc"] == 1 and v22["selected_cycles"] == v22["cycles"]
assert complete22, "out/v154_n22.json is not a completed run"
V[(342, 0)] = (OK if ev == [10, 12, 14, 18, 20] else WRONG,
               "one strongly connected G1 with all cycles selected at n = %s in the sealed sample; at n = 22 the same holds "
               "(out/v154_n22.json, complete run over %d of %d orbit representatives: %s)" % (ev, v22["V_rows_computed"], v22["rotation_orbits"], ok22))
# every result file named in a reason must exist when the audit is written
for key, (verdict, reason) in V.items():
    for name in re.findall(r"out/[A-Za-z0-9_]+\.(?:jsonl|json|csv)", reason):
        assert os.path.exists(os.path.join(HERE, name)), "missing evidence file %s for line %d" % (name, key[0])
rows = []
for i, l in enumerate(lines):
    for k, m in enumerate(re.finditer(r"\[(proved|computed|observed)[^\]]*\]", l)):
        key = (i + 1, k)
        assert key in V, "no verdict for tag at line %d: %s" % (i + 1, m.group(0))
        a, b = max(0, m.start() - 150), m.start()
        rows.append({"line": i + 1, "tag": m.group(0), "kind": m.group(1), "text_before_tag": l[a:b].strip(),
                     "verdict": V[key][0], "reason": V[key][1]})
assert len(rows) == len(V)
with open(os.path.join(HERE, "out", "tags_audit.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0]))
    w.writeheader()
    w.writerows(rows)
summ = {"tags": len(rows), "by_kind": {}, "by_verdict": {}, "evidence_files_exist": True,
        "line_342_verdict_computed_after_v154_n22_complete": bool(complete22),
        "proved_lines": [r["line"] for r in rows if r["kind"] == "proved" and r["verdict"] != DEF],
        "not_matching": [[r["line"], r["tag"], r["verdict"]] for r in rows if r["verdict"] in (OVER, WRONG)]}
for r in rows:
    summ["by_kind"][r["kind"]] = summ["by_kind"].get(r["kind"], 0) + 1
    summ["by_verdict"][r["verdict"]] = summ["by_verdict"].get(r["verdict"], 0) + 1
json.dump(summ, open(os.path.join(HERE, "out", "tags_audit.json"), "w"), indent=1)
print(json.dumps(summ))
