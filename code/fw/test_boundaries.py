"""Guarding tests for the boundary-aware successor map and code mask (run: python3 -m pytest -q
code/fw/test_boundaries.py).

RING-*: the ring stays bit-identical. The default boundary is the ring; these tests recompute the ring
results for n = 4..12 (all 88 class representatives) with the modified code and compare every result
field with data/fw_sweep.csv, compare succ_map / code_mask with a verbatim copy of the version-0.4
functions, and regenerate ring certificates byte for byte.
WALL-*: the wall versions against a naive per-cell implementation, and the symmetries used in
Section 2 of report_boundaries.md (reflection for every boundary; complement maps null to fixed-1).
These tests compute no stochastic potentials under walls."""
import gzip, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
import pytest
import fwlib, cert, check_cert

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")


# --- verbatim copies of the version-0.4 (commit 2765f7e) ring functions --------------------------
def succ_map_v04(rule, n):
    x = np.arange(1 << n, dtype=np.int64)
    out = np.zeros_like(x)
    for i in range(n):
        l = (x >> ((i - 1) % n)) & 1
        c = (x >> i) & 1
        r = (x >> ((i + 1) % n)) & 1
        out |= ((rule >> (4 * l + 2 * c + r)) & 1) << i
    return out


def code_mask_v04(n):
    x = np.arange(1 << n, dtype=np.int64)
    m = np.zeros(1 << n, dtype=np.uint8)
    for i in range(n):
        l = (x >> ((i - 1) % n)) & 1
        c = (x >> i) & 1
        r = (x >> ((i + 1) % n)) & 1
        m |= (np.uint8(1) << (4 * l + 2 * c + r).astype(np.uint8))
    return m


def test_RING_succ_and_codes_identical_to_v04():
    for n in range(1, 13):
        cm = fwlib.code_mask(n)
        assert cm.dtype == np.uint8 and np.array_equal(cm, code_mask_v04(n))
        assert np.array_equal(fwlib.code_mask(n, "ring"), cm)
        for rule in range(256):
            F = fwlib.succ_map(rule, n)
            assert F.dtype == np.int64 and np.array_equal(F, succ_map_v04(rule, n))


def test_RING_sweep_n4_12_identical_to_fw_sweep_csv():
    import run_sweep
    ref = pd.read_csv(os.path.join(DATA, "fw_sweep.csv"), dtype=str)
    ref = ref[ref.n.astype(int) <= 12].set_index(["n", "rule"])
    assert len(ref) == 9 * 88
    for n in range(4, 13):
        for rule in fwlib.class_reps():
            rec = run_sweep.job((n, rule, 0, "_unused"))          # cert_nmax = 0: writes nothing
            row = ref.loc[(str(n), str(rule))]
            for f in run_sweep.RESULT_FIELDS[2:]:
                assert str(rec[f]) == row[f], (n, rule, f, rec[f], row[f])


@pytest.mark.parametrize("n,rule", [(8, 1), (10, 26), (12, 94), (12, 154), (9, 43), (11, 106)])
def test_RING_certificates_byte_identical(n, rule, tmp_path):
    src = os.path.join(DATA, "fw_certificates_sweep", f"n{n:02d}_rule_{rule:03d}.json.gz")
    if not os.path.exists(src):
        pytest.skip("no stored certificate")
    p = str(tmp_path / "c.json.gz")
    cert.write(cert.make_certificate(fwlib.classify(rule, n)), p)
    a = gzip.open(p).read(); b = gzip.open(src).read()
    assert a == b


def test_RING_checker_ring_functions_unchanged():
    for n in range(1, 11):
        assert np.array_equal(check_cert.codes_of(n), code_mask_v04(n).astype(np.int64))
        for rule in (0, 30, 90, 110, 154, 255):
            assert np.array_equal(check_cert.succ(rule, n), succ_map_v04(rule, n))


# --- walls -------------------------------------------------------------------------------------------
def naive(rule, n, x, boundary):
    """Successor and code set of state x, cell by cell from a Python list (wall cells explicit)."""
    cells = [(x >> i) & 1 for i in range(n)]
    wl = {"null": 0, "one": 1, "reflect": cells[0]}[boundary]
    wr = {"null": 0, "one": 1, "reflect": cells[-1]}[boundary]
    row = [wl] + cells + [wr]
    y, codes = 0, set()
    for i in range(n):
        c = 4 * row[i] + 2 * row[i + 1] + row[i + 2]
        codes.add(c)
        y |= ((rule >> c) & 1) << i
    return y, codes


