#!/usr/bin/env python3
"""Numbers and the table of ring_size_paper.tex, from the data files of the repository.

Reads (never writes) these files, paths relative to the repository root:
  data/ring_size/mechanisms.csv                 k*, k_c, cycles, ... for the 13 switching classes, n = 8..22
                                                 (no record for rule 154 at n = 22)
  data/fw_sweep.csv                             k* and k_c for all classes, n = 4..20 (used for n = 4..7)
  verify_ring_size/phase2/out/v154_n22.json     rule 154 at n = 22, computed by the verification
  proofs_94_26/out/g1_26.jsonl                  rule 26, even n: cycles by kind, k_c from the definitions (n = 4, 8, 16)
  proofs_94_26/out/g1_classes_94.jsonl          rule 94, 3 not dividing n: closed class, cycles without 101
  data/ring_size/crystal_radius.csv             can one flip leave the crystal (rule 94 at n = 3)
  proofs_43_142/out/zhu_richard_154.json        the two values quoted from Zhu and Richard, arXiv:2610.10967 (rule 154)
  literature_addendum.md                        record of the reading of that text: the bound and the range of n of the
                                                 quoted sentence (section A1), the two printed values (update of
                                                 20 November 2026).  A document, not a data file: the numbers of a
                                                 cited text enter the paper from the record of its reading.

Writes, into the folder of this script (or --outdir):
  numbers.tex       one \\newcommand per number used in the text
  table_kstar.tex   the body of Table 1
  numbers.json      every number with the file, row and field it comes from (read by test_paper.py)

The "theorem" rows of the table evaluate the statements of the paper (function theorem_value); they are not data.
Usage: python make_numbers.py [--outdir DIR]
"""
import argparse
import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MECH = "data/ring_size/mechanisms.csv"
SWEEP = "data/fw_sweep.csv"
V154 = "verify_ring_size/phase2/out/v154_n22.json"
G26 = "proofs_94_26/out/g1_26.jsonl"
G94 = "proofs_94_26/out/g1_classes_94.jsonl"
CRYSTAL = "data/ring_size/crystal_radius.csv"
ZR = "proofs_43_142/out/zhu_richard_154.json"
ADDENDUM = "literature_addendum.md"
CODES = ["000", "001", "010", "011", "100", "101", "110", "111"]      # code number 4a + 2b + c -> word abc

RULES = [154, 43, 142, 94, 26]                 # the rules of the theorems, in the order of the paper
OPEN = [35, 37, 45, 73, 122, 22, 60, 90]       # the classes of the section on open cases: all classes of MECH
                                               # that are not in RULES (asserted in build)
NS = list(range(4, 23))                        # ring sizes of the table
THM_LABEL = {154: r"Thm.~\ref{154:thm:main}", 43: r"Thm.~\ref{43:thm:main}", 142: r"Thm.~\ref{43:thm:main}",
             94: r"Thm.~\ref{94:thm:main}", 26: r"Sect.~\ref{sec:26}"}
WORDS = {4: "Four", 8: "Eight", 16: "Sixteen", 22: "TwentyTwo", 26: "TwentySix", 35: "ThirtyFive", 37: "ThirtySeven",
         45: "FortyFive", 73: "SeventyThree", 122: "OneTwentyTwo", 154: "OneFiftyFour", 94: "NinetyFour",
         43: "FortyThree", 142: "OneFortyTwo", 60: "Sixty", 90: "Ninety"}


def read_csv(rel):
    with open(os.path.join(ROOT, rel), newline="") as fh:
        return list(csv.DictReader(fh))


