"""Independent verifier for mech.analyze (run before any mechanism result is used).

Own code for everything except the definitions: the global map, the cycles, the full resistance graph
r(x, y) = H(F x, y) on all 2^n x 2^n pairs (no single-layer reduction), Dijkstra from every cycle for
V(C, C'), potentials gamma(C) by networkx minimum spanning arborescences (one per root, on the
reversed cycle graph), radii, the one-flip graph G1 and its closed classes (networkx), and the crystal
test (G2 criterion, gamma_min = m + |A| - 2). Compares field by field with mech.analyze.

Usage: python3 verify_mech.py --nmax 8 [--rules all|22,26,...] --out ../../data/ring_size/verify_mech.csv
"""
import argparse, csv, heapq, itertools, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import networkx as nx


def F_of(rule, n):
    out = []
    for x in range(1 << n):
        y = 0
        for i in range(n):
            l = (x >> ((i - 1) % n)) & 1; c = (x >> i) & 1; r = (x >> ((i + 1) % n)) & 1
            y |= ((rule >> (4 * l + 2 * c + r)) & 1) << i
        out.append(y)
    return out


def cycles_of(F):
    S = len(F); seen_on = {}
    cyc = []
    for x0 in range(S):
        x = x0
        for _ in range(S):
            x = F[x]
        if x in seen_on:
            continue
        c = [x]; y = F[x]
        while y != x:
            c.append(y); y = F[y]
        for z in c:
            seen_on[z] = len(cyc)
        cyc.append(sorted(c))
    cyc.sort(key=lambda c: c[0])
    return cyc


def popcount(v):
    return bin(v).count("1")


def dijkstra(F, n, sources):
    S = 1 << n
    dist = [10 ** 9] * S
    pq = []
    for s in sources:
        dist[s] = 0; pq.append((0, s))
    heapq.heapify(pq)
    while pq:
        d, x = heapq.heappop(pq)
        if d > dist[x]:
            continue
        fx = F[x]
        for y in range(S):
            nd = d + popcount(fx ^ y)
            if nd < dist[y]:
                dist[y] = nd; heapq.heappush(pq, (nd, y))
    return dist


def codes_mask(x, n):
    m = 0
    for i in range(n):
        l = (x >> ((i - 1) % n)) & 1; c = (x >> i) & 1; r = (x >> ((i + 1) % n)) & 1
        m |= 1 << (4 * l + 2 * c + r)
    return m


def gamma_nx(V):
    m = len(V)
    if m == 1:
        return [0]
    out = []
    for root in range(m):
        G = nx.DiGraph()
        G.add_nodes_from(range(m))
        # in-tree rooted at root on edges u->v (weight V[u][v]) == arborescence on reversed edges v->u
        for u in range(m):
            for v in range(m):
                if u != v and u != root:
                    G.add_edge(v, u, weight=V[u][v])
        T = nx.minimum_spanning_arborescence(G, attr="weight", preserve_attrs=True)
        out.append(int(sum(d["weight"] for _, _, d in T.edges(data=True))))
    return out


def independent(rule, n):
    F = F_of(rule, n)
    cyc = cycles_of(F)
    m = len(cyc)
    D = [dijkstra(F, n, c) for c in cyc]
    V = [[0 if i == j else min(D[i][z] for z in cyc[j]) for j in range(m)] for i in range(m)]
    gam = gamma_nx(V)
    gmin = min(gam)
    sel = [g == gmin for g in gam]
    rad = [min(V[i][j] for j in range(m) if j != i) if m > 1 else -1 for i in range(m)]
    G1 = nx.DiGraph(); G1.add_nodes_from(range(m))
    G1.add_edges_from((i, j) for i in range(m) for j in range(m) if i != j and V[i][j] == 1)
    C = nx.condensation(G1)
    closed = [c for c in C.nodes if C.out_degree(c) == 0]
    closed_union = set().union(*[C.nodes[c]["members"] for c in closed])
    cyc_codes = [0] * m
    for j, c in enumerate(cyc):
        for z in c:
            cyc_codes[j] |= codes_mask(z, n)
    # k_c from the definition: ord nu_c = min_C [gamma(C) + R(C -> D_c)] - gamma_min
    k_c = []
    for c in range(8):
        best = 10 ** 9
        for j in range(m):
            dc = min((D[j][z] for z in range(1 << n) if (codes_mask(z, n) >> c) & 1), default=10 ** 9)
            best = min(best, gam[j] + dc)
        k_c.append(best - gmin)
    cover = 0
    for j in range(m):
        if sel[j]:
            cover |= cyc_codes[j]
    # crystal test: selected set = one rotation orbit; entry cost; G2 criterion
    def rot(x, k):
        k %= n; full = (1 << n) - 1
        return ((x << k) | (x >> (n - k))) & full if k else x
    idx = {z: j for j, c in enumerate(cyc) for z in c}
    S = [i for i in range(m) if sel[i]]
    orbit0 = {idx[rot(cyc[S[0]][0], k)] for k in range(n)}
    crystal = set(S) == orbit0 and m > 1
    ec, g2 = -1, False
    if crystal:
        ec = max(min(V[j][a] for a in S) for j in range(m) if not sel[j])
        H = nx.DiGraph(); H.add_nodes_from(range(m))
        H.add_edges_from((i, j) for i in range(m) for j in range(m) if i != j and
                         ((not sel[i] and V[i][j] == 1) or (sel[i] and V[i][j] == 2)))
        anc = nx.ancestors(H, S[0]) | {S[0]}
        g2 = len(anc) == m and min(rad[a] for a in S) >= 2
    rec = dict(crystal_orbit=crystal, entry_cost_max=ec, g2_holds=g2, cycles=m, n_selected=sum(sel), gamma_min=gmin, kstar=max(k_c),
               k_c="-".join(map(str, k_c)), selected_cover="".join(str(c) for c in range(8) if cover >> c & 1),
               g1_sccs=C.number_of_nodes(), g1_closed=len(closed),
               selected_eq_closed_union=set(i for i in range(m) if sel[i]) == closed_union,
               radius_selected_min=min(rad[i] for i in range(m) if sel[i]),
               radius_other_max=max((rad[i] for i in range(m) if not sel[i]), default=-1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=4)
    ap.add_argument("--nmax", type=int, default=8)
    ap.add_argument("--rules", default="switching")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import mech
    sys.path.insert(0, os.path.join(HERE, "..", "fw"))
    import fwlib
    if a.rules == "switching":
        rules = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]
    elif a.rules == "all":
        rules = fwlib.class_reps()
    else:
        rules = [int(v) for v in a.rules.split(",")]
    fields = ["cycles", "n_selected", "gamma_min", "kstar", "k_c", "selected_cover", "g1_sccs", "g1_closed",
              "selected_eq_closed_union", "radius_selected_min", "radius_other_max", "crystal_orbit",
              "entry_cost_max", "g2_holds"]
    rows, bad = [], 0
    for n in range(a.nmin, a.nmax + 1):
        for rule in rules:
            Fm = fwlib.succ_map(rule, n)
            if fwlib.is_bijective(Fm):
                continue
            ind = independent(rule, n)
            mine, _ = mech.analyze(rule, n)
            diff = [f for f in fields if str(ind[f]) != str(mine[f])]
            bad += bool(diff)
            rows.append(dict(n=n, rule=rule, agree=int(not diff), differing=";".join(diff),
                             **{f"ind_{f}": ind[f] for f in fields}))
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"verify_mech: {len(rows)} (rule, n) pairs, {bad} disagreements")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
