"""Cross-check of out/check_lemmas.jsonl and of the statements of PROOF_154.md against
(a) the sealed sample ../out/sample.jsonl (rule 154, n = 8..21), which was computed from the definitions
    (dense V by 0-1 search, gamma by Edmonds for all roots) without using G1 for the selection, and
(b) the same sealed solver (../solve.py, solve_case) run here for n = 4..7, which are not in the sample.

Output: out/cross_check.txt, out/solver_n4_7.jsonl
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import solve  # noqa: E402  (the verification's own solver)

t0 = time.process_time()
mine = {}
for line in open(os.path.join(HERE, "out", "check_lemmas.jsonl")):
    r = json.loads(line)
    mine[r["n"]] = r
recs = {}
for line in open(os.path.join(HERE, "..", "out", "sample.jsonl")):
    r = json.loads(line)
    if r["rule"] == 154:
        recs[r["n"]] = ("sample", r)
with open(os.path.join(HERE, "out", "solver_n4_7.jsonl"), "w") as fh:
    for n in (4, 5, 6, 7):
        r = solve.solve_case(154, n)
        if isinstance(r, tuple):
            r = r[0]
        fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
        recs[n] = ("solver", r)

lines, allok = [], True
for n in sorted(recs):
    src, r = recs[n]
    m = r["n_cycles"]
    g1_edges = dict((int(a), int(b)) for a, b in r["V_hist"]).get(1, 0)
    tests = {}
    if n in mine:
        tests["n_cycles"] = (m == mine[n]["n_cycles"])
        tests["n_cycle_states"] = (r["n_cycle_states"] == mine[n]["n_periodic"])
        tests["G1_edges"] = (g1_edges == mine[n]["G1_edges"])
    cc = r["g1"]["closed_class_sizes"]
    pow2 = (n & (n - 1)) == 0
    if pow2:
        tests["min_gamma_eq_m_minus_1"] = (r["min_gamma"] == m - 1)
        tests["gamma_hist_is_(m-1:1),(m:m-1)"] = ([list(map(int, t)) for t in r["gamma_hist"]] == [[m - 1, 1], [m, m - 1]])
        tests["selected_is_zero_only"] = (r["selected"]["n_cycles"] == 1 and r["selected"]["orbits"][0]["rep"] == "0" * n)
        tests["closed_classes_is_zero_only"] = (cc == [1] and r["g1"]["closed_classes"][0]["members"] == ["0" * n])
        tests["k_is_0_1_1_1_1_1_1_1"] = (list(r["k"]) == [0, 1, 1, 1, 1, 1, 1, 1])
    else:
        tests["all_cycles_selected"] = (r["selected"]["n_cycles"] == m and r["min_gamma"] == m - 1)
        tests["one_closed_class_of_all_cycles"] = (cc == [m])
        tests["kstar_0"] = (r["kstar"] == 0)
    bad = [k for k, v in tests.items() if not v]
    allok = allok and not bad
    lines.append("n=%2d source=%-6s m=%6d min_gamma=%6d selected=%6d kstar=%d tests=%d failed=%s" % (
        n, src, m, r["min_gamma"], r["selected"]["n_cycles"], r["kstar"], len(tests), bad))
lines.append("ALL CROSS-CHECKS PASSED: %s" % allok)
lines.append("cpu seconds: %.2f" % (time.process_time() - t0))
txt = "\n".join(lines) + "\n"
open(os.path.join(HERE, "out", "cross_check.txt"), "w").write(txt)
print(txt, end="")
