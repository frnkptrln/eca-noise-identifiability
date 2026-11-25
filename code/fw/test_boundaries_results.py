"""Consistency tests of the wall results (run after the sweep: python3 -m pytest -q code/fw/test_boundaries_results.py).
(1) Proposition L + window lemma by linear algebra (affine_null.py) agree with the enumerated null sweep for all
    16 affine rules at n = 4..16; (2) the reflection partner of a null class has the same k* and the mirrored
    missed codes (all 256 rules at n = 8, recomputed); (3) complement conjugation: R under fixed-1 walls equals R*
    under null walls (k* and complemented missed codes, n = 6..9, 40 rules); (4) reflecting walls: R and R* agree."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, affine_null

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")
REFL = [4 * (c & 1) + 2 * ((c >> 1) & 1) + ((c >> 2) & 1) for c in range(8)]


def perm_mask(m, p):
    return sum(((m >> c) & 1) << p[c] for c in range(8))


def test_affine_linear_algebra_matches_sweep():
    sw = pd.read_csv(os.path.join(D, "null_sweep.csv")).set_index(["rule", "n"])
    for rule, co in affine_null.affine_rules().items():
        rep = min(rule, fwlib.reflect_rule(rule))
        for n in range(4, 17):
            a = affine_null.analyse(rule, n, co)
            assert a["kstar_ge1"] == int(sw.loc[(rep, n)].kstar >= 1), (rule, n)


def test_reflection_partner_same_kstar_n8():
    for r in range(256):
        a = fwlib.classify(r, 8, boundary="null"); b = fwlib.classify(fwlib.reflect_rule(r), 8, boundary="null")
        assert a["kstar"] == b["kstar"]
        assert perm_mask(a["stable_cover"], REFL) == b["stable_cover"]
        assert sorted(a["k_c"][REFL]) == sorted(b["k_c"]) and all(a["k_c"][c] == b["k_c"][REFL[c]] for c in range(8))


def test_complement_one_walls_equals_null():
    rng = np.random.default_rng(5)
    for r in rng.choice(256, 40, replace=False):
        r = int(r)
        for n in range(6, 10):
            F = fwlib.succ_map(r, n, "one")
            if fwlib.is_bijective(F):
                continue
            a = fwlib.classify(r, n, boundary="one"); b = fwlib.classify(fwlib.complement_rule(r), n, boundary="null")
            assert a["kstar"] == b["kstar"] and a["gmin"] == b["gmin"] and a["m"] == b["m"]
            assert all(a["k_c"][c] == b["k_c"][7 - c] for c in range(8))


def test_reflect_walls_complement_symmetry():
    for r in range(0, 256, 7):
        for n in (6, 7):
            F = fwlib.succ_map(r, n, "reflect")
            if fwlib.is_bijective(F):
                continue
            a = fwlib.classify(r, n, boundary="reflect"); b = fwlib.classify(fwlib.complement_rule(r), n, boundary="reflect")
            assert a["kstar"] == b["kstar"] and all(a["k_c"][c] == b["k_c"][7 - c] for c in range(8))
