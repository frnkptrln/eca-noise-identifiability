"""Runs the construction of PROOF_94.md (rule 94, 3 | n) and checks every step by direct simulation.

For a start cycle C the proof gives a chain of single flips
    stage 1 (Lemma 3): flip a non-frozen cell so that a new 101 appears, until every cell is frozen;
    stage 2 (Lemmas 4, 5): on block words of 01/011, swap (01)(011) -> (011)(01) and merge (01)^3 -> (011)^2,
which must end on a crystal phase (a rotation of (011)^(n/3)).  Here each flip is applied to a state of the
current cycle, the flipped state is iterated until it is periodic, and it is checked that the cycle reached
differs from the current one (so the step is an edge of G1) and is the one the proof predicts.

Part A: every cycle, n = 6, 9, ..., 21 (cycles enumerated with ring94.analyse).
Part B: random initial states relaxed to their cycle, n = 24 ... 300 (fixed seed).
Part C: start cycles without any 101: the all-zero state and doubled words D(u) (n = 2m, m odd, u of even weight;
        the period of such a start is recorded when it is at most PCAP steps, otherwise as "None").

Run from the repository root:  python verify_ring_size/part2_94/constructive_paths.py
Output: verify_ring_size/part2_94/out/constructive_paths.json
"""
import json
import os
import sys
import time
import resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ring94 import analyse, bits

CAP = 2_000_000      # steps allowed in one relaxation
PCAP = 20_000        # steps allowed when determining the period of a doubled start state


def step(x):
    a = np.roll(x, 1)      # a_i = x_(i-1)
    c = np.roll(x, -1)     # c_i = x_(i+1)
    return (a ^ c) | (x & (1 - (a & c)))


def frozen(x):
    a = np.roll(x, 1)
    c = np.roll(x, -1)
    cen = (1 - x) & a & c
    return cen | np.roll(cen, 1) | np.roll(cen, -1)


def key(x):
    return x.tobytes()


def relax(x):
    """Returns (a state of the cycle reached from x, its period, transient length); Brent's algorithm."""
    power = lam = 1
    tort = x
    hare = step(x)
    steps = 1
    while key(tort) != key(hare):
        if power == lam:
            tort = hare
            power *= 2
            lam = 0
        hare = step(hare)
        lam += 1
        steps += 1
        if steps > CAP:
            raise RuntimeError("cap reached")
    tort = hare = x
    for _ in range(lam):
        hare = step(hare)
    mu = 0
    while key(tort) != key(hare):
        tort = step(tort)
        hare = step(hare)
        mu += 1
    return tort, lam, mu


def cycle_states(x, lam):
    out = [x]
    for _ in range(lam - 1):
        out.append(step(out[-1]))
    return out


def same_cycle(x, lam, y):
    """Is y a state of the cycle through x (period lam)?"""
    ky = key(y)
    z = x
    for _ in range(lam):
        if key(z) == ky:
            return True
        z = step(z)
    return False


def growth_cell(x, fz):
    n = len(x)
    if not x.any():
        return 0
    i = int(np.flatnonzero(fz == 0)[0])
    L, R = x[i - 1], x[(i + 1) % n]
    if x[i] == 1:
        if L == 1 and R == 1:
            return i
        if L == 0:
            return (i - 2) % n
        return (i + 2) % n
    if L == 0 and R == 1:
        return (i - 1) % n
    if L == 1 and R == 0:
        return (i + 1) % n
    k = 2
    while x[(i + k) % n] == 0:
        k += 1
    return (i + k - 2) % n


def parse_blocks(x):
    """x fully frozen: returns (start cell of the first block, list of block lengths 2 / 3) cut before a 0."""
    n = len(x)
    z = [int(i) for i in np.flatnonzero(x == 0)]
    start = z[0]
    lens = [(z[(k + 1) % len(z)] - z[k]) % n or n for k in range(len(z))]
    assert all(l in (2, 3) for l in lens), lens
    return start, lens


