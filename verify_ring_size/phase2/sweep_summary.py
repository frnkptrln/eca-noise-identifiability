"""Summary of out/sweep88.jsonl -> out/sweep88_summary.json."""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
r = [json.loads(l) for l in open(os.path.join(HERE, "out", "sweep88.jsonl"))]
done = [x for x in r if "skipped" not in x]
skipped = [[x["rule"], x["n"], x["m"]] for x in r if "skipped" in x]
tests = defaultdict(lambda: [0, 0])
for x in done:
    for k, v in x["tests"].items():
        tests[k][0] += 1
        tests[k][1] += int(not v)
lb = [(x, d) for x in done for d in x["lemmaB"]]
res = {
    "cases_total": len(r), "cases_solved": len(done), "cases_skipped": skipped,
    "n_range": [min(x["n"] for x in r), max(x["n"] for x in r)],
    "cases_by_n": {str(n): sum(1 for x in done if x["n"] == n) for n in sorted({x["n"] for x in r})},
    "rules": len({x["rule"] for x in r}),
    "tests": {k: {"cases": v[0], "counterexamples": v[1]} for k, v in sorted(tests.items())},
    "counterexample_cases": [[x["rule"], x["n"]] for x in done if not x["all_tests_true"]],
    "unique_closed_class_cases": sum(x["unique_closed_class"] for x in done),
    "several_closed_classes_cases": sum(not x["unique_closed_class"] for x in done),
    "S_equals_union_of_all_closed_cases": sum(x["S_equals_union_of_all_closed"] for x in done),
    "S_proper_subset_of_union_cases": [[x["rule"], x["n"], x["n_closed"], x["n_closed_selected"]] for x in done
                                       if not x["S_equals_union_of_all_closed"]][:400],
    "S_proper_subset_of_union_count": sum(not x["S_equals_union_of_all_closed"] for x in done),
    "lemmaB": {
        "cases_with_a_radius_ge2_orbit": sum(1 for x in done if x["lemmaB_candidate_orbits"] > 0),
        "candidate_orbits_total": sum(x["lemmaB_candidate_orbits"] for x in done),
        "candidate_orbits_tested_directly": len(lb),
        "candidate_orbits_not_tested_directly_beyond_60_per_case": sum(max(0, x["lemmaB_candidate_orbits"] - 60) for x in done),
        "hypotheses_hold": sum(d["g2_holds"] for _, d in lb),
        "hypotheses_hold_cases": sum(1 for x in done if any(d["g2_holds"] for d in x["lemmaB"])),
        "hypotheses_hold_and_conclusion_fails": sum(d["g2_holds"] and not (d["S_equals_A"] and d["gmin_minus_formula"] == 0) for _, d in lb),
        "hypotheses_hold_by_q": dict(Counter(str(d["q"]) for _, d in lb if d["g2_holds"])),
        "hypotheses_hold_by_rule": dict(Counter(str(x["rule"]) for x, d in lb if d["g2_holds"])),
        "weak_hypothesis_holds": sum(d["g1_reach_A"] for _, d in lb),
        "weak_holds_but_G2_fails": [[x["rule"], x["n"], d["rep"], d["q"], d["S_equals_A"], d["gmin_minus_formula"]]
                                    for x, d in lb if d["g1_reach_A"] and not d["g2_holds"]],
        "weak_holds_and_S_not_A": sum(d["g1_reach_A"] and not d["S_equals_A"] for _, d in lb),
    },
    "lean_edmonds": {"cases": sum(1 for x in done if "lean_edmonds_equals_dense" in x["tests"]),
                     "supernodes_after_level1_gt1": sum(1 for x in done if x.get("lean_info", {}).get("supernodes_after_level1", 1) > 1)},
    "cpu_seconds": round(sum(x.get("cpu_seconds", 0) for x in r), 1),
    "peak_rss_mb": max(x.get("peak_rss_mb", 0) for x in r),
}
json.dump(res, open(os.path.join(HERE, "out", "sweep88_summary.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "S_proper_subset_of_union_cases"}, indent=0))
print(res["S_proper_subset_of_union_cases"][:30])
