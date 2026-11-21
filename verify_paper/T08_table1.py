"""T08 -- Table 1 of the paper recounted and recomputed.

(1) Reads paper/table_kstar.tex and paper/numbers.tex (data files of the paper, not scripts) and recounts: number of
    cells, number of cells in which the row "theorem" gives a value, number of those in which the computed value is
    one of the values admitted. Compares with the macros TableCells, TableCompared, TableAgree.
(2) Derives the "theorem" rows from the statements of the theorems (written here by hand from the paper):
      154: n >= 3: 1 if n is a power of two, else 0                     (Theorem 3.11)
      43, 142: n >= 4: 1 if 4 | n, else 0                               (Theorem 3.28)
      94: 1 if 3 | n and n >= 6; 0 if 3 does not divide n and n >= 5; no statement for n = 3, 4   (Theorem 3.43)
      26: n = 4: ">=1" (S = {{0}}, Lemma 2.2); n = 2^k, k >= 3 odd: 1; k >= 4 even: "1/2"; otherwise no statement
          (Theorem 5.7, Propositions 5.8, 5.9)
    and compares with the table.
(3) Recomputes the "computed" rows with the own engine (k* from the definitions, minimum in-tree for every root):
    values from out/T03_rule154.csv, out/T05_rule94.csv, out/T06_rules43_142.csv, out/T07_rule26.csv, and, computed
    here, rule 26 at odd n and rules 43, 142, 26 up to NX (default 20). Cells not recomputed are listed.
Output: out/T08.txt, out/T08_table1.csv.  Usage: python3 T08_table1.py [path of paper/] [NX=20] [NX154=18]
"""
import sys, time, os, re, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def theorem_value(rule, n):
    if rule == 154:
        return "1" if n & (n - 1) == 0 else "0"
    if rule in (43, 142):
        return ("1" if n % 4 == 0 else "0") if n >= 4 else "--"
    if rule == 94:
        if n % 3 == 0: return "1" if n >= 6 else "--"
        return "0" if n >= 5 else "--"
    if rule == 26:
        if n & (n - 1) == 0:
            k = n.bit_length() - 1
            if k == 2: return ">=1"
            return "1" if k % 2 == 1 else "1/2"
        return "--"

def admits(tv, kstar):
    return {"0": kstar == 0, "1": kstar == 1, "1/2": kstar in (1, 2), ">=1": kstar >= 1}[tv]

def main():
    paper = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "paper")
    NX = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    NX154 = int(sys.argv[3]) if len(sys.argv) > 3 else 18
    t0 = time.process_time(); w0 = time.time()
    L = []; fails = 0
    tab = open(os.path.join(paper, "table_kstar.tex")).read()
    num = open(os.path.join(paper, "numbers.tex")).read()
    macro = lambda name: re.search(r"\\newcommand\{\\%s\}\{(.*)\}" % name, num).group(1)
    lines = [l for l in tab.split("\n") if "&" in l]
    clean = lambda c: c.replace("\\\\", "").replace("$^\\dagger$", "").replace("$\\ge$", ">=").strip()
    ns = [int(clean(c)) for c in lines[0].split("&")[2:]]
    table = {}
    i = 1
    while i < len(lines):
        c1 = [clean(c) for c in lines[i].split("&")]; c2 = [clean(c) for c in lines[i + 1].split("&")]
        rule = int(c1[0])
        table[rule] = (dict(zip(ns, c1[2:])), dict(zip(ns, c2[2:])), c2[1])
        i += 2
    cells = sum(len(v[0]) for v in table.values())
    compared = sum(1 for v in table.values() for n in ns if v[1][n] != "--")
    agree = sum(1 for v in table.values() for n in ns if v[1][n] != "--" and admits(v[1][n], int(v[0][n])))
    ok = (cells, compared, agree) == (int(macro("TableCells")), int(macro("TableCompared")), int(macro("TableAgree")))
    if not ok: fails += 1
    L.append("(1) recount: %d cells, %d with a value of a theorem, %d of these agree; macros of the paper: %s, %s, %s -> %s" % (
        cells, compared, agree, macro("TableCells"), macro("TableCompared"), macro("TableAgree"), "ok" if ok else "DIFFERENT"))
    kinds = {}
    for v in table.values():
        for n in ns: kinds[v[1][n]] = kinds.get(v[1][n], 0) + 1
    L.append("    entries of the theorem rows by kind: %s (the caption counts '>=1' and '1/2' as 'give a value')" % dict(sorted(kinds.items())))
    bad = [(rule, n, table[rule][1][n], theorem_value(rule, n)) for rule in table for n in ns if table[rule][1][n] != theorem_value(rule, n)]
    if bad: fails += 1
    L.append("(2) theorem rows against the statements of the theorems: %d of %d cells equal%s" % (cells - len(bad), cells, "" if not bad else "; differences (rule, n, table, statement): %s" % bad))
    # (3) own values
    own = {}
    def load(fn, rulecol=None, rule=None):
        p = os.path.join(HERE, "out", fn)
        if not os.path.exists(p): return
        for row in csv.DictReader(open(p)):
            r_ = int(row[rulecol]) if rulecol else rule
            own[(r_, int(row["n"]))] = int(row["kstar"])
    load("T03_rule154.csv", rule=154); load("T05_rule94.csv", rule=94); load("T06_rules43_142.csv", rulecol="rule"); load("T07_rule26.csv", rule=26)
    computed_here = []
    for rule in (26, 43, 142, 154):
        for n in ns:
            lim = NX154 if rule == 154 else NX
            if (rule, n) in own or n > lim: continue
            S = vc.System(rule, n, level=2, workers=2)
            own[(rule, n)] = S.indices()[1]
            computed_here.append((rule, n))
    rows = ["rule,n,table_computed,table_theorem,theorem_statement,own_kstar,own_equals_table"]
    ndiff = 0; nown = 0; missing = []
    for rule in sorted(table):
        for n in ns:
            o = own.get((rule, n))
            eq = "" if o is None else str(int(o == int(table[rule][0][n])))
            if o is None: missing.append((rule, n))
            else:
                nown += 1; ndiff += (o != int(table[rule][0][n]))
            rows.append("%d,%d,%s,%s,%s,%s,%s" % (rule, n, table[rule][0][n], table[rule][1][n], theorem_value(rule, n), "" if o is None else o, eq))
    if ndiff: fails += 1
    L.append("(3) 'computed' rows against own k* from the definitions: %d of %d cells recomputed, %d differ; computed in this script: %s" % (nown, cells, ndiff, computed_here))
    L.append("    cells not recomputed (rule, n): %s" % missing)
    L.append("T08 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0, time.time() - w0))
    print("\n".join(L))
    open(os.path.join(HERE, "out", "T08.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(HERE, "out", "T08_table1.csv"), "w").write("\n".join(rows) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
