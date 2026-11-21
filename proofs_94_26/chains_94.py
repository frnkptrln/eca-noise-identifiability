"""Rule 94, rings with 3 not dividing n: the chains of flips constructed in PROOF_94_converse.md, executed.

Every flip is applied to a periodic state, the flipped state is iterated until it is periodic, and the script
asserts that the cycle reached is the one the lemma predicts and differs from the current one.

Part A (every cycle, n = 5..23 with 3 not dividing n):
  * growth flip (Lemma 3 of PROOF_94.md) for the cycles without 101;
  * freezing chain (Lemma 10) from the cycle to a block word; every flip joins two periodic states, so the
    reversed chain is a chain of flips as well (asserted);
  * the digraph on the block words whose edges are the swaps, merges and splits (Lemmas 11, 12, 13), every
    edge executed, is strongly connected (Lemma 14).
Part B (samples, n up to 301): freezing chain from the cycle reached from a random state, then sorting and
  merging down to l^b0 s^a0, then the chain to the cycle that carries the code 000 (Lemma 15).
Part C: Lemma 15 for every n in {7} and 9..300 with 3 not dividing n, and the chains to {0} for n = 5, 7, 8.

Writes out/chains_94.json. One process; about 2 minutes.
"""
import json
import os
import random
import sys
import time
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring  # noqa: E402
from ring import step, s2w, w2s, frozen94, windows94, is_block_word, limit_cycle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = 94


def bits(s, cells):
    return sum(((s >> c) & 1) << k for k, c in enumerate(cells))


def get(x, p, k, n):
    return [(x >> ((p + i) % n)) & 1 for i in range(k)]


def flip_to(y, j, n, expect_state, expect_transient=None):
    """flip cell j of the periodic state y, iterate to the limit cycle, assert that expect_state lies on it
    and that it is not the cycle of y; return the transient length."""
    assert limit_cycle(R, y, n)[0] == 0, 'flip applied to a non-periodic state'
    t, cyc = limit_cycle(R, y ^ (1 << (j % n)), n)
    assert expect_state in cyc, 'cycle reached is not the predicted one'
    assert y not in cyc, 'flip does not leave the cycle'
    if expect_transient is not None:
        assert t == expect_transient, (t, expect_transient)
    return t


# ------------------------------------------------------------------ moves on block words (Lemmas 11, 12, 13)
def move_swap_sl(x, p, n):
    """short, long at p..p+4 -> long, short. Two flips through the 2-cycle of the width-2 window."""
    assert get(x, p, 5, n) == [0, 1, 0, 1, 1]
    y1 = x ^ (1 << ((p + 2) % n))
    flip_to(x, p + 2, n, y1, 0)
    x2 = y1 ^ (1 << ((p + 3) % n))
    flip_to(y1, p + 3, n, x2, 0)
    assert is_block_word(x2, n) and get(x2, p, 5, n) == [0, 1, 1, 0, 1]
    return x2, 2


def move_swap_ls(x, p, n):
    """long, short at p..p+4 -> short, long."""
    assert get(x, p, 5, n) == [0, 1, 1, 0, 1]
    y1 = x ^ (1 << ((p + 3) % n))
    flip_to(x, p + 3, n, y1, 0)
    x2 = y1 ^ (1 << ((p + 2) % n))
    flip_to(y1, p + 2, n, x2, 0)
    assert is_block_word(x2, n) and get(x2, p, 5, n) == [0, 1, 0, 1, 1]
    return x2, 2


def move_merge(x, p, n):
    """short, short, short at p..p+5 (followed by a block start) -> long, long. One flip, transient 1."""
    assert get(x, p, 7, n) == [0, 1, 0, 1, 0, 1, 0]
    x2 = step(R, x ^ (1 << ((p + 3) % n)), n)
    flip_to(x, p + 3, n, x2, 1)
    assert is_block_word(x2, n) and get(x2, p, 6, n) == [0, 1, 1, 0, 1, 1]
    return x2, 1


