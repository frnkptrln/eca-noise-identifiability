"""Tests of proofs_43_142/ (run: python -m pytest proofs_43_142 -q; a few seconds, one process, writes nothing).

Three kinds of tests:
  1. the statements of PROOF_43_142.md re-checked at small n with a separate implementation (tuples of cells, no
     NumPy, nothing imported from ring.py);
  2. negative controls: the same checks fail when a wrong statement is put in;
  3. consistency: the output files report no violation, the tables in PROOF_43_142.md and literature_addendum.md are
     the ones make_tables.py builds from the output files, and the numbers quoted in the prose agree with them.
"""
import itertools
import json
import os
import re
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
sys.path.insert(0, HERE)

RULES = (43, 142)
WALL = {43: 184, 142: 226}


# ------------------------------------------------------------------ separate small implementation
def f(rule, a, b, c):
    return (rule >> (4 * a + 2 * b + c)) & 1


def F(rule, x):
    n = len(x)
    return tuple(f(rule, x[i - 1], x[i], x[(i + 1) % n]) for i in range(n))


def delta(x):
    n = len(x)
    return tuple(x[i] ^ x[(i + 1) % n] for i in range(n))


def flip(x, j):
    return x[:j] + (1 - x[j],) + x[j + 1:]


def comp(x):
    return tuple(1 - v for v in x)


def sigma(x):          # (sigma x)_i = x_(i-1)
    return x[-1:] + x[:-1]


def isolated(x):
    n = len(x)
    return [j for j in range(n) if x[j - 1] != x[j] != x[(j + 1) % n]]


def interior(x):
    n = len(x)
    return [j for j in range(n) if x[j - 1] == x[j] == x[(j + 1) % n]]


def states(n):
    return itertools.product((0, 1), repeat=n)


def structure(rule, n):
    """cycle label of every state (the smallest state of the cycle its orbit ends on) and the set of cycles."""
    label = {}
    for x in states(n):
        path, seen = [], {}
        y = x
        while y not in seen and y not in label:
            seen[y] = len(path)
            path.append(y)
            y = F(rule, y)
        lab = label[y] if y in label else min(path[seen[y]:])
        for z in path:
            label[z] = lab
    periodic = [x for x in label if label[x] == label[F(rule, x)] and _on_cycle(rule, x)]
    return label, periodic


def _on_cycle(rule, x):
    y = F(rule, x)
    for _ in range(4 * len(x) + 4):
        if y == x:
            return True
        y = F(rule, y)
    return False


def closed_classes(nodes, edges):
    """Closed classes of a digraph by reachability sets (small graphs only)."""
    adj = {u: set() for u in nodes}
    for u, v in edges:
        adj[u].add(v)
    reach = {}
    for u in nodes:
        seen, stack = {u}, [u]
        while stack:
            for v in adj[stack.pop()]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        reach[u] = seen
    out = set()
    for u in nodes:
        if all(u in reach[v] for v in reach[u]):
            out.add(frozenset(reach[u]))
    return out, reach


def levels(n):
    lo = max(w for w in range(0, n + 1, 2) if 2 * w < n)
    hi = min(w for w in range(0, n + 2, 2) if 2 * w > n)
    return lo, hi


# ------------------------------------------------------------------ 1. statements at small n
def test_rule_tables_form_R():
    for a, b, c in itertools.product((0, 1), repeat=3):
        if a != c:
            assert f(142, a, b, c) == c and f(43, a, b, c) == c
        else:
            assert f(142, a, b, c) == b and f(43, a, b, c) == 1 - b
        assert f(226, a, b, c) == f(184, c, b, a)
        assert f(184, a, b, c) == int((b, c) == (1, 1) or (a, b) == (1, 0))


@pytest.mark.parametrize("rule", RULES)
def test_lemmas_1_to_7_small_n(rule):
    for n in range(3, 12):
        for x in states(n):
            d = delta(x)
            y = F(rule, x)
            assert delta(y) == F(WALL[rule], d)                              # Lemma 1
            assert sum(delta(y)) == sum(d) and sum(d) % 2 == 0               # Lemma 5
            assert F(rule, comp(x)) == comp(y)                               # Lemma 5
            P = sum(1 for i in range(n) if d[i] == d[(i + 1) % n] == 1)
            Q = sum(1 for i in range(n) if d[i] == d[(i + 1) % n] == 0)
            assert P - Q == 2 * sum(d) - n                                   # Lemma 3(c)
            iso, inte = isolated(x), interior(x)
            assert len(iso) == P and len(inte) == Q
            for j in range(n):                                               # Lemma 6
                dw = sum(delta(flip(x, j))) - sum(d)
                assert dw == (2 if j in inte else -2 if j in iso else 0)
            if not iso:                                                      # Lemma 7
                assert y == (comp(sigma(x)) if rule == 43 else x[1:] + x[:1])
            if not inte:
                assert y == (x[1:] + x[:1] if rule == 43 else comp(sigma(x)))
            assert _on_cycle(rule, x) == (not iso or not inte)


