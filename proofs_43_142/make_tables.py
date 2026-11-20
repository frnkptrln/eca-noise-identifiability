"""Builds out/tables.md (section 7 of PROOF_43_142.md) and out/tables_154.md (the table of literature_addendum.md)
from the output files of this folder and copies them verbatim into the two documents, between the markers
<!-- TABLES BEGIN --> / <!-- TABLES END --> and <!-- TABLE 154 BEGIN --> / <!-- TABLE 154 END -->. No computation.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def load(name):
    with open(os.path.join(OUT, name)) as fh:
        return json.load(fh)


def nrange(ns):
    ns = sorted(ns)
    if len(ns) > 2 and all(b - a == ns[1] - ns[0] for a, b in zip(ns, ns[1:])):
        step = ns[1] - ns[0]
        return f"{ns[0]}..{ns[-1]}" + ("" if step == 1 else f" (step {step})")
    return f"{ns[0]}..{ns[-1]}, {len(ns)} sizes"


def build():
    """Returns the text of out/tables.md and of out/tables_154.md."""
    lem = load("check_lemmas.json")
    paths = load("constructive_paths.json")
    cross = load("crosscheck_data.json")
    z154 = load("zhu_richard_154.json")
    g1 = []
    with open(os.path.join(OUT, "g1_classes.jsonl")) as fh:
        for line in fh:
            g1.append(json.loads(line))
    g1.sort(key=lambda r: (r["rule"], r["n"]))
    L = []

    # ------------------------------------------------------------------ Table 1
    L.append("### Table 1. Exhaustive tests of the lemmas (`check_lemmas.py` -> `out/check_lemmas.json`)\n")
    L.append("Rules 184 and 226 are the wall rules of rules 43 and 142. Every test runs over all objects of the kind "
             "named in the column `cases` at every ring size of the column `n`.\n")
    L.append("| test | statement tested | rule | n | cases | violations |")
    L.append("|---|---|---|---|---|---|")
    for r in lem["results"]:
        stmt = r["statement"].replace("|", "\\|")
        L.append(f"| {r['test']} | {stmt} | {r['rule']} | {nrange(r['n_list'])} | {r['cases']} {r['unit']} | "
                 f"{r['violations']} |")
    L.append("")
    t1 = [r for r in lem["results"] if r["test"] == "T1"]
    L.append(f"All tests passed: {lem['all_passed']}. Return times in test T1 are exactly 1 and n/2 - 1 at every ring "
             f"size: {all(r['return_times_ok'] for r in t1)}. CPU time {lem['cpu_seconds']:.2f} s, peak memory "
             f"{lem['peak_mb']} MB.\n")

    # ------------------------------------------------------------------ Table 2
    L.append("### Table 2. G1 and its closed classes computed directly, 4 | n (`g1_classes.py` -> `out/g1_classes.jsonl`)\n")
    L.append("| rule | n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | "
             "closed classes = {X} | cycles without G1 path to X | longest shortest G1 path to X | "
             "G1 distance to X = \\|w - n/2\\| / 2 for every cycle | CPU s | peak MB |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in g1:
        if r["n"] % 4 == 0:
            L.append(f"| {r['rule']} | {r['n']} | {r['cycles']} | {r['periodic_states']} | {r['g1_edges']} | "
                     f"{r['strong_components']} | {r['closed_classes']} {r['closed_class_sizes']} | "
                     f"{r['prediction_holds']} | {r['cycles_without_path_to_crystal']} | "
                     f"{r['max_g1_distance_to_crystal']} | {r['g1_distance_equals_wall_formula']} | "
                     f"{r['cpu_seconds']:.2f} | {r['peak_mb']} |")
    L.append("")
    L.append("In every row the codes on the closed class are 1, 3, 4, 6 and X is the only cycle that no single flip "
             "leaves: " + str(all(r["closed_codes"] == [1, 3, 4, 6] and r["cycles_without_leaving_flip"] == 1
                                  for r in g1 if r["n"] % 4 == 0)) + ". The number of strong components equals "
             "n/2 + 1 (rule 43) and n/2 + 3 (rule 142) in every row: "
             + str(all(r["strong_components"] == r["n"] // 2 + (1 if r["rule"] == 43 else 3)
                       for r in g1 if r["n"] % 4 == 0)) + " (an observation; not used and not proved).\n")

    # ------------------------------------------------------------------ Table 3
    L.append("### Table 3. G1 and its closed classes computed directly, 4 not dividing n (same script)\n")
    L.append("w- and w+ are the largest even number below n/2 and the smallest even number above n/2.\n")
    L.append("| rule | n | w- | w+ | cycles | cycles with w- or w+ walls | strong components | closed classes (sizes) | "
             "closed class = the cycles with w- or w+ walls, all eight codes | CPU s | peak MB |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in g1:
        if r["n"] % 4 != 0:
            L.append(f"| {r['rule']} | {r['n']} | {r['w_minus']} | {r['w_plus']} | {r['cycles']} | "
                     f"{r['cycles_on_levels']} | {r['strong_components']} | {r['closed_classes']} "
                     f"{r['closed_class_sizes']} | {r['prediction_holds']} | {r['cpu_seconds']:.2f} | {r['peak_mb']} |")
    L.append("")
    L.append(f"Records in `out/g1_classes.jsonl`: {len(g1)} (rules 43 and 142, n = {min(r['n'] for r in g1)}.."
             f"{max(r['n'] for r in g1)}); records in which the computed closed classes are the ones stated in "
             f"Theorem 1 (4 | n) or Theorem 2 (otherwise): {sum(1 for r in g1 if r['prediction_holds'])}. "
             f"Sum of the recorded CPU times: {sum(r['cpu_seconds'] for r in g1):.2f} s; largest peak memory "
             f"{max(r['peak_mb'] for r in g1)} MB (n = 24).\n")

    # ------------------------------------------------------------------ Table 4
    L.append("### Table 4. The chains of the proofs, executed and checked step by step (`constructive_paths.py` -> "
             "`out/constructive_paths.json`)\n")
    names = {"A": "A: Theorem 1(2), every cycle", "B": "B: Theorem 1(2), samples",
             "C": "C: Theorem 1(2), stored initial states of `sampled_reach`", "D": "D: Theorem 2",
             "E": "E: Lemma 10(b), upper level"}
    L.append("| part | rule | n | start cycles | all chains end on the target | longest chain (flips) | mean | "
             "chains of length 0 | remarks |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in paths["rows"]:
        rem = r["note"]
        if r["part"] == "C":
            rem += (f"; stored path length equal / longer / shorter than the chain: {r['stored_equal']} / "
                    f"{r['stored_longer']} / {r['stored_shorter']}")
        if r["part"] == "D":
            rem += (f"; most flips towards the levels {r['max_towards']}, most slides {r['max_slides']}, chains using "
                    f"Lemma 11: {r['used_lemma11']}")
        if "distinct_cycles" in r:
            rem += f"; {r['distinct_cycles']} distinct cycles"
        if r["part"] == "E":
            rem += "; chain length = number of slides"
        L.append(f"| {names[r['part']]} | {r['rule']} | {r['n']} | {r['starts']} | {r['all_end_on_target']} | "
                 f"{r['longest']} | {r['mean']:.2f} | {r['zero_length']} | {rem} |")
    L.append("")
    nA = sum(r["starts"] for r in paths["rows"] if r["part"] == "A")
    nD = sum(r["starts"] for r in paths["rows"] if r["part"] == "D" and r["note"] == "every cycle")
    nE = sum(r["starts"] for r in paths["rows"] if r["part"] == "E" and r["note"].startswith("every"))
    L.append(f"Part A: {nA} cycles in total (both rules, n = 4, 8, 12, 16, 20), each with two choices of the flipped "
             f"cells. Part D, every cycle: {nD} cycles (both rules, n = 5..19, 4 not dividing n). Part E, every cycle of the upper level: "
             f"{nE} cycles. Random choices use "
             f"the seed {paths['seed']}. CPU time {paths['cpu_seconds']:.2f} s, peak memory {paths['peak_mb']} MB.\n")

    # ------------------------------------------------------------------ Table 5
    m, c, s = cross["mechanisms"], cross["crystal_radius"], cross["sampled_reach"]
    L.append("### Table 5. Comparison with the data of the study (`crosscheck_data.py` -> `out/crosscheck_data.json`)\n")
    L.append("| data of the study | compared with | compared | disagreements |")
    L.append("|---|---|---|---|")
    L.append(f"| `data/ring_size/mechanisms.csv`, rules 43 and 142, n = {m['n_min']}..{m['n_max']} ({m['records']} "
             f"records), fields {', '.join(m['fields'])} | Table 2, Table 3 and the values given by Theorems 1 and 2 "
             f"(one selected cycle or the cycles of the two levels; gamma_min = m - 1; k_c; k*; largest entry cost "
             f"n/4) | {m['values_compared']} values | {len(m['mismatches'])} |")
    L.append(f"| `data/ring_size/crystal_radius.csv`, rules 43 and 142, n = {c['n_min']}..{c['n_max']} ({c['rows']} "
             f"rows): radius >= 2 and largest return time | Theorem 1(1) and the return time max(1, n/2 - 1) of "
             f"Proposition 2; test T1 of Table 1 | {c['rows']} rows | {len(c['rows_not_matching'])} |")
    L.append(f"| `data/ring_size/sampled_reach/rule{{43,142}}_n{{24,28,32}}.csv` ({s['files']} files): stored length "
             f"of a one-flip path into X | length \\|w - n/2\\| / 2 of the chain of Theorem 1(2) from the same cycle "
             f"(Table 4, part C) | {s['starts']} initial states | {s['stored_longer'] + s['stored_shorter']} "
             f"(stored path longer: {s['stored_longer']}, shorter: {s['stored_shorter']}) |")
    L.append(f"| largest direct entry cost in `mechanisms.csv`, 4 \\| n | exhaustive shortest-path search of test E | "
             f"{len(cross['entry_cost'])} (rule, n) pairs | {sum(1 for x in cross['entry_cost'] if not x['equal'])} |")
    L.append("")
    L.append(f"All comparisons agree: {cross['all_agree']}.\n")

    total = lem["cpu_seconds"] + paths["cpu_seconds"] + sum(r["cpu_seconds"] for r in g1) + z154["cpu_seconds"]
    L.append(f"Total CPU time of the computing scripts of this folder as recorded in their output files "
             f"(`check_lemmas.py`, `g1_classes.py`, `constructive_paths.py`, `zhu_richard_154.py`): {total:.1f} s. "
             f"Every script ran as a single process.")

    # ------------------------------------------------------------------ rule 154 table for the literature addendum
    M = []
    M.append("| n | periodic states in E ∪ O | periodic states by Lemma 6 | periodic states, direct enumeration | equal | "
             "fraction of states not on a cycle | decimal | 2^(1 - n/2) (1 - 2^(-2^j)) equal | value quoted from "
             "arXiv:2610.10967 | agrees at the quoted precision | states without preimage (fraction) |")
    M.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in z154["rows"]:
        direct = r["periodic_direct"] if r["periodic_direct"] is not None else "not computed"
        equal = r["lemma6_equals_direct"] if r["periodic_direct"] is not None else ""
        goe = (f"{r['states_without_preimage']} ({r['fraction_without_preimage']})"
               if r["states_without_preimage"] is not None else "not computed")
        M.append(f"| {r['n']} | {r['periodic_in_EO']} | {r['periodic_lemma6']} | {direct} | "
                 f"{equal} | {r['fraction_not_periodic']} | {r['fraction_decimal']} | "
                 f"{r['closed_form_equal']} | {r.get('quoted', '')} | {r.get('agrees_with_quoted', '')} | {goe} |")
    M.append("")
    M.append(f"Lemma 6 count equals the direct count at every even n = 4..{z154['direct_n_max']}: "
             f"{z154['all_lemma6_equal_direct']}. The closed form agrees at every even n = 4..{z154['n_max']}: "
             f"{z154['all_closed_form_equal']}. Both quoted values agree: {z154['quoted_values_agree']}. Within "
             f"n = 4..{z154['n_max']} the fraction is below 0.01 "
             f"for every even n >= {z154['below_0_01_from_n']} and not for smaller even n. CPU time "
             f"{z154['cpu_seconds']:.2f} s, peak memory {z154['peak_mb']} MB "
             f"(`proofs_43_142/zhu_richard_154.py` -> `proofs_43_142/out/zhu_richard_154.json`).")
    return "\n".join(L) + "\n", "\n".join(M) + "\n"


def main():
    tables, tables154 = build()
    with open(os.path.join(OUT, "tables.md"), "w") as fh:
        fh.write(tables)
    with open(os.path.join(OUT, "tables_154.md"), "w") as fh:
        fh.write(tables154)
    print(f"wrote out/tables.md ({tables.count(chr(10))} lines) and out/tables_154.md ({tables154.count(chr(10))} lines)")
    # copy the tables into the two documents
    insert(os.path.join(HERE, "PROOF_43_142.md"), "TABLES",
           "## 7. Computations (verbatim copy of `out/tables.md`)\n\n" + tables)
    insert(os.path.join(os.path.dirname(HERE), "literature_addendum.md"), "TABLE 154", tables154)


def insert(path, tag, text):
    """Replaces the text between the markers <!-- tag BEGIN --> and <!-- tag END --> of the file by text."""
    if not os.path.exists(path):
        print(f"{os.path.basename(path)}: not present, nothing inserted")
        return
    with open(path) as fh:
        doc = fh.read()
    a, b = f"<!-- {tag} BEGIN -->", f"<!-- {tag} END -->"
    if doc.count(a) != 1 or doc.count(b) != 1:
        raise SystemExit(f"{path}: markers {a} / {b} not found exactly once")
    head, rest = doc.split(a)
    _, tail = rest.split(b)
    with open(path, "w") as fh:
        fh.write(head + a + "\n" + text + b + tail)
    print(f"{os.path.basename(path)}: tables inserted between the markers '{tag}'")


if __name__ == "__main__":
    main()
