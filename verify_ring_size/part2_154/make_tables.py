"""Tables for PROOF_154.md, generated from the output files of this folder (no computation of its own except
the 32-block check of Lemma Q1 for rule 26).  Output: out/tables.md
"""
import itertools
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    return [json.loads(line) for line in open(os.path.join(HERE, "out", name))]


out = []
# ---- Table A: rule 154
A = load("check_lemmas.jsonl")
out.append("<!-- TABLE_A -->")
out.append("| n | periodic states | cycles | G1 edges | out-degree of {0} | every cycle reaches {0} | max G1 distance to {0} "
           "| G1 strongly connected | lemma tests run / failed |")
out.append("|---|---|---|---|---|---|---|---|---|")
for r in A:
    tests = [k for k in r if k.startswith("L")]
    bad = [k for k in tests if r[k] is not True]
    out.append("| %d | %d | %d | %d | %d | %s | %d | %s | %d / %d |" % (
        r["n"], r["n_periodic"], r["n_cycles"], r["G1_edges"], r["out_degree_of_zero"],
        "yes" if r["all_cycles_reach_zero"] else "no", r["max_G1_distance_to_zero"],
        "yes" if r["G1_strongly_connected"] else "no", len(tests), len(bad)))
out.append("<!-- END -->")
out.append("")
out.append("<!-- TABLE_A2 -->")
out.append("| n | size of M | (2^(n/2)-1)^2 | cycles in M | F^n = id on M | distance histogram (distance: cycles) | "
           "distance of the all-ones cycle | distance = min-parity bound for all cycles |")
