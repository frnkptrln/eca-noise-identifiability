"""Analytic treatment of the affine rules at any n (GF(2) linear algebra, no state space).

For F(x) = Lx + b over GF(2): bijective iff L is invertible (then the uniform law is stationary and
k* = 0). Otherwise, by the Walsh-basis identity pi^(chi) = (1-2eps)^|chi| (-1)^(chi.b) pi^(L^T chi),
pi^(chi) = 0 for every chi outside the generalised kernel of L^T, so the three-cell marginals are
uniform (nu_c = n/8 for every eps, hence k* = 0) iff no nonzero character supported on three
adjacent cells lies in that generalised kernel ("bad characters"). If bad characters exist, the
marginals are not uniform and k* must be computed (the solver does so where the state space allows).
Output: data/fw_affine.csv for the affine class representatives and n = 4..64."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")


def local_map(rule):
    """Affine local rule f(a,b,c) = alpha a + beta b + gamma c + delta, or None."""
    for alpha in (0, 1):
        for beta in (0, 1):
            for gamma in (0, 1):
                for delta in (0, 1):
                    if all(((rule >> c) & 1) == (alpha * (c >> 2) ^ beta * ((c >> 1) & 1) ^ gamma * (c & 1) ^ delta)
                           for c in range(8)):
                        return alpha, beta, gamma, delta
    return None


def gf2_rank(M):
    M = M.copy() % 2; r = 0; n, m = M.shape
    for c in range(m):
        piv = next((k for k in range(r, n) if M[k, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        for k in range(n):
            if k != r and M[k, c]:
                M[k] ^= M[r]
        r += 1
    return r


def analyse(rule, n):
    a, b, g, d = local_map(rule)
    L = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        L[i, (i - 1) % n] ^= a; L[i, i] ^= b; L[i, (i + 1) % n] ^= g
    rank = gf2_rank(L)
    # generalised kernel of L^T = kernel of (L^T)^n
    LT = L.T % 2
    P = np.eye(n, dtype=np.int64)
    for _ in range(n):
        P = (LT @ P) % 2
    bad = 0
    for i in range(n):
        for mask in range(1, 8):
            chi = np.zeros(n, dtype=np.int64)
            for k in range(3):
                if (mask >> (2 - k)) & 1:
                    chi[(i - 1 + k) % n] = 1
            if not ((P @ chi) % 2).any():
                bad += 1
    gk_dim = n - gf2_rank(P)
    return dict(rule=rule, n=n, local=f"{a}{b}{g}+{d}", bijective=int(rank == n), kernel_dim=n - rank,
                gen_kernel_dim=gk_dim, bad_characters=bad,
                kstar_analytic=0 if (rank == n or bad == 0) else -1)


def main():
    reps = [r for r in fwlib.class_reps() if local_map(r) is not None]
    rows = [analyse(r, n) for r in reps for n in range(4, 65)]
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA, "fw_affine.csv"), index=False)
    print("affine reps:", reps)
    for r in reps:
        s = df[df.rule == r]
        print(r, "n with bad characters (k* not analytic):", s[s.kstar_analytic < 0].n.tolist())


if __name__ == "__main__":
    main()
