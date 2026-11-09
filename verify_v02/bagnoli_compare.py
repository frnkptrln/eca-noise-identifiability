"""Step 6: the single-flip attractor chain of Bagnoli, Baia and Matteuzzi (arXiv:2406.15408v2, Sec. 5),
rebuilt from their description, at L = n = 17 for all 88 classes, and compared with their Table 2.
W(i|j) = number of (state of cycle j, one-site flip) pairs that land in the basin of cycle i; columns normalised;
their S* = normalised entropy of the limit of Q' = W Q started from basin weights b_k / 2^L, with the mass of a
cycle spread uniformly over its states. Also: closed classes of the single-flip graph (off-diagonal W > 0).
Usage: python bagnoli_compare.py OUT n rules"""
import sys, math, time
import numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
import eca

out, n = sys.argv[1], int(sys.argv[2]); rules = [int(r) for r in sys.argv[3].split(',')]
done = {r['rule'] for r in eca.read_jsonl(out)}
N = 1 << n
for rule in rules:
    if rule in done: continue
    t0 = time.time()
    F = eca.step_map(rule, n).astype(np.int64)
    cid, cyc = eca.cycles_of(F)
    m = len(cyc)
    G = F.copy(); k = 1
    while k < N: G = G[G]; k *= 2
    lab = cid[G]                      # basin label of every state
    basin = np.bincount(lab, minlength=m)
    clen = np.array([len(c) for c in cyc])
    src = np.concatenate(cyc); srcl = cid[src]
    rows, cols = [], []
    for b in range(n):
        rows.append(lab[src ^ (1 << b)]); cols.append(srcl)
    rows = np.concatenate(rows); cols = np.concatenate(cols)
    W = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(m, m)).tocsr()
    W.sum_duplicates()
    W = W.multiply(1.0 / np.asarray(W.sum(axis=0)).ravel()[None, :]).tocsr()   # column-stochastic
    # closed classes of the single-flip graph j -> i (i != j)
    A = (W - sp.diags(W.diagonal())).T.tocsr()   # A[j, i] > 0: edge j -> i
    A.eliminate_zeros()
    ncomp, comp = connected_components(A, directed=True, connection='strong')
    # a strong component is closed if no edge leaves it
    Ac = A.tocoo()
    leaves = np.zeros(ncomp, bool); leaves[comp[Ac.row][comp[Ac.row] != comp[Ac.col]]] = True
    closed = [c for c in range(ncomp) if not leaves[c]]
    # their iteration from basin weights
    Q = basin / N; it = 0; res = 1.0
    while it < 200000 and res > 1e-14:
        Q2 = W @ Q; res = np.abs(Q2 - Q).sum(); Q = Q2; it += 1
    P = Q / clen
    nz = Q > 0
    Sstar = float(-(Q[nz] * np.log(P[nz])).sum() / (n * math.log(2)))
    support = np.nonzero(Q > 1e-12)[0]
    cm = eca.code_masks(n)
    cover = 0
    for c in range(8):
        if np.any(cm[c][np.concatenate([cyc[i] for i in support])] > 0): cover |= 1 << c
    eca.append_jsonl(out, dict(rule=rule, n=n, m_cycles=m, n_closed=len(closed),
                               closed_sizes=sorted(int((comp == c).sum()) for c in closed)[:50],
                               closed_cycles=(sorted(int(i) for i in np.nonzero(np.isin(comp, closed))[0]) if m <= 20000 else None),
                               Sstar_rebuilt=Sstar, iters=it, resid=res, support_size=int(len(support)), support_cover_mask=int(cover),
                               support_min_states=[int(cyc[i].min()) for i in support][:20],
                               sec=round(time.time() - t0, 2)))
