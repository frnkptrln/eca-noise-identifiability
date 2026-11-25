"""Reflection classes of the 256 rules (the unit under null walls) and how the 88 ring classes split.
Usage: python3 code/fw/null_classes.py  (writes data/boundaries/null_classes.csv)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import fwlib

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")


def null_rep(r):
    return min(r, fwlib.reflect_rule(r))


def null_class_reps():
    return sorted({null_rep(r) for r in range(256)})


if __name__ == "__main__":
    rows = []
    for r in null_class_reps():
        rows.append(dict(null_rep=r, members=";".join(str(v) for v in sorted({r, fwlib.reflect_rule(r)})),
                         reflection_symmetric=int(fwlib.reflect_rule(r) == r), ring_class=fwlib.class_rep(r),
                         complement_partner=null_rep(fwlib.complement_rule(r)),
                         self_partner=int(null_rep(fwlib.complement_rule(r)) == r)))
    df = pd.DataFrame(rows)
    os.makedirs(DATA, exist_ok=True)
    df.to_csv(os.path.join(DATA, "null_classes.csv"), index=False)
    print(len(df), "null classes;", int(df.reflection_symmetric.sum()), "reflection-symmetric;",
          df.ring_class.nunique(), "ring classes;", int((df.groupby("ring_class").size() == 1).sum()), "not split")