def run_chain(x0, lam0):
    """x0: a state of the start cycle (period lam0).  Returns statistics of the chain to the crystal."""
    n = len(x0)
    x, lam = x0, lam0
    n_growth = n_swap_flips = n_merge = 0
    # ---- stage 1 ----
    while True:
        fz = frozen(x)
        if fz.all():
            break
        j = growth_cell(x, fz)
        assert fz[j] == 0
        y = x.copy()
        y[j] ^= 1
        z, lam2, _ = relax(y)
        fz2 = frozen(z)
        assert (fz2 >= fz).all() and fz2.sum() > fz.sum(), "frozen set did not grow"
        # the frozen set is constant on a cycle and has grown, so the cycle is new; direct check when the
        # period of the start cycle is known
        assert lam is None or not same_cycle(x, lam, z)
        x, lam = z, lam2
        n_growth += 1
    assert lam == 1
    # ---- stage 2 ----
    while True:
        start, lens = parse_blocks(x)
        a = lens.count(2)
        if a == 0:
            break
        assert a % 3 == 0 and a >= 3
        m = len(lens)
        pos = [start]
        for l in lens[:-1]:
            pos.append(pos[-1] + l)
        trip = [k for k in range(m) if lens[k] == 2 and lens[(k + 1) % m] == 2 and lens[(k + 2) % m] == 2]
        if trip:
            p = pos[trip[0]] % n
            y = x.copy()
            y[(p + 3) % n] ^= 1
            z, lam2, _ = relax(y)
            exp = x.copy()
            for k, v in enumerate((0, 1, 1, 0, 1, 1)):
                exp[(p + k) % n] = v
            assert lam2 == 1 and key(z) == key(exp) and key(z) != key(x)
            x = z
            n_merge += 1
            continue
        # leftmost adjacent (short, long) in the linear word cut at `start`
        k = next(k for k in range(m - 1) if lens[k] == 2 and lens[k + 1] == 3)
        p = pos[k] % n
        y = x.copy()
        y[(p + 2) % n] ^= 1
        z, lam2, _ = relax(y)
        assert lam2 == 2 and not same_cycle(z, 2, x)
        w = z if z[(p + 2) % n] == 0 else step(z)
        assert w[(p + 2) % n] == 0 and w[(p + 3) % n] == 0
        y2 = w.copy()
        y2[(p + 2) % n] ^= 1
        z2, lam3, _ = relax(y2)
        exp = x.copy()
        for q, v in enumerate((0, 1, 1, 0, 1)):
            exp[(p + q) % n] = v
        assert lam3 == 1 and key(z2) == key(exp) and not same_cycle(z, 2, z2)
        x = z2
        n_swap_flips += 2
    crystal = np.array([0, 1, 1] * (n // 3), np.uint8)
    assert any(key(np.roll(crystal, r)) == key(x) for r in range(3)), "did not end on a crystal phase"
    return dict(growth=n_growth, swap_flips=n_swap_flips, merges=n_merge,
                length=n_growth + n_swap_flips + n_merge)


def summarise(rows):
    L = [r["length"] for r in rows]
    return dict(chains=len(rows), all_end_on_crystal=True, max_length=max(L), mean_length=round(sum(L) / len(L), 2),
                max_growth=max(r["growth"] for r in rows), max_swap_flips=max(r["swap_flips"] for r in rows),
                max_merges=max(r["merges"] for r in rows))


def main():
    t0 = time.process_time()
    out = dict(A=[], B=[], C=[])
    # ---- Part A ----
    for n in range(6, 22, 3):
        A = analyse(94, n)
        rows = []
        for c in A["cycles"]:
            x = np.array([int(ch) for ch in bits(c[0], n)], np.uint8)
            rows.append(run_chain(x, len(c)))
        s = summarise(rows)
        s.update(n=n, cycles=len(A["cycles"]), chains_of_length_0=sum(1 for r in rows if r["length"] == 0))
        out["A"].append(s)
        print("A", s, flush=True)
    # ---- Part B ----
    rng = np.random.default_rng(94)
    for n in (24, 27, 30, 45, 60, 99, 150, 300):
        rows = []
        periods = {}
        for _ in range(200):
            x = rng.integers(0, 2, n).astype(np.uint8)
            z, lam, mu = relax(x)
            periods[lam] = periods.get(lam, 0) + 1
            rows.append(run_chain(z, lam))
        s = summarise(rows)
        s.update(n=n, start_period_hist=sorted(periods.items()))
        out["B"].append(s)
        print("B", s, flush=True)
    # ---- Part C ----
    for n in (6, 18, 30, 42, 54, 66, 90, 150, 300):
        rows = []
        x = np.zeros(n, np.uint8)
        rows.append(run_chain(x, 1))
        periods = {"1": 1}
        m = n // 2
        ndbl = 0
        if m % 2 == 1:
            for _ in range(20):
                u = rng.integers(0, 2, m).astype(np.uint8)
                if u.sum() % 2 == 1:
                    u[0] ^= 1
                if not u.any():
                    continue
                x = np.repeat(u, 2)
                assert not frozen(x).any()
                # x = D(u) is periodic: on doubled words F acts as u -> u + shift(u) followed by a shift of the
                # doubling by one cell, and for m odd this map is injective on words of even weight.  The period
                # is determined by a bounded search; if it exceeds PCAP it is recorded as unknown (lam = None).
                y = step(x)
                lam = 1
                while key(y) != key(x) and lam < PCAP:
                    y = step(y)
                    lam += 1
                if key(y) != key(x):
                    lam = None
                periods[str(lam)] = periods.get(str(lam), 0) + 1
                rows.append(run_chain(x, lam))
                ndbl += 1
        s = summarise(rows)
        s.update(n=n, doubled_starts=ndbl, start_period_hist=sorted(periods.items()))
        out["C"].append(s)
        print("C", s, flush=True)
    out["cpu_seconds"] = round(time.process_time() - t0, 2)
    out["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 << 20), 1)
    with open(os.path.join(HERE, "out", "constructive_paths.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("cpu_seconds", out["cpu_seconds"], "peak_rss_mb", out["peak_rss_mb"])


if __name__ == "__main__":
    main()
