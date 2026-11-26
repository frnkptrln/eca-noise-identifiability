"""One (rule, n) instance: every object of Statement.lean computed from the literal model in lean_defs.py,
and a check of each of the 17 statements of Statement.lean on that instance."""
import random
from lean_defs import (rule_of_number, states, global_map, hamming, contains, D, flip, CODES, iterate,
                       periodic_pts, cycles, ends_on, R_dijkstra, all_pairs_floyd, is_in_tree, tree_weight,
                       gamma_bruteforce, gamma_edmonds, reach_matrix, closed_classes_by_subsets,
                       closed_classes_by_scc, sInf_nat, nat_sub)


def bits(x):
    return ''.join(map(str, x))


class Instance:
    def __init__(self, N, n, brute_gamma_max=6, brute_cc_max=16, crosscheck_R=True):
        self.N, self.n = N, n
        self.f = rule_of_number(N)
        self.X = states(n)
        Fraw = global_map(n, self.f)
        self.Ftab = {x: Fraw(x) for x in self.X}
        self.F = self.Ftab.__getitem__
        self.r = lambda x, y: hamming(self.Ftab[x], y)
        self.cyc = cycles(self.X, self.F)            # list of frozensets
        self.m = len(self.cyc)
        self.nodes = list(range(self.m))
        # V(C, C') = R(C -> C')
        self.V = [[R_dijkstra(self.X, self.r, self.cyc[a], self.cyc[b]) for b in self.nodes] for a in self.nodes]
        self.checks = {}
        if crosscheck_R:
            idx, d = all_pairs_floyd(self.X, self.r)
            V2 = [[min(d[idx[x]][idx[y]] for x in self.cyc[a] for y in self.cyc[b]) for b in self.nodes]
                  for a in self.nodes]
            self.checks['R: Dijkstra = Floyd-Warshall'] = (V2 == self.V)
        self.gamma = [gamma_edmonds(self.nodes, self.V, c) for c in self.nodes]
        if self.m <= brute_gamma_max:
            gb = [gamma_bruteforce(self.nodes, self.V, c) for c in self.nodes]
            self.checks['gamma: parent-map enumeration = Edmonds'] = (gb == self.gamma)
        self.gammaMin = sInf_nat(self.gamma)
        self.Sel = {c for c in self.nodes if self.gamma[c] == self.gammaMin}
        self.G1 = lambda a, b: self.V[a][b] == 1
        self.reach = reach_matrix(self.nodes, self.G1)
        self.cc = closed_classes_by_scc(self.nodes, self.G1, self.reach)
        if self.m <= brute_cc_max:
            ccs = closed_classes_by_subsets(self.nodes, self.G1, self.reach)
            self.checks['closed classes: subset enumeration = SCC'] = (set(ccs) == set(self.cc))
        # R(C -> D_v) and k_v
        self.Dv = {v: D(n, v) for v in CODES}
        self.RCD = {(c, v): R_dijkstra(self.X, self.r, self.cyc[c], self.Dv[v]) for c in self.nodes for v in CODES}
        self.kterm = {v: sInf_nat(self.gamma[c] + self.RCD[(c, v)] for c in self.nodes) for v in CODES}
        self.k = {v: nat_sub(self.kterm[v], self.gammaMin) for v in CODES}
        self.kstar = max(self.k.values())     # Finset.univ.sup over the 8 codes

    # ------------------------------------------------------------------ statements
    def check_statements(self, rng=None, trees_per_root=20):
        rng = rng or random.Random(0)
        n, X, F, r, cyc, V, nodes, m = self.n, self.X, self.F, self.r, self.cyc, self.V, self.nodes, self.m
        size = len(X)
        ch = dict(self.checks)
        # EndsOnExactlyOneCycle
        ch['EndsOnExactlyOneCycle'] = all(sum(ends_on(F, x, C, size) for C in cyc) == 1 for x in X)
        # Lemma_2_3_general and Lemma_2_3
        g, l23a, l23b, l23c = True, True, True, True
        for a in nodes:
            for b in nodes:
                if a == b:
                    continue
                one_step = any(r(y, z) == 1 and ends_on(F, z, cyc[b], size) for y in cyc[a] for z in X)
                flips = any(ends_on(F, flip(n, x, j), cyc[b], size) for x in cyc[a] for j in range(n))
                g &= (V[a][b] >= 1) and ((V[a][b] == 1) == one_step)
                l23a &= V[a][b] >= 1
                l23b &= (V[a][b] == 1) == flips
                for x in cyc[a]:
                    for j in range(n):
                        if flip(n, x, j) in cyc[b]:
                            l23c &= (V[a][b] == 1 and V[b][a] == 1)
        ch['Lemma_2_3_general'] = g
        ch['Lemma_2_3'] = l23a and l23b and l23c
        # Lemma_2_5 on random in-trees (root first in a random order, each node points to an earlier one)
        ok = True
        for B in nodes:
            for _ in range(trees_per_root if m > 1 else 0):
                order = [B] + rng.sample([d for d in nodes if d != B], m - 1)
                p = {B: rng.choice(nodes)}                       # p B is arbitrary
                for i, d in enumerate(order[1:], 1):
                    p[d] = rng.choice(order[:i])
                assert is_in_tree(nodes, B, p)
                for N_ in nodes:
                    if N_ == B:
                        continue
                    q = dict(p); q[B] = N_                       # Function.update p B N
                    ok &= is_in_tree(nodes, N_, q)
                    if V[B][N_] == 1:
                        ok &= tree_weight(nodes, V, N_, q) <= tree_weight(nodes, V, B, p)
        ch['Lemma_2_5 (sampled trees)'] = ok
        # Lemma_2_6
        ch['Lemma_2_6'] = all(b in self.Sel for a in self.Sel for b in nodes if V[a][b] == 1)
        # ClosedClassReachable
        ch['ClosedClassReachable'] = all(any(self.reach[a] & K for K in self.cc) for a in nodes)
        # Lemma_2_7
        ch['Lemma_2_7'] = all(any(c in K for K in self.cc) for c in self.Sel)
        # Theorem_2_8
        p1 = all(any(c in K and K <= self.Sel for K in self.cc) for c in self.Sel)
        p2 = True
        if len(self.cc) == 1:
            p2 = (self.Sel == set(self.cc[0])) and self.gammaMin == nat_sub(m, 1)
        ch['Theorem_2_8'] = p1 and p2
        ch['Gamma_lower_bound'] = all(nat_sub(m, 1) <= gm for gm in self.gamma)
        ch['KIndex_subtraction_exact'] = all(self.gammaMin <= self.kterm[v] for v in CODES)
        # Lemma_2_2 (the hypothesis 3 <= n is NOT imposed here, so that n <= 2 can be inspected)
        sel_contains = {v: any(contains(n, x, v) for c in self.Sel for x in cyc[c]) for v in CODES}
        flip_contains = {v: any(contains(n, flip(n, x, j), v) for c in self.Sel for x in cyc[c] for j in range(n))
                         for v in CODES}
        ch['Lemma_2_2 part 1'] = all((self.k[v] == 0) == sel_contains[v] for v in CODES)
        ch['Lemma_2_2 part 2'] = (self.kstar == 0) == all(sel_contains.values())
        ch['Lemma_2_2 part 3'] = all(self.k[v] <= 1 for v in CODES if flip_contains[v])
        if len(self.cc) == 1:
            K = self.cc[0]
            ch['Corollary_2_8'] = (self.kstar == 0) == all(any(contains(n, x, v) for c in K for x in cyc[c])
                                                           for v in CODES)
        ch['ResistanceECA'] = all((r(x, y) == 0) == (y == F(x)) for x in X for y in X)
        self.sel_contains = sel_contains
        return ch

    def summary(self):
        cyc_s = ['{' + ','.join(sorted(bits(x) for x in C)) + '}' for C in self.cyc]
        lines = [f'rule {self.N}, n = {self.n}: m = {self.m} cycles']
        for i, s in enumerate(cyc_s):
            lines.append(f'  C{i} = {s}   gamma = {self.gamma[i]}' + ('   [selected]' if i in self.Sel else ''))
        lines.append('  V (row C, column C\'):')
        for i in self.nodes:
            lines.append('    C%-2d ' % i + ' '.join('%2d' % self.V[i][j] for j in self.nodes))
        edges = [f'C{a}->C{b}' for a in self.nodes for b in self.nodes if self.V[a][b] == 1]
        lines.append(f'  G1 edges: {", ".join(edges) if edges else "none"}')
        lines.append('  closed classes: ' + '; '.join('{' + ','.join(f'C{c}' for c in sorted(K)) + '}' for K in self.cc))
        lines.append(f'  gamma_min = {self.gammaMin}, m - 1 = {self.m - 1}, S = ' + '{' + ','.join(f'C{c}' for c in sorted(self.Sel)) + '}')
        lines.append('  k_v: ' + ', '.join(f'{bits(v)}:{self.k[v]}' for v in CODES) + f'   k* = {self.kstar}')
        return '\n'.join(lines)
