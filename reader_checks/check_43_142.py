# Independent check of the claims for rules 43 and 142 (own code, definitions only).
import sys, time, numpy as np, networkx as nx
def step_table(rule, n):
    N = 1 << n; x = np.arange(N, dtype=np.int64)
    left = ((x >> 1) | ((x & 1) << (n-1)))          # value of neighbour i+1 at position i  (bit i = cell i)
    right = ((x << 1) & (N-1)) | (x >> (n-1))       # neighbour i-1
    out = np.zeros(N, dtype=np.int64)
    for i in range(n):
        a = (right >> i) & 1; b = (x >> i) & 1; c = (left >> i) & 1   # a = cell i-1, c = cell i+1
        out |= ((rule >> (4*a + 2*b + c)) & 1) << i
    return out
def codes_of(n):
    N = 1 << n; x = np.arange(N, dtype=np.int64)
    left = ((x >> 1) | ((x & 1) << (n-1))); right = ((x << 1) & (N-1)) | (x >> (n-1))
    has = np.zeros((8, N), dtype=bool)
    for i in range(n):
        code = 4*((right >> i) & 1) + 2*((x >> i) & 1) + ((left >> i) & 1)
        for c in range(8): has[c] |= (code == c)
    return has
def walls(n):
    N = 1 << n; x = np.arange(N, dtype=np.int64)
    rot = ((x >> 1) | ((x & 1) << (n-1)))
    d = x ^ rot
    return np.array([bin(v).count('1') for v in d])
def analyse(rule, n, potentials):
    N = 1 << n; F = step_table(rule, n)
    # periodic states: image of F^N' (iterate n*4 times is enough? use 2^k doubling up to >= N)
    G = F.copy(); k = 1
    while k < N: G = G[G]; k *= 2
    per = np.zeros(N, bool); per[G] = True
    # cycle labels
    lab = -np.ones(N, dtype=np.int64); m = 0; cyc = []
    for s in np.nonzero(per)[0]:
        if lab[s] < 0:
            t = s; mem = []
            while lab[t] < 0: lab[t] = m; mem.append(t); t = F[t]
            cyc.append(mem); m += 1
    att = lab[G]                      # cycle on which each state ends
    w = walls(n); wc = np.array([w[c[0]] for c in cyc])
    assert all(len(set(w[c])) == 1 for c in cyc)
    # G1
    flips = [1 << j for j in range(n)]
    E = set()
    for ci, c in enumerate(cyc):
        cs = np.array(c)
        for fmask in flips:
            for t in set(att[cs ^ fmask].tolist()):
                if t != ci: E.add((ci, t))
    g1 = nx.DiGraph(); g1.add_nodes_from(range(m)); g1.add_edges_from(E)
    cond = nx.condensation(g1)
    closed = [frozenset(cond.nodes[v]['members']) for v in cond if cond.out_degree(v) == 0]
    res = dict(rule=rule, n=n, m=m, closed=[len(k) for k in closed])
    if n % 4 == 0:
        x0 = sum(1 << i for i in range(n) if i % 4 in (2, 3)); X = lab[x0]
        res['claim_closed'] = (closed == [frozenset([X])])
        res['X_len'] = len(cyc[X]); claimS = {X}
        res['dist_ok'] = all(nx.shortest_path_length(g1, c, X) == abs(wc[c] - n//2)//2 for c in range(m))
    else:
        lo = max(v for v in range(0, n+1, 2) if v < n/2); hi = lo + 2
        claimS = set(np.nonzero((wc == lo) | (wc == hi))[0].tolist())
        res['claim_closed'] = (closed == [frozenset(claimS)])
    if potentials:
        has = codes_of(n)
        V = np.zeros((m, m), dtype=np.int64); R = np.zeros((m, 8), dtype=np.int64)
        for ci, c in enumerate(cyc):
            dist = -np.ones(N, dtype=np.int64); cur = np.array(c); dist[cur] = 0; L = 0
            while True:
                new = cur                                     # close under F
                while True:
                    nxt = np.unique(F[new]); nxt = nxt[dist[nxt] < 0]
                    if len(nxt) == 0: break
                    dist[nxt] = L; new = nxt
                lvl = np.nonzero(dist == L)[0]
                cand = np.unique(np.concatenate([lvl ^ f for f in flips])); cand = cand[dist[cand] < 0]
                if len(cand) == 0: break
                L += 1; dist[cand] = L; cur = cand
            assert (dist >= 0).all()
            for t in range(m): V[ci, t] = dist[np.array(cyc[t])].min()
            for cd in range(8): R[ci, cd] = dist[has[cd]].min() if has[cd].any() else 10**6
        gam = np.zeros(m, dtype=np.int64)
        for r in range(m):
            H = nx.DiGraph()
            for u in range(m):
                for v in range(m):
                    if u != v and u != r: H.add_edge(v, u, weight=int(V[u, v]))   # reversed: in-tree to r
            T = nx.minimum_spanning_arborescence(H)
            gam[r] = sum(d['weight'] for _, _, d in T.edges(data=True))
        gmin = gam.min(); S = set(np.nonzero(gam == gmin)[0].tolist())
        kc = [int((gam + R[:, cd]).min() - gmin) for cd in range(8)]
        res.update(gmin=int(gmin), gmin_is_m_minus_1=(gmin == m-1), S_is_claim=(S == claimS), kc=kc, kstar=max(kc),
                   kstar_claim=(max(kc) == (1 if n % 4 == 0 else 0)))
        # edge check: G1 edge iff V == 1
        res['G1_is_V1'] = (E == {(u, v) for u in range(m) for v in range(m) if u != v and V[u, v] == 1})
    return res
if __name__ == '__main__':
    nmaxG, nmaxP = int(sys.argv[1]), int(sys.argv[2])
    for rule in (43, 142):
        for n in range(4, nmaxG+1):
            t = time.time(); r = analyse(rule, n, n <= nmaxP); r['sec'] = round(time.time()-t, 1); print(r, flush=True)
