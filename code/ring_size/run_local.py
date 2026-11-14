"""Results that need no enumeration of 2^n states (single process, minutes).

  data/ring_size/seed_orbits.csv     orbit of the single flip e_0 of the zero state, rules with F(0) = 0:
                                     returns to 0 (radius(0) >= 2 by Lemma Z) or the cycle it reaches
  data/ring_size/crystal_radius.csv  every single flip of every state of a crystal on rings p | n: does
                                     the orbit return to the same cycle (radius >= 2)? (direct simulation)
  data/ring_size/lightcone.csv       Lemma H input: healing time tau on the line, n0 = 2 tau + 1
  data/ring_size/injectivity.csv     pair-graph certificate: F bijective on every odd ring
Usage: python3 run_local.py [--seed-nmax 256] [--crystal-nmax 400]
"""
import argparse, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lightcone, ringlang
from lightcone import step, from_word

OUT = os.path.join(HERE, "..", "..", "data", "ring_size")
CAP = 400000


def orbit_info(rule, x, n):
    seen = {}
    t = 0
    while x not in seen:
        seen[x] = t
        x = step(rule, x, n); t += 1
        if t > CAP:
            return None
    T = t - seen[x]
    return dict(transient=seen[x], period=T, cycle_min=min(_cyc(rule, x, n)))


def _cyc(rule, x, n):
    c = [x]; y = step(rule, x, n)
    while y != x:
        c.append(y); y = step(rule, y, n)
    return c


def write(name, rows):
    with open(os.path.join(OUT, name), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-nmax", type=int, default=256)
    ap.add_argument("--crystal-nmax", type=int, default=400)
    a = ap.parse_args()
    rows = []
    for rule in (22, 26, 122, 154):
        for n in range(4, a.seed_nmax + 1):
            assert step(rule, 0, n) == 0
            oi = orbit_info(rule, 1, n)
            if oi is None:
                rows.append(dict(rule=rule, n=n, returns_to_zero="", transient=-1, limit_period=-1, capped=1))
            else:
                rows.append(dict(rule=rule, n=n, returns_to_zero=int(oi["cycle_min"] == 0), transient=oi["transient"],
                                 limit_period=oi["period"], capped=0))
    write("seed_orbits.csv", rows)
    print("seed orbits:", len(rows), "rows,", sum(r["capped"] for r in rows), "capped")
    rows = []
    for rule, word in ((94, "011"), (43, "0011"), (142, "0011")):
        p = len(word)
        for n in range(p, a.crystal_nmax + 1, p):
            cyc = _cyc(rule, from_word(word, n), n)
            S = set(cyc)
            ok, tmax = True, 0
            for x in cyc:
                for j in range(n if n <= 2 * p else p):     # by rotation by p, positions mod p suffice
                    z = x ^ (1 << j); t = 0; seen = set()
                    while z not in S and z not in seen:      # exact: stop on return or on closing another cycle
                        seen.add(z); z = step(rule, z, n); t += 1
                    if z not in S:
                        ok = False
                    tmax = max(tmax, t)
            rows.append(dict(rule=rule, word=word, n=n, cycle_length=len(cyc), radius_ge2=int(ok), max_return_time=tmax))
    write("crystal_radius.csv", rows)
    print("crystal radius:", len(rows), "rows,", sum(1 - r["radius_ge2"] for r in rows), "with radius 1")
    rows = []
    for rule, word in ((94, "011"), (43, "0011"), (142, "0011"), (35, "100"), (26, "100"), (122, "10"), (37, "100000")):
        try:
            h = lightcone.heal(rule, word)
        except AssertionError as e:
            h = dict(rule=rule, word=word, p=len(word), cycle_length=-1, N=-1, healed=False, tau=None, n0=None)
        rows.append(h)
    write("lightcone.csv", rows)
    print("lightcone:", [(r["rule"], r["word"], r["healed"], r["tau"]) for r in rows])
    rows = []
    for rule in (22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154):
        c = ringlang.injectivity_certificate(rule)
        rows.append(dict(rule=rule, certified_bijective_odd_n=int(c["certified"]),
                         offdiag_scc_periods=";".join(str(s["period"]) for s in c["sccs"])))
    write("injectivity.csv", rows)
    print("injectivity:", [(r["rule"], r["certified_bijective_odd_n"]) for r in rows])


if __name__ == "__main__":
    main()
