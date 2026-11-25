"""Affine rules under walls, any n, by linear algebra over GF(2) (no enumeration of 2^n states).

For f(l, c, r) = a l + b c + d r + e (16 rules) the null-wall map is F x = M x + e·1 with M tridiagonal
(a below, b on, d above the diagonal). Proposition L (report, Section 5.1): all cycles form one closed
class of G1, all are noise-selected, and k* = 0 iff the periodic states jointly contain every code.
The periodic states are x* + V_inv with V_inv = image of M^(2^J) (2^J >= n) and x* = F^(2^J')(0) for any
2^J' >= n. Code c occurs at cell i in some periodic state iff the window pattern c (wall values included)
lies in pi_i(x*) + pi_i(V_inv); this is decided by Gaussian elimination.

Usage: python3 affine_null.py --nmax 200   (writes data/boundaries/affine_null.csv)
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")


def affine_rules():
    out = {}
    for a in (0, 1):
        for b in (0, 1):
            for d in (0, 1):
                for e in (0, 1):
                    rule = sum(((a * ((c >> 2) & 1) + b * ((c >> 1) & 1) + d * (c & 1) + e) % 2) << c for c in range(8))
                    out[rule] = (a, b, d, e)
    return out


def matrix(a, b, d, n):
    M = np.zeros((n, n), dtype=np.uint8)
    for i in range(n):
        M[i, i] = b
        if i > 0: M[i, i - 1] = a
        if i < n - 1: M[i, i + 1] = d
    return M


def mul(A, B):
    return (A.astype(np.int64) @ B.astype(np.int64) % 2).astype(np.uint8)


def rank(A):
    A = A.copy() % 2; r = 0
    rows, cols = A.shape
    for c in range(cols):
        piv = np.flatnonzero(A[r:, c]) if r < rows else []
        if len(piv) == 0: continue
        p = r + piv[0]; A[[r, p]] = A[[p, r]]
        nz = np.flatnonzero(A[:, c]); nz = nz[nz != r]
        A[nz] ^= A[r]
        r += 1
        if r == rows: break
    return r


def in_span(B, v):
    """v in row span of B (rows)?"""
    if B.shape[0] == 0:
        return not v.any()
    return rank(np.vstack([B, v[None, :]])) == rank(B)


def analyse(rule, n, coeffs):
    a, b, d, e = coeffs
    M = matrix(a, b, d, n)
    P = M.copy(); J = 1
    while J < n:
        P = mul(P, P); J *= 2
    # V_inv = column space of P; basis as rows of P^T
    B = P.T.copy()
    dim = rank(B)
    # x* = F^J(0) with F x = M x + e 1
    x = np.zeros(n, dtype=np.uint8)
    for _ in range(J):
        x = (mul(M, x[:, None])[:, 0] + e) % 2
    covered = 0
    for i in range(n):
        idx = [j for j in (i - 1, i, i + 1)]
        inside = [j for j in idx if 0 <= j < n]
        Bw = B[:, inside]
        for c in range(8):
            pat = [(c >> 2) & 1, (c >> 1) & 1, c & 1]
            ok = True
            for j, pbit in zip(idx, pat):
                if not (0 <= j < n) and pbit != 0:      # null wall
                    ok = False
            if not ok: continue
            target = np.array([pbit for j, pbit in zip(idx, pat) if 0 <= j < n], dtype=np.uint8) ^ x[inside]
            if in_span(Bw, target):
                covered |= 1 << c
    return dict(rule=rule, n=n, dim_periodic=dim, bijective=int(dim == n), covered=covered,
                missed="".join(str(c) for c in range(8) if not (covered >> c) & 1) or "-",
                kstar_ge1=int(covered != 255))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--nmin", type=int, default=3); ap.add_argument("--nmax", type=int, default=200)
    a = ap.parse_args()
    rows = []
    for rule, co in sorted(affine_rules().items()):
        for n in range(a.nmin, a.nmax + 1):
            rows.append(analyse(rule, n, co))
    df = pd.DataFrame(rows)
    os.makedirs(DATA, exist_ok=True)
    df.to_csv(os.path.join(DATA, "affine_null.csv"), index=False)
    for rule in (60, 90, 150, 105, 165, 153, 170, 15):
        s = df[(df.rule == rule) & (df.kstar_ge1 == 1)].n.tolist()
        print(rule, "k*>=1 at n =", s[:30], "..." if len(s) > 30 else "")
