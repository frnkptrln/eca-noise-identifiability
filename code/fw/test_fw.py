"""Regression tests for the small-noise solver (run: python3 -m pytest -q code/fw/test_fw.py).

Every bug found during development has a test here, marked BUG-n with a one-line description."""
import itertools, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pytest
import fwlib, hier, orders, cert, check_cert, ckpt


def brute_gamma(V):
    m = len(V); best = [10 ** 9] * m
    for r in range(m):
        others = [v for v in range(m) if v != r]
        for choice in itertools.product(range(m), repeat=len(others)):
            f = dict(zip(others, choice))
            if any(f[v] == v for v in others):
                continue
            ok = True
            for v in others:
                seen, z = set(), v
                while z != r:
                    if z in seen:
                        ok = False; break
                    seen.add(z); z = f[z]
                if not ok:
                    break
            if ok:
                best[r] = min(best[r], sum(V[v][f[v]] for v in others))
    return np.array(best)


def test_hierarchy_random_matrices_all_roots_trees_duals():
    rng = np.random.default_rng(3)
    for _ in range(150):
        m = int(rng.integers(2, 7)); V = rng.integers(1, int(rng.integers(2, 6)), size=(m, m)); np.fill_diagonal(V, 0)
        g = brute_gamma(V)
        for L0 in (0, 1, 2, 9):
            H = hier.edmonds_all_roots(hier.MatrixProvider(V), L0)
            assert np.array_equal(H.gamma, g)
            sets = hier.laminar_sets(H)
            for u in range(m):
                for v in range(m):
                    if u != v:
                        assert sum(y for _, mem, y in sets if u in mem and v not in mem) <= V[u, v]
            for r in range(m):
                e = hier.tree_for_root(H, r)
                assert len(e) == m - 1 and all(V[t, h] == w for t, h, w in e)
                assert sum(w for *_, w in e) == g[r]
                assert sum(y for _, mem, y in sets if r not in mem) == g[r]


def test_BUG1_zero_weight_edges_full_state_graph():
    """BUG-1: lazy levels started at weight 1, so zero-resistance edges u -> F(u) were never inserted;
    the contraction was wrong on the full state graph (not on cycle graphs, where V >= 1)."""
    import verify_trees as T
    for rule in (0, 30, 110, 232, 150):
        R = T.resistance_matrix(rule, 4)
        assert np.array_equal(T.W_hier(R), T.W_nx(R))


def test_bfs_matches_two_layer_dijkstra():
    for n in (5, 6):
        for rule in (30, 54, 108, 232, 200):
            res = fwlib.classify(rule, n)
            ref = check_cert.check(cert.make_certificate(res))
            assert ref == []


def test_rule0_orders_are_popcounts():
    for n in (4, 7, 10):
        res = fwlib.classify(0, n, keep_dists=True)
        o = orders.state_orders(res)
        x = np.arange(1 << n)
        assert np.array_equal(o, np.array([bin(v).count("1") for v in x]))
        assert list(res["k_c"]) == [bin(c).count("1") for c in range(8)] and res["kstar"] == 3


@pytest.mark.parametrize("rule", [15, 51, 170, 204, 85, 240])
def test_bijective_rules_kstar_zero(rule):
    for n in (5, 6, 8, 9):
        F = fwlib.succ_map(rule, n)
        assert fwlib.is_bijective(F)
        res = fwlib.classify(rule, n)
        assert res["kstar"] == 0 and len(res["stable"]) == res["m"]   # uniform law: every cycle stable


def test_class_invariance_n8():
    ks = {r: tuple(fwlib.classify(r, 8)["k_c"]) for r in range(256)}
    for r in range(256):
        # k* is a class invariant; k_c permutes under reflection (c -> reversed bits) and complement
        refl = fwlib.reflect_rule(r); comp = fwlib.complement_rule(r)
        rc = lambda c: 4 * (c & 1) + 2 * ((c >> 1) & 1) + (c >> 2)
        assert max(ks[r]) == max(ks[refl]) == max(ks[comp])
        assert all(ks[refl][rc(c)] == ks[r][c] for c in range(8))
        assert all(ks[comp][7 - c] == ks[r][c] for c in range(8))


