"""Step 2 / 4, continued: the seed-orbit table and sentences of Section 5.3 of the report against the study's
seed_orbits.csv and against the own orbits (out/seed_compare.json); template check (static template lines occur
verbatim in the report).  Writes out/report_numbers2.json."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, "out")
lines = open(os.path.join(REPO, "report_ring_size.md")).read().split("\n")
sc = json.load(open(os.path.join(OUT, "seed_compare.json")))["by_rule"]
res = {"seed_table": [], "sentences": []}
i = next(k for k, l in enumerate(lines) if l.startswith("| rule | returns_to_0_at_n"))
for k in range(i + 2, i + 6):
    c = [v.strip() for v in lines[k].strip().strip("|").split("|")]
    rule = c[0]
    rep_list = [int(v) for v in c[1].split(",")]
    s = sc[rule]
    res["seed_table"].append({
        "line": k + 1, "rule": int(rule), "report_returns": rep_list, "report_undetermined_count": int(c[2]),
        "study_file_returns": s["returns_study"], "study_file_capped_count": len(s["study_capped"]),
        "report_equals_study_file": rep_list == s["returns_study"] and int(c[2]) == len(s["study_capped"]),
        "own_returns": s["returns_own"], "own_returns_not_in_report": sorted(set(s["returns_own"]) - set(rep_list)),
        "report_returns_not_confirmed_by_own": sorted(set(rep_list) - set(s["returns_own"])),
        "n_still_open_after_own_runs": s["study_capped_open"],
        "study_capped_settled_by_own_simulation": len(s["study_capped_settled_by_own_simulation"]),
        "study_capped_settled_by_proof_only": len(s["study_capped_settled_by_proof_only"])})
# sentence at line 331: rule 22 at n = 2 (mod 4) and odd n
k = next(k for k, l in enumerate(lines) if l.startswith("For n ≡ 2 (mod 4) and odd n the seed orbit of rule 22 returns at"))
rep = [int(v) for v in re.search(r"returns at ([0-9, ]+) in n <= 256", lines[k]).group(1).split(",")]
s = sc["22"]
own = [n for n in s["returns_own"] if n % 4 != 0]
res["sentences"].append({"line": k + 1, "what": "rule 22, n not divisible by 4: n where the seed orbit returns",
                         "report": rep, "own": own, "missing_in_report": sorted(set(own) - set(rep)),
                         "study_undetermined_n_not_divisible_by_4": [n for n in s["study_capped"] if n % 4 != 0],
                         "still_open": [n for n in s["study_capped_open"] if n % 4 != 0]})
k = next(k for k, l in enumerate(lines) if "n = 7, 15, 31, 63, 127, 255 in n <= 256" in l)
s = sc["122"]
res["sentences"].append({"line": k + 1, "what": "rule 122: 'returns exactly at n = 7, 15, 31, 63, 127, 255 in n <= 256'",
                         "report": [7, 15, 31, 63, 127, 255], "own": s["returns_own"],
                         "study_undetermined_n": s["study_capped"], "still_open": s["study_capped_open"],
                         "capped_n_equal_those_of_rule_26_minus_one": s["study_capped"] == [n - 1 for n in sc["26"]["study_capped"]]})
# template: static lines verbatim in the report, placeholders
t = open(os.path.join(REPO, "code", "ring_size", "report_template.md")).read().split("\n")
rs = set(lines)
static = [l for l in t if "{{" not in l]
res["template"] = {"template_lines": len(t), "static_lines": len(static),
                   "static_lines_not_verbatim_in_report": sum(1 for l in static if l not in rs),
                   "placeholders": sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", "\n".join(t)))),
                   "static_lines_with_ring_sizes_examples": [[n + 1, l.strip()[:150]] for n, l in enumerate(t)
                                                              if "{{" not in l and re.search(r"n = \d+(, \d+)+|\(\d+, \d+, \d+\)", l)][:25]}
res["template"]["n_placeholders"] = len(res["template"]["placeholders"])
json.dump(res, open(os.path.join(OUT, "report_numbers2.json"), "w"), indent=1)
for r in res["seed_table"]:
    print({k: v for k, v in r.items() if k not in ("report_returns", "study_file_returns", "own_returns")})
for r in res["sentences"]:
    print(r)
print({k: v for k, v in res["template"].items() if k not in ("placeholders", "static_lines_with_ring_sizes_examples")})
print(len(res["template"]["static_lines_with_ring_sizes_examples"]))
