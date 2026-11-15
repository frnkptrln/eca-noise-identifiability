"""Regression tests for the ring-size study (run: python3 -m pytest -q code/ring_size/test_ring_size.py).
Every bug found during this study has a test here, marked BUG-Rn. Tests marked VER-Ax / VER-Dx belong to
the findings (A) and proofs (D) of the independent verification (VERIFICATION_ring_size.md)."""
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


# ---------------------------------------------------------------- findings of the independent verification

def _fw():
    sys.path.insert(0, os.path.join(HERE, "..", "fw"))
    import fwlib
    return fwlib


def test_VER_A1_rule22_seed_orbit_returns_at_n241():
    """A1: the single-flip orbit of the zero state under rule 22 at n = 241 reaches 0, after 1303564 steps
    (beyond the 400000-step cut-off of run_local.py; found by the verification)."""
    import lightcone
    x, t = 1, 0
    while x and t < 1400000:
        x = lightcone.step(22, x, 241); t += 1
    assert x == 0 and t == 1303564


def test_VER_A1_A8_seed_status_merges_study_and_verification():
    import pandas as pd, rsdata, verif
    ss = verif.seed_status(pd.read_csv(os.path.join(rsdata.OUT, "seed_orbits.csv")))
    ret = lambda r: sorted(int(n) for n in ss[(ss.rule == r) & (ss.status == "returns")].n)
    opn = lambda r: sorted(int(n) for n in ss[(ss.rule == r) & (ss.status == "open")].n)
    assert 241 in ret(22) and opn(22) == [242, 243]
    assert ret(26) == ret(154) == [4, 8, 16, 32, 64, 128, 256] and opn(26) == opn(154) == []
    assert ret(122) == [7, 15, 31, 63, 127, 255] and len(opn(122)) == 13


def test_VER_A2_A3_classes_45_and_73_selected_sets():
    """A2, A3: not all cycles of class 45 are selected at n = 18, 22; the uniform 2-cycle of class 73 is
    not selected at n = 9 and at n = 22 (the report sentences are generated from these tables)."""
    import rsdata
    M = rsdata.load("mechanisms.csv"); O = rsdata.load("cycle_orbits.csv.gz")
    m = M[M.rule == 45].set_index("n")
    assert (int(m.n_selected[18]), int(m.cycles[18])) == (199, 201) and (int(m.n_selected[22]), int(m.cycles[22])) == (271, 272)
    u = O[(O.rule == 73) & O.pattern.map(lambda q: set(q) == {"0"})]
    assert sorted(int(n) for n in u[~u.selected].n) == [9, 22]
    assert int(M[(M.rule == 73) & (M.n == 22)].kstar.iloc[0]) == 0


def test_VER_A6_A7_prediction_counts_and_class26_row():
    import pandas as pd, rsdata
    P = pd.read_csv(os.path.join(rsdata.OUT, "predictions_outcome.csv"))
    assert P.outcome.value_counts().to_dict() == {"holds": 41, "fails": 6, "not tested": 1, "holds (trivially)": 1,
                                                  "holds (observed, sampled)": 1}
    r = P[P.part == "26, other n with k* >= 1: missing code 7"].iloc[0]
    assert r.outcome == "fails" and "fails at n = 8" in r.evidence
    r = P[P.part == "class 154, n = 22: k* = 0"].iloc[0]
    assert r.outcome == "holds" and "v154_n22.json" in r.evidence


def test_VER_A17_gamma_min_of_bijective_maps_is_m_minus_1():
    """A17: for a bijective map every potential is m - 1 (G1 strongly connected); the tables carry that value."""
    import rsdata
    for rule, n in [(154, 5), (45, 5), (154, 7)]:
        ind = verify_mech.independent(rule, n)
        assert ind["gamma_min"] == ind["cycles"] - 1 and ind["n_selected"] == ind["cycles"]
    for name in ("mechanisms.csv", os.path.join("atlas", "mechanisms_atlas.csv")):
        M = rsdata.load(name); b = M[M.bijective.astype(int) == 1]
        assert len(b) and bool((b.gamma_min.astype(int) == b.cycles.astype(int) - 1).all())


