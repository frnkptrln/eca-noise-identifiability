"""Builds out/tables.md (the tables quoted in PROOF_94.md, section 7) from the output files of this folder.

Run from the repository root:  python verify_ring_size/part2_94/make_tables.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
O = os.path.join(HERE, "out")
L = json.load(open(os.path.join(O, "check_lemmas.json")))
P = json.load(open(os.path.join(O, "constructive_paths.json")))
X = json.load(open(os.path.join(O, "crosscheck_sample.json")))
G = sorted((json.loads(l) for l in open(os.path.join(O, "g1_classes.jsonl"))), key=lambda r: r["n"])

out = []
w = out.append

w("### Table 1. Exhaustive tests of the lemmas (`check_lemmas.py` -> `out/check_lemmas.json`)\n")
w("| test | statement tested | n | cases | violations |")
w("|---|---|---|---|---|")


def rng(rows):
    ns = [r["n"] for r in rows]
    step = ns[1] - ns[0] if len(ns) > 1 else 1
    return "%d..%d" % (ns[0], ns[-1]) + ("" if step == 1 else " (step %d)" % step)


def viol(rows):
    return sum(r.get("violations", 0) + r.get("violations_monotone", 0) + r.get("violations_value", 0) for r in rows)


r = L["L1"]["rows"]
w("| L1 | Lemma 1 (freezing), every state | %s | %d states | %d |" % (rng(r), sum(x["states"] for x in r), viol(r)))
r = L["L2"]["rows"]
bad = sum(0 if (x["equal"] and x["all_fixed"]) else 1 for x in r)
w("| L2 | Lemma 2 (fully frozen = block word, fixed), every state | %s | %d fully frozen states among %d | %d |"
  % (rng(r), sum(x["fully_frozen"] for x in r), sum(x["states"] for x in L["L1"]["rows"]), bad))
r = L["L3_all_states"]["rows"]
w("| L3a | Lemma 3 (growth move), every state that is not fully frozen | %s | %d states | %d |"
  % (rng(r), sum(x["not_fully_frozen_states"] for x in r), viol(r)))
r = L["L3_cycle_states"]["rows"]
w("| L3b | Corollary 3 (edge of G1 to a cycle with larger frozen set), every periodic state that is not fully "
  "frozen; frozen set constant on every cycle | %s | %d periodic states (%d cycles) | %d |"
  % (rng(r), sum(x["cycle_states_not_fully_frozen"] for x in r), sum(x["cycles"] for x in r),
     viol(r) + sum(0 if x["frozen_constant_on_cycles"] else 1 for x in r)))
r = L["L4_swap"]["rows"]
w("| L4 | Lemma 4 (swap), every block word, every occurrence | %s | %d occurrences | %d |"
  % (rng(r), sum(x["occurrences"] for x in r), viol(r)))
r = L["L5_merge"]["rows"]
w("| L5 | Lemma 5 (merge), every block word, every occurrence | %s | %d occurrences | %d |"
  % (rng(r), sum(x["occurrences"] for x in r), viol(r)))
r = L["L6_crystal"]["rows"]
w("| L6 | Lemma 6 (every flip of the crystal heals; healing time %s) | %s | %d flips | %d |"
  % (sorted(set(x["max_healing_time"] for x in r)), rng(r), sum(x["flips"] for x in r), viol(r)))
r = L["C2_codes"]["rows"]
w("| C2 | Corollary 2 (one flip of the crystal meets codes 0, 1, 2, 4, 7) | %s | %d ring sizes | %d |"
  % (rng(r), len(r), viol(r)))
w("")
w("All tests passed: %s. CPU time %.2f s, peak memory %.0f MB.\n" % (L["all_ok"], L["cpu_seconds"], L["peak_rss_mb"]))

w("### Table 2. G1 and its closed classes computed directly, 3 | n (`g1_classes.py` -> `out/g1_classes.jsonl`)\n")
w("| n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | closed classes = the "
  "three crystal phases | cycles with no G1 path to the crystal | CPU s | peak MB |")
w("|---|---|---|---|---|---|---|---|---|---|")
for r in G:
    if r["n"] % 3:
        continue
    w("| %d | %d | %d | %d | %d | %d %s | %s | %d | %.2f | %.0f |" % (
        r["n"], r["cycles"], r["periodic_states"], r["g1_edges"], r["strong_components"], r["closed_classes"],
        r["closed_class_sizes"], r["closed_classes_are_exactly_the_crystal_phases"],
        r["cycles_not_reaching_crystal"], r["cpu_seconds"], r["peak_rss_mb"]))
w("")
other = [r for r in G if r["n"] % 3]
w("For comparison, 3 not dividing n (same script): " + "; ".join(
    "n = %d: %d cycles, closed classes %s" % (r["n"], r["cycles"], r["closed_class_sizes"]) for r in other) + ".\n")
w("Cross-check with the sealed blind sample (`crosscheck_sample.py` -> `out/crosscheck_sample.json`): numbers of "
  "cycles, periodic states, G1 edges and the closed-class sizes compared for n = %d..%d (%d ring sizes); all agree: %s.\n"
  % (X["compared_n"][0], X["compared_n"][-1], len(X["compared_n"]), X["all_agree"]))

w("### Table 3. The chain of the proof, executed and checked step by step "
  "(`constructive_paths.py` -> `out/constructive_paths.json`)\n")
w("| part | n | start cycles | all chains end on a crystal phase | longest chain (flips) | mean | max growth steps | "
  "max swap flips | max merges |")
w("|---|---|---|---|---|---|---|---|---|")
names = dict(A="A: every cycle", B="B: cycles reached from 200 random states",
             C="C: all-zero state and doubled words")
for part in "ABC":
    for r in P[part]:
        w("| %s | %d | %d | %s | %d | %.2f | %d | %d | %d |" % (
            names[part], r["n"], r["chains"], r["all_end_on_crystal"], r["max_length"], r["mean_length"],
            r["max_growth"], r["max_swap_flips"], r["max_merges"]))
w("")
w("Part A total: %d cycles, of which %d are the crystal phases themselves (chain of length 0). "
  % (sum(r["chains"] for r in P["A"]), sum(r["chains_of_length_0"] for r in P["A"])))
w("Part C start periods (period: count; None = longer than the search bound): " + "; ".join(
    "n = %d: %s" % (r["n"], ", ".join("%s: %d" % (a, b) for a, b in r["start_period_hist"])) for r in P["C"]) + ".")
w("CPU time %.2f s, peak memory %.0f MB.\n" % (P["cpu_seconds"], P["peak_rss_mb"]))
tot = L["cpu_seconds"] + P["cpu_seconds"] + sum(r["cpu_seconds"] for r in G)
w("Total CPU time of the three scripts as recorded in their output files: %.1f s.\n" % tot)

open(os.path.join(O, "tables.md"), "w").write("\n".join(out))
print("\n".join(out))
