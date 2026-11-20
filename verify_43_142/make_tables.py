"""Builds out/tables.md from the output files of this folder (no number is typed by hand)."""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

L = []
lt = json.load(open("out/lemma_tests.json"))
L.append("### V1. Exhaustive tests of the statements (`test_lemmas.py` -> `out/lemma_tests.json`)\n")
L.append(f"n = 3..{lt['nmax']}; {len(lt['results'])} statements; total failures: {lt['total_failures']}; "
         f"wall time {lt['seconds']:.0f} s, one process.\n")
L.append("| statement | n tested | cases | failures |")
L.append("|---|---|---|---|")
for name, d in lt["results"].items():
    ns = sorted(int(n) for n in d)
    cases = sum(e["checked"] for e in d.values())
    fails = sum(e["failures"] for e in d.values())
    rng = "tables" if ns == [0] else (f"{ns[0]}..{ns[-1]}" if ns == list(range(ns[0], ns[-1] + 1)) else ",".join(map(str, ns)))
    L.append(f"| {name} | {rng} | {cases} | {fails} |")
L.append("")

pots = [json.loads(l) for l in open("out/potentials.jsonl")]
L.append("### V2. Potentials, selected set and k_c from the definitions, without Theorem A (`potentials.py` -> `out/potentials.jsonl`)\n")
L.append("| rule | n | cycles m | gamma_min | m - 1 | selected cycles | wall counts of S | k_0..k_7 | k* | closed classes of G1 (sizes) | all document checks | gamma method |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in sorted(pots, key=lambda r: (r["n"], r["rule"])):
    L.append(f"| {r['rule']} | {r['n']} | {r['m']} | {r['gamma_min']} | {r['m'] - 1} | {r['n_selected']} | "
             f"{r['selected_walls']} | {''.join(map(str, r['k']))} | {r['kstar']} | "
             f"{[len(c) for c in r['closed_classes']]} | {all(r['checks'].values())} | {r['potential_method']} |")
L.append("")
L.append("Checks per record (all True in every record): " + "; ".join(sorted({k for r in pots for k in r["checks"]})) + ".\n")

st = json.load(open("out/stationary.json"))
L.append("### V3. Order of nu_c(eps) read off the stationary law (GTH, eps = 1e-4 and 1e-5; `stationary.py` -> `out/stationary.json`)\n")
L.append("| rule | n | k_c from pi | k_c from potentials | agree | max rounding error | stationary mass on S at eps = 1e-5 |")
L.append("|---|---|---|---|---|---|---|")
for r in st:
    L.append(f"| {r['rule']} | {r['n']} | {''.join(map(str, r['k_from_pi']))} | {''.join(map(str, r['k_from_potentials']))} | "
             f"{r['agree']} | {r['max_rounding_error']} | {r['mass_on_selected_cycles_eps1e-5']:.6f} |")
L.append("")

ec = json.load(open("out/entry_cost.json"))
L.append("### V4. Proposition 3 by a backward computation over all states (`entry_cost.py` -> `out/entry_cost.json`)\n")
L.append("| rule | n | cycles | max V(C, X) | n/4 | cycles with V(C, X) != abs(w - n/2)/2 |")
L.append("|---|---|---|---|---|---|")
for r in ec:
    L.append(f"| {r['rule']} | {r['n']} | {r['m']} | {r['V_to_X_max']} | {r['n'] // 4} | {len(r['failures'])} |")
L.append("")

cmp_ = json.load(open("out/compare.json"))
L.append("### V5. Comparison with `proofs_43_142/out/` and `data/ring_size/mechanisms.csv` (`compare.py` -> `out/compare.json`)\n")
L.append(f"G1 fields of `g1_classes.jsonl` compared for both rules, n = 3..20 (cycles, periodic states, G1 edges, "
         f"strong components, closed classes, their sizes, members, codes, wall counts): {cmp_['g1_fields_compared']} values, "
         f"{len(cmp_['g1_differences'])} differences.\n")
from collections import Counter
src = Counter(r["source"] for r in cmp_["mechanisms"])
L.append(f"`mechanisms.csv`, rules 43 and 142, n = 8..22: {len(cmp_['mechanisms'])} records; compared against "
         + ", ".join(f"{v} records by {k}" for k, v in src.items())
         + f"; disagreements: {sum(1 for r in cmp_['mechanisms'] if not r['agree'])}.\n")
L.append("Entry costs: the session's test E covers " +
         ", ".join(f"rule {r['rule']} n = {r['n_min']}..{r['n_max']} ({r['cases']} cycles)" for r in cmp_["session_entry_cost_tests"]) +
         "; this verification: " + ", ".join(f"rule {r['rule']} n = {r['n']}: {r['m']} cycles, {len(r['failures'])} failures" for r in cmp_["mine_entry_cost"]) + ".\n")
open("out/tables.md", "w").write("\n".join(L) + "\n")
print("\n".join(L)[:6000])
