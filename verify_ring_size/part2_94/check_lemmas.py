"""Exhaustive small-n tests of the lemmas used in PROOF_94.md (rule 94).

Run from the repository root:  python verify_ring_size/part2_94/check_lemmas.py
Writes verify_ring_size/part2_94/out/check_lemmas.json and prints a summary.

Lemma numbering as in PROOF_94.md:
  L1  freezing of 101                      all states, n = 3..20
  L2  fully frozen <=> block word of 01/011 all states, n = 3..20
  L3  growth move (explicit choice of the flipped cell)
                                           all states n = 5..16; all cycle states n = 5..20
  L4  swap move  (01)(011) -> (011)(01)    all block words, all positions, n = 5..30
  L5  merge move (01)(01)(01) -> (011)(011) all block words, all positions, n = 6..30
  L6  every single flip of the crystal heals, n = 6, 9, ..., 99
  C2  one flip of the crystal meets the five codes missing from it, n = 6, 9, ..., 99
"""
import json
import os
import sys
import time
import resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ring94 import build_F, analyse, bits, step_str

RULE = 94


def rl(x, n):      # (rl x)_i = x_(i+1)
    m = np.uint32((1 << n) - 1)
    return ((x << np.uint32(1)) & m) | (x >> np.uint32(n - 1))


def rr(x, n):      # (rr x)_i = x_(i-1)
    return (x >> np.uint32(1)) | ((x & np.uint32(1)) << np.uint32(n - 1))


def frozen_mask(x, n):
    """Bit mask of the cells lying in an occurrence of 101 (cyclic)."""
    m = np.uint32((1 << n) - 1)
    cen = (~x) & rr(x, n) & rl(x, n) & m
    return cen | rl(cen, n) | rr(cen, n)


def frozen_set_str(s):
    n = len(s)
    fz = set()
    for i in range(n):
        if s[i] == "0" and s[i - 1] == "1" and s[(i + 1) % n] == "1":
            fz.update(((i - 1) % n, i, (i + 1) % n))
    return fz


def block_words(n):
    """All cyclic bit strings of length n that are concatenations of blocks 01 and 011 (any cut point)."""
    lin = {0: [""]}
    for k in range(1, n + 1):
        lin[k] = [w + "01" for w in lin.get(k - 2, [])] + [w + "011" for w in lin.get(k - 3, [])]
    full = set()
    for w in lin[n]:
        for r in range(n):
            full.add(w[r:] + w[:r])
    return full


def growth_cell(s):
    """The cell flipped by the growth move of Lemma 3 (case analysis of the proof).  s is not fully frozen."""
    n = len(s)
    fz = frozen_set_str(s)
    if "1" not in s:
        return 0
    i = min(c for c in range(n) if c not in fz)
    L, R = s[i - 1], s[(i + 1) % n]
    if s[i] == "1":
        if L == "1" and R == "1":
            return i
        if L == "0":
            assert s[i - 2] == "0"
            return (i - 2) % n
        assert s[(i + 2) % n] == "0"
        return (i + 2) % n
    if L == "0" and R == "1":
        return (i - 1) % n
    if L == "1" and R == "0":
        return (i + 1) % n
    assert L == "0" and R == "0"
    k = 2
    while s[(i + k) % n] == "0":
        k += 1
    return (i + k - 2) % n


def flip(s, j):
    return s[:j] + ("1" if s[j] == "0" else "0") + s[j + 1:]


def relax(s):
    """Iterate F until a state repeats; return the cycle as a list of strings starting at its smallest state."""
    seen = {}
    t = 0
    while s not in seen:
        seen[s] = t
        s = step_str(s, RULE)
        t += 1
    cyc = [s]
    y = step_str(s, RULE)
    while y != s:
        cyc.append(y)
        y = step_str(y, RULE)
    k = cyc.index(min(cyc))
    return cyc[k:] + cyc[:k]


