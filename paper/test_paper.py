"""Tests of paper/: every number of the paper against the data files, and the build of the PDF.

Run from the repository root or from paper/:   python -m pytest paper/test_paper.py -q
The build test needs pdflatex (and bibtex with plain.bst, or pybtex) on PATH; without pdflatex it FAILS, unless
PAPER_ALLOW_NO_TEX=1 is set, in which case it is skipped.

What "every number" means here.  The text of ring_size_paper.tex contains three kinds of numerals:
  (a) values taken from data files: they enter only through the macros of numbers.tex and through table_kstar.tex,
      both written by make_numbers.py.  Tests 1 to 5 recompute each of them here, with separate code, from the files.
  (b) numbers that belong to the mathematics or name its objects (rule numbers, ring sizes in statements and in the
      simulated figures, indices, exponents) and bibliographic numbers and dates.  They are not data.  Test 6 lists
      every numeral of the source that is not of kind (a) and compares the list with the allowlist below, so that a
      number typed by hand into the text is noticed.
  (c) statements without a number that the text takes from a data file ("claims" of numbers.json): test 4.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True


def _csv(rel):
    with open(os.path.join(ROOT, rel), newline="") as fh:
        return list(csv.DictReader(fh))


def _jsonl(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return {int(json.loads(l)["n"]): json.loads(l) for l in fh if l.strip()}


def _read(name):
    with open(os.path.join(HERE, name)) as fh:
        return fh.read()


def _macros():
    return dict(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}\{(.*)\}\s*$", _read("numbers.tex"), flags=re.M))


def _kstar():
    """k* by (rule, n), read independently of make_numbers.py: n <= 7 from fw_sweep.csv, n >= 8 from mechanisms.csv."""
    k = {}
    for r in _csv("data/fw_sweep.csv"):
        if int(r["n"]) <= 7:
            k[(int(r["rule"]), int(r["n"]))] = int(r["kstar"])
    for r in _csv("data/ring_size/mechanisms.csv"):
        k[(int(r["rule"]), int(r["n"]))] = int(float(r["kstar"]))
    return k


# ---------------------------------------------------------------- 1. generated files are up to date

def test_generated_files_are_fresh(tmp_path):
    subprocess.run([sys.executable, os.path.join(HERE, "make_numbers.py"), "--outdir", str(tmp_path)], check=True,
                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    for name in ("numbers.tex", "table_kstar.tex", "numbers.json"):
        assert (tmp_path / name).read_text() == _read(name), f"{name} is stale: run make_numbers.py"


# ---------------------------------------------------------------- 2. Table 1 against the data files

def _theorem(rule, n):
    """The statements of the paper, written out once more (not imported from make_numbers.py)."""
    pow2 = n & (n - 1) == 0
    if rule == 154:
        return "1" if pow2 else "0"
    if rule in (43, 142):
        return "1" if n % 4 == 0 else "0"
    if rule == 94:
        if n % 3 == 0:
            return "1" if n >= 6 else "--"
        return "0" if n >= 5 else "--"
    if rule == 26:
        if pow2 and n >= 8:
            return "1" if n in (8, 32, 128) else "1/2"          # 2^k with k odd / k even
        if n == 4:
            return r"$\ge$1"
        return "--"
    raise ValueError(rule)


def test_table_against_data_files():
    k = _kstar()
    v154 = json.load(open(os.path.join(ROOT, "verify_ring_size/phase2/out/v154_n22.json")))
    assert (154, 22) not in k and v154["rule"] == 154 and v154["n"] == 22
    rows = [l for l in _read("table_kstar.tex").splitlines() if "&" in l]
    assert [c.strip(" \\") for c in rows[0].split("&")][2:] == [str(n) for n in range(4, 23)]
    body = rows[1:]
    assert len(body) == 10
    compared = agree = 0
    for i, rule in enumerate((154, 43, 142, 94, 26)):
        data = [c.strip(" \\") for c in body[2 * i].split("&")]
        thm = [c.strip(" \\") for c in body[2 * i + 1].split("&")]
        assert data[0] == str(rule) and data[1] == "computed" and thm[0] == ""
        for n, d, t in zip(range(4, 23), data[2:], thm[2:]):
            if (rule, n) == (154, 22):
                assert d == f"{v154['kstar']}" + r"$^\dagger$"
                value = int(v154["kstar"])
            else:
                assert d == str(k[(rule, n)]), (rule, n)
                value = k[(rule, n)]
            assert t == _theorem(rule, n), (rule, n, t)
            if t != "--":
                compared += 1
                agree += value >= 1 if t == r"$\ge$1" else str(value) in t.split("/")
    m = _macros()
    assert (int(m["TableCompared"]), int(m["TableAgree"]), int(m["TableCells"])) == (compared, agree, 95)
    assert compared == agree, "a computed value contradicts a theorem"


def test_overlap_of_the_two_data_files():
    """mechanisms.csv (n >= 8) and fw_sweep.csv (n <= 20) agree where both have the five rules."""
    sweep = {(int(r["rule"]), int(r["n"])): int(r["kstar"]) for r in _csv("data/fw_sweep.csv")}
    k = _kstar()
    for rule in (154, 43, 142, 94, 26):
        for n in range(8, 21):
            assert sweep[(rule, n)] == k[(rule, n)], (rule, n)


# ---------------------------------------------------------------- 3. every macro of numbers.tex

def _ns(pred, rule, lo=8, hi=22):
    k = _kstar()
    return ", ".join(str(n) for n in range(lo, hi + 1) if pred(k[(rule, n)], n)) or "none"


def test_every_number_against_data_files():
    m = _macros()
    k = _kstar()
    g26 = _jsonl("proofs_94_26/out/g1_26.jsonl")
    g94 = _jsonl("proofs_94_26/out/g1_classes_94.jsonl")
    mech = _csv("data/ring_size/mechanisms.csv")
    pow2 = lambda n: n & (n - 1) == 0
    codes = ["000", "001", "010", "011", "100", "101", "110", "111"]
    doubled = []
    for n in (10, 14, 20, 22):
        q = g94[n]
        doubled.append(f"{q['cycles_without_101_in_K'] - int(q['zero_state_in_K'])} of "
                       f"{q['cycles_without_101'] - 1} at $n={n}$")
    expected = {
        "TableNmin": "4", "TableNmax": "22", "TableSweepNmax": "7",
        "TableMechNmin": str(min(int(r["n"]) for r in mech)),
        "TableCells": "95",
        "NumSwitching": str(len({r["rule"] for r in mech})),
        "OpenNmin": str(min(int(r["n"]) for r in mech)), "OpenNmax": str(max(int(r["n"]) for r in mech)),
        "TwentySixFourCycles": str(g26[4]["cycles"]),
        "TwentySixFourKv": ", ".join(map(str, g26[4]["k_c_from_the_definition"])),
        "KstarTwentySixAtFour": str(k[(26, 4)]),
        "KsevenTwentySixAtSixteen": str(g26[16]["k_c_from_the_definition"][7]),
        "KstarTwentySixAtSixteen": str(k[(26, 16)]),
        "TwentySixSixteenWith": str(g26[16]["cycles_by_kind"]["with_111"]),
        "TwentySixSixteenReach": g26[16]["cycles_with_111_reachable_from_T2"].split(" of ")[0],
        "TwentySixSixteenCarrier": str(g26[16]["cycles_with_111_through_a_carrier_word"]),
        "TwentySixTwentyTwoChi": " and ".join(map(str, sorted(g26[22]["c_of_cycles_with_111"]))),
        "TwentySixEvenZero": _ns(lambda v, n: v == 0 and n % 2 == 0 and not pow2(n), 26),
        "TwentySixEvenPos": _ns(lambda v, n: v >= 1 and n % 2 == 0 and not pow2(n), 26),
        "NinetyFourFourClosed": str(len(g94[4]["closed_classes"])),
        "NinetyFourFourClassSize": str(g94[4]["closed_classes"][0]),
        "NinetyFourFourCodes": " and ".join(r"$\code{%s}$" % codes[c] for c in g94[4]["codes_on_K"]),
        "KstarNinetyFourAtFour": str(k[(94, 4)]),
        "NinetyFourDoubledInK": ", ".join(doubled[:-1]) + " and " + doubled[-1],
        "KposThirtyFive": _ns(lambda v, n: v >= 1, 35),
        "KposFortyFive": _ns(lambda v, n: v >= 1, 45), "KposSeventyThree": _ns(lambda v, n: v >= 1, 73),
        "KposTwentyTwo": _ns(lambda v, n: v >= 1, 22),
        "KzeroThirtySeven": _ns(lambda v, n: v == 0, 37), "KzeroOneTwentyTwo": _ns(lambda v, n: v == 0, 122),
    }
    derived = {"TableCompared", "TableAgree"}                            # checked in test_table_against_data_files
    assert set(m) == set(expected) | derived, set(m) ^ (set(expected) | derived)
    for name, value in expected.items():
        assert m[name] == value, (name, m[name], value)
    # the same values in the second file that has them
    assert max(g26[4]["k_c_from_the_definition"]) == k[(26, 4)]
    assert max(g26[16]["k_c_from_the_definition"]) == k[(26, 16)]
    # what the text says in words about these numbers
    assert m["KposThirtyFive"] == ", ".join(str(n) for n in range(8, 23) if n % 3 == 0)    # "the multiples of 3"
    assert m["KposFortyFive"] == "8" and m["KposSeventyThree"] == "9"                       # "only"
    assert int(m["TwentySixSixteenReach"]) == 0 and int(m["KstarTwentySixAtSixteen"]) == 2


# ---------------------------------------------------------------- 4. claims without a number

def test_claims_against_data_files():
    claims = {c["key"]: c for c in json.loads(_read("numbers.json"))["claims"]}
    g26 = _jsonl("proofs_94_26/out/g1_26.jsonl")
    g94 = _jsonl("proofs_94_26/out/g1_classes_94.jsonl")
    crystal = [r for r in _csv("data/ring_size/crystal_radius.csv") if r["rule"] == "94" and r["n"] == "3"]
    checks = {
        "26_n16_not_only_carriers":
            g26[16]["cycles_with_111_through_a_carrier_word"] < g26[16]["cycles_by_kind"]["with_111"],
        "26_n22_chi_below_n_over_3": min(g26[22]["c_of_cycles_with_111"]) < 22 / 3,
        "94_n4_class_is_block_words":
            g94[4]["block_words"] == g94[4]["closed_classes"][0] == 2 and g94[4]["block_words_all_in_K"],
        "94_n3_flip_leaves_crystal": len(crystal) == 1 and crystal[0]["radius_ge2"] == "0",
        "94_n16_zero_outside_K": not g94[16]["zero_state_in_K"] and g94[16]["zero_state_in_degree"] == 0,
    }
    assert set(claims) == set(checks)
    for key, ok in checks.items():
        assert ok and claims[key]["holds"], key


# ---------------------------------------------------------------- 5. the text uses the macros, all of them

def _body():
    tex = re.sub(r"(?<!\\)%.*", "", _read("ring_size_paper.tex"))
    return tex[tex.index(r"\begin{document}"):]


def test_macros_used_and_defined():
    m = _macros()
    body = _body() + _read("table_kstar.tex")
    for name in m:
        assert re.search(r"\\%s(?![A-Za-z])" % name, body), f"\\{name} is defined but not used"
    assert r"\input{numbers.tex}" in _read("ring_size_paper.tex") and r"\input{table_kstar.tex}" in body
    for marker in ("\\GAP", "\\SOURCEERR", "\\DATA", "TODO", "??"):
        assert marker not in body, marker


# ---------------------------------------------------------------- 6. no number typed by hand

# Numerals of the source that are not data (kind (b) of the module docstring), with the reason.
ALLOWED = {
    # rule numbers
    "18", "22", "26", "35", "37", "43", "45", "60", "73", "90", "94", "122", "142", "154", "184", "226",
    # ring sizes and constants in statements, proofs and captions (16, 12, 24: the simulated rings of the figures)
    "10", "12", "16", "24", "64", "256",
    # bibliographic: pages, sections, statement and equation numbers of references, volumes, years, identifiers
    "28", "29", "38", "49", "61", "1991", "1993", "3.3", "3.4", "3.5", "3.7", "6.2", "2610.10967",
    # dates of the sessions (statement on the use of AI; from the git log and the verification reports)
    "13", "14", "17", "20", "2026",
}


def _numerals():
    body = _body()
    body = re.sub(r"\\(label|ref|eqref|cite|input|includegraphics|bibliography|bibliographystyle)(\[[^\]]*\])?\{[^}]*\}",
                  " ", body)
    body = re.sub(r"\\code\{[01]+\}", " ", body)                      # codes and words of cells
    body = re.sub(r"\\texttt\{[^}]*\}", " ", body)                    # file names
    body = re.sub(r"\\href\{[^}]*\}\{[^}]*\}|\\url\{[^}]*\}", " ", body)  # links (ORCID, DOI, repository)
    body = re.sub(r"p\{[0-9.]+\\textwidth\}|width=[0-9.]+\\textwidth|[0-9.]+(pt|em|ex|cm)", " ", body)
    body = re.sub(r"\\[A-Za-z]+\*?", " ", body)                        # remaining commands, e.g. the \ge of \ge10
    # a numeral: not part of a word or identifier (A070886, 4a), dots only between digits
    return set(re.findall(r"(?<![\w.])\d+(?:\.\d+)*(?!\w)", body))


def test_no_number_typed_by_hand():
    found = _numerals()
    stray = sorted(x for x in found if not (x.isdigit() and int(x) <= 9) and x not in ALLOWED)
    assert not stray, f"numerals in the text that are neither macros nor allowlisted: {stray}"
    unused = sorted(ALLOWED - found)
    assert not unused, f"allowlist entries that no longer occur in the text: {unused}"


# ---------------------------------------------------------------- 7. figures

def test_figures_are_reproduced(tmp_path):
    """make_figures.py asserts the statements of its panel titles; here it runs into a temporary folder."""
    code = ("import sys; sys.dont_write_bytecode = True; sys.path.insert(0, %r); import make_figures as f; "
            "f.OUT = %r; print(f.fig_crystal_43()); print(f.fig_zero_154())") % (HERE, str(tmp_path))
    out = subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True,
                         env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}).stdout
    assert "'tau_left': 1, 'tau_right': 11" in out and "16: {'transient': 8, 'period': 1}" in out
    for name in ("fig_crystal_43.pdf", "fig_zero_154.pdf"):
        assert (tmp_path / name).stat().st_size > 1000
        assert os.path.exists(os.path.join(HERE, "figures", name)), f"figures/{name} is missing: run make_figures.py"


# ---------------------------------------------------------------- 8. the PDF builds

def test_pdf_builds(tmp_path):
    tex = os.environ.get("PDFLATEX", "pdflatex")
    if shutil.which(tex) is None:
        if os.environ.get("PAPER_ALLOW_NO_TEX") == "1":
            pytest.skip("no pdflatex on PATH (PAPER_ALLOW_NO_TEX=1)")
        pytest.fail("no pdflatex on PATH: the build of the PDF cannot be checked")
    r = subprocess.run(["bash", os.path.join(HERE, "build.sh"), str(tmp_path)], capture_output=True, text=True,
                       env={**os.environ, "PYTHON": sys.executable})
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-4000:]
    pdf = tmp_path / "ring_size_paper.pdf"
    assert pdf.stat().st_size > 50_000
    log = (tmp_path / "ring_size_paper.log").read_text(errors="replace")
    assert "undefined" not in log.lower().replace("undefined control sequence", "X") or \
        not re.search(r"(Reference|Citation) `[^']*' .* undefined", log), "undefined reference or citation"
    assert not re.search(r"^! ", log, flags=re.M), "LaTeX error"
    try:
        from pypdf import PdfReader
    except ImportError:
        return
    text = "\n".join((p.extract_text() or "") for p in PdfReader(str(pdf)).pages)
    assert "??" not in text, "unresolved reference in the PDF"
    for needle in ("Theorem A", "Rule 154", "Rules 43 and 142", "Rule 94", "Rule 26", "References",
                   "Proofs of the lemmas for rule 94"):
        assert needle in text, needle
    # the committed PDF has the same number of pages as a fresh build
    committed = os.path.join(HERE, "ring_size_paper.pdf")
    if os.path.exists(committed):
        assert len(PdfReader(committed).pages) == len(PdfReader(str(pdf)).pages), "paper/ring_size_paper.pdf is stale"