@pytest.mark.parametrize("boundary", ["null", "one", "reflect"])
def test_WALL_succ_and_codes_against_naive(boundary):
    for n in range(1, 9):
        cm = fwlib.code_mask(n, boundary)
        cm2 = check_cert.codes_of(n, boundary)
        for rule in range(256):
            F = fwlib.succ_map(rule, n, boundary)
            assert np.array_equal(F, check_cert.succ(rule, n, boundary))
            if rule % 17 == 0:
                for x in range(1 << n):
                    y, codes = naive(rule, n, x, boundary)
                    assert F[x] == y
                    assert int(cm[x]) == sum(1 << c for c in codes) == int(cm2[x])


def test_WALL_null_edge_codes():
    """Null walls: the left edge cell reads codes 0..3, the right edge cell even codes, the single
    cell of n = 1 reads 0 or 2; every code occurs in some state for n >= 3 (at an interior cell)."""
    for n in range(2, 11):
        x = np.arange(1 << n)
        left = 2 * (x & 1) + ((x >> 1) & 1)
        right = 4 * ((x >> (n - 2)) & 1) + 2 * ((x >> (n - 1)) & 1)
        cm = fwlib.code_mask(n, "null")
        assert set(np.unique(left)) == {0, 1, 2, 3} and set(np.unique(right)) == {0, 2, 4, 6}
        assert ((cm >> left) & 1).all() and ((cm >> right) & 1).all()
        assert int(np.bitwise_or.reduce(cm)) == (255 if n >= 3 else 0b01011111)
    assert list(fwlib.code_mask(1, "null")) == [1, 4]


def reverse_bits(x, n):
    y = np.zeros_like(x)
    for i in range(n):
        y |= ((x >> i) & 1) << (n - 1 - i)
    return y


def code_perm(mask, perm):
    out = np.zeros_like(mask)
    for c in range(8):
        out |= ((mask >> c) & 1) << perm[c]
    return out


REFL = [4 * (c & 1) + 2 * ((c >> 1) & 1) + ((c >> 2) & 1) for c in range(8)]   # 1<->4, 3<->6
COMP = [7 - c for c in range(8)]


@pytest.mark.parametrize("boundary", ["ring", "null", "one", "reflect"])
def test_WALL_reflection_conjugation(boundary):
    """rev o F_R = F_{refl R} o rev, and codes(rev x) = refl(codes(x)), for every boundary."""
    for n in range(1, 11):
        x = np.arange(1 << n, dtype=np.int64)
        rx = reverse_bits(x, n)
        cm = fwlib.code_mask(n, boundary).astype(np.int64)
        assert np.array_equal(cm[rx], code_perm(cm, REFL))
        for rule in range(256):
            F = fwlib.succ_map(rule, n, boundary)
            G = fwlib.succ_map(fwlib.reflect_rule(rule), n, boundary)
            assert np.array_equal(G[rx], reverse_bits(F, n))


def test_WALL_complement_maps_null_to_one():
    """~ o F_R^null = F_{R*}^one o ~ with R* = complement_rule(R), codes(~x) under 'one' = 7 - codes(x)
    under 'null'; the same with the walls exchanged; ring and reflect are complement-invariant."""
    for n in range(1, 11):
        full = (1 << n) - 1
        x = np.arange(1 << n, dtype=np.int64)
        for b1, b2 in (("null", "one"), ("one", "null"), ("ring", "ring"), ("reflect", "reflect")):
            c1 = fwlib.code_mask(n, b1).astype(np.int64); c2 = fwlib.code_mask(n, b2).astype(np.int64)
            assert np.array_equal(c2[full ^ x], code_perm(c1, COMP))
            for rule in range(256):
                F = fwlib.succ_map(rule, n, b1)
                G = fwlib.succ_map(fwlib.complement_rule(rule), n, b2)
                assert np.array_equal(G[full ^ x], full ^ F)


def test_WALL_complement_is_not_a_null_symmetry():
    """Complement does not preserve null walls: for n = 6 the null maps of R and R* are conjugate by ~
    only when R* equals R under null walls up to ~ -- record how many rules satisfy that (it is not all)."""
    n = 6; full = (1 << n) - 1; x = np.arange(1 << n)
    same = [r for r in range(256)
            if np.array_equal(fwlib.succ_map(fwlib.complement_rule(r), n, "null")[full ^ x],
                              full ^ fwlib.succ_map(r, n, "null"))]
    assert len(same) < 256


def test_WALL_unknown_boundary_rejected():
    with pytest.raises(ValueError):
        fwlib.succ_map(30, 5, "nul")
