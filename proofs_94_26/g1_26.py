"""Rule 26, even n: G1 and its closed classes from all 2^n states; for n = 4, 8, 16 also the potentials
gamma, the resistances V and R and the indices k_c from the definitions.

Usage: python g1_26.py N [N ...]   (appends one JSON record per ring size to out/g1_26.jsonl; sizes present are skipped)
One process. Cost at n = 22: about 10 s and 0.3 GB.

Definitions used for n = 4, 8, 16 (report_ring_size.md, Section 3; verify_ring_size/part2_154/PROOF_154.md, Section 1):
  r(x, y) = H(F x, y); V(C, C') = least total resistance of a path from a state of C to a state of C';
  gamma(C) = least weight of a spanning in-tree of the cycles rooted at C with weights V;
  D_c = states containing the code c; R(C -> D_c) = least resistance of a path from C to D_c;
  k_c = min over C of [gamma(C) + R(C -> D_c)] - min gamma; k* = max_c k_c.
A path of resistance d is a sequence of F-steps (cost 0) and single flips (cost 1), so V and R are distances in
the graph on the states with these two kinds of edges (0-1 breadth-first search, vectorised).
gamma is computed for every root by the Chu-Liu/Edmonds algorithm (own implementation) for n = 4, 8, 16
(552 roots at n = 16, about 3 minutes).
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
import r26  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'g1_26.jsonl')
R = 26


def dist_from(F, n, sources):
    """resistance distance from the set of states `sources` to every state (F-steps cost 0, flips cost 1)."""
    N = 1 << n
    dist = np.full(N, -1, dtype=np.int8)
    frontier = np.array(sorted(sources), dtype=np.uint32)
    d = 0
    while len(frontier):
        # closure under F at cost 0
        new = frontier
        level = []
        while len(new):
            new = np.unique(new[dist[new] < 0])
            dist[new] = d
            level.append(new)
            new = F[new]
        level = np.concatenate(level) if level else np.array([], dtype=np.uint32)
        nxt = [level ^ np.uint32(1 << j) for j in range(n)]
        frontier = np.unique(np.concatenate(nxt)) if len(level) else level
        frontier = frontier[dist[frontier] < 0]
        d += 1
    return dist


def edmonds(W, root):
    """least weight of a spanning in-tree rooted at `root` for the dense weight matrix W (W[i][j] = weight of the
    edge i -> j; every node chooses one outgoing edge). Chu-Liu/Edmonds with contraction (NumPy)."""
    W = np.array(W, dtype=float)
    m = len(W)
    np.fill_diagonal(W, np.inf)
    alive = np.ones(m, dtype=bool)
    total = 0.0
    while True:
        nodes = np.nonzero(alive)[0]
        sub = W[np.ix_(nodes, nodes)]
        arg = nodes[np.argmin(sub, axis=1)]
        best = sub.min(axis=1)
        out = {int(v): (int(a), float(b)) for v, a, b in zip(nodes, arg, best) if v != root}
        color = {}
        cyc = None
        for v in out:
            if v in color:
                continue
            path = []
            u = v
            while u != root and u not in color:
                color[u] = v
                path.append(u)
                u = out[u][0]
            if u != root and color[u] == v:
                cyc = path[path.index(u):]
                break
        if cyc is None:
            return int(round(total + sum(w for (_, w) in out.values())))
        total += sum(out[v][1] for v in cyc)
        c = cyc[0]
        red = np.array([out[v][1] for v in cyc])
        row = (W[cyc, :] - red[:, None]).min(axis=0)       # edges leaving the cycle, reduced
        col = W[:, cyc].min(axis=1)                        # edges entering the cycle
        for v in cyc[1:]:
            alive[v] = False
            W[v, :] = np.inf
            W[:, v] = np.inf
        W[c, :] = row
        W[:, c] = col
        W[c, c] = np.inf
        for v in cyc[1:]:
            W[c, v] = np.inf
            W[v, c] = np.inf


def record(n, full_k):
    t0 = time.process_time()
    r = ring.g1(R, n)
    cycles, lab, A, att, F = r['cycles'], r['lab'], r['A'], r['att'], r['F']
    m = r['m']
    E = sum(1 << i for i in range(0, n, 2))
    O = E << 1
    zero = int(att[0])
    kind = []
    cval = []
    for cyc in cycles:
        s = cyc[0]
        cval.append(r26.c_changes(s, n))
        if s == 0:
            kind.append('zero')
        elif any(r26.has111(v, n) for v in cyc):
            kind.append('with_111')
        elif (s & E) == 0 or (s & O) == 0:
            kind.append('one_parity')
        else:
            kind.append('domain')
            assert all(r26.is_domain_state(v, n) for v in cyc)
    kind = np.array(kind)
    cval = np.array(cval)
    closed_sizes = sorted(int((lab == c).sum()) for c in r['closed'])
    rec = dict(n=n, power_of_two=(n & (n - 1)) == 0, cycles=m, periodic_states=int(r['per'].sum()), g1_edges=r['n_edges'],
               strong_components=r['ncomp'], closed_classes=closed_sizes,
               cycles_by_kind=dict(sorted(Counter(kind.tolist()).items())))
    K = lab[zero]
    inK = lab == K
    rec['zero_in_the_closed_class'] = bool(len(r['closed']) == 1 and r['closed'][0] == K)
    rec['one_parity_cycles_in_K'] = '%d of %d' % (int((inK & (kind == 'one_parity')).sum()), int((kind == 'one_parity').sum()))
    rec['domain_cycles_in_K'] = '%d of %d' % (int((inK & (kind == 'domain')).sum()), int((kind == 'domain').sum()))
    rec['cycles_with_111_in_K'] = '%d of %d' % (int((inK & (kind == 'with_111')).sum()), int((kind == 'with_111').sum()))
    rec['cycles_outside_K_all_carry_111'] = bool((kind[~inK] == 'with_111').all())
    codes = set()
    for i in np.nonzero(inK)[0]:
        for s in cycles[i]:
            codes |= ring.codes_of(s, n)
    rec['codes_on_K'] = sorted(codes)
    rec['c_of_domain_cycles'] = sorted(set(cval[kind == 'domain'].tolist()))
    rec['c_of_cycles_with_111'] = sorted(set(cval[kind == 'with_111'].tolist()))
    words = r26.carrier_words(n)
    rec['cycles_with_111_through_a_carrier_word'] = int(sum(1 for i in np.nonzero(kind == 'with_111')[0]
                                                            if any(s in words for s in cycles[i])))
    # every G1 edge raises c by at most 2
    coo = A.tocoo()
    rec['max_increase_of_c_along_a_G1_edge'] = int((cval[coo.col] - cval[coo.row]).max()) if coo.nnz else None
    # distance to {0} in G1
    rev = A.T.tocsr()
    dist = np.full(m, -1)
    dist[zero] = 0
    front = [zero]
    while front:
        nf = []
        for v in front:
            for u in rev.indices[rev.indptr[v]:rev.indptr[v + 1]]:
                if dist[u] < 0:
                    dist[u] = dist[v] + 1
                    nf.append(int(u))
        front = nf
    rec['cycles_with_a_G1_path_to_zero'] = int((dist >= 0).sum())
    rec['max_G1_distance_to_zero'] = int(dist.max())
    rec['G1_distance_to_zero_by_c'] = {str(int(cv)): [int(dist[cval == cv].min()), int(dist[cval == cv].max())]
                                       for cv in sorted(set(cval.tolist()))}
    if rec['power_of_two']:
        # T2: cycles at resistance 2 from {0}; Q: cycles reachable from T2 in G1
        d0 = dist_from(F, n, [0])
        V0 = np.array([int(d0[cyc].min()) for cyc in cycles])
        rec['V_from_zero_hist'] = dict(sorted(Counter(V0.tolist()).items()))
        T2 = [i for i in range(m) if V0[i] == 2]
        Q = ring.reach_from(A.tocsr(), T2) if T2 else np.zeros(m, dtype=bool)
        rec['T2_cycles'] = len(T2)
        rec['cycles_reachable_from_T2'] = int(Q.sum())
        rec['domain_cycles_reachable_from_T2'] = '%d of %d' % (int((Q & (kind == 'domain')).sum()), int((kind == 'domain').sum()))
        rec['cycles_with_111_reachable_from_T2'] = '%d of %d' % (int((Q & (kind == 'with_111')).sum()), int((kind == 'with_111').sum()))
        if full_k:
            # V between all cycles, R to every code, gamma, k_c from the definitions
            Vm = np.zeros((m, m), dtype=np.int64)
            Rc = np.zeros((m, 8), dtype=np.int64)
            code_sets = []
            x = np.arange(1 << n, dtype=np.uint32)
            mask = np.uint32((1 << n) - 1)
            left = ((x << np.uint32(1)) | (x >> np.uint32(n - 1))) & mask
            right = ((x >> np.uint32(1)) | (x << np.uint32(n - 1))) & mask
            for code in range(8):
                a, b, c = (code >> 2) & 1, (code >> 1) & 1, code & 1
                code_sets.append(((left if a else ~left) & (x if b else ~x) & (right if c else ~right) & mask) != 0)
            for i, cyc in enumerate(cycles):
                d = dist_from(F, n, cyc)
                for j, cyc2 in enumerate(cycles):
                    Vm[i, j] = d[cyc2].min()
                for code in range(8):
                    Rc[i, code] = d[code_sets[code]].min()
            rec['V_hist'] = dict(sorted(Counter(Vm[~np.eye(m, dtype=bool)].tolist()).items()))
            # G1 edges are exactly the pairs with V = 1
            rec['G1_edges_equal_pairs_with_V_1'] = bool(int((Vm == 1).sum()) == r['n_edges']
                                                       and all(Vm[a, b] == 1 for a, b in zip(coo.row, coo.col)))
            Wl = Vm.tolist()
            if m <= 600:
                roots = list(range(m))
            else:
                carr = [int(i) for i in np.nonzero(kind == 'with_111')[0]]
                dom = [int(i) for i in np.nonzero(kind == 'domain')[0]]
                roots = [zero] + carr + dom[:3]
            gamma = {i: edmonds(Wl, i) for i in roots}
            rec['gamma_roots_computed_by_Edmonds'] = len(roots)
            rec['gamma_zero'] = gamma[zero]
            rec['gamma_by_kind'] = {kd: sorted({gamma[i] for i in roots if kind[i] == kd}) for kd in sorted(set(kind[roots].tolist()))}
            # Theorem 3: gamma = m - 1 at {0}; = m on the cycles reachable from T2; >= m + 1 elsewhere
            g_thm = np.where(np.arange(m) == zero, m - 1, np.where(Q, m, m + 1))       # lower bound m + 1 outside Q
            rec['gamma_agrees_with_Theorem_3_on_the_computed_roots'] = bool(all(
                (gamma[i] == g_thm[i]) if (i == zero or Q[i]) else (gamma[i] >= m + 1) for i in roots))
            gmin = m - 1
            if m <= 600:
                gam = np.array([gamma[i] for i in range(m)])
                k = [int((gam + Rc[:, code]).min() - gam.min()) for code in range(8)]
                rec['k_c_from_the_definition'] = k
                rec['selected_cycles'] = [ring.s2w(cycles[i][0], n) for i in range(m) if gam[i] == gam.min()]
            else:
                # exact gamma on {0} and on Q; outside Q the bound gamma >= m + 1 (Theorem 3) and the Edmonds values above
                lo = [int(min((g_thm + Rc[:, code]).min(), 10 ** 9) - gmin) for code in range(8)]
                rec['k_c_from_V_R_and_Theorem_3'] = lo
            rec['R_from_zero_to_code'] = Rc[zero].tolist()
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
        rec = record(n, full_k=n in (4, 8, 16))
        with open(OUT, 'a') as fh:
            fh.write(json.dumps(rec, default=int) + '\n')
        print(json.dumps(rec, default=int), flush=True)


if __name__ == '__main__':
    main()
