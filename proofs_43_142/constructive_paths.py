"""Executes the chains of single flips constructed in PROOF_43_142.md and checks every step by simulation
(one process; writes out/constructive_paths.json).

Part A  4 | n, every cycle (n = 4, 8, 12, 16, 20): chain of Theorem 1(2). At every step a cell is flipped that is
        interior (wall count below n/2) or isolated (above n/2); the flipped state is iterated until periodic; the
        script asserts that the new cycle has wall count w + 2 (w - 2), differs from the current one, and that the
        chain ends on X after exactly |w - n/2| / 2 flips. Two choices of the cell: the smallest admissible cell of
        the first state of the cycle, and a random admissible cell of a random state of the cycle (seed 43142).
Part B  4 | n, larger n: cycles reached from random initial states and from structured states with few or many
        walls.
Part C  the starting points of the paths stored in data/ring_size/sampled_reach/rule{43,142}_n{24,28,32}.csv: the
        chain of Theorem 1(2) from the cycle of every stored initial state x0; its length is compared with the
        stored path length.
Part D  4 does not divide n: chain of Theorem 2. (i) flips towards the levels w-, w+; (ii) one flip from the upper to
        the lower level; (iii) slides (Lemma 10) to a state with run lengths (e+2, 2, ..., 2); (iv) if this state is on
        the cycle of the complement of x0, the path of Lemma 11 (complemented); the chain must end on the cycle Z
        of z0. Every cycle for n = 5..19 (4 not dividing n), samples for larger n.

Part E  4 does not divide n: the sorting of Lemma 10(b) on the upper level. From a state without interior cell and
        with w+ walls, slides bring the run lengths to (2, ..., 2, 1, ..., 1); the final state must lie on the cycle of
        x1 (the state with these run lengths starting at cell 0 with zeros) or of its complement (Step 2 of the proof
        of Theorem 2). Every cycle of the upper level for n = 5..19, random states of the upper level for larger n.

Cycles are compared through their smallest state. Every state on which a flip is made is checked to be periodic
(F^T x = x found by iteration).
"""
import csv
import json
import os
import random
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ring  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
SEED = 43142


def bit(x, i, n):
    return (x >> (i % n)) & 1


def interior_cells(x, n):
    return [j for j in range(n) if bit(x, j - 1, n) == bit(x, j, n) == bit(x, j + 1, n)]


def isolated_cells(x, n):
    return [j for j in range(n) if bit(x, j - 1, n) != bit(x, j, n) != bit(x, j + 1, n)]


def levels(n):
    lo = max(w for w in range(0, n + 1, 2) if 2 * w < n)
    hi = min(w for w in range(0, n + 2, 2) if 2 * w > n)
    return lo, hi


def cycle_of(rule, x, n):
    cyc, _ = ring.limit_cycle(rule, x, n)
    return cyc


def is_periodic(rule, x, n):
    y = ring.step(rule, x, n)
    for _ in range(2 * n + 2):
        if y == x:
            return True
        y = ring.step(rule, y, n)
    return False