def test_VER_A18_stored_sampled_paths_verify():
    """A18: every stored one-flip path of two sampled files is exact (re-verified from the csv)."""
    import pandas as pd, rsdata, sample_reach, lightcone
    for name, rule, n, word in [("rule94_n24.csv", 94, 24, "011"), ("rule22_n30.csv", 22, 30, None)]:
        s = pd.read_csv(os.path.join(rsdata.OUT, "sampled_reach", name), dtype={"cycle_label": object, "path": str})
        tcyc = [0] if word is None else sample_reach.limit(rule, lightcone.from_word(word, n), n)
        tlab = sample_reach.canon_label(tcyc, n)
        for r in s[s.found == 1].head(40).itertuples():
            path = [] if not isinstance(r.path, str) or not r.path else [
                (int(a.split(":")[0], 16), int(a.split(":")[1].split(">")[0]), int(a.split(">")[1], 16)) for a in r.path.split(";")]
            assert len(path) == r.path_len
            if path:
                assert sample_reach.verify_path(rule, n, int(r.cycle_label), path, tlab)


def test_VER_A24_rule45_is_complement_of_mirror_of_rule154():
    fw = _fw()
    for n in (5, 6, 7, 8):
        x = np.arange(1 << n)
        mirror = np.zeros_like(x)
        for i in range(n):
            mirror |= ((x >> i) & 1) << ((n - i) % n)
        F154, F210, F45 = fw.succ_map(154, n), fw.succ_map(210, n), fw.succ_map(45, n)
        assert bool((F210[mirror] == mirror[F154]).all())             # rule 210 is the mirror image of rule 154
        assert bool((F45 == ((1 << n) - 1) ^ F210).all())             # rule 45 is the output complement of rule 210


def test_VER_D1_rule94_frozen_101_and_closed_classes():
    """D1 (Theorem V94): 101 is frozen under rule 94; fully frozen states are fixed; at 3 | n the closed classes
    of G1 are the three crystal phases, S is these three cycles and k* = 1."""
    import lightcone
    for n in range(3, 13):
        full = (1 << n) - 1
        for x in range(1 << n):
            l = ((x << 1) | (x >> (n - 1))) & full; r = ((x >> 1) | (x << (n - 1))) & full
            occ = l & ~x & r                                           # centres of 101
            y = lightcone.step(94, x, n)
            ly = ((y << 1) | (y >> (n - 1))) & full; ry = ((y >> 1) | (y << (n - 1))) & full
            assert occ & ~(ly & ~y & ry) == 0, (n, x)                  # every occurrence persists
            frozen = occ | ((occ << 1) | (occ >> (n - 1))) & full | ((occ >> 1) | (occ << (n - 1))) & full
            if frozen == full:
                assert y == x
    for n in (6, 9, 12):
        rec, _ = mech.analyze(94, n)
        assert rec["g1_closed"] == 3 and rec["n_selected"] == 3 and rec["kstar"] == 1 and rec["selected_cover"] == "356"


def test_VER_D2_rule154_permutes_M_and_selection():
    """D2 (Theorem V154): on an even ring, states with the same image lie on one parity class, F permutes the
    set M of states with ones on both parity classes; k* = 1 at n = 4, 8 with S = {0}, k* = 0 at n = 6, 10."""
    fw = _fw()
    for n in (4, 6, 8, 10, 12):
        F = fw.succ_map(154, n); x = np.arange(1 << n)
        E = sum(1 << i for i in range(0, n, 2)); Od = sum(1 << i for i in range(1, n, 2))
        inM = ((x & E) != 0) & ((x & Od) != 0)
        assert bool(inM[F[inM]].all()) and len(np.unique(F[inM])) == int(inM.sum())
        cnt = np.bincount(F, minlength=1 << n)
        assert not inM[cnt[F] > 1].any()                               # collisions only outside M
    for n in (3, 5, 7, 9):
        assert fw.is_bijective(fw.succ_map(154, n))
    for n, k in ((4, 1), (8, 1), (6, 0), (10, 0)):
        rec, _ = mech.analyze(154, n)
        assert rec["kstar"] == k and rec["g1_closed"] == 1
        assert rec["n_selected"] == (1 if k else rec["cycles"]) and rec["gamma_min"] == rec["cycles"] - 1


def test_VER_D3_rule26_zero_state_radius_at_odd_n():
    """D3 (Proposition V26): for odd n the only preimages of 0 under rule 26 are 0 and 1^n, and 1^n has no
    preimage, so the single-flip orbit of 0 never returns to 0."""
    fw = _fw(); import lightcone
    for n in (5, 7, 9, 11, 13):
        F = fw.succ_map(26, n); full = (1 << n) - 1
        assert sorted(np.nonzero(F == 0)[0].tolist()) == [0, full] and not (F == full).any()
        x = 1; seen = set()
        while x and x not in seen:
            seen.add(x); x = lightcone.step(26, x, n)
        assert x != 0