def move_split(x, p, n):
    """short, long, long at p..p+7 -> four short blocks. Two flips; the second has transient 5."""
    assert get(x, p, 8, n) == [0, 1, 0, 1, 1, 0, 1, 1]
    y1 = x ^ (1 << ((p + 2) % n))
    flip_to(x, p + 2, n, y1, 0)
    y0 = step(R, y1, n)
    assert step(R, y0, n) == y1 and get(y0, p, 8, n) == [0, 1, 0, 0, 1, 0, 1, 1]
    z = y0 ^ (1 << ((p + 6) % n))
    x2 = z
    for _ in range(5):
        x2 = step(R, x2, n)
    flip_to(y0, p + 6, n, x2, 5)
    assert is_block_word(x2, n) and get(x2, p, 8, n) == [0, 1, 0, 1, 0, 1, 0, 1]
    return x2, 2


def block_moves(x, n):
    """all swaps, merges and splits applicable to the block word x: list of (target, flips)."""
    out = []
    for p in range(n):
        if (x >> p) & 1 or not (x >> ((p - 1) % n)) & 1:
            continue                                   # p must be a block start
        if n >= 5 and get(x, p, 5, n) == [0, 1, 0, 1, 1]:
            out.append(move_swap_sl(x, p, n))
        if n >= 5 and get(x, p, 5, n) == [0, 1, 1, 0, 1] and get(x, p, 6, n)[5] == 0:
            out.append(move_swap_ls(x, p, n))
        if n >= 6 and get(x, p, 7, n) == [0, 1, 0, 1, 0, 1, 0]:
            out.append(move_merge(x, p, n))
        if n >= 8 and get(x, p, 8, n) == [0, 1, 0, 1, 1, 0, 1, 1]:
            out.append(move_split(x, p, n))
    return out


def canonical(n):
    """the block word l^b0 s^a0 cut at cell 0 (a0 = 1 for n = 2 mod 3, a0 = 2 for n = 1 mod 3)."""
    a0 = {1: 2, 2: 1}[n % 3]
    b0 = (n - 2 * a0) // 3
    return w2s('011' * b0 + '01' * a0), a0, b0


# ------------------------------------------------------------------ freezing chain (Lemma 10)
def freeze_flip(s, n):
    """the flip of Lemma 10 for the first window of the periodic state s that is not in the state 1001;
    None if the state is a block word; 'wait' if every window is a width-4 window in the state 1001."""
    wins = windows94(s, n)
    if not wins:
        return None
    for cells in wins:
        w = len(cells)
        u = bits(s, cells)
        if w == 4:
            if u == w2s('1111'):
                return cells[0]
            if u == w2s('0000'):
                return cells[1]
            continue
        A, B = ring.AB_window(w)
        assert w % 3 == 2 and u in (A, B), 'window that is not live'
        return cells[1] if u == A else cells[0]
    return 'wait'


def freeze_chain(s, n):
    """from the periodic state s (non-empty frozen set) to a block word by the flips of Lemma 10.
    Returns (block word, number of flips). Every flip is asserted to join two periodic states of different
    cycles, the second with a strictly larger frozen set."""
    flips = 0
    while True:
        j = freeze_flip(s, n)
        if j is None:
            assert is_block_word(s, n) and step(R, s, n) == s
            return s, flips
        if j == 'wait':
            s = step(R, s, n)
            continue
        y = s ^ (1 << j)
        t, cyc = limit_cycle(R, y, n)
        assert t == 0, 'flipped state is not periodic'
        assert s not in cyc
        assert frozen94(y, n) > frozen94(s, n)
        # reverse flip: y is periodic, y + e_j = s is periodic, so the reversed step is a flip chain too
        assert limit_cycle(R, y ^ (1 << j), n)[0] == 0
        s = y
        flips += 1


def growth_flip(s, n):
    """Lemma 3 of PROOF_94.md for a periodic state with empty frozen set: a flip after which the orbit has a
    frozen cell. Returns a periodic state of the cycle reached."""
    assert not frozen94(s, n)
    if s == 0:
        j = 0
    else:
        j = next(j for j in range(n) if j in frozen94(s ^ (1 << j), n))
    t, cyc = limit_cycle(R, s ^ (1 << j), n)
    assert frozen94(cyc[0], n) and s not in cyc
    return cyc[0]