def crystal(n):
    x0 = ring.from_string("0011" * (n // 4))
    return {ring.rot_up(x0, n, k) for k in range(4)}


def towards(rule, cyc, n, target_ok, rng=None):
    """Flips towards n/2 (Theorem 1(2) / Lemma 9) until target_ok(w) holds. Returns (cycle, number of flips)."""
    flips = 0
    while True:
        x = cyc[0] if rng is None else rng.choice(cyc)
        w = ring.wall_count(x, n)
        assert all(ring.wall_count(s, n) == w for s in cyc), "wall count not constant on the cycle"
        if target_ok(w):
            return cyc, flips
        cells = interior_cells(x, n) if 2 * w < n else isolated_cells(x, n)
        assert cells, "no admissible cell"
        j = cells[0] if rng is None else rng.choice(cells)
        new = cycle_of(rule, x ^ (1 << j), n)
        w2 = ring.wall_count(new[0], n)
        assert w2 == (w + 2 if 2 * w < n else w - 2), "wall count did not move by 2 towards n/2"
        assert min(new) != min(cyc), "flip did not leave the cycle"
        cyc = new
        flips += 1


def chain_T1(rule, cyc, n, rng=None):
    """Chain of Theorem 1(2) from the cycle cyc to X. Returns the number of flips."""
    w0 = ring.wall_count(cyc[0], n)
    cyc, flips = towards(rule, cyc, n, lambda w: 2 * w == n, rng)
    assert set(cyc) == crystal(n), "chain did not end on X"
    assert flips == abs(w0 - n // 2) // 2, "chain length differs from |w - n/2| / 2"
    return flips


def runs_of(x, n):
    """Cyclic runs of a non-constant state as a list of (first cell, length), starting at a run boundary."""
    s = next(i for i in range(n) if bit(x, i - 1, n) != bit(x, i, n))
    out = []
    i = s
    while True:
        L = 1
        while bit(x, i + L, n) == bit(x, i, n) and L < n:
            L += 1
        out.append((i % n, L))
        i += L
        if i % n == s:
            break
    return out


def x0_state(n):
    lo, _ = levels(n)
    e = n - 2 * lo
    return ring.from_string("0" * (e + 2) + "1100" * ((lo - 2) // 2) + "11"), e


def lemma11_path(rule, x, n, e, base):
    """The e flips of Lemma 11 applied to the state x = base rotated/complemented copy with its long run on the
    cells base .. base+e+1: flips the cells base+e+1, ..., base+2. Returns (final state, flips)."""
    flips = 0
    y = x
    for cell in range(e + 1, 1, -1):
        y ^= 1 << ((base + cell) % n)
        assert not isolated_cells(y, n), "intermediate state of Lemma 11 has an isolated cell"
        assert is_periodic(rule, y, n), "intermediate state of Lemma 11 is not periodic"
        flips += 1
    return y, flips


def chain_T2(rule, cyc, n, stats):
    """Chain of Theorem 2 from the cycle cyc to the cycle Z of x0. Returns the number of flips."""
    lo, hi = levels(n)
    x0, e = x0_state(n)
    Z = set(cycle_of(rule, x0, n))
    CZ = set(cycle_of(rule, ring.comp(x0, n), n))
    assert x0 in Z, "x0 is not periodic"
    # (i) towards the levels
    cyc, f1 = towards(rule, cyc, n, lambda w: w in (lo, hi))
    # (ii) upper level -> lower level
    f2 = 0
    if ring.wall_count(cyc[0], n) == hi:
        cyc, f2 = towards(rule, cyc, n, lambda w: w == lo)
    # (iii) slides: move all excess into the first run
    x = cyc[0]
    assert not isolated_cells(x, n), "periodic state of the lower level has an isolated cell"
    f3 = 0
    rr = runs_of(x, n)
    assert len(rr) == lo
    starts = [s for s, _ in rr]
    lens = [L for _, L in rr]
    for k in range(lo - 1, 0, -1):
        while lens[k] > 2:
            x ^= 1 << starts[k]                      # the first cell of run k joins run k-1
            starts[k] = (starts[k] + 1) % n
            lens[k] -= 1
            lens[k - 1] += 1
            assert not isolated_cells(x, n) and ring.wall_count(x, n) == lo, "slide left the level"
            assert is_periodic(rule, x, n), "state after a slide is not periodic"
            f3 += 1
    assert lens == [e + 2] + [2] * (lo - 1)
    assert x in Z or x in CZ, "slides did not end on the cycle of x0 or of its complement"
    # (iv) from the cycle of the complement to Z
    f4 = 0
    if x not in Z:
        y, f4 = lemma11_path(rule, x, n, e, starts[0])
        assert y in Z, "Lemma 11 path did not end on Z"
        stats["used_lemma11"] += 1
    stats["max_towards"] = max(stats["max_towards"], f1)
    stats["max_slides"] = max(stats["max_slides"], f3)
    return f1 + f2 + f3 + f4


def chain_upper(rule, x, n):
    """Lemma 10(b): slides from a state x of the upper level to run lengths (2, ..., 2, 1, ..., 1). Returns the
    number of slides."""
    _, hi = levels(n)
    assert ring.wall_count(x, n) == hi and not interior_cells(x, n) and is_periodic(rule, x, n)
    rr = runs_of(x, n)
    starts = [s for s, _ in rr]
    lens = [L for _, L in rr]
    assert len(lens) == hi and set(lens) <= {1, 2}
    slides = 0
    while True:
        k = next((k for k in range(hi - 1) if lens[k] == 1 and lens[k + 1] == 2), None)
        if k is None:
            break
        x ^= 1 << starts[k + 1]                      # the first cell of run k+1 joins run k
        starts[k + 1] = (starts[k + 1] + 1) % n
        lens[k], lens[k + 1] = 2, 1
        assert not interior_cells(x, n) and ring.wall_count(x, n) == hi, "slide left the upper level"
        assert is_periodic(rule, x, n), "state after a slide is not periodic"
        slides += 1
    a, b = n - hi, 2 * hi - n
    assert lens == [2] * a + [1] * b
    x1 = ring.from_string("".join(("00", "11")[k % 2] for k in range(a)) + "".join("01"[(a + k) % 2] for k in range(b)))
    assert ring.wall_count(x1, n) == hi and not interior_cells(x1, n)
    assert x in set(cycle_of(rule, x1, n)) | set(cycle_of(rule, ring.comp(x1, n), n)), \
        "sorted state is not on the cycle of x1 or of its complement"
    return slides


def random_upper_state(n, rng):
    _, hi = levels(n)
    lens = [2] * (n - hi) + [1] * (2 * hi - n)
    rng.shuffle(lens)
    s = "".join(str(k % 2) * L for k, L in enumerate(lens))
    x = ring.from_string(s)
    x = ring.rot_up(x, n, rng.randrange(n))
    return ring.comp(x, n) if rng.random() < 0.5 else x


def all_cycles(rule, n):
    A = ring.analyse(rule, n)
    return [[int(s) for s in c] for c in A["cycles"]]


def structured_states(n, rng):
    """States with few or many walls: constant, alternating, one block, sparse and dense random wall sets."""
    out = [0, (1 << n) - 1, ring.from_string("01" * (n // 2) + "0" * (n % 2)), ring.from_string("0" * (n - 3) + "111"),
           ring.from_string("0" * (n // 2) + "1" * (n - n // 2))]
    for frac in (0.05, 0.15, 0.3, 0.7, 0.85, 0.95):
        for _ in range(3):
            k = 2 * max(1, int(frac * n / 2))
            pos = sorted(rng.sample(range(n), k))
            x, val = 0, 0
            for i in range(n):
                if i in pos:
                    val ^= 1
                x |= val << i
            out.append(x)
    return out


def main():
    t0 = time.process_time()
    rows = []
    rng = random.Random(SEED)

    # ---------------------------------------------------------------- Part A
    for rule in (43, 142):
        for n in (4, 8, 12, 16, 20):
            cycles = all_cycles(rule, n)
            L1 = [chain_T1(rule, c, n) for c in cycles]
            L2 = [chain_T1(rule, c, n, rng) for c in cycles]
            assert L1 == L2
            rows.append(dict(part="A", rule=rule, n=n, starts=len(cycles), all_end_on_target=True,
                             longest=max(L1), mean=round(sum(L1) / len(L1), 2), zero_length=sum(1 for v in L1 if v == 0),
                             note="every cycle; two choices of the flipped cell"))
            print(rows[-1], flush=True)

    # ---------------------------------------------------------------- Part B
    for rule in (43, 142):
        for n in (24, 28, 32, 48, 64, 100, 200, 400):
            starts = [rng.getrandbits(n) for _ in range(200)] + structured_states(n, rng)
            L = []
            seen = set()
            for x in starts:
                c = cycle_of(rule, x, n)
                seen.add(min(c))
                L.append(chain_T1(rule, c, n))
            rows.append(dict(part="B", rule=rule, n=n, starts=len(starts), distinct_cycles=len(seen),
                             all_end_on_target=True, longest=max(L), mean=round(sum(L) / len(L), 2),
                             zero_length=sum(1 for v in L if v == 0),
                             note="200 random initial states and 23 structured states"))
            print(rows[-1], flush=True)

    # ---------------------------------------------------------------- Part C
    for rule in (43, 142):
        for n in (24, 28, 32):
            path = os.path.join(ROOT, "data", "ring_size", "sampled_reach", f"rule{rule}_n{n}.csv")
            with open(path, newline="") as fh:
                stored = list(csv.DictReader(fh))
            eq = longer = shorter = 0
            L = []
            for r in stored:
                c = cycle_of(rule, int(r["x0"]), n)
                assert len(c) == int(r["period"]), "period differs from the stored one"
                mine = chain_T1(rule, c, n)
                L.append(mine)
                sl = int(r["path_len"])
                if r["path"]:
                    first = int(r["path"].split(";")[0].split(":")[0], 16)
                    assert is_periodic(rule, first, n)
                    assert abs(ring.wall_count(first, n) - n // 2) // 2 == mine, "stored start has another wall count"
                eq += sl == mine
                longer += sl > mine
                shorter += sl < mine
            rows.append(dict(part="C", rule=rule, n=n, starts=len(stored), all_end_on_target=True, longest=max(L),
                             mean=round(sum(L) / len(L), 2), zero_length=sum(1 for v in L if v == 0),
                             stored_equal=eq, stored_longer=longer, stored_shorter=shorter,
                             stored_max=max(int(r["path_len"]) for r in stored),
                             note="cycles of the stored initial states x0"))
            print(rows[-1], flush=True)

    # ---------------------------------------------------------------- Part D
    for rule in (43, 142):
        for n in [k for k in range(5, 20) if k % 4]:
            stats = dict(used_lemma11=0, max_towards=0, max_slides=0)
            cycles = all_cycles(rule, n)
            L = [chain_T2(rule, c, n, stats) for c in cycles]
            rows.append(dict(part="D", rule=rule, n=n, starts=len(cycles), all_end_on_target=True, longest=max(L),
                             mean=round(sum(L) / len(L), 2), zero_length=sum(1 for v in L if v == 0), **stats,
                             note="every cycle"))
            print(rows[-1], flush=True)
        for n, k in ((21, 200), (22, 200), (23, 200), (25, 200), (26, 200), (27, 200), (50, 50), (101, 50), (202, 50)):
            stats = dict(used_lemma11=0, max_towards=0, max_slides=0)
            starts = [rng.getrandbits(n) for _ in range(k)] + structured_states(n, rng)
            L = []
            seen = set()
            for x in starts:
                c = cycle_of(rule, x, n)
                seen.add(min(c))
                L.append(chain_T2(rule, c, n, stats))
            rows.append(dict(part="D", rule=rule, n=n, starts=len(starts), distinct_cycles=len(seen),
                             all_end_on_target=True, longest=max(L), mean=round(sum(L) / len(L), 2),
                             zero_length=sum(1 for v in L if v == 0), **stats,
                             note=f"{k} random initial states and 23 structured states"))
            print(rows[-1], flush=True)

    # ---------------------------------------------------------------- Part E
    for rule in (43, 142):
        for n in [k for k in range(5, 20) if k % 4]:
            _, hi = levels(n)
            cycles = [c for c in all_cycles(rule, n) if ring.wall_count(c[0], n) == hi]
            L = [chain_upper(rule, c[0], n) for c in cycles]
            rows.append(dict(part="E", rule=rule, n=n, starts=len(cycles), all_end_on_target=True, longest=max(L),
                             mean=round(sum(L) / len(L), 2), zero_length=sum(1 for v in L if v == 0),
                             note="every cycle of the upper level"))
            print(rows[-1], flush=True)
        for n, k in ((21, 100), (22, 100), (23, 100), (25, 100), (26, 100), (27, 100), (50, 50), (101, 50), (202, 20)):
            L = [chain_upper(rule, random_upper_state(n, rng), n) for _ in range(k)]
            rows.append(dict(part="E", rule=rule, n=n, starts=k, all_end_on_target=True, longest=max(L),
                             mean=round(sum(L) / len(L), 2), zero_length=sum(1 for v in L if v == 0),
                             note=f"{k} random states of the upper level"))
            print(rows[-1], flush=True)

    cpu = time.process_time() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak / 1e6 if sys.platform == "darwin" else peak / 1e3
    out = dict(script="constructive_paths.py", seed=SEED, all_chains_end_on_target=True, cpu_seconds=round(cpu, 2),
               peak_mb=round(peak_mb), rows=rows)
    with open(os.path.join(OUT, "constructive_paths.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"all chains ended on their target (any failure raises); CPU {cpu:.2f} s; peak {peak_mb:.0f} MB")


if __name__ == "__main__":
    main()
