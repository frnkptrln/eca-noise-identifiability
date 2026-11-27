"""Sanity check of the instance Section_2_4_ECA for rule 154 at n = 2, 4, 8 (powers of two) and n = 6:
closed classes of G_1, Sel, gamma_min = m - 1 (Theorem 2.8), every in-tree weight >= m - 1
(TreeWeight_lower_bound, through gamma). Compared with Theorem 3.9(d), (e) and Theorem 3.10 of the paper."""
import heapq
from model import eca_system, zero, gamma_all, sel, G1
import networkx as nx

def V_matrix(S):
    m = S.m
    V = [[0] * m for _ in range(m)]
    for a, A in enumerate(S.cycles):
        dist = {x: 0 for x in A}
        pq = [(0, x) for x in A]; done = set()
        while pq:
            d, x = heapq.heappop(pq)
            if x in done: continue
            done.add(x)
            Fx = S.Fx[x]
            for y in S.X:
                w = d + sum(u != v for u, v in zip(Fx, y))
                if w < dist.get(y, 10 ** 9):
                    dist[y] = w; heapq.heappush(pq, (w, y))
        for b, B in enumerate(S.cycles):
            V[a][b] = min(dist[y] for y in B)
    return V

out = []
for n in (2, 4, 6, 8):
    S = eca_system(n, 154)
    V = V_matrix(S)
    if n <= 4:  # the per-pair R of the model agrees
        assert V == S.V()
    m = S.m
    g = nx.DiGraph(); g.add_nodes_from(range(m)); g.add_edges_from(G1(V))
    comps = [set(c) for c in nx.strongly_connected_components(g)]
    closed = [c for c in comps if all(b in c for a in c for b in g.successors(a))]
    gam = gamma_all(V)
    Sl = sel(gam)
    c0 = S.cycles.index(frozenset([zero(n)]))
    out.append(f"n = {n}: m = {m}; closed classes: {len(closed)}"
               f"{' = {{0}}' if closed == [{c0}] else ''}; Sel = {sorted(Sl)} ({{0}} is {c0}); "
               f"gamma_min = {min(gam)} (m - 1 = {m - 1}); gamma({{0}}) = {gam[c0]}; "
               f"gamma of the others: {sorted(set(gam[c] for c in range(m) if c != c0))}; "
               f"min gamma >= m - 1: {min(gam) >= m - 1}")
open("out/section_2_4_check.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
