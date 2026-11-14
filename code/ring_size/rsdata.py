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
