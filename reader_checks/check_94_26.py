# Independent check (own code, definitions only) of the headline claims for rule 94 (3 not | n) and rule 26 (even n).
import sys, time, numpy as np, networkx as nx
from check_43_142 import step_table, codes_of
def base(rule, n):
    N = 1 << n; F = step_table(rule, n)
    G = F.copy(); k = 1
    while k < N: G = G[G]; k *= 2
    per = np.zeros(N, bool); per[G] = True
    lab = -np.ones(N, dtype=np.int64); cyc = []
    for s in np.nonzero(per)[0]:
        if lab[s] < 0:
            t = s; mem = []
            while lab[t] < 0: lab[t] = len(cyc); mem.append(int(t)); t = F[t]
            cyc.append(mem)
    att = lab[G]; m = len(cyc); flips = [1 << j for j in range(n)]
    E = set()
    for ci, c in enumerate(cyc):
        cs = np.array(c)
        for f in flips:
            for t in set(att[cs ^ f].tolist()):
                if t != ci: E.add((ci, t))
    g1 = nx.DiGraph(); g1.add_nodes_from(range(m)); g1.add_edges_from(E)
    cond = nx.condensation(g1)
    closed = [set(cond.nodes[v]['members']) for v in cond if cond.out_degree(v) == 0]
    return N, F, cyc, lab, att, flips, E, g1, closed
def potentials(n, N, F, cyc, flips):
    m = len(cyc); has = codes_of(n)
    V = np.zeros((m, m), dtype=np.int64); R = np.zeros((m, 8), dtype=np.int64)
    for ci, c in enumerate(cyc):
        dist = -np.ones(N, dtype=np.int64); cur = np.array(c); dist[cur] = 0; L = 0
        while True:
            new = cur
            while True:
                nxt = np.unique(F[new]); nxt = nxt[dist[nxt] < 0]
                if len(nxt) == 0: break
                dist[nxt] = L; new = nxt
            lvl = np.nonzero(dist == L)[0]
            cand = np.unique(np.concatenate([lvl ^ f for f in flips])); cand = cand[dist[cand] < 0]
            if len(cand) == 0: break
            L += 1; dist[cand] = L; cur = cand
        for t in range(m): V[ci, t] = dist[np.array(cyc[t])].min()
        for cd in range(8): R[ci, cd] = dist[has[cd]].min()
    gam = np.zeros(m, dtype=np.int64)
    for r in range(m):
        H = nx.DiGraph(); H.add_node(r)
        for u in range(m):
            for v in range(m):
                if u != v and u != r: H.add_edge(v, u, weight=int(V[u, v]))
        gam[r] = sum(d['weight'] for _, _, d in nx.minimum_spanning_arborescence(H).edges(data=True)) if m > 1 else 0
    gmin = gam.min(); S = set(np.nonzero(gam == gmin)[0].tolist())
    kc = [int((gam + R[:, cd]).min() - gmin) for cd in range(8)]
    return gam, int(gmin), S, kc
def has101(x, n):
    b = [(x >> i) & 1 for i in range(n)]
    return any(b[i-1] == 1 and b[i] == 0 and b[(i+1) % n] == 1 for i in range(n))
def has111(x, n):
    b = [(x >> i) & 1 for i in range(n)]
    return any(b[i-1] == 1 and b[i] == 1 and b[(i+1) % n] == 1 for i in range(n))
def cpar(x, n):
    ones = [i for i in range(n) if (x >> i) & 1]
    if len(ones) < 2: return 0
    return sum((ones[i] - ones[i-1]) % 2 for i in range(len(ones)))
mode = sys.argv[1]; pmax = int(sys.argv[3])
if mode == '94':
    for n in range(4, int(sys.argv[2])+1):
        if n % 3 == 0: continue
        t = time.time(); N, F, cyc, lab, att, flips, E, g1, closed = base(94, n); m = len(cyc); has = codes_of(n)
        K = closed[0]; zero = int(lab[0])
        c101 = {i for i, c in enumerate(cyc) if any(has101(x, n) for x in c)}
        codesK = sorted(c for c in range(8) if any(has[c][x] for i in K for x in cyc[i]))
        r = dict(n=n, m=m, nclosed=len(closed), K=len(K), all101_in_K=c101 <= K, outsideK_has_no_101=all(i not in c101 for i in set(range(m)) - K),
                 codesK=codesK, edge_into_zero=any(v == zero for u, v in E), K_is_all_but_zero=(K == set(range(m)) - {zero}), K_is_all=(len(K) == m))
        if m <= pmax:
            gam, gmin, S, kc = potentials(n, N, F, cyc, flips); r.update(S_is_K=(S == K), gmin_m1=(gmin == m-1), kc=kc)
        r['sec'] = round(time.time()-t, 1); print(r, flush=True)
else:
    for n in range(4, int(sys.argv[2])+1, 2):
        t = time.time(); N, F, cyc, lab, att, flips, E, g1, closed = base(26, n); m = len(cyc); has = codes_of(n)
        zero = int(lab[0]); pow2 = (n & (n-1)) == 0
        # Lemma 2: c does not increase
        cs = np.array([cpar(x, n) for x in range(N)]) if n <= 16 else None
        r = dict(n=n, m=m, nclosed=len(closed), closed_sizes=[len(k) for k in closed], zero_in_K=(zero in closed[0]))
        if cs is not None: r['c_nonincreasing'] = bool((cs[F] <= cs).all())
        K = closed[0]
        r['codesK'] = sorted(c for c in range(8) if any(has[c][x] for i in K for x in cyc[i]))
        r['outsideK_all_have_111'] = all(any(has111(x, n) for x in cyc[i]) for i in set(range(m)) - K)
        if pow2: r['closed_is_zero'] = (closed == [{zero}])
        if m <= pmax:
            gam, gmin, S, kc = potentials(n, N, F, cyc, flips)
            r.update(S_is_K=(S == K), gmin_m1=(gmin == m-1), kc=kc, n_gam_m=int((gam == m).sum()) if pow2 else None)
        r['sec'] = round(time.time()-t, 1); print(r, flush=True)
