"""Route (a), exact: stationary laws as rational functions of eps for n = 4, 5.

Tree theorem: the unnormalised stationary weight T_x(eps) = det of (I - P) with row x and column x removed,
an integer polynomial of degree <= n (2^n - 1). nu_c = G_c / Z with G_c = sum_x N_c(x) T_x, Z = sum_x T_x.
G_c and Z are obtained exactly: evaluation at D+1 integer points (flint exact integer determinants) and
exact Newton interpolation. Check: at eps = 1/7 the exact linear solve of pi P = pi must give G_c/Z.
Usage: python exact_small.py n
"""
import sys, time, json
from fractions import Fraction
import numpy as np
import flint
import eca

n = int(sys.argv[1])
N = 1 << n
D = n * (N - 1)
pts = list(range(-(D // 2), D - D // 2 + 1))
assert len(pts) == D + 1
out = f'out/exact_n{n}.jsonl'
done = {r['rule'] for r in eca.read_jsonl(out)}
Ncodes = eca.code_counts(n).astype(int)
pc = eca.popcount(np.arange(N, dtype=np.uint32)).astype(int)


def Pmatrix(F, e):
    """Exact P at eps = e (int or Fraction); entries e^d (1-e)^(n-d)."""
    pw = [e ** d * (1 - e) ** (n - d) for d in range(n + 1)]
    return [[pw[pc[int(F[x]) ^ y]] for y in range(N)] for x in range(N)]


def newton_coeffs(xs, ys):
    """Exact interpolation; returns monomial coefficients (Fractions), low degree first."""
    m = len(xs)
    c = [Fraction(v) for v in ys]
    for j in range(1, m):
        for i in range(m - 1, j - 1, -1):
            c[i] = (c[i] - c[i - 1]) / (xs[i] - xs[i - j])
    poly = [Fraction(0)] * m
    # Horner on Newton form
    for i in range(m - 1, -1, -1):
        # poly = poly * (x - xs[i]) + c[i]
        new = [Fraction(0)] * m
        for k in range(m - 1):
            new[k + 1] += poly[k]
        for k in range(m):
            new[k] -= xs[i] * poly[k]
        new[0] += c[i]
        poly = new
    return poly


def order_lc(p):
    for k, v in enumerate(p):
        if v != 0:
            return k, v
    return None, 0


for rule in eca.class_reps():
    if rule in done:
        continue
    t0 = time.time()
    F = eca.step_map(rule, n)
    G = [[0] * len(pts) for _ in range(8)]
    Z = [0] * len(pts)
    for ip, e in enumerate(pts):
        P = Pmatrix(F, e)
        L = [[(1 if x == y else 0) - P[x][y] for y in range(N)] for x in range(N)]
        for x in range(N):
            idx = [i for i in range(N) if i != x]
            M = flint.fmpz_mat([[L[i][j] for j in idx] for i in idx])
            T = int(M.det())
            Z[ip] += T
            for c in range(8):
                G[c][ip] += int(Ncodes[c, x]) * T
    Zp = newton_coeffs(pts, Z)
    Gp = [newton_coeffs(pts, G[c]) for c in range(8)]
    assert all(v.denominator == 1 for p in [Zp] + Gp for v in p)
    # exact check at eps = 1/7 by a direct linear solve
    e = Fraction(1, 7)
    P = Pmatrix(F, e)
    A = [[(P[y][x] - (1 if x == y else 0)) for y in range(N)] for x in range(N)]  # (P^T - I)
    A[-1] = [1] * N
    b = [0] * (N - 1) + [1]
    Am = flint.fmpq_mat([[flint.fmpq(v.numerator, v.denominator) for v in row] for row in A])
    pi = Am.solve(flint.fmpq_mat([[v] for v in b]))
    pi = [Fraction(int(pi[i, 0].p), int(pi[i, 0].q)) for i in range(N)]
    def ev(p, x):
        s = Fraction(0)
        for v in reversed(p):
            s = s * x + v
        return s
    zval = ev(Zp, e)
    check = all(sum(pi[x] * int(Ncodes[c, x]) for x in range(N)) == ev(Gp[c], e) / zval for c in range(8))
    kz, lz = order_lc(Zp)
    kc, lc = [], []
    for c in range(8):
        k, l = order_lc(Gp[c])
        kc.append(k - kz)
        lc.append(str(Fraction(l) / Fraction(lz)))
    ks = max(kc)
    a = min(Fraction(lc[c]) for c in range(8) if kc[c] == ks)
    eca.append_jsonl(out, dict(rule=rule, n=n, k_c=kc, k_star=ks, lead_coef_nu=lc, a=str(a), a_float=float(a),
                               exact_check_eps_1_7=check, ord_Z=kz,
                               Z=[str(int(v)) for v in Zp], G=[[str(int(v)) for v in p] for p in Gp],
                               sec=round(time.time() - t0, 2)))
print('done', n)
