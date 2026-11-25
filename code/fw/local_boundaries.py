"""Checks beyond the enumerated sizes (no enumeration of 2^n states), null walls unless stated.
(1) crystal radius: for a given fixed point or cycle X, every single flip of every state of X is followed
    until it returns to X or reaches another cycle (Floyd-free: dictionary of visited states, step limit);
    r(X) >= 2 iff every flip returns. Rules/patterns: 94 with (011) crystal 11(011)^k, n = 2 mod 3;
    133 with (010) pattern (010)^(n/3), 3 | n; 75 with 11(011)^k, n = 2 mod 3.
(2) seed orbits: for rules with F(0) = 0, whether the orbit of every e_i returns to 0 (r(0) >= 2 iff yes).
Outputs: data/boundaries/local_radius.csv, data/boundaries/local_seed.csv
Usage: python3 local_boundaries.py --nmax 200"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")


def step(rule, n, x, boundary="null"):
    """One step on an int state (bit i = cell i), wall values inserted."""
    full = (1 << n) - 1
    if boundary == "null":
        left, right = 0, 0
    elif boundary == "one":
        left, right = 1, 1
    l = ((x << 1) | left) & full                       # cell i sees x_{i-1}; cell 0 sees the left wall
    r = (x >> 1) | (right << (n - 1))                  # cell i sees x_{i+1}; cell n-1 sees the right wall
    c = x
    y = 0
    for code in range(8):
        if (rule >> code) & 1:
            m = (l if code & 4 else ~l) & (c if code & 2 else ~c) & (r if code & 1 else ~r) & full
            y |= m
    return y


def orbit_until(rule, n, x, targets, limit=10 ** 6, boundary="null"):
    """Follow x; True if it enters targets, False if it closes a cycle elsewhere, None at the limit."""
    seen = set()
    for _ in range(limit):
        if x in targets:
            return True
        if x in seen:
            return False
        seen.add(x); x = step(rule, n, x, boundary)
    return None


def cycle_of(rule, n, x, boundary="null"):
    cyc = [x]; y = step(rule, n, x, boundary)
    while y != x:
        cyc.append(y); y = step(rule, n, y, boundary)
        assert len(cyc) < 10 ** 6
    return cyc


def pattern(n, word, offset=0):
    return sum(int(word[(i + offset) % len(word)]) << i for i in range(n))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--nmax", type=int, default=200)
    a = ap.parse_args()
    rows = []
    specs = [(94, "110", lambda n: n % 3 == 2), (75, "110", lambda n: n % 3 == 2), (133, "010", lambda n: n % 3 == 0)]
    for rule, word, ok in specs:
        for n in range(4, a.nmax + 1):
            if not ok(n):
                continue
            x0 = pattern(n, word)
            cyc = cycle_of(rule, n, x0); T = set(cyc)
            res = [orbit_until(rule, n, x ^ (1 << i), T, 10 ** 4) for x in cyc for i in range(n)]
            rows.append(dict(rule=rule, n=n, word=word, period=len(cyc), all_flips_return=int(all(v is True for v in res)),
                             undecided=sum(v is None for v in res)))
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "local_radius.csv"), index=False)
    srows = []
    for rule in (22, 26, 154, 90, 122, 126):
        for n in range(4, min(a.nmax, 64) + 1):
            res = [orbit_until(rule, n, 1 << i, {0}, 2 * 10 ** 4) for i in range(n)]
            srows.append(dict(rule=rule, n=n, all_seeds_die=int(all(v is True for v in res)), undecided=sum(v is None for v in res)))
    pd.DataFrame(srows).to_csv(os.path.join(DATA, "local_seed.csv"), index=False)
    d = pd.DataFrame(rows); s = pd.DataFrame(srows)
    for rule in (94, 75, 133):
        t = d[d.rule == rule]; print(rule, "radius >= 2 at all", len(t), "n:", bool(t.all_flips_return.all()), "fails at", t[t.all_flips_return == 0].n.tolist()[:20])
    for rule in s.rule.unique():
        t = s[s.rule == rule]; print(rule, "seeds die at n =", t[t.all_seeds_die == 1].n.tolist(), "undecided", t[t.undecided > 0].n.tolist()[:10])


if __name__ == "__main__":
    main()