out.append("|---|---|---|---|---|---|---|---|")
for r in A:
    n = r["n"]
    if n & (n - 1) == 0:
        out.append("| %d | %d | %d | %d | %s | %s | %d | %s |" % (
            n, r["size_M"], (2 ** (n // 2) - 1) ** 2, r["n_cycles_in_M"],
            "yes" if r["obs_F_pow_n_identity_on_M"] else "no",
            ", ".join("%d: %d" % (a, b) for a, b in r["distance_hist"]), r["distance_of_all_ones"],
            "yes" if r["distance_eq_bound_for_all_cycles"] else "no"))
out.append("<!-- END -->")
out.append("")
# ---- Table S: sampled large n
S = load("sample_large_n.jsonl")
out.append("<!-- TABLE_S -->")
out.append("| n | sampled states of M | F(x) in M | F^n(x) = x | descent: intermediate states tested / periodic | "
           "descents ending in 0 within n/2 steps |")
out.append("|---|---|---|---|---|---|")
for r in S:
    out.append("| %d | %d | %d | %d | %d / %d | %d of %d |" % (
        r["n"], r["samples"], r["in_M_after_F"], r["F_pow_n_identity"], r["descent_states_tested"],
        r["descent_states_periodic"], r["descent_reaches_zero_within_half_n"], r["descent_samples"]))
out.append("<!-- END -->")
out.append("")
# ---- Table B: rule 122, even n
X = load("explore_122_26.jsonl")
D = {r["n"]: r for r in load("cb_defect_122.jsonl")}
out.append("<!-- TABLE_B -->")
out.append("| n | cycles | closed classes: sizes | 0 in closed class | CB in closed class | out-neighbours of {0} | "
           "out-degree of CB | smallest out-neighbour of CB (rep) | fate of the defect orbit | cycles with a G1 path to CB | "
           "CB has a G1 path to {0} | codes missing on the closed class |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in sorted(X, key=lambda r: r["n"]):
    if r["rule"] == 122 and r["n"] % 2 == 0:
        n = r["n"]
        d = D[n]
        out.append("| %d | %d | %s | %s | %s | %s | %d | `%s` | %s | %d | %s | %s |" % (
            n, r["n_cycles"], r["closed_class_sizes"], "yes" if r["zero_in_closed_class"] else "no",
            "yes" if r["cb_in_closed_class"] else "no",
            "CB only" if r["zero_out_nbrs_reps"] == ["01" * (n // 2)] else str(r["zero_out_nbrs_reps"]),
            r["cb_out_degree"], min(r["cb_out_nbrs_reps"]),
            "%s (transient %d, period %d)" % (d["end"], d["transient"], d["period"]),
            r["n_cycles_reaching_cb"], "yes" if r["cb_reaches_zero"] else "no",
            r["codes_missing_on_closed_classes"] or "none"))
out.append("<!-- END -->")
out.append("")
out.append("<!-- TABLE_B2 -->")
ends = {}
for n in sorted(D):
    ends.setdefault(D[n]["end"], []).append(n)
for k in ("zero", "checkerboard", "other", "undetermined"):
    out.append("- defect orbit ends on **%s**: n = %s" % (k, ", ".join(map(str, ends.get(k, []))) or "(none)"))
und = [D[n] for n in ends.get("undetermined", [])]
if und:
    out.append("- undetermined cases: cycle not closed within %d steps; 0 or CB met within these steps: %s" % (
        und[0]["steps_run"], ", ".join("n = %d: %s" % (D[n]["n"], "yes" if D[n]["zero_or_checkerboard_hit_within_steps_run"] else "no")
                                      for n in ends["undetermined"])))
out.append("<!-- END -->")
out.append("")
out.append("<!-- TABLE_B3 -->")
out.append("| n (odd) | cycles | closed classes: sizes | 0 in closed class | out-degree of {0} | codes missing on the closed class |")
out.append("|---|---|---|---|---|---|")
for r in sorted(X, key=lambda r: r["n"]):
    if r["rule"] == 122 and r["n"] % 2 == 1:
        out.append("| %d | %d | %s | %s | %d | %s |" % (
            r["n"], r["n_cycles"], r["closed_class_sizes"], "yes" if r["zero_in_closed_class"] else "no",
            r["zero_out_degree"], r["codes_missing_on_closed_classes"] or "none"))
out.append("<!-- END -->")
out.append("")
# ---- Table C: rule 26
out.append("<!-- TABLE_C -->")
out.append("| n | n mod 3 | cycles | closed classes: sizes | transient cycles | cycles carrying 111 | of these in the closed class "
           "| transient cycles = 111-carriers outside the closed class | codes missing on the closed class | "
           "smallest 111-carrier in the closed class (rep) |")
out.append("|---|---|---|---|---|---|---|---|---|---|")
all_c = True
for r in sorted(X, key=lambda r: r["n"]):
    if r["rule"] == 26:
        n = r["n"]
        same = (r["n_transient_cycles"] == r["cycles_with_code7"] - r["cycles_with_code7_in_closed"])
        if n & (n - 1):
            all_c &= same
        reps = r["code7_closed_reps_first6"]
        out.append("| %d%s | %d | %d | %s | %d | %d | %d | %s | %s | %s |" % (
            n, " (2^k)" if n & (n - 1) == 0 else "", n % 3, r["n_cycles"], r["closed_class_sizes"],
            r["n_transient_cycles"], r["cycles_with_code7"], r["cycles_with_code7_in_closed"],
            "yes" if same else "no", r["codes_missing_on_closed_classes"] or "none",
            "`%s`" % reps[0] if reps else "-"))
out.append("<!-- END -->")
out.append("")
out.append("<!-- TABLE_C2 -->")
ns = sorted(r["n"] for r in X if r["rule"] == 26)
out.append("- for every n in %d..%d that is not a power of two, the transient cycles are exactly the 111-carrying "
           "cycles outside the closed class: %s" % (ns[0], ns[-1], all_c))
no7 = [r["n"] for r in X if r["rule"] == 26 and 7 not in r["codes_missing_on_closed_classes"]]
out.append("- n in %d..%d with a 111-carrying cycle in the closed class (k* = 0): %s" % (ns[0], ns[-1], sorted(no7)))
# Lemma Q1 (rule 26): the only 5-block whose image has 111 is 10011
blocks = []
for b in itertools.product((0, 1), repeat=5):
    img = [(26 >> (4 * b[i - 1] + 2 * b[i] + b[i + 1])) & 1 for i in (1, 2, 3)]
    if img == [1, 1, 1]:
        blocks.append("".join(map(str, b)))
out.append("- rule 26, 5-blocks x_(i-2..i+2) whose image has 111 at i-1..i+1: %s" % blocks)
out.append("<!-- END -->")
out.append("")
out.append("<!-- TABLE_COST -->")


def last_cpu(name):
    for line in open(os.path.join(HERE, "out", name)):
        if line.startswith("cpu seconds"):
            return line.split(":")[1].strip()


out.append("| script | CPU seconds | source of the figure |")
out.append("|---|---|---|")
out.append("| check_lemmas.py (n = 3..16) | %s | out/check_lemmas.txt |" % last_cpu("check_lemmas.txt"))
out.append("| cross_check.py (solver for n = 4..7 and comparison) | %s | out/cross_check.txt |" % last_cpu("cross_check.txt"))
out.append("| sample_large_n.py (n = 32..1024) | %s | out/sample_large_n.jsonl (cumulative, last record) |"
           % S[-1]["cpu_seconds_cumulative"])
out.append("| cb_defect_122.py (even n = 4..256, fate up to 100) | %s | out/cb_defect_122.txt |" % last_cpu("cb_defect_122.txt"))
for lo, hi in ((4, 20), (21, 24), (25, 26)):
    tot = sum(r["cpu_seconds"] for r in X if lo <= r["n"] <= hi)
    out.append("| explore_122_26.py, n = %d..%d (sum of the per-case figures) | %.1f | out/explore_122_26.jsonl |" % (lo, hi, tot))
out.append("<!-- END -->")
txt = "\n".join(out) + "\n"
open(os.path.join(HERE, "out", "tables.md"), "w").write(txt)
print(txt)