# ------------------------------------------------------------------ sorting and merging (explicit procedure)
def blocks_from(x, c0, n):
    """block lengths of the block word x read from the block start c0."""
    out, p = [], c0
    while True:
        L = 3 if (x >> ((p + 2) % n)) & 1 else 2
        out.append(L)
        p = (p + L) % n
        if p == c0:
            return out


def sort_and_merge(x, n):
    """swaps short,long -> long,short until the word read from a fixed block start is l^b s^a, then merges of
    the first three short blocks; ends at l^b0 s^a0. Returns (state, start cell of the word, flips)."""
    c0 = next(p for p in range(n) if not (x >> p) & 1 and (x >> ((p - 1) % n)) & 1)
    flips = 0
    while True:
        bl = blocks_from(x, c0, n)
        k = next((k for k in range(len(bl) - 1) if bl[k] == 2 and bl[k + 1] == 3), None)
        if k is not None:
            x, f = move_swap_sl(x, (c0 + sum(bl[:k])) % n, n)
            flips += f
            continue
        a = bl.count(2)
        if a >= 3:
            x, f = move_merge(x, (c0 + 3 * bl.count(3)) % n, n)
            flips += f
            continue
        return x, c0, flips


def chain_to_code0(x, c0, n):
    """from the block word l^b0 s^a0 (word read from c0) to the cycle with a width-4 window in the state 0000.
    Needs n = 7 or n >= 10 (3 not dividing n). Returns (state with code 000, flips)."""
    bl = blocks_from(x, c0, n)
    b0, a0 = bl.count(3), bl.count(2)
    assert bl == [3] * b0 + [2] * a0 and a0 in (1, 2)
    flips = 0
    p = (c0 + 3 * b0) % n                      # start of the first short block
    if a0 == 1:
        x, f = move_split(x, p, n)             # s l l -> s s s s   (the two long blocks follow cyclically)
        flips += f
        p = (p + 4) % n                        # third of the four short blocks; then short, short, long
    assert get(x, p, 7, n) == [0, 1, 0, 1, 0, 1, 1]
    y = x ^ (1 << ((p + 5) % n))               # 0 1 0 1 [0 0] 1 : width-2 window in the state 00
    flip_to(x, p + 5, n, y, 0)
    z = y ^ (1 << ((p + 3) % n))               # 0 1 [0 0 0 0] 1 : width-4 window in the state 0000
    flip_to(y, p + 3, n, z, 0)
    t, cyc = limit_cycle(R, z, n)
    assert t == 0 and len(cyc) == 3 and 0 in ring.codes_of(z, n)
    return z, flips + 2


