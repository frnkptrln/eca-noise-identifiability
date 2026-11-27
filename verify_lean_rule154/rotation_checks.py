"""Lemma 2.4 from the literal model.
(1) GlobalMap_rot and Resistance_rot for all 256 rules at n = 1..6, for rot (x_{i-1}) and, to show what the
    check cannot distinguish, for the other direction (x_{i+1}).
(2) Lemma_2_4 for asymmetric rules at n = 3..6: the image of every cycle is a cycle (literal IsCycle),
    C -> rot C is a bijection of the cycles, and V, gamma, Sel, G_1 are preserved.
(3) Lemma_2_4_general for two other bijections s: the complement for rules 150 and 105 (s commutes with F and
    preserves r) and the reflection for rule 154 (does not commute): what fails without the hypotheses."""
from model import (eca_system, states, rot, rot_inv, refl, rule_of_number, global_map, hamming,
                   gamma_all, sel, G1)

out = []
# (1)
for n in range(1, 7):
    X = states(n)
    for N in range(256):
        f = rule_of_number(N)
        F = {x: global_map(n, f, x) for x in X}
        for s in (rot, rot_inv):
            assert all(F[s(n, x)] == s(n, F[x]) for x in X), (n, N, s.__name__)
            assert all(hamming(F[s(n, x)], s(n, y)) == hamming(F[x], y) for x in X for y in X)
out.append("(1) GlobalMap_rot and Resistance_rot hold for all 256 rules, n = 1..6, all states / pairs; "
           "the same holds for the opposite rotation x_{i+1}.")

def check_map(n, N, s, label):
    S = eca_system(n, N)
    idx = {C: i for i, C in enumerate(S.cycles)}
    img = [frozenset(s(n, x) for x in C) for C in S.cycles]
    is_cyc = [S.is_cycle(D) for D in img]
    res = {"n": n, "N": N, "map": label, "m": S.m, "images_are_cycles": all(is_cyc)}
    if not all(is_cyc):
        res["first_non_cycle"] = next(sorted(map(lambda x: "".join(map(str, x)), C))
                                      for C, ok in zip(S.cycles, is_cyc) if not ok)
        return res, S
    phi = [idx[D] for D in img]
    res["bijection"] = sorted(phi) == list(range(S.m))
    V = S.V()
    res["V"] = all(V[phi[a]][phi[b]] == V[a][b] for a in range(S.m) for b in range(S.m))
    gam = gamma_all(V)
    res["gamma"] = all(gam[phi[a]] == gam[a] for a in range(S.m))
    Sl = sel(gam)
    res["Sel"] = all((phi[a] in Sl) == (a in Sl) for a in range(S.m))
    E1 = G1(V)
    res["G1"] = all(((phi[a], phi[b]) in E1) == ((a, b) in E1) for a in range(S.m) for b in range(S.m))
    res["rot_nontrivial"] = any(phi[a] != a for a in range(S.m))
    res["gamma_values"] = sorted(set(gam))
    res["|Sel|"] = len(Sl)
    return res, S

# (2) asymmetric rules (not their own mirror image)
def mirror(N):
    return sum(((N >> (4 * a + 2 * b + c)) & 1) << (4 * c + 2 * b + a)
               for a in (0, 1) for b in (0, 1) for c in (0, 1))
rules = [154, 26, 43, 142, 30, 110, 14, 2, 184, 106]
assert all(mirror(N) != N for N in rules)
out.append("(2) Lemma_2_4, rot, asymmetric rules " + str(rules) + ", n = 3..6:")
allok = True
for N in rules:
    for n in range(3, 7):
        res, S = check_map(n, N, rot, "rot")
        ok = all(res[k] for k in ("images_are_cycles", "bijection", "V", "gamma", "Sel", "G1"))
        allok &= ok
        out.append(f"    rule {N:3d}, n = {n}: m = {res['m']:2d}, cycles moved by rot: {res['rot_nontrivial']}, "
                   f"gamma values {res['gamma_values']}, |Sel| = {res['|Sel|']}; all clauses hold: {ok}")
assert allok
# (3)
comp = lambda n, x: tuple(1 - v for v in x)
out.append("(3) Lemma_2_4_general with other bijections s:")
for N in (150, 105):
    for n in range(3, 7):
        res, _ = check_map(n, N, comp, "complement")
        ok = all(res[k] for k in ("images_are_cycles", "bijection", "V", "gamma", "Sel", "G1"))
        out.append(f"    complement, rule {N}, n = {n}: m = {res['m']}, all clauses hold: {ok}")
        assert ok
for n in range(3, 7):
    res, S = check_map(n, 154, refl, "reflection")
    X = states(n)
    commutes = all(S.Fx[refl(n, x)] == refl(n, S.Fx[x]) for x in X)
    line = f"    reflection, rule 154, n = {n}: commutes with F: {commutes}; images of cycles are cycles: " \
           f"{res['images_are_cycles']}"
    if res['images_are_cycles']:
        line += f"; V preserved: {res['V']}; gamma preserved: {res['gamma']}"
    else:
        line += f" (e.g. the image of the cycle {res['first_non_cycle']} is not a cycle)"
    out.append(line)
open("out/rotation_checks.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
