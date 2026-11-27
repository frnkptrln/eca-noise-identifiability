"""Lemma_3_3, Lemma_3_4_a, Single_mem on all states of E and O (parE, parO through i.val),
for n = 1..16; and what the definitions give for odd n."""
from model import rule_of_number, global_map, rule90, e, zero, par_E, par_O, iterate
import itertools

f = rule_of_number(154)
F = lambda n, x: global_map(n, f, x)
out = []

def class_states(n, which):
    """all states of parE (which = 'E') or parO ('O'), built directly: free on the allowed cells."""
    free = [i for i in range(n) if (i % 2 == 0) == (which == 'E')]
    res = []
    for bits in itertools.product((0, 1), repeat=len(free)):
        x = [0] * n
        for i, b in zip(free, bits):
            x[i] = b
        x = tuple(x)
        assert (par_E if which == 'E' else par_O)(n, x)
        res.append(x)
    return res

def all_t_equal(n, x):
    """F^[t] x = L^[t] x for all t: compare until the F-orbit repeats (then both sequences repeat)."""
    seen = {}
    a = b = x
    t = 0
    while a not in seen:
        if a != b:
            return False, t
        seen[a] = t
        a, b, t = F(n, a), rule90(n, b), t + 1
    return a == b, t

for n in range(2, 17, 2):
    E = class_states(n, 'E'); O = class_states(n, 'O')
    assert set(E) & set(O) == {zero(n)}
    c1 = all(par_O(n, F(n, x)) and F(n, x) == rule90(n, x) for x in E)
    c2 = all(par_E(n, F(n, x)) and F(n, x) == rule90(n, x) for x in O)
    c3 = all(all_t_equal(n, x)[0] for x in set(E) | set(O))
    out.append(f"n = {n:2d}: |E| = |O| = {len(E)}; Lemma_3_3 clause 1: {c1}, clause 2: {c2}, clause 3: {c3}")
    assert c1 and c2 and c3
    EO = set(E) | set(O)
    hit = all(iterate(lambda y: F(n, y), n // 2, x) == zero(n) for x in EO)
    times = []
    for x in EO:
        y, t = x, 0
        while y != zero(n) and t <= 4 * n:
            y, t = F(n, y), t + 1
        times.append(t if y == zero(n) else None)
    never = sum(t is None for t in times)
    worst = max(t for t in times if t is not None)
    pow2 = n & (n - 1) == 0
    out.append(f"        F^(n/2) x = 0 for all x in E u O: {hit}  (n power of two: {pow2}); "
               f"largest time to reach 0: {worst}; states of E u O not at 0 after 4n steps: {never}")
    if pow2:
        assert hit
    else:
        assert not hit

# Single_mem for every n = 1..16, odd n included
for n in range(1, 17):
    assert all(par_E(n, e(n, j)) or par_O(n, e(n, j)) for j in range(n))
out.append("Single_mem: e_j in parE u parO for every n = 1..16 and every j: OK")

# odd n: what parE / parO mean, and that Lemma_3_3 needs Even n
for n in (1, 3, 5, 7):
    E = class_states(n, 'E'); O = class_states(n, 'O')
    bad = [x for x in E if not (par_O(n, F(n, x)) and F(n, x) == rule90(n, x))]
    out.append(f"odd n = {n}: |parE| = {len(E)}, |parO| = {len(O)}; states of parE violating "
               f"Lemma_3_3 clause 1: {len(bad)}" + (f", e.g. x = {''.join(map(str, bad[0]))}, "
               f"F x = {''.join(map(str, F(n, bad[0])))}, L x = {''.join(map(str, rule90(n, bad[0])))}"
               if bad else ""))

# n = 2 in detail
n = 2
out.append("n = 2: F on all states: " + ", ".join(f"{''.join(map(str,x))}->{''.join(map(str,F(n,x)))}"
           for x in itertools.product((0, 1), repeat=2)) + "; L = rule90 is the zero map: "
           + str(all(rule90(2, x) == (0, 0) for x in itertools.product((0, 1), repeat=2))))
open("out/parity_checks.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
