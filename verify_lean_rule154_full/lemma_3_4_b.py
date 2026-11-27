"""Lemma_3_4_b_zero: for even n that is not a power of two, F^t(e_0) != 0 for all t >= 0 (rule 154, literal
global map).  Checked for every even n <= 24, and for every cell j (the paper's form) as well.  The orbit is
followed until a state repeats, so "for all t" is decided exactly.  For powers of two the first t with
F^t(e_j) = 0 is printed (the hypothesis "not a power of two" is needed).
Run: python lemma_3_4_b.py > out/lemma_3_4_b.txt
"""
from model import rule_of_number, is_pow_two

f = rule_of_number(154)


def step(x, n):
    y = 0
    for i in range(n):
        a = (x >> ((i - 1) % n)) & 1
        b = (x >> i) & 1
        c = (x >> ((i + 1) % n)) & 1
        if f(a, b, c):
            y |= 1 << i
    return y


def orbit_hits_zero(x, n):
    seen = {}
    t = 0
    while x not in seen:
        if x == 0:
            return t, None
        seen[x] = t
        x = step(x, n)
        t += 1
    return None, (t - seen[x])  # never zero; period of the cycle reached


def main():
    ok = True
    for n in range(2, 25, 2):
        p = is_pow_two(n)
        res = [orbit_hits_zero(1 << j, n) for j in range(n)]
        hit0 = res[0][0]
        allcells_never = all(r[0] is None for r in res)
        cell0_never = hit0 is None
        lean = cell0_never if not p else None
        print(f"n={n:2d} power of two={p!s:5} e_0 reaches 0 at t={hit0} (period reached: {res[0][1]});"
              f" Lemma_3_4_b_zero applies={not p} holds={lean}; paper form (all cells) never zero={allcells_never}")
        if not p:
            ok = ok and cell0_never and allcells_never
        else:
            ok = ok and all(r[0] is not None and r[0] <= n // 2 for r in res)
    print("ALL OK" if ok else "FAILED")


if __name__ == "__main__":
    main()
