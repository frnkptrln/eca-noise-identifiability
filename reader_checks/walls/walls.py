"""Reader's check of the open-boundary study (report_boundaries.md). Claude, the reader outside the sessions,
25 November 2026. Own code; nothing is imported from the repository.
Usage: python walls.py <ring|null|one|reflect> <nmin> <nmax> <rules, comma separated, or all> [cap]
For at most `cap` cycles (default 70) the potentials of all cycles are computed (Edmonds, one run per root) and with
them every k_c. Above the cap only the one-flip graph G_1 is computed; if it has one closed class K, then K is the
selected set and gamma_min = m - 1 (an in-tree of m - 1 edges of weight 1 exists exactly for the roots in K), and
the record has no k_c. Below the cap this statement is asserted against the potentials, not used.
State: integer, bit i = cell i. Code read at cell i: 4*x[i-1] + 2*x[i] + x[i+1]; new value = bit code of rule.
Noise step: x -> F(x) XOR flips, resistance = number of flips."""
import sys, csv, numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def cells(n, boundary):
    s = np.arange(1 << n, dtype=np.int64)
    bit = [(s >> i) & 1 for i in range(n)]
    out = []
    for i in range(n):
        if i > 0: l = bit[i-1]
        else: l = {'ring': bit[n-1], 'null': 0*s, 'one': 0*s+1, 'reflect': bit[0]}[boundary]
        if i < n-1: r = bit[i+1]
        else: r = {'ring': bit[0], 'null': 0*s, 'one': 0*s+1, 'reflect': bit[n-1]}[boundary]
        out.append(4*l + 2*bit[i] + r)
    return s, out

def model(rule, n, boundary):
    s, cs = cells(n, boundary)
    F = np.zeros_like(s); mask = np.zeros_like(s)
    for i, c in enumerate(cs):
        F |= ((rule >> c) & 1) << i
        mask |= 1 << c
    return F, mask

def cycles(F):
    N = len(F); alive = np.ones(N, bool)
    while True:
        cnt = np.bincount(F[alive], minlength=N)
        dead = alive & (cnt == 0)
        if not dead.any(): break
        alive &= ~dead
    lab = -np.ones(N, np.int64); m = 0
    for x in np.flatnonzero(alive):
        if lab[x] < 0:
            y = x
            while lab[y] < 0:
                lab[y] = m; y = F[y]
            m += 1
    return lab, m

def dist_from(F, n, src):
    """least number of flips on a noisy path from the set src (closed under F) to every state"""
    N = len(F); d = np.full(N, 127, np.int8); cur = src.copy(); d[cur] = 0; lev = 0
    while True:
        # closure under F at this level
        fr = cur
        while True:
            nx = np.zeros(N, bool); nx[F[np.flatnonzero(fr)]] = True
            nx &= d == 127
            if not nx.any(): break
            d[nx] = lev; fr = nx
        allc = np.flatnonzero(d == lev)
        nxt = np.zeros(N, bool)
        for i in range(n): nxt[allc ^ (1 << i)] = True
        nxt &= d == 127
        if not nxt.any(): break
        lev += 1; d[nxt] = lev; cur = nxt
    return d

def min_out_arb(W, root):
    """Chu-Liu/Edmonds: least weight of a spanning arborescence with edges pointing away from root. W[u][v] = weight u->v."""
    W = W.astype(np.int64).copy(); res = 0
    while True:
        k = len(W); BIG = 10**9
        A = W.copy(); np.fill_diagonal(A, BIG)
        pre = A.argmin(axis=0); inw = A.min(axis=0); inw[root] = 0
        res += int(inw.sum())
        ident = -np.ones(k, int); vis = -np.ones(k, int); cnt = 0
        for v in range(k):
            u = v
            while vis[u] != v and ident[u] < 0 and u != root:
                vis[u] = v; u = pre[u]
            if u != root and ident[u] < 0:
                w = pre[u]
                while w != u: ident[w] = cnt; w = pre[w]
                ident[u] = cnt; cnt += 1
        if cnt == 0: return res
        for v in range(k):
            if ident[v] < 0: ident[v] = cnt; cnt += 1
        B = np.full((cnt, cnt), BIG, np.int64)
        Aadj = A - inw[None, :]
        for u in range(k):
            iu = ident[u]
            np.minimum.at(B[iu], ident, np.where(ident != iu, Aadj[u], BIG))
        W = B; root = ident[root]

