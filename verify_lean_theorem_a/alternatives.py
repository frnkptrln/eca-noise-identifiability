"""Alternative readings of the definitions of Statement.lean, and small cases on which they differ from it.
Run from this directory: python alternatives.py"""
import heapq
from itertools import product
from instance import Instance, bits
from lean_defs import CODES, sInf_nat, tree_weight, R_dijkstra

out = []


def say(s=''):
    out.append(s)
    print(s)


# A1. R with paths of at least one step.
def R_pos(X, r, A, B):
    dist = {x: float('inf') for x in X}
    pq = []
    for a in A:                      # the first step is forced
        for y in X:
            if r(a, y) < dist[y]:
                dist[y] = r(a, y)
                heapq.heappush(pq, (dist[y], y))
    while pq:
        d, x = heapq.heappop(pq)
        if d > dist[x]:
            continue
        for y in X:
            if d + r(x, y) < dist[y]:
                dist[y] = d + r(x, y)
                heapq.heappush(pq, (dist[y], y))
    return sInf_nat(dist[b] for b in B if dist[b] < float('inf'))


diff = tot = 0
for n in (3, 4):
    for N in range(256):
        I = Instance(N, n, crosscheck_R=False, brute_gamma_max=0, brute_cc_max=0)
        for a in I.nodes:
            for b in I.nodes:
                tot += 1
                diff += R_pos(I.X, I.r, I.cyc[a], I.cyc[b]) != I.V[a][b]
            for v in CODES:
                tot += 1
                diff += R_pos(I.X, I.r, I.cyc[a], I.Dv[v]) != I.RCD[(a, v)]
say(f'A1 R with paths of >= 1 step vs R of Statement.lean (length 0 allowed), source a cycle, '
    f'n = 3, 4, all 256 rules: {diff} differences in {tot} values (V(C,C\') and R(C -> D_v))')
J = Instance(0, 3, crosscheck_R=False)
A = {(1, 1, 1)}
say(f'A1b rule 0, n = 3, A = B = {{111}} (not a cycle): R with length 0 allowed = {R_dijkstra(J.X, J.r, A, A)}, '
    f'R with >= 1 step = {R_pos(J.X, J.r, A, A)}')


# A2. In-tree conditions.
def is_in_tree_noavoid(nodes, c, p):
    """IsInTree without the hypothesis (∀ j < k, p^[j] d ≠ c)."""
    for d in nodes:
        y = d
        for _ in range(len(nodes)):
            y = p[y]
            if y == d:
                return False
    return True


def is_loopfree(nodes, c, p):
    """Only p d ≠ d for d ≠ c (edges between distinct nodes; circuits allowed)."""
    return all(p[d] != d for d in nodes if d != c)


def gamma_alt(nodes, V, c, test):
    others = [d for d in nodes if d != c]
    ws = []
    for vals in product(nodes, repeat=len(others)):
        for pc in nodes:             # p c is enumerated too, since an alternative test may look at it
            p = dict(zip(others, vals))
            p[c] = pc
            if test(nodes, c, p):
                ws.append(tree_weight(nodes, V, c, p))
    return sInf_nat(ws)


I = Instance(154, 4, crosscheck_R=False)
ga = [gamma_alt(I.nodes, I.V, c, is_in_tree_noavoid) for c in I.nodes]
say(f'A2 rule 154, n = 4: gamma (Statement.lean) = {I.gamma}; gamma if IsInTree had no hypothesis '
    f'"forall j < k, p^[j] d != c" = {ga} (no map qualifies, since every map of a finite set to itself has a circuit; sInf of the empty set = 0)')
for N, n in ((154, 4), (90, 3), (154, 3)):
    I = Instance(N, n, crosscheck_R=False)
    gb = [gamma_alt(I.nodes, I.V, c, is_loopfree) for c in I.nodes]
    say(f'A2b rule {N}, n = {n}: gamma = {I.gamma}; with circuits allowed = {gb}')
for n in (3, 4):
    found = None
    for N in range(256):
        I = Instance(N, n, crosscheck_R=False, brute_gamma_max=0, brute_cc_max=0)
        if I.m > 5:
            continue
        gb = [gamma_alt(I.nodes, I.V, c, is_loopfree) for c in I.nodes]
        Sb = {c for c in I.nodes if gb[c] == min(gb)}
        if Sb != I.Sel:
            found = f'rule {N}: gamma {I.gamma}, S {sorted(I.Sel)}; with circuits allowed gamma {gb}, S {sorted(Sb)}'
            break
    say(f'A2c first rule (m <= 5) at n = {n} where allowing circuits changes S: {found}')


# A3. Bit order of the rule number and orientation of the neighbourhood.
def mirror(N):
    return sum(((N >> (4 * a + 2 * b + c)) & 1) << (4 * c + 2 * b + a)
               for a in (0, 1) for b in (0, 1) for c in (0, 1))


def reverse_index(N):
    return sum(((N >> i) & 1) << (7 - i) for i in range(8))


say(f'A3 mirror f\'(a,b,c) = f(c,b,a): 90 -> {mirror(90)}, 204 -> {mirror(204)}, 154 -> {mirror(154)}; '
    f'bit index 7 - (4a+2b+c): 90 -> {reverse_index(90)}, 204 -> {reverse_index(204)}')
for N in (154, 2):
    I, J = Instance(N, 4, crosscheck_R=False), Instance(mirror(N), 4, crosscheck_R=False)
    say(f'    n = 4: rule {N}: k_v ' + ' '.join(f'{bits(v)}:{I.k[v]}' for v in CODES) + f', k* = {I.kstar}')
    say(f'           rule {mirror(N)}: k_v ' + ' '.join(f'{bits(v)}:{J.k[v]}' for v in CODES) + f', k* = {J.kstar}')

open('out/alternatives.txt', 'w').write('\n'.join(out) + '\n')
