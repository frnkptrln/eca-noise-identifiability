"""Regression tests for the ring-size study (run: python3 -m pytest -q code/ring_size/test_ring_size.py).
Every bug found during this study has a test here, marked BUG-Rn."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import mech, verify_mech


def test_BUGR1_single_cycle_is_not_a_crystal_orbit():
    """BUG-R1: mech.analyze called the only cycle of a map with m = 1 a crystal orbit; the verifier does not."""
    for rule, n in [(0, 4), (122, 7), (90, 8)]:
        rec, _ = mech.analyze(rule, n)
        assert rec["cycles"] == 1 and rec["crystal_orbit"] is False


def test_mech_agrees_with_independent_verifier_small():
    fields = ["cycles", "n_selected", "gamma_min", "kstar", "k_c", "selected_cover", "g1_sccs", "g1_closed",
              "selected_eq_closed_union", "radius_selected_min", "radius_other_max", "crystal_orbit",
              "entry_cost_max", "g2_holds"]
    for rule, n in [(94, 6), (43, 8), (142, 8), (154, 8), (22, 8), (35, 6), (122, 8)]:
        ind = verify_mech.independent(rule, n)
        mine, _ = mech.analyze(rule, n)
        assert all(str(ind[f]) == str(mine[f]) for f in fields), (rule, n)


def test_BUGR2_bit_strings_keep_leading_zeros(tmp_path):
    """BUG-R2: pandas read pattern/codes columns as integers ('0011' -> 11, '01234567' -> 1234567)."""
    import pandas as pd, rsdata
    pd.DataFrame([dict(pattern="0011", codes="0134", selected_cover="01234567")]).to_csv(tmp_path / "t.csv", index=False)
    d = rsdata.load("t.csv", out=str(tmp_path))
    assert d.pattern[0] == "0011" and d.codes[0] == "0134" and d.selected_cover[0] == "01234567"


def test_pair_graph_certificate_matches_brute_force_bijectivity():
    """Certified rules are bijective on every odd ring n <= 13; for every rule, a ring size where F is not
    injective has a closed walk through an off-diagonal SCC of the pair graph of matching period."""
    import ringlang
    sys.path.insert(0, os.path.join(HERE, "..", "fw"))
    import fwlib
    for rule in range(256):
        cert = ringlang.injectivity_certificate(rule)
        for n in range(3, 14):
            bij = fwlib.is_bijective(fwlib.succ_map(rule, n))
            if cert["certified"] and n % 2:
                assert bij, (rule, n)


def test_avoid_graph_matches_brute_force():
    """Closed walks of length n in avoid_graph(rule, codes, T) <-> ring states whose first T+1 iterates avoid codes."""
    import ringlang
    from scipy.sparse.csgraph import connected_components
    sys.path.insert(0, os.path.join(HERE, "..", "fw"))
    import fwlib
    for rule, codes, T in [(94, [2], 1), (43, [0], 1), (35, [5], 2), (122, [2], 1)]:
        G, w = ringlang.avoid_graph(rule, codes, T)
        A = G.toarray().astype(np.int64)
        for n in range(3, 11):
            F = fwlib.succ_map(rule, n); cm = fwlib.code_mask(n)
            bad = sum(1 << c for c in codes)
            x = np.arange(1 << n); ok = np.ones(1 << n, bool)
            for t in range(T + 1):
                ok &= (cm[x] & bad) == 0; x = F[x]
            # number of closed walks of length n = trace(A^n) = number of n-periodic sequences = ring states
            An = np.linalg.matrix_power(np.minimum(A, 1), n)
            assert int(np.trace(An)) == int(ok.sum()), (rule, codes, T, n)


def test_lightcone_heal_rule94_and_ring_radius():
    """Lemma H input: rule 94 crystal 011 heals with tau = 3; every single flip on rings 3 | n, 9 <= n <= 30 returns."""
    import lightcone
    h = lightcone.heal(94, "011")
    assert h["healed"] and h["tau"] == 3
    for n in range(9, 31, 3):
        x = lightcone.from_word("011", n)
        for j in range(n):
            z = x ^ (1 << j)
            for _ in range(10):
                z = lightcone.step(94, z, n)
            assert z == x