@pytest.mark.parametrize("rule", RULES)
def test_theorem_1_small_n(rule):
    for n in (4, 8, 12):
        label, periodic = structure(rule, n)
        x0 = tuple([0, 0, 1, 1] * (n // 4))
        X = {x0, sigma(x0), sigma(sigma(x0)), sigma(sigma(sigma(x0)))}
        assert {x for x in periodic if sum(delta(x)) == n // 2} == X         # Lemma 8
        lab = label[x0]
        w = {label[x]: sum(delta(x)) for x in periodic}
        edges = {(label[x], label[flip(x, j)]) for x in periodic for j in range(n)}
        edges = {e for e in edges if e[0] != e[1]}
        assert not any(u == lab for u, v in edges)                           # Theorem 1(1)
        classes, reach = closed_classes(set(w), edges)
        assert classes == {frozenset([lab])}                                 # only closed class
        # G1 distance to X equals |w - n/2| / 2 (Theorem 1(2) and the lower bound of Proposition 3)
        dist = {lab: 0}
        frontier = [lab]
        while frontier:
            nxt = []
            for v in frontier:
                for a, b in edges:
                    if b == v and a not in dist:
                        dist[a] = dist[v] + 1
                        nxt.append(a)
            frontier = nxt
        assert all(dist[c] == abs(w[c] - n // 2) // 2 for c in w)
        codes = {(x[i - 1], x[i], x[(i + 1) % n]) for x in X for i in range(n)}
        assert codes == {(0, 0, 1), (0, 1, 1), (1, 0, 0), (1, 1, 0)}


@pytest.mark.parametrize("rule", RULES)
def test_proposition_2_healing_time(rule):
    for n in (4, 8, 12, 16, 20, 40):
        x = tuple([0, 0, 1, 1] * (n // 4))
        X = {x, sigma(x), sigma(sigma(x)), sigma(sigma(sigma(x)))}
        for j in range(n):
            left = x[j - 1] != x[j]
            slow = (not left) if rule == 43 else left
            y, t = flip(x, j), 0
            while y not in X:
                y, t = F(rule, y), t + 1
                assert t <= n
            assert t == (max(1, n // 2 - 1) if slow else 1)


@pytest.mark.parametrize("rule", RULES)
def test_theorem_2_small_n(rule):
    for n in (5, 6, 7, 9, 10, 11):
        label, periodic = structure(rule, n)
        lo, hi = levels(n)
        w = {label[x]: sum(delta(x)) for x in periodic}
        edges = {(label[x], label[flip(x, j)]) for x in periodic for j in range(n)}
        edges = {e for e in edges if e[0] != e[1]}
        classes, _ = closed_classes(set(w), edges)
        K = frozenset(c for c in w if w[c] in (lo, hi))
        assert classes == {K}
        codes = {(x[i - 1], x[i], x[(i + 1) % n]) for x in periodic if label[x] in K for i in range(n)}
        assert len(codes) == 8


# ------------------------------------------------------------------ 2. negative controls
def test_negative_controls():
    n = 8
    # the wall rules are not interchangeable
    assert any(delta(F(43, x)) != F(226, delta(x)) for x in states(n))
    assert any(delta(F(142, x)) != F(184, delta(x)) for x in states(n))
    # a rule outside the two classes does not conserve the wall count
    assert any(sum(delta(F(94, x))) != sum(delta(x)) for x in states(n))
    # the healing times of the two rules are not interchangeable
    x = (0, 0, 1, 1) * 3
    X = {x, sigma(x), sigma(sigma(x)), sigma(sigma(sigma(x)))}
    y, t = flip(x, 0), 0                                  # cell 0 is a left cell: rule 43 heals it in one step
    while y not in X:
        y, t = F(142, y), t + 1
    assert t == 12 // 2 - 1 != 1
    # for n = 2 mod 4 the crystal statement is false: the cycle of 000111 can be left by one flip
    label, periodic = structure(142, 6)
    z = (0, 0, 0, 1, 1, 1)
    assert any(label[flip(z, j)] != label[z] for j in range(6))


# ------------------------------------------------------------------ 3. consistency of files, tables and text
def load(name):
    with open(os.path.join(OUT, name)) as fh:
        return json.load(fh)


def test_output_files_report_no_violation():
    lem = load("check_lemmas.json")
    assert lem["all_passed"] and all(r["violations"] == 0 and r["cases"] > 0 for r in lem["results"])
    assert {r["test"] for r in lem["results"]} == {"L1", "L2", "L3", "L4", "L5", "L6", "L7", "L7c", "L8", "L8b", "T2s",
                                                   "T1", "E", "L9", "L9b", "L10", "L10s", "L10a", "L10b", "L11"}
    with open(os.path.join(OUT, "g1_classes.jsonl")) as fh:
        g1 = [json.loads(line) for line in fh]
    assert sorted((r["rule"], r["n"]) for r in g1) == sorted((rule, n) for rule in RULES for n in range(3, 25))
    assert all(r["prediction_holds"] for r in g1)
    paths = load("constructive_paths.json")
    assert paths["all_chains_end_on_target"] and all(r["all_end_on_target"] for r in paths["rows"])
    assert load("crosscheck_data.json")["all_agree"]
    z = load("zhu_richard_154.json")
    assert z["all_lemma6_equal_direct"] and z["quoted_values_agree"] and z["all_closed_form_equal"]


def between(doc, tag):
    a, b = f"<!-- {tag} BEGIN -->\n", f"<!-- {tag} END -->"
    assert doc.count(a) == 1 and doc.count(b) == 1
    return doc.split(a)[1].split(b)[0]


def test_tables_in_documents_are_the_generated_ones():
    import make_tables
    tables, tables154 = make_tables.build()
    with open(os.path.join(OUT, "tables.md")) as fh:
        assert fh.read() == tables
    with open(os.path.join(OUT, "tables_154.md")) as fh:
        assert fh.read() == tables154
    with open(os.path.join(HERE, "PROOF_43_142.md")) as fh:
        proof = fh.read()
    assert between(proof, "TABLES") == "## 7. Computations (verbatim copy of `out/tables.md`)\n\n" + tables
    with open(os.path.join(ROOT, "literature_addendum.md")) as fh:
        assert between(fh.read(), "TABLE 154") == tables154


def test_numbers_quoted_in_the_prose():
    """Numbers stated outside section 7 of PROOF_43_142.md, checked against the output files."""
    with open(os.path.join(HERE, "PROOF_43_142.md")) as fh:
        proof = fh.read()
    prose = proof.split("<!-- TABLES BEGIN -->")[0] + proof.split("<!-- TABLES END -->")[1]
    with open(os.path.join(OUT, "g1_classes.jsonl")) as fh:
        g1 = [json.loads(line) for line in fh]
    ns = sorted({r["n"] for r in g1})
    assert f"computed for n = {ns[0]}..{ns[-1]}" in prose
    paths = load("constructive_paths.json")["rows"]
    every = sorted({r["n"] for r in paths if r["part"] == "A" or (r["part"] == "D" and r["note"] == "every cycle")})
    max4 = max(r["n"] for r in paths if r["part"] in "AB")
    maxo = max(r["n"] for r in paths if r["part"] == "D")
    assert (f"every cycle for n = {every[0]}..{every[-1]}, samples up to n = {max4} (4 \\| n) and n = {maxo} "
            f"(otherwise)") in prose
    lem = load("check_lemmas.json")
    t1 = [r for r in lem["results"] if r["test"] == "T1"]
    assert all(r["n_max"] == 400 and r["return_times_ok"] for r in t1)
    # section 8: number of cycles at n = 4; section 9: cost of reproduction
    c4 = {r["rule"]: r["cycles"] for r in g1 if r["n"] == 4}
    words = {3: "three", 5: "five"}
    assert f"{words[c4[43]]} cycles for rule 43, {words[c4[142]]} for rule 142" in prose
    z = load("zhu_richard_154.json")
    total = lem["cpu_seconds"] + load("constructive_paths.json")["cpu_seconds"] + z["cpu_seconds"] \
        + sum(r["cpu_seconds"] for r in g1)
    assert "under two minutes of CPU time" in prose and total < 120
    assert "about 1.3 GB at n = 24" in prose and 1200 <= max(r["peak_mb"] for r in g1) <= 1400
    # every "n = a..b" range named in section 8 for a script exists in the outputs
    for m in re.finditer(r"\[computed for n = (\d+)\]", prose):
        assert int(m.group(1)) in ns
    # the tests named in section 8 as added after the second reading exist
    ids = {r["test"] for r in lem["results"]}
    assert "(Table 1: L7c, L8b, L9b, L10s, L10a, L10b)" in prose and {"L7c", "L8b", "L9b", "L10s", "L10a", "L10b"} <= ids
    assert os.path.exists(os.path.join(HERE, "review", "second_read.json"))


def test_only_new_files_are_touched():
    """No existing file of the repository differs from origin/main (needs git; skipped if git is not usable)."""
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, timeout=30)
        d = subprocess.run(["git", "diff", "--name-only", "origin/main"], cwd=ROOT, capture_output=True, text=True,
                           timeout=30)
    except Exception:
        pytest.skip("git not usable here")
    if r.returncode != 0 or d.returncode != 0:
        pytest.skip("git not usable here")
    changed = [line[3:] for line in r.stdout.splitlines()] + d.stdout.split()
    allowed = ("proofs_43_142/", "literature_addendum.md", "PR_DRAFT.md", "PR_BODY.md", "VERIFICATION_43_142.md",
               "verify_43_142/")
    assert all(p.startswith(allowed) for p in changed), [p for p in changed if not p.startswith(allowed)]
