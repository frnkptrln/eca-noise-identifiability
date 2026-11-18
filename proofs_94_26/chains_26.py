"""Rule 26: the chains of flips constructed in PROOF_26.md, executed step by step.

Every flip is applied to a periodic state; the flipped state is iterated until it is periodic; the script asserts
what the lemma predicts about the cycle reached.

Part A  every cycle, even n = 4..20: the chain of Theorem 2 (delete a singleton group, or clear the free cells of a
        domain and then delete its source) down to a cycle on one parity class; for n = 4, 8, 16 it ends at {0}.
Part B  samples for n = 32..1024: the same chain from the cycle reached from a random state, to {0}.
Part C  n = 8, 32, 128, 512: the chain of Theorem 4(c) from 0 through e_0 + e_5 to the carrier word 11100 (100)^q.
Part D  even n = 6..20 that are not powers of two: every cycle on one parity class <-> {0} (Lemma 9), and every
        domain cycle <-> a cycle on one parity class by flips between periodic states (Theorem 5).
Part E  Theorem 3(d): from e_(s1) + e_(s2) (resistance 2 from 0) to a given domain state by flips between domain states;
        every domain cycle for n = 8, 16, samples for n = 32, 64.
Part F  Theorem 4(b): the path of resistance 2 from 0 to a state with 111, n = 8..1024.

Writes out/chains_26.json. One process; about 3 minutes.
"""
import json
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring  # noqa: E402
import r26  # noqa: E402
from ring import step, w2s, s2w, limit_cycle  # noqa: E402
from r26 import R, c_changes, groups, is_domain_state, has111  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def periodic(s, n):
    return limit_cycle(R, s, n)[0] == 0


def reduce_chain(x, n):
    """Theorem 2: from the periodic state x to a periodic state on one parity class.
    Returns (final periodic state, flips, number of cycle changes forced by a drop of c)."""
    assert periodic(x, n)
    flips = drops = 0
    while True:
        g = groups(x, n)
        if g is None:
            return x, flips, drops
        c0 = c_changes(x, n)
        single = [grp[0] for grp in g if len(grp) == 1]
        if single:
            y = x ^ (1 << single[0])
            assert c_changes(y, n) == c0 - 2
            t, cyc = limit_cycle(R, y, n)
            assert c_changes(cyc[0], n) <= c0 - 2 and x not in cyc
            x = cyc[0]
            flips += 1
            drops += 1
        else:
            assert is_domain_state(x, n)
            grp = min(g, key=len)
            y = x ^ (1 << grp[-1])                      # delete the last free one of the domain
            assert is_domain_state(y, n) and periodic(y, n)
            x = y
            flips += 1


