"""Rule 94: exhaustive tests of the lemmas of PROOF_94_converse.md at small n.

Writes out/check_lemmas_94.json. One process; about 1 minute.
Every test counts its cases and its violations; a test passes iff violations == 0.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring  # noqa: E402
from ring import step, s2w, w2s, frozen94, windows94, is_block_word, phi  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = 94


def bits(s, cells):
    return sum(((s >> c) & 1) << k for k, c in enumerate(cells))


def runs_cyclic(s, n):
    """lengths of the maximal runs of a non-constant cyclic word."""
    start = next(i for i in range(n) if ((s >> i) & 1) != ((s >> ((i - 1) % n)) & 1))
    out, length = [], 1
    for k in range(1, n):
        i = (start + k) % n
        if ((s >> i) & 1) == ((s >> ((i - 1) % n)) & 1):
            length += 1
        else:
            out.append(length)
            length = 1
    out.append(length)
    return out


def live_predicted(w):
    """the live orbits claimed by Lemma 8, as a set of frozensets."""
    out = set()
    if w % 3 == 2:
        out.add(frozenset(ring.AB_window(w)))
    if w == 4:
        out.add(frozenset([w2s('0000'), w2s('1001'), w2s('1111')]))
    return out


def is_live(u, w):
    return any(u in orb for orb in live_predicted(w))


def phi_periodic(u, w):
    seen = set()
    v = u
    while v not in seen:
        seen.add(v)
        v = phi(R, v, w)
    return v == u


def predicted_periodic(s, n, vper_cache={}):
    """Theorem 1: the description of the periodic states."""
    if s == 0:
        return True
    wins = windows94(s, n)
    if wins is None:                                    # empty frozen set
        if s == (1 << n) - 1 or n % 2:
            return False
        if any(L % 2 for L in runs_cyclic(s, n)):
            return False
        h = n // 2
        ph = next(i for i in range(n) if ((s >> i) & 1) != ((s >> ((i - 1) % n)) & 1)) % 2   # parity of the run starts
        v = sum(((s >> ((2 * k + ph) % n)) & 1) << k for k in range(h))
        if h not in vper_cache:                         # periodic vectors of v -> v + (v shifted) on Z/h
            mask = (1 << h) - 1
            m = lambda z: (z ^ ((z << 1) | (z >> (h - 1)))) & mask
            per = set()
            for z in range(1 << h):
                y = z
                for _ in range(h):
                    y = m(y)
                per.add(y)                              # image of the h-th power = periodic part
            vper_cache[h] = per
        return v in vper_cache[h]
    for cells in wins:
        if not is_live(bits(s, cells), len(cells)):
            return False
    return True


def main():
    t0 = time.process_time()
    res = {}

    # ---- L7: product structure of the dynamics over the windows, every state with a non-empty frozen set
    cases = viol = 0
    for n in range(5, 15):
        for s in range(1 << n):
            wins = windows94(s, n)
            if not wins:
                continue
            W = frozen94(s, n)
            cases += 1
            ok = all(((s >> ((c[0] - 1) % n)) & 1) == 1 and ((s >> ((c[-1] + 1) % n)) & 1) == 1 and len(c) <= n - 3
                     for c in wins)
            y = s
            us = [bits(s, c) for c in wins]
            for t in range(10):
                y = step(R, y, n)
                us = [phi(R, u, len(c)) for u, c in zip(us, wins)]
                if any(((y >> i) & 1) != ((s >> i) & 1) for i in W) or any(bits(y, c) != u for u, c in zip(us, wins)):
                    ok = False
            viol += not ok
    res['L7'] = dict(statement='Lemma 7 (windows): boundary cells are frozen ones, width <= n-3, F^t = identity on the frozen '
                               'set and = phi^t on every window, t = 1..10; every state with non-empty frozen set that is not fully frozen',
                     n='5..14', cases=cases, violations=viol)

    # ---- L8: live window orbits, all 2^w window states
    viol = 0
    widths = list(range(1, 23))
    found = {}
    for w in widths:
        got = {frozenset(o) for o in ring.live_window_orbits(w)}
        found[w] = sorted(sorted(s2w(u, w) for u in o) for o in got)
        viol += got != live_predicted(w)
    res['L8'] = dict(statement='Lemma 8 (live window orbits): the periodic unfrozen orbits of the window map are {A_w, B_w} for '
                               'w = 2 mod 3, the 3-cycle 0000, 1001, 1111 for w = 4, and none otherwise; all 2^w window states',
                     n='w = 1..22', cases=sum(1 << w for w in widths), violations=viol,
                     live_orbits={str(w): found[w] for w in widths if found[w]})

    # ---- per-ring enumerations (all states) used by several tests
    per_tables = {}
    for n in range(3, 21):
        F, per, cycles, att = ring.analyse(R, n)
        per_tables[n] = (per, cycles, att)

    # ---- L7c: a state with non-empty frozen set is periodic iff every window content is phi-periodic
    cases = viol = 0
    for n in range(5, 17):
        per = per_tables[n][0]
        for s in range(1 << n):
            wins = windows94(s, n)
            if wins is None:
                continue
            cases += 1
            pred = all(phi_periodic(bits(s, c), len(c)) for c in wins)
            viol += pred != bool(per[s])
    res['L7c'] = dict(statement='Lemma 7(c): a state with non-empty frozen set is periodic iff all its window contents are '
                                'phi-periodic; every state with non-empty frozen set', n='5..16', cases=cases, violations=viol)

    # ---- L9: periodic states with empty frozen set
    cases = viol = 0
    counts = {}
    for n in range(3, 21):
        per, cycles, att = per_tables[n]
        k = 0
        for cyc in cycles:
            for s in cyc:
                if frozen94(s, n):
                    continue
                k += 1
                cases += 1
                if s == 0:
                    continue
                if s == (1 << n) - 1 or n % 2 or any(L % 2 for L in runs_cyclic(s, n)):
                    viol += 1
        counts[n] = k
        h = n // 2
        if n % 2 == 0:
            e = 0
            while h % (2 ** (e + 1)) == 0:
                e += 1
            expect = 2 * (2 ** (h - 2 ** e) - 1) + 1       # two phases of the non-zero periodic vectors, and 0
        else:
            expect = 1
        if n >= 5:
            viol += k != expect
    res['L9'] = dict(statement='Lemma 9: a periodic state with empty frozen set is 0 or has only runs of even length; their '
                               'number is 1 for odd n and 2(2^(n/2 - 2^e) - 1) + 1 for even n = 2^(e+1) q, q odd (n >= 5); every periodic state',
                     n='3..20', cases=cases, violations=viol, counts={str(n): counts[n] for n in counts})

    # ---- T1: description of all periodic states (both directions), every state
    cases = viol = 0
    for n in range(3, 17):
        per = per_tables[n][0]
        for s in range(1 << n):
            cases += 1
            viol += predicted_periodic(s, n) != bool(per[s])
    cases2 = viol2 = 0
    for n in range(17, 21):
        per, cycles, att = per_tables[n]
        for cyc in cycles:
            for s in cyc:
                cases2 += 1
                viol2 += not predicted_periodic(s, n)
    res['T1'] = dict(statement='Theorem 1 (periodic states): a state is periodic iff it is 0, or a doubled word with periodic '
                               'half word, or has non-empty frozen set and only live windows; every state',
                     n='3..16', cases=cases, violations=viol)
    res['T1b'] = dict(statement='Theorem 1, direction "periodic implies the description"; every periodic state',
                      n='17..20', cases=cases2, violations=viol2)

    # ---- L10: reversible freezing, every cycle with non-empty frozen set that is not a block word
    cases = viol = 0
    for n in range(5, 21):
        per, cycles, att = per_tables[n]
        for ci, cyc in enumerate(cycles):
            if not frozen94(cyc[0], n) or is_block_word(cyc[0], n):
                continue
            cases += 1
            ok = False
            for s in cyc:
                cells = windows94(s, n)[0]
                w = len(cells)
                u = bits(s, cells)
                A, B = ring.AB_window(w) if w % 3 == 2 else (None, None)
                if w == 4:
                    j = {w2s('1111'): cells[0], w2s('0000'): cells[1]}.get(u)
                elif u == A:
                    j = cells[1]
                elif u == B:
                    j = cells[0]
                else:
                    j = None
                if j is None:
                    continue
                y = s ^ (1 << j)
                good = bool(per[y]) and frozen94(y, n) > frozen94(s, n) and att[y] != ci \
                    and len(frozen94(y, n)) == len(frozen94(s, n)) + (2 if w in (2, 4) else 3)
                if not good:
                    ok = False
                    break
                ok = True
            viol += not ok
    res['L10'] = dict(statement='Lemma 10 (reversible freezing): in every state of the cycle whose first window is not 1001, the '
                                'flip named in the lemma gives a periodic state of another cycle with a strictly larger frozen set; '
                                'every cycle with non-empty frozen set that is not a block word',
                      n='5..20', cases=cases, violations=viol)

    # ---- L11, L12, L13: swap, merge, split on every block word, every occurrence
    c11 = v11 = c12 = v12 = c13 = v13 = 0
    for n in range(5, 25):
        for (x, a, b) in ring.block_words(n):
            g = lambda p, k: (x >> ((p + k) % n)) & 1
            for p in range(n):
                if n >= 5 and [g(p, k) for k in range(5)] == [0, 1, 0, 1, 1] and g(p, -1) == 1:
                    c11 += 1
                    j2, j3 = 1 << ((p + 2) % n), 1 << ((p + 3) % n)
                    y1, y0, x2 = x ^ j2, x ^ j3, x ^ j2 ^ j3
                    ok = step(R, y1, n) == y0 and step(R, y0, n) == y1 and is_block_word(x2, n) and step(R, x2, n) == x2 \
                        and [(x2 >> ((p + k) % n)) & 1 for k in range(5)] == [0, 1, 1, 0, 1]
                    v11 += not ok
                if n >= 6 and [g(p, k) for k in range(7)] == [0, 1, 0, 1, 0, 1, 0] and g(p, -1) == 1:
                    c12 += 1
                    y = x ^ (1 << ((p + 3) % n))
                    x2 = step(R, y, n)
                    ok = is_block_word(x2, n) and [(x2 >> ((p + k) % n)) & 1 for k in range(6)] == [0, 1, 1, 0, 1, 1] \
                        and all(((x2 >> i) & 1) == ((x >> i) & 1) for i in range(n) if (i - p) % n >= 6)
                    v12 += not ok
                if n >= 8 and [g(p, k) for k in range(8)] == [0, 1, 0, 1, 1, 0, 1, 1] and g(p, -1) == 1:
                    c13 += 1
                    y1 = x ^ (1 << ((p + 2) % n))
                    y0 = step(R, y1, n)
                    z = y0 ^ (1 << ((p + 6) % n))
                    z4 = z
                    for _ in range(5):
                        z4 = step(R, z4, n)
                    ok = step(R, y0, n) == y1 and y1 != y0 \
                        and [(y0 >> ((p + k) % n)) & 1 for k in range(8)] == [0, 1, 0, 0, 1, 0, 1, 1] \
                        and is_block_word(z4, n) and step(R, z4, n) == z4 \
                        and [(z4 >> ((p + k) % n)) & 1 for k in range(8)] == [0, 1, 0, 1, 0, 1, 0, 1] \
                        and all(((z4 >> i) & 1) == ((x >> i) & 1) for i in range(n) if (i - p) % n >= 8)
                    v13 += not ok
    res['L11'] = dict(statement='Lemma 11 (swap, both directions): x + e_(p+2) and x + e_(p+3) form a 2-cycle and '
                                'x + e_(p+2) + e_(p+3) is the block word with the two blocks exchanged; every block word, every '
                                'pair of consecutive blocks short, long', n='5..24', cases=c11, violations=v11)
    res['L12'] = dict(statement='Lemma 12 (merge): F(x + e_(p+3)) is the block word with the three short blocks replaced by two '
                                'long ones; every block word, every triple of consecutive short blocks', n='6..24', cases=c12, violations=v12)
    res['L13'] = dict(statement='Lemma 13 (split): x + e_(p+2) has period 2; five steps after flipping the cell p+6 of its other '
                                'state the block word with short, long, long replaced by four short blocks is reached; every block '
                                'word, every occurrence of short, long, long', n='8..24', cases=c13, violations=v13)

    # ---- L16: basin of the zero state when 8 does not divide n
    cases = viol = 0
    for n in range(5, 21):
        if n % 8 == 0:
            continue
        per, cycles, att = per_tables[n]
        zero = att[0]
        for s in np.nonzero(att == zero)[0]:
            s = int(s)
            cases += 1
            if s == 0 or s == (1 << n) - 1:
                continue
            # word over the blocks 001 and 0011: zeros in runs of exactly two, ones in runs of one or two
            rl = runs_cyclic(s, n)
            start = next(i for i in range(n) if ((s >> i) & 1) != ((s >> ((i - 1) % n)) & 1))
            val = (s >> start) & 1
            ok = all((L == 2) if (val ^ (k % 2)) == 0 else (L in (1, 2)) for k, L in enumerate(rl))
            viol += not ok
        # converse: every such word is in the basin
        for s in range(1 << n):
            if s in (0, (1 << n) - 1):
                continue
            rl = runs_cyclic(s, n)
            start = next(i for i in range(n) if ((s >> i) & 1) != ((s >> ((i - 1) % n)) & 1))
            val = (s >> start) & 1
            if all((L == 2) if (val ^ (k % 2)) == 0 else (L in (1, 2)) for k, L in enumerate(rl)):
                cases += 1
                viol += att[s] != zero
    res['L16'] = dict(statement='Lemma 16 (basin of 0): if 8 does not divide n, the states whose orbit ends in 0 are exactly 0, '
                                '1^n and the cyclic words over the blocks 001 and 0011 (case = one state of the basin of 0, or one such word)', n='5..20 (8 not dividing n)',
                      cases=cases, violations=viol)


    # ---- LW: windows cut out of a block word, every block word, every admissible window, every content
    cases = viol = 0
    for n in range(5, 14):
        for (x, a, b) in ring.block_words(n):
            for p in range(n):
                if ((x >> ((p - 1) % n)) & 1, (x >> p) & 1) != (0, 1):
                    continue
                for w in range(1, min(n - 3, 7) + 1):
                    if ((x >> ((p + w + 1) % n)) & 1, (x >> ((p + w + 2) % n)) & 1) != (1, 0):
                        continue
                    cells = [(p + 1 + k) % n for k in range(w)]
                    outside = [i for i in range(n) if i not in cells]
                    base = x & ~sum(1 << c for c in cells)
                    for u in range(1 << w):
                        cases += 1
                        y = base | sum(((u >> k) & 1) << c for k, c in enumerate(cells))
                        ok = all(i in frozen94(y, n) for i in outside)
                        v = u
                        for t in range(6):
                            y = step(R, y, n)
                            v = phi(R, v, w)
                            ok &= bits(y, cells) == v and all(((y >> i) & 1) == ((x >> i) & 1) for i in outside)
                        viol += not ok
    res['LW'] = dict(statement='Lemma W: every cell outside the window is frozen, F^t = identity outside and = phi^t inside, t = 1..6; '
                               'every block word, every admissible window of width <= 7, every content (case = one content)',
                     n='5..13', cases=cases, violations=viol)

    # ---- L16a: parts (i), (ii), (iii) of Lemma 16, every state
    cases = viol = 0
    for n in range(3, 17):
        F = ring.F_table(R, n)
        full = (1 << n) - 1

        def p2(s):
            if s in (0, full):
                return False
            rl = runs_cyclic(s, n)
            st = next(i for i in range(n) if ((s >> i) & 1) != ((s >> ((i - 1) % n)) & 1))
            val = (s >> st) & 1
            return all((L == 2) if (val ^ (k % 2)) == 0 else (L in (1, 2)) for k, L in enumerate(rl))
        isp2 = np.array([p2(s) for s in range(1 << n)])
        for s in range(1 << n):
            cases += 1
            viol += (int(F[s]) == 0) != (s in (0, full))                      # (i)
            viol += (int(F[s]) == full) != bool(isp2[s])                      # (ii)
            viol += bool(isp2[int(F[s])]) and n % 8 != 0                      # (iii)
    res['L16a'] = dict(statement='Lemma 16 (i), (ii), (iii): F(x) = 0 iff x is 0 or 1^n; F(x) = 1^n iff x is a word over 001 and 0011; '
                                 'F(z) is such a word only if 8 divides n; every state (case = one state)', n='3..16',
                       cases=cases, violations=viol)

    res['all_passed'] = all(v['violations'] == 0 for v in res.values() if isinstance(v, dict))
    res['cpu_s'] = round(time.process_time() - t0, 2)
    with open(os.path.join(HERE, 'out', 'check_lemmas_94.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=int)
    for k, v in res.items():
        if isinstance(v, dict):
            print('%-5s n = %-28s cases = %-9d violations = %d' % (k, v['n'], v['cases'], v['violations']))
    print('all passed:', res['all_passed'], ' cpu s:', res['cpu_s'])


if __name__ == '__main__':
    main()