def basins(F, lab):
    """cycle reached from every state (pointer jumping)"""
    G = F.copy()
    while (lab[G] < 0).any(): G = G[G]
    return lab[G]

def analyse(rule, n, boundary, full_max=70):
    F, mask = model(rule, n, boundary)
    lab, m = cycles(F)
    res = dict(rule=rule, n=n, boundary=boundary, cycles=m)
    per = np.flatnonzero(lab >= 0)
    allc = int(np.bitwise_or.reduce(mask[per])); res['btype'] = int(allc != 255)
    # one-flip graph G1 from the definition: C -> C' iff some state of C with one cell flipped runs into C'
    bas = basins(F, lab)
    src = np.concatenate([lab[per]] * n); dst = np.concatenate([bas[per ^ (1 << i)] for i in range(n)])
    keep = src != dst
    pairs = np.unique(src[keep] * m + dst[keep])            # each edge once (no summing of duplicates)
    G1s = csr_matrix((np.ones(len(pairs), np.int8), (pairs // m, pairs % m)), shape=(m, m))
    ncomp, comp = connected_components(G1s, directed=True, connection='strong')
    has_out = np.zeros(ncomp, bool)
    co = G1s.tocoo(); cross = comp[co.row] != comp[co.col]; has_out[comp[co.row[cross]]] = True
    closed = np.flatnonzero(~has_out)
    res['closed_classes'] = len(closed)
    gamma = None
    if m <= full_max:
        D = np.empty((m, len(F)), np.int8)
        for c in range(m): D[c] = dist_from(F, n, lab == c)
        V = np.full((m, m), 127, np.int64)
        order = np.argsort(lab[per], kind='stable'); ps = per[order]; ls = lab[per][order]
        starts = np.searchsorted(ls, np.arange(m))
        V = np.minimum.reduceat(D[:, ps].astype(np.int64), starts, axis=1)
        np.fill_diagonal(V, 0)
        assert ((V == 1) == (G1s.toarray() > 0)).all(), "G1 from distances differs from G1 from single flips"
        gamma = np.array([min_out_arb(V.T, c) for c in range(m)])
        gmin = gamma.min(); sel = gamma == gmin
        if len(closed) == 1:
            assert gmin == m - 1 and (sel == (comp == closed[0])).all(), "Theorem A check failed"
    elif len(closed) == 1:
        sel = comp == closed[0]; gmin = m - 1
    else:
        res['note'] = 'not decided (many cycles, several closed classes)'; return res
    res['gamma_min'] = int(gmin); res['selected'] = int(sel.sum())
    selstates = sel[lab[per]]
    cover = int(np.bitwise_or.reduce(mask[per[selstates]]))
    res['missed'] = ''.join(str(c) for c in range(8) if not (cover >> c) & 1)
    res['side'] = int(cover != 255)
    if gamma is not None:
        o = (gamma[:, None] + D.astype(np.int64)).min(axis=0) - gmin
        kc = [int(o[(mask >> c) & 1 == 1].min()) if ((mask >> c) & 1).any() else -1 for c in range(8)]
        res['kc'] = '-'.join(map(str, kc)); res['kstar'] = max(kc)
    return res

if __name__ == '__main__':
    boundary, nmin, nmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rules = [int(r) for r in sys.argv[4].split(',')] if len(sys.argv) > 4 and sys.argv[4] != 'all' else range(256)
    full_max = int(sys.argv[5]) if len(sys.argv) > 5 else 70
    w = csv.DictWriter(sys.stdout, ['rule','n','boundary','cycles','closed_classes','gamma_min','selected','missed','side','btype','kc','kstar','note'])
    w.writeheader()
    for n in range(nmin, nmax + 1):
        for r in rules:
            w.writerow(analyse(r, n, boundary, full_max)); sys.stdout.flush()