def to_period_multiple(v, n, mult):
    """F^T(v) for a T >= transient that is a multiple of `mult` and of the period of the cycle reached."""
    t, cyc = limit_cycle(R, v, n)
    P = len(cyc) * mult // math.gcd(len(cyc), mult)
    T = P * max(1, -(-t // P))
    return cyc[(T - t) % len(cyc)], len(cyc)


def main():
    t0 = time.process_time()
    random.seed(2694)
    out = dict(part_A=[], part_B=[], part_C=[], part_D=[])

    # ---------------- Part A
    for n in range(4, 21, 2):
        F, per, cycles, att = ring.analyse(R, n)
        mf = md = 0
        ends_zero = 0
        for cyc in cycles:
            x, flips, drops = reduce_chain(cyc[0], n)
            mf, md = max(mf, flips), max(md, drops)
            ends_zero += x == 0
        pow2 = n & (n - 1) == 0
        assert not pow2 or ends_zero == len(cycles)
        out['part_A'].append(dict(n=n, cycles=len(cycles), all_chains_end_on_one_parity_class=True,
                                  chains_ending_at_zero=ends_zero, max_flips=mf, max_drops_of_c=md))
        print('A', out['part_A'][-1], flush=True)

    # ---------------- Part B
    for n, k in ((32, 100), (64, 100), (128, 50), (256, 50), (512, 20), (1024, 10)):
        mf = md = mc = 0
        for _ in range(k):
            t, cyc = limit_cycle(R, random.getrandbits(n), n)
            mc = max(mc, c_changes(cyc[0], n))
            x, flips, drops = reduce_chain(cyc[0], n)
            assert x == 0
            mf, md = max(mf, flips), max(md, drops)
        out['part_B'].append(dict(n=n, start_states=k, all_chains_end_at_zero=True, max_c_of_start_cycle=mc,
                                  max_flips=mf, max_drops_of_c=md))
        print('B', out['part_B'][-1], flush=True)

    # ---------------- Part C
    for n in (8, 32, 128, 512):
        q = (n - 5) // 3
        assert n == 5 + 3 * q and q % 2 == 1
        x = (1 << 0) | (1 << 5)                                   # e_0 + e_5: resistance 2 from the zero state
        assert step(R, 0, n) == 0 and bin(x).count('1') == 2 and is_domain_state(x, n) and periodic(x, n)
        states = [x]
        for i in range(1, q):                                     # add the sources 8, 11, ..., 5 + 3(q-1)
            x ^= 1 << (5 + 3 * i)
            states.append(x)
        x ^= 1 << 2                                               # free cell of the domain of length 5
        states.append(x)
        assert x == w2s('10100' + '100' * q)
        for s in states:
            assert is_domain_state(s, n) and periodic(s, n) and not has111(s, n)
        y = x ^ (1 << 1)
        assert y == w2s('11100' + '100' * q) and periodic(y, n) and has111(y, n)
        cyc_y = limit_cycle(R, y, n)[1]
        assert x not in cyc_y
        out['part_C'].append(dict(n=n, q=q, flips_after_e0_e5=len(states), all_intermediate_states_are_periodic_domain_states=True,
                                  final_state_is_the_carrier_word=True, period_of_the_carrier_cycle=len(cyc_y),
                                  c_of_last_domain_state=c_changes(x, n), c_of_carrier=c_changes(y, n)))
        print('C', out['part_C'][-1], flush=True)

    # ---------------- Part D
    for n in range(6, 21, 2):
        if n & (n - 1) == 0:
            continue
        F, per, cycles, att = ring.analyse(R, n)
        E = sum(1 << i for i in range(0, n, 2))
        e = 0
        while (n // 2) % (2 ** (e + 1)) == 0:
            e += 1
        n_one = n_dom = 0
        for cyc in cycles:
            x = cyc[0]
            if x == 0:
                continue
            g = groups(x, n)
            if g is None:
                # (i) one parity class: x -> 0 and 0 -> x by flips at the ones of x
                n_one += 1
                supp = r26.ones(x, n)
                z = x
                for j in supp:
                    z, _ = to_period_multiple(z ^ (1 << j), n, len(limit_cycle(R, z, n)[1]))
                assert z == 0
                z = 0
                for j in supp:
                    z, _ = to_period_multiple(z ^ (1 << j), n, len(cyc))
                assert z in cyc
                continue
            if any(has111(s, n) for s in cyc):
                continue
            # (ii) domain cycle: flips between periodic states down to a periodic state on one parity class
            n_dom += 1
            while True:
                g = groups(x, n)
                if len(g) == 2:
                    break
                grp = min(g, key=len)
                for j in reversed(grp):                              # clear the domain, then delete its source
                    x ^= 1 << j
                    assert is_domain_state(x, n) and periodic(x, n)
            src = [grp[0] for grp in g]
            L = [(src[1] - src[0]) % n, (src[0] - src[1]) % n]
            big = 0 if L[0] >= L[1] else 1
            assert L[big] >= 2 ** (e + 1) + 1
            a, b = src[big], src[1 - big]
            for j in reversed(g[1 - big][1:]):                       # clear the other domain
                x ^= 1 << j
                assert is_domain_state(x, n) and periodic(x, n)
            want = {(a + 2 ** (e + 1)) % n}                          # free cells of the long domain: one 1 at offset 2^(e+1)
            for k in range(1, (L[big] + 1) // 2):
                j = (a + 2 * k) % n
                if ((x >> j) & 1) != (j in want):
                    x ^= 1 << j
                    assert is_domain_state(x, n) and periodic(x, n)
            y = x ^ (1 << b)
            assert y == (1 << a) | (1 << ((a + 2 ** (e + 1)) % n))
            assert periodic(y, n) and c_changes(y, n) == 0 and y != 0
        out['part_D'].append(dict(n=n, one_parity_cycles_joined_to_zero_both_ways=n_one,
                                  domain_cycles_joined_to_a_one_parity_cycle_by_flips_between_periodic_states=n_dom))
        print('D', out['part_D'][-1], flush=True)


    # ---------------- Part E: Theorem 3(d), from e_(s1) + e_(s2) to a given domain state by flips between domain states
    out['part_E'] = []
    for n, reps in ((8, None), (16, None), (32, 200), (64, 200)):
        if reps is None:
            F, per, cycles, att = ring.analyse(R, n)
            starts = [cyc[0] for cyc in cycles if is_domain_state(cyc[0], n)]
        else:
            starts = []
            while len(starts) < reps:
                cyc = limit_cycle(R, random.getrandbits(n), n)[1]
                if is_domain_state(cyc[0], n):
                    starts.append(cyc[0])
        mx = 0
        for x in starts:
            g = groups(x, n)
            src = [grp[0] for grp in g]
            z = (1 << src[0]) | (1 << src[1])
            assert step(R, 0, n) == 0 and bin(z).count('1') == 2          # resistance 2 from the zero state
            assert is_domain_state(z, n) and periodic(z, n)
            flips = 0
            for j in src[2:] + [j for grp in g for j in grp[1:]]:
                z ^= 1 << j
                flips += 1
                assert is_domain_state(z, n) and periodic(z, n)
            assert z == x
            mx = max(mx, flips)
        out['part_E'].append(dict(n=n, domain_states=len(starts), every_domain_cycle=reps is None,
                                  all_intermediate_states_are_periodic_domain_states=True, max_flips=mx))
        print('E', out['part_E'][-1], flush=True)

    # ---------------- Part F: Theorem 4(b), a path of resistance 2 from the zero state to a state with 111
    out['part_F'] = []
    for n in (8, 16, 32, 64, 128, 256, 512, 1024):
        s1 = 1                                                # e_0, one flip
        s2 = step(R, s1, n)
        assert s2 == (1 << 1) | (1 << (n - 1))
        s3 = step(R, s2, n) ^ (1 << 1)                        # second flip
        assert s3 == (1 << (n - 2)) | (1 << 1) | (1 << 2)
        s4 = step(R, s3, n)
        assert has111(s4, n)
        # resistance 1 is not enough: the orbit of a single flip has no two adjacent ones
        v, ok = 1, True
        for _ in range(n):
            ok &= (v & ring.rot(v, 1, n)) == 0
            v = step(R, v, n)
        assert ok and v == 0
        out['part_F'].append(dict(n=n, path_of_resistance_2_reaches_111=True, single_flip_orbit_has_no_adjacent_ones_and_dies=True))
    print('F', out['part_F'], flush=True)

    out['cpu_s'] = round(time.process_time() - t0, 2)
    with open(os.path.join(HERE, 'out', 'chains_26.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=int)
    print('cpu s', out['cpu_s'])


if __name__ == '__main__':
    main()
