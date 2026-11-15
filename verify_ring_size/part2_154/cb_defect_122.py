"""Rule 122 on even rings: the two one-flip moves out of {0, checkerboard} (step 9 of PROOF_154.md, section 7).

Tests, by direct simulation with Python integers (x_0 = most significant bit):
 T1  the orbit of a single one e_0 is the growing checkerboard and equals a checkerboard state at time n/2
     (Lemma R1), even n = 4..256;
 T2  flipping a one of a checkerboard state does not change its image (Lemma R2), even n = 4..256;
 T3  the orbit of D_n = checkerboard with one zero set to one equals the closed formula of Lemma R3 for
     t = 0 .. n/2 - 1 (even n = 4..256);
 T4  for n = 2^k - 2 (6 .. 2046) that orbit is the all-ones state at time n/2 - 1 and 0 at time n/2 (Lemma R4);
 T5  fate of D_n for even n = 4..NFATE: ends on 0, on the checkerboard, or on another cycle (period and
     canonical representative), found by Brent's cycle detection; if the cycle is not closed after CAP steps
     the case is reported as undetermined, with a plain run of CAP steps that looks for 0 or the checkerboard;
 T6  comparison of T5 with the out-neighbours of the checkerboard in out/explore_122_26.jsonl (n <= 26).
Output: out/cb_defect_122.jsonl (one record per n for T5), out/cb_defect_122.txt (summary).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
NFATE = int(sys.argv[1]) if len(sys.argv) > 1 else 100
CAP = 400000


def make_F(n, rule=122):
    mask = (1 << n) - 1
    tt = [(rule >> c) & 1 for c in range(8)]

    def F(x):
        c = ((x << 1) | (x >> (n - 1))) & mask
        a = (x >> 1) | ((x & 1) << (n - 1))
        y = 0
        for code in range(8):
            if tt[code]:
                y |= (a if code & 4 else ~a) & (x if code & 2 else ~x) & (c if code & 1 else ~c)
        return y & mask
    return F


def state(n, ones):
    x = 0
    for j in ones:
        x |= 1 << (n - 1 - (j % n))
    return x


def rule90_row(t):
    """dict i -> R_t(i) for the single-seed orbit of rule 90 on Z (i of the parity of t, |i| <= t)."""
    row = [1]
    for _ in range(t):
        row = [(u + v) % 2 for u, v in zip([0] + row, row + [0])]
    return {-t + 2 * k: row[k] for k in range(t + 1)}


def formula_state(n, t):
    """Lemma R3: ring state at time t <= n/2 - 1; sites j = -n/2+1 .. n/2."""
    a = rule90_row(t + 1)
    ones = []
    for j in range(-n // 2 + 1, n // 2 + 1):
        i = abs(j)
        if (i - (t + 1)) % 2 == 0:
            v = a.get(i, 0) if i <= t + 1 else 1
        else:
            v = a.get(i + 1, 0)
        if v:
            ones.append(j)
    return state(n, ones)


def canon(n, cyc):
    mask = (1 << n) - 1
    best = None
    for x in cyc:
        for s in range(n):
            y = ((x >> s) | (x << (n - s))) & mask
            if best is None or y < best:
                best = y
    return format(best, "0%db" % n)


def fate(n, x0, F):
    # Brent
    power = lam = 1
    tort, hare = x0, F(x0)
    steps = 1
    while tort != hare:
        if power == lam:
            tort, power, lam = hare, power * 2, 0
        hare = F(hare)
        lam += 1
        steps += 1
        if steps > CAP:
            return None
    tort = hare = x0
    for _ in range(lam):
        hare = F(hare)
    mu = 0
    while tort != hare:
        tort, hare, mu = F(tort), F(hare), mu + 1
    cyc, y = [], tort
    for _ in range(lam):
        cyc.append(y)
        y = F(y)
    return mu, lam, cyc


def main():
    t0 = time.process_time()
    lines = []
    ok1 = ok2 = ok3 = True
    for n in range(4, 257, 2):
        F = make_F(n)
        cb_odd = state(n, range(1, n, 2))
        cb_even = state(n, range(0, n, 2))
        # T1
        x = state(n, [0])
        for t in range(n // 2):
            ok1 &= (x == state(n, range(-t, t + 1, 2)))
            x = F(x)
        ok1 &= (x in (cb_odd, cb_even))
        # T2
        ok2 &= all(F(cb_odd ^ (1 << (n - 1 - p))) == F(cb_odd) for p in range(1, n, 2))
        # T3
        x = cb_odd | state(n, [0])
        for t in range(n // 2):
            ok3 &= (x == formula_state(n, t))
            x = F(x)
    lines.append("T1 single seed grows to the checkerboard at time n/2, even n = 4..256: %s" % ok1)
    lines.append("T2 flipping a one of the checkerboard leaves the image unchanged, even n = 4..256: %s" % ok2)
    lines.append("T3 defect orbit equals the formula of Lemma R3 for t <= n/2 - 1, even n = 4..256: %s" % ok3)
    ok4 = True
    for k in range(3, 12):
        n = 2 ** k - 2
        F = make_F(n)
        x = state(n, range(1, n, 2)) | state(n, [0])
        for t in range(n // 2 - 1):
            x = F(x)
        ok4 &= (x == (1 << n) - 1) and F(x) == 0
    lines.append("T4 n = 2^k - 2 (6..2046): all ones at time n/2 - 1, zero at time n/2: %s" % ok4)
    # T5, T6
    known = {}
    p = os.path.join(HERE, "out", "explore_122_26.jsonl")
    if os.path.exists(p):
        for line in open(p):
            d = json.loads(line)
            if d["rule"] == 122 and d["n"] % 2 == 0:
                known[d["n"]] = d
    ok6, n6 = True, 0
    with open(os.path.join(HERE, "out", "cb_defect_122.jsonl"), "w") as fh:
        for n in range(4, NFATE + 1, 2):
            F = make_F(n)
            cb_odd = state(n, range(1, n, 2))
            res = fate(n, cb_odd | state(n, [0]), F)
            rec = {"n": n}
            if res is None:
                # cycle not closed within the cap: plain run of CAP steps, looking for 0 or the checkerboard
                x, hit = cb_odd | state(n, [0]), None
                for t in range(CAP):
                    if x == 0 or x == cb_odd or x == (cb_odd ^ ((1 << n) - 1)):
                        hit = t
                        break
                    x = F(x)
                rec["end"] = "undetermined"
                rec["steps_run"] = CAP
                rec["zero_or_checkerboard_hit_within_steps_run"] = hit is not None
            else:
                mu, lam, cyc = res
                rec["transient"] = mu
                rec["period"] = lam
                rec["end"] = "zero" if cyc == [0] else ("checkerboard" if cb_odd in cyc else "other")
                rec["rep"] = canon(n, cyc) if n <= 64 else None
                rec["ones_min_max_on_cycle"] = [min(bin(c).count("1") for c in cyc), max(bin(c).count("1") for c in cyc)]
                rec["zero_checkerboard_closed_class"] = rec["end"] in ("zero", "checkerboard")
                if n in known:
                    d = known[n]
                    n6 += 1
                    if rec["end"] == "zero":
                        ok6 &= (d["cb_out_nbrs_reps"] == ["0" * n])
                    elif rec["end"] == "other":
                        ok6 &= (min(d["cb_out_nbrs_reps"]) == rec["rep"])
                    else:
                        ok6 &= (d["cb_out_degree"] == 0)
                    rec["cb_in_closed_class_enumerated"] = d["cb_in_closed_class"]
                    rec["zero_in_closed_class_enumerated"] = d["zero_in_closed_class"]
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            lines.append("T5 n=%3d end=%-12s transient=%s period=%s rep=%s" % (
                n, rec["end"], rec.get("transient"), rec.get("period"), rec.get("rep")))
    lines.append("T6 limit cycle of the defect agrees with the enumerated out-neighbours of the checkerboard "
                 "(%d even n <= 26): %s" % (n6, ok6))
    lines.append("cpu seconds: %.1f" % (time.process_time() - t0))
    txt = "\n".join(lines) + "\n"
    open(os.path.join(HERE, "out", "cb_defect_122.txt"), "w").write(txt)
    sys.stdout.write(txt)


if __name__ == "__main__":
    main()