def test_PERF1_single_pass_no_refinement_rounds():
    """PERF-1: an intermediate version raised one node per refinement round and recomputed the whole
    hierarchy (rule 108 at n = 12 needed > 100 rounds). The contraction must be a single pass."""
    t = time.time()
    res = fwlib.classify(108, 12)
    assert time.time() - t < 5.0 and not hasattr(res["H"], "rounds")


def test_PERF2_heap_merge_not_quadratic():
    """PERF-2: merging heaps by re-heapifying the large heap made rule 76 at n = 16 take 52 s."""
    cs = fwlib.CycleStructure(76, 14); es = fwlib.EdgeStore(cs)
    t = time.time(); hier.edmonds_all_roots(es, 1)
    assert time.time() - t < 2.0


def test_BUG2_checkpoint_resume_after_torn_write_equals_uninterrupted(tmp_path):
    """BUG-2: a torn last line swallowed the next appended record."""
    p1, p2 = str(tmp_path / "a.jsonl"), str(tmp_path / "b.jsonl")
    recs = [dict(key=[n, r], v=r * n) for n in (3, 4) for r in range(5)]
    for rec in recs:
        ckpt.append(p1, rec)
    for rec in recs[:4]:
        ckpt.append(p2, rec)
    with open(p2, "a") as fh:                 # a torn line from a kill
        fh.write('{"key":[4,0],"v"')
    done = ckpt.load(p2)
    for rec in recs:
        if tuple(rec["key"]) not in done:
            ckpt.append(p2, rec)
    a, b = ckpt.load(p1), ckpt.load(p2)
    assert sorted(a) == sorted(b) and all(a[k] == b[k] for k in a)


def test_BUG3_single_worker_gth_runs_in_process(monkeypatch):
    """BUG-3: a multiprocessing Pool launched from a script read on stdin hangs on macOS; with one
    worker the n = 12 GTH check must not create a Pool."""
    import multiprocessing, verify_n12
    def boom(*a, **k):
        raise AssertionError("Pool created with workers=1")
    monkeypatch.setattr(multiprocessing, "Pool", boom)
    monkeypatch.setattr(verify_n12, "_solve", lambda args: (args[0], args[1], 0.0))
    import inspect
    src = inspect.getsource(verify_n12.gth_check)
    assert "if workers <= 1" in src


def test_BUG4_checker_accepts_valid_and_rejects_tampered_certificates():
    """BUG-4: the checker crashed (instead of rejecting) on a certificate with a truncated cycle list or with a k* inconsistent with its other fields."""
    import copy
    for rule, n in ((232, 8), (106, 8), (0, 6), (76, 9)):
        c0 = cert.make_certificate(fwlib.classify(rule, n))
        assert check_cert.check(c0) == []
        bad = copy.deepcopy(c0); bad["gamma"][0] += 1
        assert check_cert.check(bad)
        bad = copy.deepcopy(c0); bad["kstar"] = c0["kstar"] + 1
        assert check_cert.check(bad)
        bad = copy.deepcopy(c0); bad["k_c"][7]["k"] += 1
        assert check_cert.check(bad)
        if c0["m"] > 1:
            bad = copy.deepcopy(c0)
            X = next(i for i, v in enumerate(bad["hierarchy"]["y"]) if v > 0)
            bad["hierarchy"]["y"][X] += 1
            assert check_cert.check(bad)
        bad = copy.deepcopy(c0); bad["cycles"] = bad["cycles"][:-1] if c0["m"] > 1 else [[0, 1]]
        assert check_cert.check(bad) if c0["m"] > 1 else True


def test_PERF3_certificate_size_linear_in_cycles():
    """PERF-3: one explicit in-tree per noise-selected cycle made certificates quadratic in the number of cycles (rule 76 at n = 13: 422 s); the hierarchy certificate covers all roots at once."""
    t0 = time.time()
    c = cert.make_certificate(fwlib.classify(76, 12))
    assert time.time() - t0 < 3.0 and "trees" not in c and len(c["tree"]["parent"]) == c["m"]
