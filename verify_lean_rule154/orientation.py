"""What the orientation checks Rule154_local and Rule170_shift detect, and whether the statements on rule 154
depend on the orientation at all. Four conventions: ruleOfNumber with bit 4a+2b+c (Lean, paper) or 4c+2b+a
(mirrored), and globalMap with (x_{i-1}, x_i, x_{i+1}) (Lean, paper) or (x_{i+1}, x_i, x_{i-1}) (mirrored)."""
import itertools
from model import states, zero, e, rule90, par_E, par_O, System, hamming

def ron(N, mirrored):
    if mirrored:
        return lambda a, b, c: (N >> (4 * c + 2 * b + a)) & 1
    return lambda a, b, c: (N >> (4 * a + 2 * b + c)) & 1

def gmap(n, f, x, mirrored):
    if mirrored:
        return tuple(f(x[(i + 1) % n], x[i], x[(i - 1) % n]) for i in range(n))
    return tuple(f(x[(i - 1) % n], x[i], x[(i + 1) % n]) for i in range(n))

out = []
for mr, mg in itertools.product((False, True), repeat=2):
    f154 = ron(154, mr)
    local = all(f154(a, b, c) == (c + a * (1 + b)) % 2 for a, b, c in itertools.product((0, 1), repeat=3))
    f170 = ron(170, mr)
    shift = all(gmap(n, f170, x, mg)[i] == x[(i + 1) % n] for n in range(1, 7) for x in states(n) for i in range(n))
    out.append(f"ruleOfNumber mirrored: {mr!s:5}, globalMap mirrored: {mg!s:5} -> Rule154_local: {local!s:5}, "
               f"Rule170_shift: {shift}")

# mirror image of rule 154 is rule 166; do Lemma 3.3, 3.4(a), 3.9(b) hold for it too?
def mirror(N):
    return sum(((N >> (4 * a + 2 * b + c)) & 1) << (4 * c + 2 * b + a)
               for a in (0, 1) for b in (0, 1) for c in (0, 1))
M = mirror(154)
f = ron(M, False)
ok33 = ok34 = True
for n in range(2, 17, 2):
    for x in itertools.product((0, 1), repeat=n):
        if par_E(n, x) or par_O(n, x):
            y = gmap(n, f, x, False)
            ok33 &= (y == rule90(n, x)) and (par_O(n, y) if par_E(n, x) else par_E(n, y))
            if n & (n - 1) == 0:
                z = x
                for _ in range(n // 2):
                    z = gmap(n, f, z, False)
                ok34 &= z == zero(n)
ok39 = True
for n in (2, 4, 8):
    X = states(n)
    S = System(X, lambda x: gmap(n, f, x, False), None)
    S.r = lambda x, y, S=S: hamming(S.Fx[x], y)
    z0 = frozenset([zero(n)])
    ok39 &= all(S.R(z0, C) >= 2 for C in S.cycles if C != z0)
out.append(f"mirror image of rule 154 is rule {M}; for rule {M}: Lemma 3.3 (n even <= 16): {ok33}, "
           f"Lemma 3.4(a) (n = 2, 4, 8, 16): {ok34}, Theorem 3.9(b) (n = 2, 4, 8): {ok39}")
open("out/orientation.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
