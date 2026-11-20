# Independent check of the paper's statements for rule 154 (Thm 3.9-3.11) and rule 94 at 3|n (Thm 3.43(i)),
# plus Remark 3.44 (rule 94, n=3,4) and Prop 3.22 (healing time). Own code, definitions only.
import sys, time, numpy as np, networkx as nx
sys.path.insert(0, __import__('os').path.dirname(__file__))
from check_43_142 import step_table, codes_of
CODES = ['000','001','010','011','100','101','110','111']
def analyse(rule, n, pot_max_m=70):
    N = 1 << n; F = step_table(rule, n)
    G = F.copy(); k = 1
    while k < N: G = G[G]; k *= 2
    per = np.zeros(N, bool); per[G] = True
    lab = -np.ones(N, dtype=np.int64); m = 0; cyc = []
    for s in np.nonzero(per)[0]:
        if lab[s] < 0:
            t = s; mem = []
            while lab[t] < 0: lab[t] = m; mem.append(t); t = F[t]
            cyc.append(mem); m += 1
    att = lab[G]; flips = [1 << j for j in range(n)]
    E = set()
    for ci, c in enumerate(cyc):
        cs = np.array(c)
        for f in flips:
            for t in set(att[cs ^ f].tolist()):
                if t != ci: E.add((ci, t))
    g1 = nx.DiGraph(); g1.add_nodes_from(range(m)); g1.add_edges_from(E)
    cond = nx.condensation(g1)
    closed = [frozenset(cond.nodes[v]['members']) for v in cond if cond.out_degree(v) == 0]
    has = codes_of(n)
    res = dict(rule=rule, n=n, m=m, n_closed=len(closed), closed_sizes=sorted(len(c) for c in closed),
               strongly_connected=(cond.number_of_nodes() == 1))
    out = dict(cyc=cyc, lab=lab, closed=closed, has=has, F=F, att=att, g1=g1)
    if m <= pot_max_m:
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
            if m == 1: break
            H = nx.DiGraph()
            for u in range(m):
                for v in range(m):
                    if u != v and u != r: H.add_edge(v, u, weight=int(V[u, v]))
            T = nx.minimum_spanning_arborescence(H)
            gam[r] = sum(d['weight'] for _, _, d in T.edges(data=True))
        gmin = gam.min(); S = set(np.nonzero(gam == gmin)[0].tolist())
        kc = [int((gam + R[:, cd]).min() - gmin) for cd in range(8)]
        res.update(gmin_minus_m=int(gmin) - m, S_size=len(S), kv=kc, kstar=max(kc),
                   G1_is_V1=(E == {(u, v) for u in range(m) for v in range(m) if u != v and V[u, v] == 1}))
        out.update(gam=gam, S=S, V=V)
    return res, out
def pow2(n): return n & (n-1) == 0
if __name__ == '__main__':
    print('--- rule 154'); nG = int(sys.argv[1])
    for n in range(3, nG+1):
        t = time.time(); r, o = analyse(154, n)
        z = int(o['lab'][0])
        if 'S' in o:
            if pow2(n):
                r['claim'] = (o['S'] == {z} and r['gmin_minus_m'] == -1 and all(o['gam'][c] == r['m'] for c in range(r['m']) if c != z)
                              and r['kv'] == [0,1,1,1,1,1,1,1] and r['n_closed'] == 1 and o['closed'][0] == frozenset([z]))
            else:
                r['claim'] = (r['strongly_connected'] and r['S_size'] == r['m'] and r['gmin_minus_m'] == -1 and r['kv'] == [0]*8)
        else:
            r['claim_G1_only'] = (o['closed'] == [frozenset([z])]) if pow2(n) else r['strongly_connected']
        r['sec'] = round(time.time()-t, 1); print(r, flush=True)
    print('--- rule 94')
    for n in [3, 4, 6, 9, 12, 15]:
        if n > nG: continue
        t = time.time(); r, o = analyse(94, n)
        if n % 3 == 0:
            A = [sum(1 << i for i in range(n) if (i + s) % 3 != 0) for s in range(3)]
            Ac = {int(o['lab'][a]) for a in A}
            r['crystal_fixed'] = all(o['F'][a] == a for a in A)
            r['closed_are_crystals'] = (sorted(o['closed'], key=min) == sorted([frozenset([c]) for c in Ac], key=min))
            r['flip_returns_in_3'] = all(o['F'][o['F'][o['F'][a ^ (1 << j)]]] == a for a in A for j in range(n))
            if 'S' in o: r['S_is_A'] = (o['S'] == Ac); r['kv_claim'] = (r['kv'] == [1,1,1,0,1,0,0,1])
        if n == 4 and 'S' in o:
            st = sorted(s for c in o['S'] for s in o['cyc'][c]); r['S_states'] = [format(s, '04b') for s in st]
            cl = sorted(s for c in o['closed'][0] for s in o['cyc'][c]); r['closed_states'] = [format(s, '04b') for s in cl]
        r['sec'] = round(time.time()-t, 1); print(r, flush=True)
    print('--- healing time, Prop 3.22')
    for rule in (43, 142):
        for n in (4, 8, 12, 16, 20):
            F = step_table(rule, n)
            x = sum(1 << i for i in range(n) if i % 4 in (2, 3)); X = {x}; y = F[x]
            while y != x: X.add(int(y)); y = F[y]
            taus = {}
            for j in range(n):
                xm, xj, xp = (x >> ((j-1) % n)) & 1, (x >> j) & 1, (x >> ((j+1) % n)) & 1
                kind = 'left' if (xm != xj and xj == xp) else 'right'
                y = x ^ (1 << j); tt = 0
                while True:
                    y = int(F[y]); tt += 1
                    if y in X: break
                taus.setdefault(kind, set()).add(tt)
            print(rule, n, len(X), {k: sorted(v) for k, v in taus.items()}, 'n/2-1 =', n//2 - 1)
