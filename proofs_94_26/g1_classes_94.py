"""Rule 94, rings with 3 not dividing n: G1 and its closed classes computed directly from all 2^n states.

Usage: python g1_classes_94.py N [N ...]      (appends one JSON record per ring size to out/g1_classes_94.jsonl;
                                                ring sizes already present are skipped)
Independent of the proofs: tabulates F on all states, finds the periodic states and the cycle every state
falls to, follows all single flips of all periodic states, and computes strong components.
One process. Cost at n = 23: about 10 s and 0.6 GB.
"""
import json
import os
import resource
import sys
import time
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'g1_classes_94.jsonl')


def record(n):
    t0 = time.process_time()
    r = ring.g1(94, n)
    cycles, lab, A = r['cycles'], r['lab'], r['A']
    m = r['m']
    rep = [c[0] for c in cycles]
    frozen_size = [len(ring.frozen94(s, n)) for s in rep]
    is_bw = [len(c) == 1 and ring.is_block_word(c[0], n) for c in cycles]
    closed_sizes = sorted(int((lab == c).sum()) for c in r['closed'])
    rec = dict(n=n, n_mod_3=n % 3, cycles=m, periodic_states=int(r['per'].sum()), g1_edges=r['n_edges'],
               strong_components=r['ncomp'], closed_classes=closed_sizes)
    bw_idx = [i for i in range(m) if is_bw[i]]
    rec['block_words'] = len(bw_idx)
    rec['block_word_classes_ab'] = sorted({(a, b) for (s, a, b) in ring.block_words(n)}) if n <= 20 else None
    rec['block_words_in_one_component'] = len({int(lab[i]) for i in bw_idx}) == 1 if bw_idx else None
    if len(r['closed']) == 1:
        K = r['closed'][0]
        inK = lab == K
        rec['block_words_all_in_K'] = bool(all(inK[i] for i in bw_idx))
        with101 = [i for i in range(m) if frozen_size[i] > 0]
        without = [i for i in range(m) if frozen_size[i] == 0]
        rec['cycles_with_101'] = len(with101)
        rec['cycles_with_101_in_K'] = int(sum(inK[i] for i in with101))
        rec['cycles_without_101'] = len(without)
        rec['cycles_without_101_in_K'] = int(sum(inK[i] for i in without))
        rec['periods_without_101_in_K'] = dict(sorted(Counter(len(cycles[i]) for i in without if inK[i]).items()))
        rec['periods_without_101_outside_K'] = dict(sorted(Counter(len(cycles[i]) for i in without if not inK[i]).items()))
        rec['cycles_outside_K'] = int((~inK).sum())
        rec['cycles_outside_K_with_101'] = int(sum(1 for i in with101 if not inK[i]))
        zero = int(r['att'][0])
        rec['zero_state_in_K'] = bool(inK[zero])
        # incoming G1 edges of {0}
        rec['zero_state_in_degree'] = int(A.tocsc()[:, zero].nnz)
        codes = set()
        for i in range(m):
            if inK[i]:
                for s in cycles[i]:
                    codes |= ring.codes_of(s, n)
        rec['codes_on_K'] = sorted(codes)
        # K as the forward closure of the block words
        reach = ring.reach_from(A, bw_idx)
        rec['K_equals_cycles_reachable_from_block_words'] = bool((reach == inK).all())
        rec['periods_in_K'] = dict(sorted(Counter(len(cycles[i]) for i in range(m) if inK[i]).items()))
        # cycles with code 000 in K that contain a 101
        rec['cycles_with_101_and_code_000'] = int(sum(1 for i in with101 if any(0 in ring.codes_of(s, n) for s in cycles[i])))
    rec['cpu_s'] = round(time.process_time() - t0, 2)
    rec['peak_rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == 'darwin' else 1024), 0)
    return rec


def main():
    ns = [int(a) for a in sys.argv[1:]]
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as fh:
            done = {json.loads(line)['n'] for line in fh if line.strip()}
    for n in ns:
        if n in done:
            print('n = %d already present, skipped' % n)
            continue
        rec = record(n)
        with open(OUT, 'a') as fh:
            fh.write(json.dumps(rec) + '\n')
        print(json.dumps(rec))


if __name__ == '__main__':
    main()
