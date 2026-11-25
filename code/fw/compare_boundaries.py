"""Ring vs null comparison. data/boundaries/ring_vs_null.csv: one row per rule (all 256) and n with the ring k*
(class representative, data/fw_sweep.csv, n = 4..20) and the null k* (reflection representative,
data/boundaries/null_sweep.csv), the codes missed by the selected cycles, and both bijectivity flags.
Prints the markdown table of the named classes used in report_boundaries.md, Section 5."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import fwlib

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
ring = pd.read_csv(os.path.join(D, "fw_sweep.csv")).set_index(["rule", "n"])
null = pd.read_csv(os.path.join(D, "boundaries", "null_sweep.csv")).set_index(["rule", "n"])
rows = []
for r in range(256):
    rc = fwlib.class_rep(r); nc = min(r, fwlib.reflect_rule(r))
    for n in range(4, 21):
        a = ring.loc[(rc, n)] if (rc, n) in ring.index else None
        b = null.loc[(nc, n)] if (nc, n) in null.index else None
        rows.append(dict(rule=r, n=n, ring_class=rc, null_class=nc,
                         ring_kstar=None if a is None else int(a.kstar), null_kstar=None if b is None else int(b.kstar),
                         ring_bijective=None if a is None else int(a.bijective), null_bijective=None if b is None else int(b.bijective),
                         null_missed=None if b is None else b.missed_codes))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(D, "boundaries", "ring_vs_null.csv"), index=False)

ns = list(range(4, 21))
def cell(v):
    return "" if v is None or pd.isna(v) else str(int(v))
order = [(94, [94, 133]), (43, [43]), (142, [142]), (35, [35, 59]), (26, [26, 167]), (37, [37, 91]), (154, [154, 166]),
         (22, [22, 151]), (60, [60, 153]), (90, [90, 165]), (122, [122, 161]), (45, [45, 75]), (73, [73, 109]),
         (150, [150]), (30, [30, 135]), (110, [110, 137]), (126, [126, 129])]
print("| ring class | boundary | rule | " + " | ".join(map(str, ns)) + " |")
print("|---|---|---|" + "---|" * len(ns))
for rc, nrs in order:
    print(f"| {rc} | ring | {rc} | " + " | ".join(cell(ring.loc[(rc, n)].kstar) if (rc, n) in ring.index else "" for n in ns) + " |")
    for k, nr in enumerate(nrs):
        lab = "null" if k == 0 else "null (= fixed-1 of %d)" % rc
        print(f"| | {lab} | {nr} | " + " | ".join(cell(null.loc[(nr, n)].kstar) if (nr, n) in null.index else "" for n in ns) + " |")
