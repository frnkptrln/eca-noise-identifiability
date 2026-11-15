"""Typed loaders for data/ring_size tables. BUG-R2: pandas parsed bit strings ('0011', codes '01234567')
as integers and dropped leading zeros; every string column is read with dtype=str here."""
import os
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "data", "ring_size")
STR_COLS = ["pattern", "codes", "selected_cover", "k_c", "selected_spatial_periods", "selected_temporal_periods",
            "word", "codes_avoided", "states", "seed_pattern"]


def load(name, out=OUT):
    path = os.path.join(out, name)
    head = pd.read_csv(path, nrows=0).columns
    return pd.read_csv(path, dtype={c: str for c in STR_COLS if c in head})


def v02_disagreements(mrg):
    """(rule, n, field) where a record merged with data/fw_sweep.csv (suffix _v02) differs from v0.2.
    gamma_min is not compared on bijective records: this study writes m - 1 there, v0.2 the placeholder 0."""
    bad = []
    for f, g in [("cycles", "cycles_v02"), ("n_selected", "n_stable"), ("gamma_min", "gamma_min_v02"), ("k_c", "k_c_v02"), ("kstar", "kstar_v02")]:
        d = mrg[mrg[f].astype(str) != mrg[g].astype(str)]
        if f == "gamma_min":
            d = d[d.bijective.astype(int) == 0]
        bad += [(int(r.rule), int(r.n), f) for r in d.itertuples()]
    return bad
