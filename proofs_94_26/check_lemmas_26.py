"""Rule 26: exhaustive tests of the lemmas of PROOF_26.md at small n.

Writes out/check_lemmas_26.json. One process; about 2 minutes.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring  # noqa: E402
import r26  # noqa: E402
from ring import step, rot, w2s, s2w  # noqa: E402
from r26 import R, ones, c_changes, groups, is_domain_state, has_ancestor_pattern, has111  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def U(u, n):
    return rot(step(R, u, n), 1, n)


def main():
    t0 = time.process_time()
    res = {}

    # ---- M1: moving-frame form of the rule
    cases = viol = 0
    for n in range(4, 15):
        for u in range(1 << n):
            cases += 1
            v = 0
            for j in range(n):
                a, b, t = (u >> ((j - 2) % n)) & 1, (u >> ((j - 1) % n)) & 1, (u >> j) & 1
                v |= (t ^ (a & (1 ^ (b & (1 ^ t))))) << j
            viol += v != U(u, n)
    res['M1'] = dict(statement='Lemma 1 (moving frame): sigma F (u)(j) = u(j) + u(j-2)[1 + u(j-1)(1 + u(j))]; every state',
                     n='4..14', cases=cases, violations=viol)

    # ---- M2: c does not increase (even n), every state; also: a single flip changes c by -2, 0 or +2
    cases = viol = 0
    cases_f = viol_f = 0
    tables = {}
    for n in range(4, 21, 2):
        F = ring.F_table(R, n)
        c = r26.c_changes_all(n)
        tables[n] = (F, c)
        cases += 1 << n
        viol += int((c[F] > c).sum())
        if n <= 16:
            x = np.arange(1 << n, dtype=np.uint32)
            for j in range(n):
                d = c[x ^ np.uint32(1 << j)].astype(int) - c
                cases_f += 1 << n
                viol_f += int((~np.isin(d, (-2, 0, 2))).sum())
                bit = ((x >> np.uint32(j)) & 1).astype(bool)
                viol_f += int((d[bit] > 0).sum())            # deleting a one never raises c
    res['M2'] = dict(statement='Lemma 2 (c does not increase): c(F x) <= c(x); every state', n='4..20 (even)',
                     cases=cases, violations=viol)
    res['M2f'] = dict(statement='Lemma 2, remark: one flip changes c by -2, 0 or 2, and deleting a one does not raise c; '
                                'every state, every cell', n='4..16 (even)', cases=cases_f, violations=viol_f)

    # ---- M3: domain states
    cases = viol = 0
    counts = {}
    for n in range(4, 19, 2):
        F, c = tables[n]
        dom = np.zeros(1 << n, dtype=bool)
        E = sum(1 << i for i in range(0, n, 2))
        O = E << 1
        for s in range(1 << n):
            d = is_domain_state(s, n)
            dom[s] = d
            cases += 1
            inM = (s & E) != 0 and (s & O) != 0
            viol += d != (inM and not has_ancestor_pattern(s, n))            # the two descriptions agree
            if d:
                # sources fixed in the moving frame; free cells: c'_k = c_k + c_(k-1), c_0 = 1; other cells 0
                g = groups(s, n)
                src = [grp[0] for grp in g]
                v = U(s, n)
                ok = True
                for a, b in zip(src, src[1:] + src[:1]):
                    L = (b - a) % n
                    ck = [(s >> ((a + 2 * k) % n)) & 1 for k in range((L + 1) // 2)]
                    for k in range((L + 1) // 2):
                        want = 1 if k == 0 else ck[k] ^ ck[k - 1]
                        ok &= ((v >> ((a + 2 * k) % n)) & 1) == want
                    for k in range(1, L, 2):
                        ok &= ((v >> ((a + k) % n)) & 1) == 0
                viol += not ok
        img = F[dom]
        viol += int((~dom[img]).sum())                       # F maps domain states to domain states
        viol += int(len(np.unique(img)) != int(dom.sum()))   # injectively
        counts[n] = int(dom.sum())
        tables[n] = (F, c, dom)
    res['M3'] = dict(statement='Lemma 3 (domain states): the description by sources equals "ones on both parities and no pattern '
                               '1 0^(2r) 1 1"; in the moving frame the sources stay, the free cells follow c_k -> c_k + c_(k-1), '
                               'the other cells stay 0; F permutes the domain states; every state', n='4..18 (even)',
                     cases=cases, violations=viol, domain_states={str(k): v for k, v in counts.items()})

    # ---- M4: a pattern 1 0^(2r) 1 1 gives 111 after exactly r steps (moving frame, same place)
    cases = viol = 0
    for n in range(4, 17, 2):
        for s in range(1 << n):
            for (j, r) in has_ancestor_pattern(s, n):
                cases += 1
                v = s
                for _ in range(r):
                    v = U(v, n)
                viol += not all((v >> ((j + k) % n)) & 1 for k in (-1, 0, 1))
    res['M4'] = dict(statement='Lemma 4: if u(j) = u(j+1) = 1 and the preceding one is at distance 2r+1 from j, then after r steps '
                               'the cells j-1, j, j+1 of the moving frame carry 111; every state, every such pattern',
                     n='4..16 (even)', cases=cases, violations=viol)

    # ---- M5: description of the periodic states (even n)
    cases = viol = 0
    kinds = {}
    for n in range(4, 19, 2):
        Fa, per, cycles, att = ring.analyse(R, n)
        E = sum(1 << i for i in range(0, n, 2))
        O = E << 1
        k = dict(zero=0, one_parity=0, domain=0, with_111=0)
        for cyc in cycles:
            cs = {c_changes(s, n) for s in cyc}
            viol += len(cs) != 1                                # c constant on a cycle
            any111 = any(has111(s, n) for s in cyc)
            for s in cyc:
                cases += 1
                if s == 0:
                    k['zero'] += 1
                elif (s & E) == 0 or (s & O) == 0:
                    k['one_parity'] += 1
                    viol += any111
                elif is_domain_state(s, n):
                    k['domain'] += 1
                    viol += any111
                else:
                    k['with_111'] += 1
                    viol += not any111
        dom = tables[n][2]
        viol += int((dom & ~per).sum())                      # every domain state is periodic
        if n & (n - 1) == 0:
            viol += k['one_parity'] != 0
        kinds[n] = k
    res['M5'] = dict(statement='Theorem 1 (periodic states, even n): c is constant on a cycle; a periodic state is 0, or lies on one '
                               'parity class, or is a domain state, or its orbit contains 111; domain states are periodic; for '
                               'n = 4, 8, 16 no periodic state other than 0 lies on one parity class; every periodic state',
                     n='4..18 (even)', cases=cases, violations=viol, periodic_states_by_kind={str(a): b for a, b in kinds.items()})

    # ---- M6: a state with ones on both parities that is not a domain state has a singleton group; deleting it lowers c by 2
    cases = viol = 0
    for n in range(4, 17, 2):
        F, c, dom = tables[n]
        E = sum(1 << i for i in range(0, n, 2))
        O = E << 1
        for s in range(1 << n):
            if (s & E) == 0 or (s & O) == 0 or dom[s]:
                continue
            cases += 1
            sg = r26.singleton_groups(s, n)
            viol += not sg or any(int(c[s ^ (1 << j)]) != int(c[s]) - 2 for j in sg)
    res['M6'] = dict(statement='Lemma 5: every state with ones on both parities that is not a domain state has a singleton group, and '
                               'deleting a singleton group lowers c by 2; every such state', n='4..16 (even)', cases=cases, violations=viol)

    # ---- M7: carrier words
    cases = viol = 0
    for n in range(5, 32):
        for s in r26.carrier_words(n):
            cases += 1
            viol += step(R, step(R, s, n), n) != rot(s, 1, n) or not has111(s, n)
    res['M7'] = dict(statement='Lemma 7 (carrier words): F^2(w) is w shifted by one cell for every cyclic word over the blocks 11100 '
                               'and 100 that contains 11100; every such word, every rotation', n='5..31', cases=cases, violations=viol)

    # ---- M8: rule 26 = rule 90 on one parity class, nilpotent for n = 2^k
    cases = viol = 0
    for n in (4, 8, 16):
        E = sum(1 << i for i in range(0, n, 2))
        for base in (E, E << 1):
            sub = base
            while True:                                         # all subsets of the parity class
                cases += 1
                v = sub
                viol += step(R, v, n) != step(90, v, n)
                for _ in range(n // 2):
                    v = step(R, v, n)
                viol += v != 0
                if sub == 0:
                    break
                sub = (sub - 1) & base
    for n in range(4, 17, 2):                                   # even n in general: rule 90, and E <-> O
        E = sum(1 << i for i in range(0, n, 2))
        for base, other in ((E, E << 1), (E << 1, E)):
            sub = base
            while True:
                cases += 1
                img = step(R, sub, n)
                viol += img != step(90, sub, n) or (img & ~other) != 0
                if sub == 0:
                    break
                sub = (sub - 1) & base
    for n in (32, 64, 128, 256, 512, 1024):
        for j in (0, 1):
            cases += 1
            v = 1 << j
            for _ in range(n // 2):
                v = step(R, v, n)
            viol += v != 0
    res['M8'] = dict(statement='Lemma 6: on one parity class rule 26 is rule 90 and maps E into O and O into E (every state of E and O, even '
                               'n = 4..16); F^(n/2) = 0 there for n = 2^k (every state of E and O for n = 4, 8, 16; the two single '
                               'seeds for n = 32..1024)', n='4..16 (even); 32..1024 (powers of two)',
                     cases=cases, violations=viol)

    # ---- M9: codes on the cycles (Lemma 8)
    cases = viol = 0
    for n in range(6, 19, 2):
        Fa, per, cycles, att = ring.analyse(R, n)
        pow2 = n & (n - 1) == 0
        for cyc in cycles:
            if cyc == [0]:
                continue
            codes = set()
            for s in cyc:
                codes |= ring.codes_of(s, n)
            if is_domain_state(cyc[0], n):
                cases += 1
                viol += not {1, 2, 3, 4, 5, 6} <= codes
            elif pow2:
                cases += 1
                viol += not {3, 6} <= codes
    res['M9'] = dict(statement='Lemma 8: every domain cycle contains the codes 001, 010, 011, 100, 101, 110; for n = 8, 16 every '
                               'cycle other than {0} contains 011 and 110; every such cycle', n='6..18 (even)',
                     cases=cases, violations=viol)

    res['all_passed'] = all(v['violations'] == 0 for v in res.values() if isinstance(v, dict))
    res['cpu_s'] = round(time.process_time() - t0, 2)
    with open(os.path.join(HERE, 'out', 'check_lemmas_26.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=int)
    for k, v in res.items():
        if isinstance(v, dict):
            print('%-4s n = %-26s cases = %-9d violations = %d' % (k, v['n'], v['cases'], v['violations']))
    print('all passed:', res['all_passed'], ' cpu s:', res['cpu_s'])


if __name__ == '__main__':
    main()