def main():
    t0 = time.process_time()
    res = {}

    # ---- L1, L2 --------------------------------------------------------------------------------------
    l1 = []
    l2 = []
    for n in range(3, 21):
        F = build_F(RULE, n)
        x = np.arange(1 << n, dtype=np.uint32)
        fz = frozen_mask(x, n)
        fzF = frozen_mask(F, n)
        bad_grow = int(np.count_nonzero(fz & ~fzF))
        bad_val = int(np.count_nonzero((x ^ F) & fz))
        l1.append(dict(n=n, states=1 << n, violations_monotone=bad_grow, violations_value=bad_val))
        full = np.flatnonzero(fz == np.uint32((1 << n) - 1))
        P = block_words(n)
        setfull = set(bits(v, n) for v in full)
        fixed_ok = bool(np.all(F[full] == full))
        l2.append(dict(n=n, fully_frozen=len(setfull), block_words=len(P), equal=setfull == P, all_fixed=fixed_ok))
    res["L1"] = dict(rows=l1, ok=all(r["violations_monotone"] == 0 and r["violations_value"] == 0 for r in l1))
    res["L2"] = dict(rows=l2, ok=all(r["equal"] and r["all_fixed"] for r in l2))

    # ---- L3 ------------------------------------------------------------------------------------------
    l3a = []
    for n in range(5, 17):
        bad = 0
        cnt = 0
        for v in range(1 << n):
            s = bits(v, n)
            fz = frozen_set_str(s)
            if len(fz) == n:
                continue
            cnt += 1
            j = growth_cell(s)
            y = flip(s, j)
            if j in fz:
                bad += 1
                continue
            if v == 0:
                y2 = step_str(step_str(y, RULE), RULE)
                if not frozen_set_str(y2):
                    bad += 1
                continue
            fy = frozen_set_str(y)
            if not (fz < fy and j in fy):
                bad += 1
        l3a.append(dict(n=n, not_fully_frozen_states=cnt, violations=bad))
    l3b = []
    for n in range(5, 21):
        A = analyse(RULE, n)
        st = np.flatnonzero(A["on"]).astype(np.uint32)
        fz_state = frozen_mask(np.arange(1 << n, dtype=np.uint32), n)
        # frozen mask is constant along every cycle
        const = all(len(set(fz_state[c].tolist())) == 1 for c in A["cycles"])
        bad = 0
        cnt = 0
        for v in st.tolist():
            if fz_state[v] == (1 << n) - 1:
                continue
            cnt += 1
            s = bits(v, n)
            j = growth_cell(s)
            y = v ^ (1 << (n - 1 - j))
            c_new = int(A["label"][y])
            c_old = int(A["cid"][v])
            f_new = int(fz_state[int(A["cycles"][c_new][0])])
            f_old = int(fz_state[v])
            if c_new == c_old or (f_old & ~f_new) != 0 or f_new == f_old:
                bad += 1
        l3b.append(dict(n=n, cycles=len(A["cycles"]), cycle_states=int(len(st)), frozen_constant_on_cycles=const,
                        cycle_states_not_fully_frozen=cnt, violations=bad))
    res["L3_all_states"] = dict(rows=l3a, ok=all(r["violations"] == 0 for r in l3a))
    res["L3_cycle_states"] = dict(rows=l3b, ok=all(r["violations"] == 0 and r["frozen_constant_on_cycles"]
                                                   for r in l3b))

    # ---- L4, L5 --------------------------------------------------------------------------------------
    l4 = []
    l5 = []
    for n in range(5, 31):
        P = sorted(block_words(n))
        n4 = b4 = n5 = b5 = 0
        for s in P:
            d = s + s
            for p in range(n):
                # swap: blocks 01 011 at p..p+4, next block starts at p+5
                if d[p:p + 6] == "010110" and n >= 5:
                    n4 += 1
                    y = flip(s, (p + 2) % n)
                    c2 = relax(y)
                    exp_a = y
                    exp_b = step_str(y, RULE)
                    ok = len(c2) == 2 and set(c2) == {exp_a, exp_b} and s not in c2
                    zb = [u for u in c2 if u[(p + 2) % n] == "0"]
                    ok = ok and len(zb) == 1 and zb[0][(p + 3) % n] == "0"
                    if ok:
                        z = flip(zb[0], (p + 2) % n)
                        target = list(s)
                        for k, ch in enumerate("01101"):
                            target[(p + k) % n] = ch
                        target = "".join(target)
                        ok = z == target and step_str(z, RULE) == z and z in set(P)
                    if not ok:
                        b4 += 1
                # merge: blocks 01 01 01 at p..p+5, next block starts at p+6
                if n >= 6 and (d + d)[p:p + 7] == "0101010":
                    n5 += 1
                    y = flip(s, (p + 3) % n)
                    target = list(s)
                    for k, ch in enumerate("011011"):
                        target[(p + k) % n] = ch
                    target = "".join(target)
                    ok = step_str(y, RULE) == target and step_str(target, RULE) == target and target != s \
                        and target in set(P)
                    if not ok:
                        b5 += 1
        l4.append(dict(n=n, block_words=len(P), occurrences=n4, violations=b4))
        if n >= 6:
            l5.append(dict(n=n, block_words=len(P), occurrences=n5, violations=b5))
    res["L4_swap"] = dict(rows=l4, ok=all(r["violations"] == 0 for r in l4))
    res["L5_merge"] = dict(rows=l5, ok=all(r["violations"] == 0 for r in l5))

    # ---- L6 ------------------------------------------------------------------------------------------
    l6 = []
    for n in range(6, 100, 3):
        x = "011" * (n // 3)
        assert step_str(x, RULE) == x
        worst = 0
        bad = 0
        for j in range(n):
            y = flip(x, j)
            t = 0
            while y != x and t < 10:
                y = step_str(y, RULE)
                t += 1
            if y != x:
                bad += 1
            worst = max(worst, t)
        l6.append(dict(n=n, flips=n, violations=bad, max_healing_time=worst))
    res["L6_crystal"] = dict(rows=l6, ok=all(r["violations"] == 0 for r in l6))

    # ---- C2: codes met at resistance one from the crystal ---------------------------------------------
    def codes(w):
        m = len(w)
        return set(4 * int(w[i - 1]) + 2 * int(w[i]) + int(w[(i + 1) % m]) for i in range(m))

    c2 = []
    for n in range(6, 100, 3):
        x = "011" * (n // 3)
        y = flip(x, 1)                      # first 1 of the block at cells 0, 1, 2
        y1 = step_str(y, RULE)
        y2 = step_str(y1, RULE)
        got = dict(y=sorted(codes(y)), Fy=sorted(codes(y1)), FFy=sorted(codes(y2)))
        union = codes(y) | codes(y1) | codes(y2)
        c2.append(dict(n=n, crystal_codes=sorted(codes(x)), codes_on_path=got,
                       violations=0 if (union == set(range(8)) and codes(x) == {3, 5, 6}
                                        and step_str(y2, RULE) == x) else 1))
    res["C2_codes"] = dict(rows=c2, ok=all(r["violations"] == 0 for r in c2))

    res["cpu_seconds"] = round(time.process_time() - t0, 2)
    res["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 << 20), 1)
    res["all_ok"] = all(v["ok"] for k, v in res.items() if isinstance(v, dict))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "check_lemmas.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    for k, v in res.items():
        if isinstance(v, dict):
            tot = sum(r.get("violations", r.get("violations_monotone", 0) + r.get("violations_value", 0))
                      if "violations" in r or "violations_monotone" in r else 0 for r in v["rows"])
            print("%-18s ok=%s  n=%d..%d  violations=%d" % (k, v["ok"], v["rows"][0]["n"], v["rows"][-1]["n"], tot))
    print("cpu_seconds", res["cpu_seconds"], "peak_rss_mb", res["peak_rss_mb"], "all_ok", res["all_ok"])


if __name__ == "__main__":
    main()