def read_jsonl(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return {int(r["n"]): r for r in (json.loads(line) for line in fh if line.strip())}


def is_pow2(n):
    return n >= 1 and n & (n - 1) == 0


def theorem_value(rule, n):
    """What the statements of the paper give for k* (a set of possible values), or None if they give nothing.

    154: Theorem 154:thm:main, every n >= 3.
    43, 142: Theorem 43:thm:main, every n >= 4.
    94: Theorem 94:thm:main; 3 | n needs n >= 6, 3 not dividing n needs n >= 5.
    26: Theorem 26:thm:main and Proposition 26:prop:indices.  n = 2^k >= 8: k* is 1 or 2, and 1 if k is odd.
        n = 4: only S = {{0}}, hence k* >= 1 (Lemma lem:kzero).  Other n: no value.
    """
    if rule == 154 and n >= 3:
        return {1} if is_pow2(n) else {0}
    if rule in (43, 142) and n >= 4:
        return {1} if n % 4 == 0 else {0}
    if rule == 94:
        if n % 3 == 0 and n >= 6:
            return {1}
        if n % 3 != 0 and n >= 5:
            return {0}
        return None
    if rule == 26 and is_pow2(n):
        if n >= 8:
            return {1} if (n.bit_length() - 1) % 2 == 1 else {1, 2}
        if n == 4:
            return "ge1"
    return None


def load():
    """k*[(rule, n)] -> (value, source file, description of the row); k_c likewise."""
    kstar, kc, extra = {}, {}, {}
    for row in read_csv(SWEEP):
        r, n = int(row["rule"]), int(row["n"])
        if n <= 7:
            kstar[(r, n)] = (int(row["kstar"]), SWEEP, f"rule={r}, n={n}, field kstar")
            kc[(r, n)] = (row["k_c"], SWEEP, f"rule={r}, n={n}, field k_c")
    for row in read_csv(MECH):
        r, n = int(row["rule"]), int(row["n"])
        kstar[(r, n)] = (int(float(row["kstar"])), MECH, f"rule={r}, n={n}, field kstar")
        kc[(r, n)] = (row["k_c"], MECH, f"rule={r}, n={n}, field k_c")
        extra[(r, n)] = row
    with open(os.path.join(ROOT, V154)) as fh:
        j = json.load(fh)
    assert j["rule"] == 154 and j["n"] == 22
    assert (154, 22) not in kstar, "mechanisms.csv now has rule 154 at n = 22: drop the special case"
    kstar[(154, 22)] = (int(j["kstar"]), V154, "field kstar")
    return kstar, kc, extra


def fmt_thm(v):
    if v is None:
        return "--"
    if v == "ge1":
        return r"$\ge$1"
    return "/".join(str(a) for a in sorted(v))


def agrees(v, data):
    if v is None:
        return None
    if v == "ge1":
        return data >= 1
    return data in v


def nlist(ns):
    return ", ".join(str(a) for a in ns) if ns else "none"


def build():
    kstar, kc, extra = load()
    numbers = []          # (macro, value as typeset, source file, row/field)

    def num(macro, value, src, where):
        assert macro.isalpha(), macro
        numbers.append({"macro": macro, "value": str(value), "file": src, "where": where})

    # ---- Table 1
    lines = []
    compared = agree = uncovered = 0
    cells = []
    for r in RULES:
        data_cells, thm_cells = [], []
        for n in NS:
            val, src, where = kstar[(r, n)]
            mark = r"$^\dagger$" if src == V154 else ""
            data_cells.append(f"{val}{mark}")
            tv = theorem_value(r, n)
            thm_cells.append(fmt_thm(tv))
            ok = agrees(tv, val)
            if ok is None:
                uncovered += 1
            else:
                compared += 1
                agree += bool(ok)
            cells.append({"rule": r, "n": n, "data": val, "file": src, "where": where, "theorem": fmt_thm(tv),
                          "agree": ok})
        lines.append(f"{r} & computed & " + " & ".join(data_cells) + r" \\")
        lines.append(rf" & {THM_LABEL[r]} & " + " & ".join(thm_cells) + r" \\")
        lines.append(r"\hline")
    head = r"rule & & " + " & ".join(str(n) for n in NS) + r" \\"
    table = "\n".join([r"\begin{tabular}{@{}rl*{" + str(len(NS)) + r"}{c}@{}}", r"\hline", head, r"\hline"] + lines
                      + [r"\end{tabular}"]) + "\n"
    num("TableNmin", NS[0], "-", "first ring size of Table 1")
    num("TableNmax", NS[-1], "-", "last ring size of Table 1")
    num("TableSweepNmax", 7, SWEEP, "ring sizes 4..7 of Table 1 are taken from this file")
    num("TableMechNmin", 8, MECH, "smallest n of the file")
    assert max(int(r["n"]) for r in read_csv(SWEEP)) >= 7 and min(int(r["n"]) for r in read_csv(SWEEP)) <= 4
    num("TableCells", len(RULES) * len(NS), "-", "cells of Table 1")
    num("TableCompared", compared, "table", "cells for which the theorems give a value")
    num("TableAgree", agree, "table", "of these, cells whose computed value is admitted by the theorems")

    # ---- rule 26: the computed values quoted in the section on rule 26 (from the outputs of proofs_94_26)
    claims = []           # statements without a number that the text takes from a data file

    def claim(key, ok, src, where, text):
        assert ok, (key, text)
        claims.append({"key": key, "holds": bool(ok), "file": src, "where": where, "statement": text})

    g26 = read_jsonl(G26)
    r4, r16, r22 = g26[4], g26[16], g26[22]
    num("TwentySixFourCycles", r4["cycles"], G26, "n=4, field cycles")
    num("TwentySixFourKv", ", ".join(str(a) for a in r4["k_c_from_the_definition"]), G26,
        "n=4, field k_c_from_the_definition (codes 000, 001, ..., 111)")
    num("KstarTwentySixAtFour", max(r4["k_c_from_the_definition"]), G26, "n=4, maximum of k_c_from_the_definition")
    num("KsevenTwentySixAtSixteen", r16["k_c_from_the_definition"][7], G26,
        "n=16, field k_c_from_the_definition, entry of code 111")
    num("KstarTwentySixAtSixteen", max(r16["k_c_from_the_definition"]), G26,
        "n=16, maximum of k_c_from_the_definition")
    reach, of = r16["cycles_with_111_reachable_from_T2"].split(" of ")
    assert int(of) == r16["cycles_by_kind"]["with_111"]
    num("TwentySixSixteenWith", int(of), G26, "n=16, field cycles_by_kind, entry with_111")
    num("TwentySixSixteenReach", int(reach), G26, "n=16, field cycles_with_111_reachable_from_T2")
    num("TwentySixSixteenCarrier", r16["cycles_with_111_through_a_carrier_word"], G26,
        "n=16, field cycles_with_111_through_a_carrier_word")
    claim("26_n16_not_only_carriers",
          r16["cycles_with_111_through_a_carrier_word"] < r16["cycles_by_kind"]["with_111"], G26,
          "n=16, fields cycles_by_kind and cycles_with_111_through_a_carrier_word",
          "at n = 16 some cycle that contains 111 does not pass through a carrier word")
    chi22 = sorted(r22["c_of_cycles_with_111"])
    num("TwentySixTwentyTwoChi", " and ".join(str(a) for a in chi22), G26, "n=22, field c_of_cycles_with_111")
    claim("26_n22_chi_below_n_over_3", 3 * min(chi22) < 22, G26, "n=22, field c_of_cycles_with_111",
          "at n = 22 some cycle that contains 111 has chi < n/3")
    for n in (4, 16):                                  # the same values in the files of the study
        assert kstar[(26, n)][0] == max(g26[n]["k_c_from_the_definition"])
        assert [int(a) for a in kc[(26, n)][0].split("-")] == g26[n]["k_c_from_the_definition"]
    even_np2 = [n for n in range(8, 23) if n % 2 == 0 and not is_pow2(n)]
    num("TwentySixEvenZero", nlist([n for n in even_np2 if kstar[(26, n)][0] == 0]), MECH,
        "rule=26, even n in 8..22 not a power of two, with kstar = 0")
    num("TwentySixEvenPos", nlist([n for n in even_np2 if kstar[(26, n)][0] >= 1]), MECH,
        "rule=26, even n in 8..22 not a power of two, with kstar >= 1")

    # ---- rule 94: n = 3, 4 and the cycles without 101
    g94 = read_jsonl(G94)
    q4 = g94[4]
    num("NinetyFourFourClosed", len(q4["closed_classes"]), G94, "n=4, number of entries of closed_classes")
    num("NinetyFourFourClassSize", q4["closed_classes"][0], G94, "n=4, field closed_classes")
    num("NinetyFourFourCodes", " and ".join(rf"$\code{{{CODES[c]}}}$" for c in q4["codes_on_K"]), G94,
        "n=4, field codes_on_K")
    claim("94_n4_class_is_block_words",
          q4["block_words"] == q4["closed_classes"][0] and q4["block_words_all_in_K"], G94,
          "n=4, fields block_words, block_words_all_in_K, closed_classes",
          "at n = 4 the closed class consists of the block words")
    num("KstarNinetyFourAtFour", kstar[(94, 4)][0], SWEEP, "rule=94, n=4, field kstar")
    rad = [r for r in read_csv(CRYSTAL) if r["rule"] == "94" and r["n"] == "3"]
    claim("94_n3_flip_leaves_crystal", len(rad) == 1 and rad[0]["radius_ge2"] == "0", CRYSTAL,
          "rule=94, n=3, field radius_ge2", "at n = 3 a single flip can leave the crystal phase")
    parts = []
    for n in (10, 14, 20, 22):
        q = g94[n]
        doubled = q["cycles_without_101"] - 1                      # all cycles without 101 except {0}
        in_k = q["cycles_without_101_in_K"] - int(q["zero_state_in_K"])
        parts.append(f"{in_k} of {doubled} at $n={n}$")
    num("NinetyFourDoubledInK", ", ".join(parts[:-1]) + " and " + parts[-1], G94,
        "n=10,14,20,22: fields cycles_without_101, cycles_without_101_in_K, zero_state_in_K")
    claim("94_n16_zero_outside_K", (not g94[16]["zero_state_in_K"]) and g94[16]["zero_state_in_degree"] == 0, G94,
          "n=16, fields zero_state_in_K, zero_state_in_degree",
          "at n = 16 the cycle {0} is not in K and no edge of G_1 enters it")

    # ---- the classes of the section on open cases: where k* >= 1 in the computed range
    for r in (35, 45, 73, 22, 60, 90):
        pos = [n for n in range(8, 23) if kstar[(r, n)][0] >= 1]
        num(f"Kpos{WORDS[r]}", nlist(pos), MECH, f"rule={r}, the n in 8..22 with kstar >= 1")
    # classes 60 and 90: the value of k* and the number of cycles at the n with k* >= 1
    cyc = set()
    for r in (60, 90):
        pos = [n for n in range(8, 23) if kstar[(r, n)][0] >= 1]
        vals = {kstar[(r, n)][0] for n in pos}
        assert len(vals) == 1, (r, vals)
        num(f"Kstar{WORDS[r]}Pos", vals.pop(), MECH, f"rule={r}, field kstar at the n in 8..22 with kstar >= 1")
        cyc |= {int(float(extra[(r, n)]["cycles"])) for n in pos}
        claim(f"{r}_only_cycle_is_zero_state",
              all(int(float(extra[(r, n)]["cycles"])) == 1 and int(float(extra[(r, n)]["n_selected"])) == 1
                  and extra[(r, n)]["selected_cover"] == "0" and extra[(r, n)]["selected_spatial_periods"] == "1"
                  and extra[(r, n)]["selected_temporal_periods"] == "1" for n in pos), MECH,
              f"rule={r}, the n in 8..22 with kstar >= 1: fields cycles, n_selected, selected_cover, "
              "selected_spatial_periods, selected_temporal_periods",
              f"class {r}: at the n of the range with k* >= 1 there is one cycle, a fixed point of spatial period 1 "
              "that contains the code 000 only, i.e. the zero state")
        claim(f"{r}_kpos_are_the_powers_of_two", pos == [n for n in range(8, 23) if is_pow2(n)], MECH,
              f"rule={r}, field kstar", f"class {r}: k* >= 1 exactly at the powers of two of the range")
    assert len(cyc) == 1, cyc
    num("CyclesSixtyNinetyPos", cyc.pop(), MECH, "rule=60 and rule=90, field cycles at the n in 8..22 with kstar >= 1")
    num("KzeroThirtySeven", nlist([n for n in range(8, 23) if kstar[(37, n)][0] == 0]), MECH,
        "rule=37, the n in 8..22 with kstar = 0")
    num("KzeroOneTwentyTwo", nlist([n for n in range(8, 23) if kstar[(122, n)][0] == 0]), MECH,
        "rule=122, the n in 8..22 with kstar = 0")
    mech_rows = read_csv(MECH)
    classes = {int(r["rule"]) for r in mech_rows}
    num("NumSwitching", len(classes), MECH, "number of distinct values of the field rule")
    assert set(RULES) <= classes and classes - set(RULES) == set(OPEN) and len(OPEN) == len(set(OPEN)), \
        "OPEN must list exactly the classes of mechanisms.csv that the theorems do not treat"
    num("NumOtherSwitching", len(classes - set(RULES)), MECH,
        "number of distinct values of the field rule, without the rules 154, 43, 142, 94, 26")
    assert min(int(r["n"]) for r in mech_rows) == 8 and max(int(r["n"]) for r in mech_rows) == 22
    num("OpenNmin", 8, MECH, "smallest n of the file")
    num("OpenNmax", 22, MECH, "largest n of the file")

    # ---- Zhu and Richard, arXiv:2610.10967 (rule 154): numbers of the cited text, from the record of its reading
    with open(os.path.join(ROOT, ZR)) as fh:
        zr = json.load(fh)
    quoted = {int(n): str(v) for n, v in zr["quoted"].items()}
    assert sorted(quoted) == [22, 24], quoted
    num("ZRValues", " and ".join(f"{quoted[n]} at $n={n}$" for n in sorted(quoted)), ZR,
        "field quoted (the values named to the session that wrote the file; printed in Figure 13 of the text "
        "according to literature_addendum.md, update of 20 November 2026)")
    with open(os.path.join(ROOT, ADDENDUM), encoding="utf-8") as fh:
        add = fh.read()
    a1 = add[add.index("### A1. Zhu and Richard"):add.index("### A2.")]
    upd = " ".join(add[add.index("## Update of 20 November 2026"):add.index("## Search queries")].split())
    hit = re.findall(r"is always below ([0-9.]+) for n∈\{(\d+),…,(\d+)\}", a1)
    assert len(hit) == 1, hit
    num("ZRBound", hit[0][0], ADDENDUM, "section A1, the sentence quoted from arXiv:2610.10967 (p. 14): the bound")
    num("ZRNmin", hit[0][1], ADDENDUM, "section A1, the sentence quoted from arXiv:2610.10967: first n of the range")
    num("ZRNmax", hit[0][2], ADDENDUM, "section A1, the sentence quoted from arXiv:2610.10967: last n of the range")
    claim("zr_values_printed_in_the_text",
          all(f'{quoted[n]}" for n = {n}' in upd for n in quoted) and "Figure 13" in upd, ADDENDUM,
          "update of 20 November 2026, item 'Rule 154'",
          "the two values are recorded as printed in Figure 13 of arXiv:2610.10967 for n = 22 and n = 24")
    claim("zr_values_agree_with_the_count", zr["quoted_values_agree"] is True and zr["all_lemma6_equal_direct"] is True,
          ZR, "fields quoted_values_agree, all_lemma6_equal_direct",
          "the two values agree with the fraction of states on no cycle counted for rule 154, and the count by the "
          "description of the periodic states equals the direct count for even n = 4..24")

    tex = ["% generated by make_numbers.py from the data files of the repository; do not edit"]
    for d in numbers:
        tex.append(rf"\newcommand{{\{d['macro']}}}{{{d['value']}}}")
    return "\n".join(tex) + "\n", table, {"numbers": numbers, "claims": claims, "table": cells}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=HERE)
    a = ap.parse_args()
    tex, table, meta = build()
    os.makedirs(a.outdir, exist_ok=True)
    with open(os.path.join(a.outdir, "numbers.tex"), "w") as fh:
        fh.write(tex)
    with open(os.path.join(a.outdir, "table_kstar.tex"), "w") as fh:
        fh.write(table)
    with open(os.path.join(a.outdir, "numbers.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    print(f"{len(meta['numbers'])} numbers, {len(meta['claims'])} claims, {len(meta['table'])} table cells -> {a.outdir}")
