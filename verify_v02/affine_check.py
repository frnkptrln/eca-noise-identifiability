"""Own GF(2) analysis of the affine classes, n = 4..64: kernel and generalised kernel of L^T, bijectivity,
nonzero characters supported on three adjacent cells inside the generalised kernel (uniform 3-cell marginals iff none),
and the 'only cycle is the zero state' property (nilpotent L, b = 0)."""
import itertools, pandas as pd, eca

def affine_coeffs(rule):
    # f(l,c,r) = a l + b c + g r + d over GF(2), if affine
    d = rule & 1
    a = ((rule >> 4) & 1) ^ d; b = ((rule >> 2) & 1) ^ d; g = ((rule >> 1) & 1) ^ d
    for code in range(8):
        l, c, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
        if ((rule >> code) & 1) != (a * l ^ b * c ^ g * r ^ d):
            return None
    return a, b, g, d

def rank_gf2(rows):
    rows = list(rows); r = 0; piv_rows = []
    basis = {}
    for v in rows:
        for p in sorted(basis, reverse=True):
            if (v >> p) & 1: v ^= basis[p]
        if v:
            basis[v.bit_length() - 1] = v; r += 1
    return r

def matmul(A, B, n):
    # rows as int bitmasks; (AB)_i = XOR over j in A_i of B_j
    out = []
    for i in range(n):
        v = 0; a = A[i]; j = 0
        while a:
            if a & 1: v ^= B[j]
            a >>= 1; j += 1
        out.append(v)
    return out

def kernel_contains(M, n, v):
    # M v = 0 ?
    return all(bin(M[i] & v).count('1') % 2 == 0 for i in range(n))

rows = []
affine = [r for r in eca.class_reps() if affine_coeffs(r) is not None]
for rule in affine:
    a, b, g, d = affine_coeffs(rule)
    for n in range(4, 65):
        # (Lx)_i = a x_{i-1} + b x_i + g x_{i+1}; row i of L as bitmask
        L = [((a << ((i - 1) % n)) ^ (b << i) ^ (g << ((i + 1) % n))) for i in range(n)]
        LT = [sum(((L[j] >> i) & 1) << j for j in range(n)) for i in range(n)]
        rk = rank_gf2(L)
        P = LT[:]; 
        for _ in range(n - 1): P = matmul(P, LT, n)  # (L^T)^n
        gk = n - rank_gf2(P)
        bad = sum(1 for chi in range(1, 8) if kernel_contains(P, n, ((chi & 1) << (n - 1)) | ((chi >> 1) << 0)))  # cells n-1, 0, 1
        Ln = L[:]
        for _ in range(n - 1): Ln = matmul(Ln, L, n)
        nilpotent = all(v == 0 for v in Ln)
        rows.append(dict(rule=rule, n=n, kernel_dim=n - rk, gen_kernel_dim=gk, bijective=int(rk == n), bad_characters=bad,
                         uniform_marginals=int(bad == 0), L_nilpotent=int(nilpotent), b=d,
                         pow2=int(n & (n - 1) == 0)))
df = pd.DataFrame(rows); df.to_csv('out/affine_check.csv', index=False)
print('affine classes', affine)
for r in (60, 90):
    x = df[df.rule == r]
    print(r, 'non-uniform at n =', x[x.uniform_marginals == 0].n.tolist(), '; nilpotent at n =', x[x.L_nilpotent == 1].n.tolist())
