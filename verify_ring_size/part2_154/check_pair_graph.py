"""Finite check behind Lemma 5 of PROOF_154.md (collisions of rule 154), valid for every ring size n >= 3.

A pair (x, x') of states on a ring of n cells with F(x) = F(x') is the same thing as a closed walk of length n
in the pair graph: nodes (a, b, a', b') = (x_(i-1), x_i, x'_(i-1), x'_i); for y in {0, 1} an edge to
(b, c, b', c') where c, c' are the unique bits with f(a, b, c) = y = f(a', b', c') (rule 154 is
right-permutive).  The script lists the nodes that lie on a closed walk through off-diagonal nodes
(a, b) != (a', b') and the edges between them.

Output: out/check_pair_graph.txt
"""
import itertools
import os

RULE = 154
HERE = os.path.dirname(os.path.abspath(__file__))


def f(a, b, c):
    return (RULE >> (4 * a + 2 * b + c)) & 1


out = []
# right-permutivity and the algebraic form
assert all(f(a, b, 0) != f(a, b, 1) for a in (0, 1) for b in (0, 1))
assert all(f(a, b, c) == (c ^ (a & (1 - b))) for a in (0, 1) for b in (0, 1) for c in (0, 1))
out.append("rule 154: f(a,b,c) = c XOR (a AND NOT b) on all 8 codes: True; right-permutive: True")

nodes = list(itertools.product((0, 1), repeat=4))
succ = {}
for (a, b, a2, b2) in nodes:
    s = []
    for y in (0, 1):
        c = [c for c in (0, 1) if f(a, b, c) == y][0]
        c2 = [c for c in (0, 1) if f(a2, b2, c) == y][0]
        s.append(((b, c, b2, c2), y))
    succ[(a, b, a2, b2)] = s
diag = [v for v in nodes if (v[0], v[1]) == (v[2], v[3])]
off = [v for v in nodes if v not in diag]
assert all(w in diag for v in diag for (w, y) in succ[v])
out.append("diagonal nodes (x = x' locally) only lead to diagonal nodes: True")

# nodes on closed walks inside the off-diagonal subgraph: repeatedly delete nodes without successor or
# without predecessor inside the remaining set, then keep nodes that reach themselves
alive = set(off)
changed = True
while changed:
    changed = False
    for v in list(alive):
        has_succ = any(w in alive for (w, y) in succ[v])
        has_pred = any(v == w for u in alive for (w, y) in succ[u])
        if not (has_succ and has_pred):
            alive.discard(v)
            changed = True


def reaches_itself(v):
    seen, stack = set(), [w for (w, y) in succ[v] if w in alive]
    while stack:
        u = stack.pop()
        if u == v:
            return True
        if u in seen:
            continue
        seen.add(u)
        stack.extend(w for (w, y) in succ[u] if w in alive)
    return False


ess = sorted(v for v in alive if reaches_itself(v))
out.append("off-diagonal nodes: %d; nodes on a closed off-diagonal walk: %d" % (len(off), len(ess)))


def kind(v):
    a, b, a2, b2 = v
    if b == 0 and b2 == 0 and a != a2:
        return "B"     # x_i = x'_i = 0, x_(i-1) != x'_(i-1)
    if a == 0 and a2 == 0 and b != b2:
        return "A"     # x_(i-1) = x'_(i-1) = 0, x_i != x'_i
    if v in ((1, 0, 0, 1), (0, 1, 1, 0)):
        return "C"     # (x, x') locally (10, 01) or (01, 10)
    return "?"


edges = []
for v in ess:
    for (w, y) in succ[v]:
        if w in ess:
            edges.append((v, w, y))
            out.append("  %s [%s] --y=%d--> %s [%s]" % (v, kind(v), y, w, kind(w)))
kinds = {v: kind(v) for v in ess}
ok_kinds = all(k in "ABC" for k in kinds.values())
ok_edges = all((kinds[v], kinds[w]) in (("A", "B"), ("B", "A"), ("C", "C")) for (v, w, y) in edges)
ok_C = all(w != v for (v, w, y) in edges if kinds[v] == "C")
out.append("every such node is of kind A, B or C: %s" % ok_kinds)
out.append("every edge between such nodes is A->B, B->A or C->C (C->C edges join the two different C nodes): %s"
           % (ok_edges and ok_C))
out.append("RESULT: %s" % ("PASS" if (ok_kinds and ok_edges and ok_C and len(ess) == 6) else "FAIL"))
txt = "\n".join(out) + "\n"
open(os.path.join(HERE, "out", "check_pair_graph.txt"), "w").write(txt)
print(txt, end="")
