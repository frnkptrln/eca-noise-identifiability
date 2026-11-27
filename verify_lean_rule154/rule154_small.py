"""Rule 154 at n = 1..8 from the literal model: the cycles, V({0}, C) for every cycle C,
the edges of G_1 out of {0}, and the two clauses of Theorem_3_9_b where n = 2^(k+1)."""
from model import eca_system, zero, rule_of_number, global_map, e, hamming

def s(x):
    return "".join(map(str, x))

lines = []
summary = []
for n in range(1, 9):
    S = eca_system(n, 154)
    z = zero(n)
    C0 = [i for i, C in enumerate(S.cycles) if C == frozenset([z])]
    assert len(C0) == 1, "Zero_cycle: {0} is a cycle"
    c0 = C0[0]
    V0 = [S.R(S.cycles[c0], C) for C in S.cycles]
    lines.append(f"n = {n}: m = {S.m} cycles; sizes " +
                 str(sorted([len(C) for C in S.cycles])))
    for i, C in enumerate(S.cycles):
        rep = min(C)
        lines.append(f"  cycle {i:2d}: size {len(C):2d}, least state {s(rep)}, V({{0}}, C) = {V0[i]}"
                     + ("   <- {0}" if i == c0 else ""))
    others = [V0[i] for i in range(S.m) if i != c0]
    out_edges = [i for i in range(S.m) if V0[i] == 1]
    pow2 = n in (2, 4, 8)
    clause1 = all(v >= 2 for v in others)
    clause2 = len(out_edges) == 0
    lines.append(f"  V({{0}},{{0}}) = {V0[c0]}; least V({{0}}, C) over C != {{0}}: "
                 f"{min(others) if others else None}; G_1 edges out of {{0}}: {out_edges}")
    lines.append(f"  n = 2^(k+1)? {pow2}; clause 1 (V >= 2): {clause1}; clause 2 (no G_1 edge): {clause2}")
    summary.append((n, S.m, min(others) if others else None, len(out_edges), pow2, clause1 and clause2))
    if pow2:
        assert clause1 and clause2, f"Theorem_3_9_b fails at n = {n}"

# cross-check of V({0}, C) = 1 by Lemma 2.3: orbit of e_j ends on C
for n in range(1, 9):
    S = eca_system(n, 154)
    z = zero(n)
    ends = set()
    for j in range(n):
        x = e(n, j)
        for _ in range(2 ** n + 1):
            x = S.Fx[x]
        ends.update(i for i, C in enumerate(S.cycles) if x in C)
    V0 = [S.R(frozenset([z]), C) for C in S.cycles]
    assert ends - {S.cycles.index(frozenset([z]))} == {i for i in range(S.m) if V0[i] == 1}, n

lines.append("")
lines.append("n  m  least V({0},C), C != {0}  #G1 edges out of {0}  n=2^(k+1)  Theorem_3_9_b holds")
for row in summary:
    lines.append("  ".join(str(v) for v in row))
lines.append("Cross-check: for n = 1..8 the G_1 edges out of {0} are exactly the cycles other than {0} "
             "on which the orbit of some e_j ends (Lemma 2.3): OK")
open("out/rule154_small.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines[-11:]))