def main():
    t0 = time.process_time()
    random.seed(9426)
    out = dict(part_A=[], part_B=[], part_C={})

    # ---------------- Part A
    for n in [5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23]:
        F, per, cycles, att = ring.analyse(R, n)
        bws = [s for (s, a, b) in ring.block_words(n)]
        # block-word move graph, every edge executed
        adj = {x: block_moves(x, n) for x in bws}
        n_moves = sum(len(v) for v in adj.values())
        can = canonical(n)[0]
        dist_from = {can: 0}
        dq = deque([can])
        while dq:
            v = dq.popleft()
            for (u, f) in adj[v]:
                if u not in dist_from:
                    dist_from[u] = dist_from[v] + f
                    dq.append(u)
        radj = {x: [] for x in bws}
        for v in bws:
            for (u, f) in adj[v]:
                radj[u].append((v, f))
        dist_to = {can: 0}
        dq = deque([can])
        while dq:
            v = dq.popleft()
            for (u, f) in radj[v]:
                if u not in dist_to:
                    dist_to[u] = dist_to[v] + f
                    dq.append(u)
        strongly = len(dist_from) == len(bws) and len(dist_to) == len(bws)
        n_growth = 0
        max_freeze = 0
        sum_freeze = 0
        n101 = 0
        for cyc in cycles:
            s = cyc[0]
            if not frozen94(s, n):
                s = growth_flip(s, n)
                n_growth += 1
            else:
                n101 += 1
            bw, flips = freeze_chain(s, n)
            assert bw in dist_to
            max_freeze = max(max_freeze, flips)
            sum_freeze += flips
        out['part_A'].append(dict(n=n, cycles=len(cycles), cycles_with_101=n101, growth_flips=n_growth,
                                  all_chains_end_on_a_block_word=True, max_freezing_flips=max_freeze,
                                  mean_freezing_flips=round(sum_freeze / len(cycles), 2), block_words=len(bws),
                                  block_word_moves_executed=n_moves, block_word_graph_strongly_connected=strongly,
                                  max_flips_block_word_to_canonical=max(dist_to.values()),
                                  max_flips_canonical_to_block_word=max(dist_from.values())))
        print('A', out['part_A'][-1], flush=True)

    # ---------------- Part B
    for n in [25, 26, 31, 40, 50, 64, 100, 200, 301]:
        maxf = maxs = 0
        tot = 0
        for _ in range(200):
            s = random.getrandbits(n)
            t, cyc = limit_cycle(R, s, n)
            s = cyc[0]
            if not frozen94(s, n):
                s = growth_flip(s, n)
            bw, f1 = freeze_chain(s, n)
            x, c0, f2 = sort_and_merge(bw, n)
            z, f3 = chain_to_code0(x, c0, n)
            maxf = max(maxf, f1)
            maxs = max(maxs, f2)
            tot += f1 + f2 + f3
        out['part_B'].append(dict(n=n, start_states=200, all_chains_end_on_the_cycle_with_code_000=True,
                                  max_freezing_flips=maxf, max_sorting_and_merging_flips=maxs,
                                  mean_flips=round(tot / 200, 2)))
        print('B', out['part_B'][-1], flush=True)

    # ---------------- Part C
    ns = [n for n in [7] + list(range(10, 301)) if n % 3]
    lens = {}
    for n in ns:
        x, a0, b0 = canonical(n)
        z, f = chain_to_code0(x, 0, n)
        lens[n] = f
    out['part_C']['code_000'] = dict(n='7 and 10..300, 3 not dividing n', ring_sizes=len(ns), all_chains_executed=True,
                                     flips=sorted(set(lens.values())),
                                     flips_by_residue={'n = 1 mod 3': sorted({lens[n] for n in ns if n % 3 == 1}),
                                                       'n = 2 mod 3': sorted({lens[n] for n in ns if n % 3 == 2})})
    # chains to the zero state for n = 5, 7, 8
    zero = {}
    # n = 5, 7: 1^n + e_0 is periodic (frozen 101 and a live all-ones window); flipping cell 0 gives 1^n -> 0
    for n in (5, 7):
        y = ((1 << n) - 1) ^ 1
        t, cyc = limit_cycle(R, y, n)
        assert t == 0 and frozen94(y, n) == {n - 1, 0, 1}
        bw, f = freeze_chain(y, n)                     # reversible chain between y and a block word
        t2, cyc2 = limit_cycle(R, y ^ 1, n)
        assert cyc2 == [0] and t2 == 1
        zero[n] = dict(periodic_state=s2w(y, n), period=len(cyc), flip_cell=0, steps_to_zero=t2,
                       reversible_flips_from_a_block_word=f, block_word=s2w(bw, n))
    n = 8
    y = w2s('01111010')
    t, cyc = limit_cycle(R, y, n)
    assert t == 0 and frozen94(y, n) == {4, 5, 6}
    bw, f = freeze_chain(y, n)
    orbit = [y ^ (1 << 5)]
    while orbit[-1] != 0:
        orbit.append(step(R, orbit[-1], n))
    zero[n] = dict(periodic_state=s2w(y, n), period=len(cyc), flip_cell=5, steps_to_zero=len(orbit) - 1,
                   orbit_after_flip=[s2w(v, n) for v in orbit], reversible_flips_from_a_block_word=f,
                   block_word=s2w(bw, n))
    out['part_C']['zero_state'] = {str(k): v for k, v in zero.items()}
    out['cpu_s'] = round(time.process_time() - t0, 2)
    with open(os.path.join(HERE, 'out', 'chains_94.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=int)
    print('C', json.dumps(out['part_C'])[:600])
    print('cpu s', out['cpu_s'])


if __name__ == '__main__':
    main()
